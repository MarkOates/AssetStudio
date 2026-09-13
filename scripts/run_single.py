import sys
import json
import os
import google.generativeai as genai
from PIL import Image
import hashlib
import ast

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
from auto_catalog_ai import extract_color_profile, get_file_hash, PROPOSALS_PATH, ASSETS_DIR

# Dynamically extract system_instruction from auto_catalog_ai.py to avoid hardcoding
with open('scripts/auto_catalog_ai.py', 'r') as f:
    source = f.read()
tree = ast.parse(source)
system_instruction = ""
for node in ast.walk(tree):
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == 'system_instruction':
                system_instruction = node.value.value
                break

def run_single(rel_path):
    print(f"Running on {rel_path}...")
    
    proposals = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
            
    # Purge ANY old artifacts pointing to this source file
    proposals = [p for p in proposals if rel_path not in p["resource"]["source_files"]]
            
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=system_instruction,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.0
        }
    )
    
    physical_path = os.path.join(ASSETS_DIR, rel_path)
    img = Image.open(physical_path)
    color_profile = extract_color_profile(img)
    
    prompt = f"Analyze this uncatalogued game asset visually. The image is {img.width}x{img.height} pixels. Its file path is '{rel_path}'."
    response = model.generate_content([prompt, img])
    
    result_data = json.loads(response.text)
    
    vendor = rel_path.split('/')[0]
    pack = rel_path.split('/')[1]
    
    proposed = result_data["catalog_proposal"]
    
    if proposed.get("type") in ["static_image", "preview"] or proposed.get("is_subframe"):
        proposed["inferred_grid"] = None
    
    filename_with_ext = os.path.basename(rel_path)
    deterministic_name = os.path.splitext(filename_with_ext)[0]
    safe_rel_path = rel_path.replace('.', '_')
    deterministic_id = f"synthetic/{safe_rel_path}"
    
    asset_dict = {
        "identifier": deterministic_id,
        "name": deterministic_name,
        "asset_pack_identifier": f"{vendor}/{pack}",
        "type": proposed["type"],
        "is_subframe": proposed.get("is_subframe", False),
        "is_icon": proposed.get("is_icon", False),
        "visibility": "public",
        "sheet_row_number": None,
        "resource": {
            "type": proposed["type"],
            "source_files": [f"/Assets/{rel_path}"],
            "cell_dimensions": proposed.get("cell_dimensions"),
            "inferred_grid": proposed.get("inferred_grid"),
            "hash": get_file_hash(physical_path)
        },
        "theme_profile": result_data.get("theme_profile", {}),
        "inference_reasoning": result_data.get("inference_reasoning", []),
        "color_profile": color_profile
    }
    
    proposals.append(asset_dict)
    print(f"-> Success! Synthesized asset: {asset_dict['identifier']}")
        
    with open(PROPOSALS_PATH, 'w', encoding='utf-8') as f:
        json.dump(proposals, f, indent=2)

if __name__ == "__main__":
    run_single(sys.argv[1])
