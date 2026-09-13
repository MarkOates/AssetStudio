import os
import json
import time
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

canary_paths = [
    "finalbossblues/quirky-npcs/extracted/quirky_npcs/fullcolor/2x(RMVX)/sunandmoon.png",
    "rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Props/animated/doors/doors-wood-door frame 3-opening.png",
    "aamatniekss/grasslands-era-of-fantasy-pixelart-asset-pack/extracted/EraOfFantasy_Grasslands_v1/Animation/Small_Cliff_Sand/No_Shadow/SmallCliff_Sand_No_Shadow.png"
]

ASSETS_DIR = '/Users/markoates/Assets'

system_instruction = """You are an expert game asset cataloger and data engineer.
Given an image and its file path, analyze it using the Formalized Heuristic Rules to generate a catalog override.

**Formalized Rules for Asset Inference:**
* **Rule 1: Strip Suffix Matching** - If the filename matches `_strip<N>`, it is `animation_frames` with exactly `<N>` frames.
* **Rule 2: Embedded Resolution** - If the filename states a resolution like `16x16px`, these are likely the cell or tile dimensions.
* **Rule 3: Action Signatures** - Action verbs like `idle`, `walk`, `run`, `attack`, `jump`, `death` indicate character/entity animations.
* **Rule 4: Multi-File Sequences** - Filenames ending in sequential numbers denote a `multi_file_animation`. You must flag `is_subframe: true` because it is part of a sequence.
* **Rule 5: Environment/Tilesets** - Filenames with `tileset`, `map`, `bg`, `layer` are usually environmental. 
* **Rule 6: Parallax Backgrounds** - Wide aspect ratios or keywords like `sky`, `mountains`, `layers/`, `far`, `mid` indicate Background layers.
* **Rule 7: UI & HUD** - Keywords `gui`, `ui`, `border`, `cursor`, `icon` indicate interface elements.
* **Rule 8: Visual Effects (VFX)** - Keywords like `fx1_`, `explosion`, `spark`, `impact` denote particle/VFX assets.
* **Rule 9: Mockups & Previews** - Files containing `mockup`, `preview`, `sample` are valid `preview` assets and must be cataloged.
* **Rule 10: Variant Tagging** - Suffixes like `_shadow`, `_outline`, `100%`, `_c1` are variant modifiers that belong in tags.
* **Rule 11: Alternative Reasoning** - If you cannot find a specific rule that fits perfectly, state your own logical reasoning here.
* **Rule 12: Icons & Small Graphics** - If the asset is a very small standalone graphic (like 16x16 or 32x32) representing an item, weapon, material, or UI element, you must flag `is_icon: true`.
* **Rule 13: Visual Grid Deduction** - You MUST visually analyze sprite sheets. Do not just rely on the filename. Count the columns and rows to deduce exact pixel dimensions. If a single sheet contains MULTIPLE distinct animations on different rows, you MUST return a separate proposal for each animation sequence.
* **Rule 14: Type Definitions** - 
    - `animation_frames`: A discrete animation sequence, typically arranged as a 1D strip of frames.
    - `multi_directional_sprite`: A 2D grid containing the same animation rendered from multiple cardinal directions (e.g. 4-directional JRPG walk cycle).
    - `sprite_sheet`: A 2D atlas containing multiple distinct animations (e.g., idle, walk, attack) or an atlas of distinct items.
    - `sprite_sheet_cell`: A single static asset intended to be extracted from a larger sheet of props or items.
    - `tileset`: An environmental grid of map tiles intended to be assembled in a level editor.
    - `multi_file_animation`: A single frame image belonging to a sequentially numbered directory of frames.
    - `static_image`: A standalone image containing no animation data.
    - `preview`: Vendor promotional art or layout mockups.
    - `sound_effect` / `music`: Audio files.
    - `pixel_font` / `ttf_font`: Typography files.
    - `3d_model`: 3D object files.
    - `text`: Documentation, license, or readme files.
* **Rule 15: Multi-Directional Character Sheets** - Character sprites are frequently arranged in grids where each row represents the same animation sequence (e.g., a walk cycle) rendered from a different cardinal direction. These MUST be typed as `multi_directional_sprite` and should be interpreted as a single animation entity (`contains_multiple_animations: false`) rather than distinct narrative actions.

You MUST output ONLY valid JSON matching this exact schema:
{
  "catalog_proposal": {
    "type": "animation_frames | multi_directional_sprite | multi_file_animation | static_image | preview | sprite_sheet | sprite_sheet_cell | tileset | sound_effect | music | pixel_font | ttf_font | 3d_model | text",
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

def main():
    model = genai.GenerativeModel(
        model_name="gemini-3.5-flash-lite",
        system_instruction=system_instruction,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.0
        }
    )
    
    results = {}
    
    for rel_path in canary_paths:
        print(f"Testing Canary: {rel_path}")
        physical_path = os.path.join(ASSETS_DIR, rel_path)
        img = Image.open(physical_path)
        
        prompt = f"Analyze this uncatalogued game asset visually. The image is {img.width}x{img.height} pixels. Its file path is '{rel_path}'."
        
        response = model.generate_content([prompt, img])
        result_data = json.loads(response.text)
        
        if "sunandmoon" in rel_path:
            results["sunandmoon_png"] = result_data
        elif "doors-wood-door" in rel_path:
            results["doors-wood-door frame 3-opening_png"] = result_data
        else:
            results["SmallCliff_Sand_No_Shadow_png"] = result_data
            
        time.sleep(2)
        
    with open('scripts/canary_cheap.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    print("Canary tests finished!")

if __name__ == "__main__":
    main()
