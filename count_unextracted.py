import json

SNAPSHOT_FILE = 'snapshots/assets_dir_listing_20260914_110524.json'
with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
    snapshot = json.load(f)

# Find all pack directories that don't have an 'extracted' subfolder
# Actually, the easiest way is to group by pack directory
packs = {}
for item in snapshot:
    # item path is like "vendor/pack/filename"
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
total_asset_files = 0
total_archives = 0
total_all_files = 0

for pack_id, data in unextracted_packs.items():
    for arch in data['archives']:
        total_archives += 1
        contents = arch['archive_contents']
        total_all_files += len(contents)
        for f in contents:
            if f.lower().endswith(asset_extensions):
                total_asset_files += 1

print(f"Found {len(unextracted_packs)} unextracted packs.")
print(f"These packs contain {total_archives} archives.")
print(f"Inside these archives, there are {total_all_files} total files.")
print(f"Of those, {total_asset_files} are recognizable asset files (images/audio).")

