import json
import os
from collections import Counter

SNAPSHOT_FILE = 'snapshots/assets_dir_listing_20260914_110524.json'
with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
    snapshot = json.load(f)

packs = {}
for item in snapshot:
    parts = item['path'].split('/')
    if len(parts) >= 2:
        pack_id = f"{parts[0]}/{parts[1]}"
        if pack_id not in packs:
            packs[pack_id] = {'has_extracted': False, 'archives': []}
        
        if len(parts) >= 3 and parts[2] == 'extracted':
            packs[pack_id]['has_extracted'] = True
            
        if item.get('archive_contents'):
            packs[pack_id]['archives'].append(item)

unextracted_packs = {k: v for k, v in packs.items() if not v['has_extracted']}

asset_extensions = ('.png', '.gif', '.jpg', '.jpeg', '.wav', '.ogg', '.mp3')
other_extensions = Counter()
directories = 0
no_extension = 0

for pack_id, data in unextracted_packs.items():
    for arch in data['archives']:
        contents = arch['archive_contents']
        for f in contents:
            # Check if it's a directory (usually ends with / in zip files)
            if f.endswith('/'):
                directories += 1
                continue
                
            ext = os.path.splitext(f)[1].lower()
            if ext not in asset_extensions:
                if ext:
                    other_extensions[ext] += 1
                else:
                    no_extension += 1

print(f"Directories (in zip internal structure): {directories}")
print(f"Files with no extension: {no_extension}")
print("\nTop 30 other extensions:")
for ext, count in other_extensions.most_common(30):
    print(f"{ext}: {count}")

