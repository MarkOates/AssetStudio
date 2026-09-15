import os
import json
import sys
import subprocess
import datetime
import glob

ASSETS_DIR = "/Users/markoates/Assets"
PACKS_DB = os.path.join(os.path.dirname(__file__), '../web/packs.json')

def extract_pack(pack_id):
    if not os.path.exists(PACKS_DB):
        print(f"Error: Packs database not found at {PACKS_DB}")
        sys.exit(1)
        
    import fcntl
    with open(PACKS_DB, 'r', encoding='utf-8') as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            packs_data = json.load(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
        
    if pack_id not in packs_data:
        print(f"Error: Pack '{pack_id}' not found in packs.json")
        sys.exit(1)
        
    pack_info = packs_data[pack_id]
    
    if not pack_info.get("can_be_extracted_by_automation"):
        print(f"Error: Pack '{pack_id}' cannot be extracted by automation (can_be_extracted_by_automation is false).")
        sys.exit(1)
        
    pack_path = os.path.join(ASSETS_DIR, pack_id)
    if not os.path.isdir(pack_path):
        print(f"Error: Pack directory does not exist at {pack_path}")
        sys.exit(1)
        
    extracted_dir = os.path.join(pack_path, "extracted")
    if os.path.exists(extracted_dir):
        print(f"Error: 'extracted/' directory already exists for {pack_id}.")
        sys.exit(1)
        
    archives = []
    for ext in ['*.zip', '*.rar', '*.7z', '*.tar.gz']:
        archives.extend(glob.glob(os.path.join(pack_path, ext)))
        
    loose_files = []
    for item in os.listdir(pack_path):
        item_path = os.path.join(pack_path, item)
        if os.path.isfile(item_path):
            is_archive = any(item.lower().endswith(ext.replace('*', '')) for ext in ['.zip', '.rar', '.7z', '.tar.gz'])
            if not is_archive and item not in ['.DS_Store', 'download_log.txt']:
                loose_files.append(item_path)
        
    if not archives and not loose_files:
        print(f"Error: No files found to process in {pack_path}")
        sys.exit(1)
        
    os.makedirs(extracted_dir)
    print(f"Created extraction directory: {extracted_dir}")
    
    import shutil
    success = True
    
    for loose_file in loose_files:
        print(f"Copying loose file: {os.path.basename(loose_file)}...")
        try:
            shutil.copy2(loose_file, extracted_dir)
        except Exception as e:
            print(f"Failed to copy {loose_file}: {e}")
            success = False

    for archive in archives:
        print(f"Extracting: {os.path.basename(archive)}...")
        ext = archive.lower()
        try:
            if ext.endswith('.zip'):
                subprocess.run(['unzip', '-o', '-q', archive, '-d', extracted_dir], check=True)
            elif ext.endswith('.rar'):
                subprocess.run(['unrar', 'x', '-y', archive, extracted_dir + '/'], check=True)
            elif ext.endswith('.tar.gz'):
                subprocess.run(['tar', '-xzf', archive, '-C', extracted_dir], check=True)
            elif ext.endswith('.7z'):
                subprocess.run(['7z', 'x', '-y', archive, f'-o{extracted_dir}'], check=True)
            else:
                print(f"Unsupported archive format for automation: {archive}")
                success = False
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract {archive}: {e}")
            success = False
            
    if not success:
        print("Warning: Extraction completed with errors for some files. Marking as dirty.")
        dirty_file = os.path.join(extracted_dir, ".dirty")
        with open(dirty_file, 'w') as f:
            f.write("failed during extraction\n")
        print(f"Marked {pack_id} as dirty.")
    else:
        now_iso = datetime.datetime.now().astimezone().isoformat()
        
        # Update packs.json concurrently using file locks
        import fcntl
        with open(PACKS_DB, 'r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                packs_data = json.load(f)
                if pack_id in packs_data:
                    packs_data[pack_id]['extractor'] = 'automated'
                    packs_data[pack_id]['extracted_at'] = now_iso
                    packs_data[pack_id]['extraction_status'] = 'extracted'
                f.seek(0)
                json.dump(packs_data, f, indent=2)
                f.truncate()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
            
        print(f"Successfully extracted {pack_id} and updated packs.json.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/extract_pack.py <vendor/pack_name>")
        sys.exit(1)
        
    extract_pack(sys.argv[1])
