import os
import json
import datetime
import zipfile
import subprocess
import tarfile

ASSETS_DIR = '/Users/markoates/Assets'
TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
OUT_FILE = f'snapshots/assets_dir_listing_{TIMESTAMP}.json'

result = []

def get_archive_contents(f_path):
    lower = f_path.lower()
    contents = []
    try:
        if lower.endswith('.zip'):
            with zipfile.ZipFile(f_path, 'r') as z:
                contents = z.namelist()
        elif lower.endswith('.rar'):
            out = subprocess.check_output(['unrar', 'lb', f_path], stderr=subprocess.STDOUT)
            contents = [x.strip() for x in out.decode('utf-8', errors='ignore').split('\n') if x.strip()]
        elif lower.endswith('.tar.gz') or lower.endswith('.tgz') or lower.endswith('.gz'):
            # only if tar
            try:
                with tarfile.open(f_path, 'r:gz') as t:
                    contents = t.getnames()
            except tarfile.ReadError:
                contents = ["(Gzip file, not a tar archive)"]
    except Exception as e:
        contents = [f"(Error reading archive: {e})"]
    return contents

for root, dirs, files in os.walk(ASSETS_DIR):
    for d in dirs:
        d_path = os.path.join(root, d)
        stat = os.stat(d_path)
        result.append({
            'path': d_path.replace(ASSETS_DIR + '/', ''),
            'type': 'directory',
            'size': stat.st_size,
            'last_updated': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        })
    for f in files:
        f_path = os.path.join(root, f)
        stat = os.stat(f_path)
        item = {
            'path': f_path.replace(ASSETS_DIR + '/', ''),
            'type': 'file',
            'size': stat.st_size,
            'last_updated': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
        
        if f_path.lower().endswith(('.zip', '.rar', '.7z', '.tar.gz', '.tgz', '.gz')):
            item['archive_contents'] = get_archive_contents(f_path)
            
        result.append(item)

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f"Snapshot saved to {OUT_FILE} with {len(result)} items.")
