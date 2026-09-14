import os
import json
import datetime

ASSETS_DIR = '/Users/markoates/Assets'
OUT_FILE = 'snapshots/assets_dir_listing.json'

result = []

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
        result.append({
            'path': f_path.replace(ASSETS_DIR + '/', ''),
            'type': 'file',
            'size': stat.st_size,
            'last_updated': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
        })

with open(OUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2)

print(f"Snapshot saved to {OUT_FILE} with {len(result)} items.")
