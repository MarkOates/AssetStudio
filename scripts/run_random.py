import json
import os
import random
import google.generativeai as genai
from PIL import Image
import hashlib

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
from auto_catalog_ai import extract_color_profile, get_file_hash, PROPOSALS_PATH, ASSETS_DIR

system_instruction = """You are an expert game asset cataloger and data engineer.
You are analyzing game assets visually on a strict 1:1 file-to-asset basis. Do not slice the file.

You MUST output ONLY valid JSON matching this exact schema:
{
  "catalog_proposal": {
    "type": "animation_frames | multi_file | static_image | preview | sprite_sheet | sprite_sheet_cell",
    "num_frames": 1,
    "cell_dimensions": {"width": null, "height": null},
    "is_subframe": false,
    "is_icon": false,
    "inferred_grid": {
      "columns": 1,
      "rows": 1,
      "cell_width": 128,
      "cell_height": 128,
      "contains_multiple_animations": false,
      "inferred_animations": [
        {
          "name": "idle",
          "row": 0,
          "start_frame": 0,
          "frame_count": 7,
          "inference_reasoning": [
            {
              "rule": "Visual Deduction",
              "rationale": "Row 0 clearly shows a character standing still."
            }
          ]
        }
      ]
    } // Set to null if the asset is a static image or a single subframe
  },
  "theme_profile": {
    "description": "A short, vivid description of the asset.",
    "tags": ["tag1", "tag2"],
    "style": "Invent a creative style descriptor based on the asset, or leave blank if not applicable.",
    "color_descriptors": ["deep purples", "soft minty green", "orange"]
  },
  "inference_reasoning": [
    {
      "rule": "Rule X: Name of Rule",
      "rationale": "Explicit reason why this rule applies to this asset."
    }
  ]
}
DO NOT wrap the response in markdown blocks like ```json. Just return the raw JSON object."""

def run():
    print("Finding random assets...")
    
    with open('web/viewer_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    errors = data.get('errors', [])
    uncat_files = [e['context']['file'] for e in errors if e['type'] == 'UncataloguedFile']
    
    random.shuffle(uncat_files)
    batch = uncat_files[:20]
    
    proposals = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
            
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest",
        system_instruction=system_instruction,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.0
        }
    )
    
    for idx, rel_path in enumerate(batch):
        print(f"\n--- [{idx+1}/{len(batch)}] Processing: {rel_path} ---")
        physical_path = os.path.join(ASSETS_DIR, rel_path)
        
        if not os.path.exists(physical_path):
            continue
            
        img = None
        color_profile = None
        if physical_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                img = Image.open(physical_path)
                color_profile = extract_color_profile(img)
            except Exception as e:
                pass
                
        prompt = f"Analyze this uncatalogued game asset visually. The image is {img.width}x{img.height} pixels. Its file path is '{rel_path}'." if img else f"Analyze this uncatalogued game asset. Its file path is '{rel_path}'."
        
        try:
            if img:
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content([prompt])
                
            result_data = json.loads(response.text)
            
            parts = rel_path.split('/')
            vendor = parts[0]
            pack = parts[1]
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
                "color_profile": color_profile if color_profile else {},
                "ai_audit": {
                    "pass1_model": "gemini-flash-latest",
                    "pass1_timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
                }
            }
            proposals.append(asset_dict)
            print(f"-> Success! Synthesized asset: {asset_dict['identifier']} as {proposed['type']}")
        except Exception as e:
            print(f"Failed: {e}")
            
    with open(PROPOSALS_PATH, 'w', encoding='utf-8') as f:
        json.dump(proposals, f, indent=2)

if __name__ == "__main__":
    run()
