import os

ASSETS_DIR = '/Users/markoates/Assets'

total_packs = 0
has_extracted = 0
no_extracted = 0

extracted_patterns = {
    'direct_to_extracted': 0,
    'into_named_subfolder': 0,
    'unclear': 0
}

for vendor in os.listdir(ASSETS_DIR):
    vendor_path = os.path.join(ASSETS_DIR, vendor)
    if not os.path.isdir(vendor_path): continue
    if vendor.startswith('.'): continue
    
    for pack in os.listdir(vendor_path):
        pack_path = os.path.join(vendor_path, pack)
        if not os.path.isdir(pack_path): continue
        if pack.startswith('.'): continue
        
        total_packs += 1
        
        extracted_path = os.path.join(pack_path, 'extracted')
        if os.path.exists(extracted_path) and os.path.isdir(extracted_path):
            has_extracted += 1
            
            # Now let's analyze the extraction policy
            # Find archives in the pack folder
            archives = [f for f in os.listdir(pack_path) if f.lower().endswith(('.zip', '.rar', '.7z', '.tar.gz'))]
            
            # Look at immediate children of extracted/
            children = [f for f in os.listdir(extracted_path) if not f.startswith('.')]
            
            if not archives:
                extracted_patterns['unclear'] += 1
                continue
                
            # Heuristic: did it create a folder matching the zip name?
            # E.g. "asset_pack_v1.zip" -> "asset_pack_v1"
            matched_named_folder = False
            for arch in archives:
                base_name = os.path.splitext(arch)[0]
                if base_name in children:
                    matched_named_folder = True
                    break
                    
            if matched_named_folder:
                extracted_patterns['into_named_subfolder'] += 1
            else:
                # If the zip didn't create a folder exactly matching its name, 
                # did it just extract internal contents directly?
                # Usually if there are many files/folders in extracted/ that don't match the zip name,
                # it was extracted directly.
                extracted_patterns['direct_to_extracted'] += 1
                
        else:
            no_extracted += 1

print(f"Total packs analyzed: {total_packs}")
print(f"Packs WITH 'extracted/' folder: {has_extracted}")
print(f"Packs WITHOUT 'extracted/' folder: {no_extracted}")
print("\nExtraction Policy Inference (for packs with archives):")
print(f"- Extracted into a named subfolder matching archive name: {extracted_patterns['into_named_subfolder']}")
print(f"- Extracted directly into 'extracted/' (or mismatched folder name): {extracted_patterns['direct_to_extracted']}")
print(f"- Unclear (no archives found in pack root): {extracted_patterns['unclear']}")

