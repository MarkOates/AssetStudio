import os
import csv
import json

ASSETS_DIR = "/Users/markoates/Assets"
CSV_PATH = os.path.join(ASSETS_DIR, "assets_db.csv")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../web/viewer_data.json")

def read_download_log(pack_dir):
    log_path = os.path.join(pack_dir, "download_log.txt")
    source_url = ""
    expected_files = []
    
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]
            if lines:
                source_url = lines[0]
            if len(lines) > 2:
                expected_files = lines[2:]
    return source_url, expected_files

def get_actual_files(extracted_dir):
    actual_files = []
    if os.path.exists(extracted_dir):
        for root, _, files in os.walk(extracted_dir):
            for file in files:
                if not file.startswith('.'): # ignore .DS_Store etc
                    # Get path relative to the extracted directory
                    rel_path = os.path.relpath(os.path.join(root, file), extracted_dir)
                    actual_files.append(rel_path)
    return actual_files

def main():
    providers = {}
    asset_packs = {}
    assets = []
    
    # 1. Parse the CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        # Skip the 3-line header
        data_rows = rows[3:]
        
        for row in data_rows:
            if not row or not row[0].strip():
                continue
                
            visibility = row[2]
            identifier = row[3]
            asset_pack_id = row[4] # e.g. seethingswarm/catset
            intra_pack_id = row[5]
            
            cell_width = int(row[6]) if row[6].strip() else None
            cell_height = int(row[7]) if row[7].strip() else None
            
            image_filename = row[14]
            images_list = row[15]
            
            asset_type = row[17]
            num_frames = int(row[18]) if row[18].strip() else 1
            frame_duration = float(row[20]) if row[20].strip() else 0.08
            playmode = row[24]
            
            # Register Provider & Pack
            if asset_pack_id and '/' in asset_pack_id:
                provider_name, pack_name = asset_pack_id.split('/', 1)
                
                if provider_name not in providers:
                    providers[provider_name] = {"name": provider_name}
                    
                if asset_pack_id not in asset_packs:
                    pack_dir = os.path.join(ASSETS_DIR, provider_name, pack_name)
                    extracted_dir = os.path.join(pack_dir, "extracted")
                    
                    source_url, expected_files = read_download_log(pack_dir)
                    actual_files = get_actual_files(extracted_dir)
                    
                    sync_status = "synced"
                    # Very basic sync check for V1
                    if not actual_files and expected_files:
                        sync_status = "missing_extracted_files"
                        
                    asset_packs[asset_pack_id] = {
                        "provider": provider_name,
                        "pack_name": pack_name,
                        "source_url": source_url,
                        "extracted_path": f"/Assets/{provider_name}/{pack_name}/extracted",
                        "expected_files": expected_files,
                        "actual_files_on_disk": actual_files,
                        "sync_status": sync_status
                    }
            else:
                provider_name = "unknown"
                pack_name = "unknown"
            
            # FileMapping logic
            source_files = []
            is_from_sprite_sheet = False
            
            base_url = f"/Assets/{provider_name}/{pack_name}/extracted/"
            
            if images_list:
                # Comma separated list of images
                # NOTE: CSV parser strips quotes, we do a simple split here
                files = [f.strip(' "') for f in images_list.split(',')]
                source_files = [base_url + f for f in files if f]
            elif image_filename:
                source_files = [base_url + image_filename]
                if cell_width and cell_height:
                    is_from_sprite_sheet = True
                    
            # Build the Asset
            asset = {
                "identifier": identifier,
                "name": intra_pack_id,
                "asset_pack_id": asset_pack_id,
                "type": asset_type,
                "visibility": visibility,
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
            
    # Output to JSON
    output_data = {
        "providers": providers,
        "asset_packs": asset_packs,
        "assets": assets
    }
    
    # Ensure web dir exists
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Successfully generated {OUTPUT_PATH} with {len(assets)} assets.")

if __name__ == "__main__":
    main()
