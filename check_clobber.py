import json

SNAPSHOT_FILE = 'snapshots/assets_dir_listing_20260914_110524.json'
with open(SNAPSHOT_FILE, 'r', encoding='utf-8') as f:
    snapshot = json.load(f)

packs = {}
for item in snapshot:
    parts = item['path'].split('/')
    if len(parts) >= 2:
        pack_id = f"{parts[0]}/{parts[1]}"
        if pack_id not in packs:
            packs[pack_id] = {'archives': {}}
        
        if item.get('archive_contents'):
            packs[pack_id]['archives'][item['path']] = item['archive_contents']

clobbering_packs = []
total_clobber_files = 0

for pack_id, data in packs.items():
    archives = data['archives']
    if len(archives) > 1:
        # Check for overlaps
        seen_files = {}
        pack_clobbers = set()
        
        for arch_path, contents in archives.items():
            for f in contents:
                if f.endswith('/'): continue # Ignore directories
                if f in seen_files:
                    pack_clobbers.add(f)
                else:
                    seen_files[f] = arch_path
                    
        if pack_clobbers:
            clobbering_packs.append({
                'pack': pack_id,
                'clobbered_files_count': len(pack_clobbers),
                'archives_involved': list(archives.keys())
            })
            total_clobber_files += len(pack_clobbers)

print(f"Found {len(clobbering_packs)} packs that would have clobbering issues.")
print(f"Total files that would be overwritten: {total_clobber_files}")

for issue in clobbering_packs[:10]:
    print(f"- Pack: {issue['pack']}")
    print(f"  Archives: {issue['archives_involved']}")
    print(f"  Overlapping files: {issue['clobbered_files_count']}")

if len(clobbering_packs) > 10:
    print(f"... and {len(clobbering_packs) - 10} more.")
