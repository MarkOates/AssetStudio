import os
import json
import glob
from collections import defaultdict

ASSETS_DIR = "/Users/markoates/Assets"
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "packs.json")
SNAPSHOT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "snapshots", "assets_dir_listing_20260914_110524.json")

def generate_packs_db():
    packs_data = {}
    existing_packs_data = {}
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_packs_data = json.load(f)
        except Exception:
            pass
    
    if not os.path.exists(ASSETS_DIR):
        print(f"Error: {ASSETS_DIR} does not exist.")
        return
        
    print("Loading snapshot data for clobber analysis...")
    snapshot_data = []
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
            snapshot_data = json.load(f)
            
    # Group archives by pack
    pack_archives = defaultdict(list)
    for entry in snapshot_data:
        if entry.get('type') == 'file' and 'archive_contents' in entry:
            # path is like vendor/pack/archive.zip
            parts = entry['path'].split('/')
            if len(parts) >= 3:
                vendor = parts[0]
                pack = parts[1]
                pack_id = f"{vendor}/{pack}"
                archive_name = parts[-1]
                pack_archives[pack_id].append({
                    'name': archive_name,
                    'contents': entry['archive_contents']
                })

    print("Analyzing packs...")
    # Iterate through vendors
    for vendor in os.listdir(ASSETS_DIR):
        vendor_path = os.path.join(ASSETS_DIR, vendor)
        if not os.path.isdir(vendor_path) or vendor.startswith('.'):
            continue
            
        # Iterate through packs
        for pack in os.listdir(vendor_path):
            pack_path = os.path.join(vendor_path, pack)
            if not os.path.isdir(pack_path) or pack.startswith('.'):
                continue
                
            pack_id = f"{vendor}/{pack}"
            extracted_dir = os.path.join(pack_path, "extracted")
            
            import datetime
            
            extraction_folder_exists = os.path.isdir(extracted_dir)
            status = "extracted" if extraction_folder_exists else "unextracted"
            
            extracted_at = None
            extractor = None
            if extraction_folder_exists:
                if pack_id in existing_packs_data:
                    extractor = existing_packs_data[pack_id].get('extractor')
                    extracted_at = existing_packs_data[pack_id].get('extracted_at')
                    
                if not extractor:
                    extractor = "user"
                if not extracted_at:
                    stat = os.stat(extracted_dir)
                    extracted_at = datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                
            # Check for clobbering
            clobbered_files = defaultdict(list)
            if status == "unextracted" and pack_id in pack_archives:
                file_to_archives = defaultdict(list)
                for archive in pack_archives[pack_id]:
                    for f in archive['contents']:
                        file_to_archives[f].append(archive['name'])
                        
                for f, archives in file_to_archives.items():
                    if len(archives) > 1:
                        # This file is present in multiple archives
                        clobbered_files[f] = archives
                        
            multiple_archive_files_would_clobber_results = bool(clobbered_files)
            clobber_data = dict(clobbered_files) if clobbered_files else None
                
            # PackDrift check
            has_pack_drift = False
            log_path = os.path.join(pack_path, "download_log.txt")
            has_missing_log_file = not os.path.exists(log_path)
            
            if not has_missing_log_file:
                try:
                    with open(log_path, 'r', encoding='utf-8') as f:
                        lines = [l.strip() for l in f.readlines() if l.strip()]
                        if len(lines) > 1 and lines[1].isdigit():
                            expected_count = int(lines[1])
                            actual_archives = len([f for f in os.listdir(pack_path) if os.path.isfile(os.path.join(pack_path, f)) and not f.endswith('.txt') and not f.startswith('.')])
                            if actual_archives != expected_count:
                                has_pack_drift = True
                except Exception:
                    pass

            if pack_id in existing_packs_data:
                existing_status = existing_packs_data[pack_id].get('extraction_status')
                if existing_status == "extracted":
                    status = "extracted"
                    
            can_be_extracted = (not extraction_folder_exists and not multiple_archive_files_would_clobber_results and not has_pack_drift and not has_missing_log_file and status != "extracted")
            
            # Check for social share image
            safe_id = pack_id.replace('/', '_')
            images_dir = os.path.join(os.path.dirname(__file__), '../web/images/packs')
            existing_images = glob.glob(os.path.join(images_dir, f"{safe_id}.social-share-image.*"))
            social_share_image_exists = bool(existing_images)
                
            packs_data[pack_id] = {
                "identifier": pack_id,
                "provider": vendor,
                "name": pack,
                "extraction_status": status,
                "extraction_folder_exists": extraction_folder_exists,
                "multiple_archive_files_would_clobber_results": multiple_archive_files_would_clobber_results,
                "has_pack_drift": has_pack_drift,
                "has_missing_log_file": has_missing_log_file,
                "extractor": extractor,
                "extracted_at": extracted_at,
                "can_be_extracted_by_automation": can_be_extracted,
                "social_share_image_exists": social_share_image_exists,
                "path": pack_path
            }
            if clobber_data:
                packs_data[pack_id]["clobbered_files"] = clobber_data
            
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(packs_data, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_FILE} with {len(packs_data)} packs.")

if __name__ == "__main__":
    generate_packs_db()
