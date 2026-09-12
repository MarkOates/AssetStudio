import json
import os
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
    "type": "animation_frames | multi_file | static_image | preview",
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
    }
  },
  "theme_profile": {
    "description": "A short, vivid description.",
    "tags": ["tag1"],
    "style": "Invent a creative style descriptor.",
    "color_descriptors": ["deep purples"]
  },
  "inference_reasoning": [
    {
      "rule": "Rule X",
      "rationale": "Explicit reason."
    }
  ]
}
"""

def run_single():
    print("Running on skeleton file...")
    rel_path = "rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Characters/Skeleton/skeleton-variation1-all animations.png"
    
    proposals = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
            
    # Purge ANY old skeleton artifacts
    proposals = [p for p in proposals if "skeleton_variation1" not in p["name"] and "skeleton-variation1" not in p["name"]]
            
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
    
    filename_with_ext = os.path.basename(rel_path)
    deterministic_name = os.path.splitext(filename_with_ext)[0]
    deterministic_id = f"synthetic/{os.path.splitext(rel_path)[0]}"
    
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
    run_single()
