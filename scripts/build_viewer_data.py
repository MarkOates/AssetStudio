import os
import csv
import json

ASSETS_DIR = "/Users/markoates/Assets"
CSV_PATH = os.path.join(ASSETS_DIR, "assets_db.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../web/viewer_data.json")

# --- CUSTOM EXCEPTIONS ---
class AssetException(Exception): pass
class MissingOrigin(AssetException): pass
class UnextractedPack(AssetException): pass
class UncataloguedFile(AssetException): pass
class MissingFile(AssetException): pass
class DuplicateIdentifier(AssetException): pass
class MalformedSpriteData(AssetException): pass
class PackDrift(AssetException): pass

# Global error log
audit_errors = []

def log_error(error_class_name, message, context):
    audit_errors.append({
        "type": error_class_name,
        "message": message,
        "context": context
    })

def read_download_log(pack_dir):
    log_path = os.path.join(pack_dir, "download_log.txt")
    source_url = ""
    expected_files = []
    expected_count = 0
    
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if lines:
                source_url = lines[0]
            if len(lines) > 1 and lines[1].isdigit():
                expected_count = int(lines[1])
            if len(lines) > 2:
                expected_files = lines[2:]
    return source_url, expected_count, expected_files

def get_actual_files(extracted_dir):
    actual_files = []
    abs_files = []
    if os.path.exists(extracted_dir):
        for root, _, files in os.walk(extracted_dir):
            for file in files:
                if not file.startswith('.') and file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.wav', '.ogg', '.mp3', '.json')):
                    abs_path = os.path.join(root, file)
                    rel_path = os.path.relpath(abs_path, extracted_dir)
                    actual_files.append(rel_path)
                    abs_files.append(abs_path)
    return actual_files, abs_files

def main():
    providers = {}
    asset_packs = {}
    assets = []
    
    all_physical_files = set()
    tracked_logical_files = set()
    seen_identifiers = set()
    
    # 1. Audit Physical Packs (Discover A & D errors)
    if os.path.exists(ASSETS_DIR):
        for provider in os.listdir(ASSETS_DIR):
            provider_path = os.path.join(ASSETS_DIR, provider)
            if not os.path.isdir(provider_path) or provider.startswith('.'):
                continue
                
            for pack in os.listdir(provider_path):
                pack_path = os.path.join(provider_path, pack)
                if not os.path.isdir(pack_path) or pack.startswith('.'):
                    continue
                    
                pack_id = f"{provider}/{pack}"
                log_path = os.path.join(pack_path, "download_log.txt")
                extracted_dir = os.path.join(pack_path, "extracted")
                
                # Check MissingOrigin
                if not os.path.exists(log_path):
                    log_error("MissingOrigin", "Missing download_log.txt", {"pack_id": pack_id})
                
                source_url, expected_count, expected_files = read_download_log(pack_path)
                
                # Check PackDrift
                if os.path.exists(log_path):
                    actual_archives = len([f for f in os.listdir(pack_path) if os.path.isfile(os.path.join(pack_path, f)) and not f.endswith('.txt') and not f.startswith('.')])
                    if actual_archives != expected_count:
                        log_error("PackDrift", f"Expected {expected_count} archives, found {actual_archives}", {"pack_id": pack_id})
                
                # Check UnextractedPack
                actual_rel_files, actual_abs_files = get_actual_files(extracted_dir)
                if not os.path.exists(extracted_dir) or not actual_abs_files:
                    log_error("UnextractedPack", "Missing or empty extracted/ folder", {"pack_id": pack_id})
                else:
                    all_physical_files.update(actual_abs_files)
                
                providers[provider] = {"name": provider}
                asset_packs[pack_id] = {
                    "provider": provider,
                    "pack_name": pack,
                    "source_url": source_url,
                    "extracted_path": f"/Assets/{provider}/{pack}/extracted",
                    "expected_files": expected_files,
                    "actual_files_on_disk": actual_rel_files,
                    "sync_status": "synced" if actual_abs_files else "missing_extracted_files"
                }

    # 2. Parse the CSV (Discover C & B errors)
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            data_rows = rows[3:]
            
            for i, row in enumerate(data_rows, start=4):
                if not row or not row[0].strip():
                    continue
                    
                visibility = row[2]
                identifier = row[3]
                asset_pack_id = row[4]
                intra_pack_id = row[5]
                
                # Check DuplicateIdentifier
                if identifier in seen_identifiers:
                    log_error("DuplicateIdentifier", "Duplicate identifier found in CSV", {"identifier": identifier, "row": i})
                seen_identifiers.add(identifier)
                
                cell_width = int(row[6]) if row[6].strip() else None
                cell_height = int(row[7]) if row[7].strip() else None
                image_filename = row[14]
                images_list = row[15]
                asset_type = row[17]
                num_frames_raw = row[18].strip()
                num_frames = int(num_frames_raw) if num_frames_raw else 1
                frame_duration_raw = row[20].strip()
                frame_duration = float(frame_duration_raw) if frame_duration_raw else 0.08
                playmode = row[24]
                
                # Check MalformedSpriteData
                if (cell_width or cell_height) and not num_frames_raw:
                    log_error("MalformedSpriteData", "Asset has cell dimensions but missing num_frames.", {"identifier": identifier, "row": i})
                if asset_type == 'animation' and not frame_duration_raw:
                    log_error("MalformedSpriteData", "Asset is an animation but missing frame_duration.", {"identifier": identifier, "row": i})

                source_files = []
                is_from_sprite_sheet = False
                base_url = f"/Assets/{asset_pack_id}/extracted/"
                
                if images_list:
                    files = [f.strip(' "') for f in images_list.split(',')]
                    source_files = [base_url + f for f in files if f]
                elif image_filename:
                    source_files = [base_url + image_filename]
                    if cell_width and cell_height:
                        is_from_sprite_sheet = True
                
                # Check MissingFile and track logical files
                for src in source_files:
                    # Map the virtual URL to physical path for checking
                    physical_src = os.path.join(ASSETS_DIR, src[len("/Assets/"):])
                    if not os.path.exists(physical_src):
                        log_error("MissingFile", "CSV expects a file but it is missing on disk.", {"identifier": identifier, "file": src, "row": i})
                    else:
                        tracked_logical_files.add(physical_src)
                        
                asset = {
                    "identifier": identifier,
                    "name": intra_pack_id,
                    "asset_pack_id": asset_pack_id,
                    "type": asset_type,
                    "visibility": visibility,
                    "sheet_row_number": i,
                    "animation_profile": {
                        "playmode": playmode,
                        "num_frames": num_frames,
                        "frame_duration": frame_duration
                    },
                    "FileMapping": {
                        "source_files": source_files,
                        "is_from_sprite_sheet": is_from_sprite_sheet,
                        "cell_dimensions": {
                            "width": cell_width,
                            "height": cell_height
                        } if is_from_sprite_sheet else None
                    }
                }
                assets.append(asset)

    # 3. Final Sweep: UncataloguedFiles (Discover B errors)
    for physical_file in all_physical_files:
        if physical_file not in tracked_logical_files:
            rel_file = physical_file[len(ASSETS_DIR):].lstrip('/') # e.g. provider/pack/extracted/...
            log_error("UncataloguedFile", "File exists on disk but is uncatalogued", {"file": rel_file})

    # Output to JSON
    output_data = {
        "providers": providers,
        "asset_packs": asset_packs,
        "assets": assets,
        "errors": audit_errors
    }
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Generated {OUTPUT_PATH} with {len(assets)} assets and {len(audit_errors)} errors detected.")

if __name__ == "__main__":
    main()
