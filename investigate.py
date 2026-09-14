import os
ASSETS_DIR = '/Users/markoates/Assets'
for vendor in os.listdir(ASSETS_DIR):
    vendor_path = os.path.join(ASSETS_DIR, vendor)
    if not os.path.isdir(vendor_path) or vendor.startswith('.'): continue
    for pack in os.listdir(vendor_path):
        pack_path = os.path.join(vendor_path, pack)
        if not os.path.isdir(pack_path) or pack.startswith('.'): continue
        extracted = os.path.join(pack_path, 'extracted')
        if os.path.isdir(extracted):
            archives = [f for f in os.listdir(pack_path) if f.lower().endswith(('.zip', '.rar'))]
            if archives:
                children = [f for f in os.listdir(extracted) if not f.startswith('.')]
                matched = any(os.path.splitext(a)[0] in children for a in archives)
                if not matched:
                    print(f"\nMismatch found in: {vendor}/{pack}")
                    print(f"Archives: {archives}")
                    print(f"Extracted children: {children}")
