import json
import sys

def compare(old_file, new_file):
    print(f"Comparing {old_file} to {new_file}")
    
    with open(old_file, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
        
    with open(new_file, 'r', encoding='utf-8') as f:
        new_data = json.load(f)
        
    # Map paths to their dicts
    old_map = {item['path']: item for item in old_data}
    new_map = {item['path']: item for item in new_data}
    
    added = set(new_map.keys()) - set(old_map.keys())
    removed = set(old_map.keys()) - set(new_map.keys())
    
    modified = []
    
    for path in set(old_map.keys()) & set(new_map.keys()):
        old_item = old_map[path]
        new_item = new_map[path]
        
        # Compare size and archive contents
        if old_item.get('size') != new_item.get('size'):
            modified.append(f"{path} (Size changed from {old_item.get('size')} to {new_item.get('size')})")
        elif old_item.get('archive_contents') != new_item.get('archive_contents'):
            modified.append(f"{path} (Archive contents changed)")
            
    print(f"Added items: {len(added)}")
    if added:
        for a in list(added)[:5]: print("  +", a)
        if len(added) > 5: print("  ...and more")
        
    print(f"Removed items: {len(removed)}")
    if removed:
        for r in list(removed)[:5]: print("  -", r)
        if len(removed) > 5: print("  ...and more")
        
    print(f"Modified items (size/contents): {len(modified)}")
    if modified:
        for m in modified[:5]: print("  ~", m)
        if len(modified) > 5: print("  ...and more")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        compare(sys.argv[1], sys.argv[2])
    else:
        print("Usage: python compare_snapshots.py <old> <new>")
