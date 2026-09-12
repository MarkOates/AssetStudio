import os
import json
import hashlib
import time
import google.generativeai as genai
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = os.path.join(BASE_DIR, 'web', 'viewer_data.json')
PROPOSALS_PATH = os.path.join(BASE_DIR, 'scripts', 'ai_catalog_proposals.json')

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_color_profile(img):
    try:
        img = img.convert("RGBA")
        colors = img.getcolors(maxcolors=1000)
        
        def rgba_to_hex(r, g, b, a):
            if a == 255: return f"#{r:02x}{g:02x}{b:02x}"
            return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
            
        if colors and len(colors) <= 32:
            colors.sort(reverse=True, key=lambda x: x[0])
            return {
                "color_space": f"{len(colors)}-color exact",
                "palette": [rgba_to_hex(*c[1]) for c in colors],
                "is_exact_palette": True,
                "palette_swappable": True
            }
        else:
            quantized = img.quantize(colors=4, method=Image.MEDIANCUT).convert("RGBA")
            q_colors = quantized.getcolors(4)
            q_colors.sort(reverse=True, key=lambda x: x[0]) if q_colors else None
            return {
                "color_space": "full-color",
                "palette": [rgba_to_hex(*c[1]) for c in q_colors] if q_colors else [],
                "is_exact_palette": False,
                "palette_swappable": False
            }
    except Exception:
        return None

def get_file_hash(filepath):
    if not os.path.exists(filepath): return None
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def main():
    print("Loading Viewer Data to find UncataloguedFiles...")
    with open(VIEWER_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    errors = data.get('errors', [])
    uncat_files = [e['context']['file'] for e in errors if e['type'] == 'UncataloguedFile']
    
    proposals = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
            
    proposed_paths = set(p['resource']['source_files'][0].replace('/Assets/', '') for p in proposals if p.get('resource') and p['resource'].get('source_files'))
    
    uncat_files = [f for f in uncat_files if f not in proposed_paths]
    
    # Process 500 new files
    batch = uncat_files[:50]
    print(f"Found {len(uncat_files)} uncatalogued files. Processing {len(batch)}...")
    
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
* **Rule 15: Multi-Directional Character Sheets** - Character sprites are frequently arranged in grids where each row represents the same animation sequence (e.g., a walk cycle) rendered from a different cardinal direction. These should be interpreted as a single animation entity (`contains_multiple_animations: false`) rather than distinct narrative actions.

You MUST output ONLY valid JSON matching this exact schema:
{
  "catalog_proposal": {
    "type": "animation_frames | multi_file_animation | static_image | preview | sprite_sheet | sprite_sheet_cell | tileset | sound_effect | music | pixel_font | ttf_font | 3d_model | text",
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
            print(f"Error: Physical file missing at {physical_path}. Skipping.")
            continue
            
        print(f"Loading Image: {physical_path}")
        img = None
        color_profile = None
        if physical_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                img = Image.open(physical_path)
                color_profile = extract_color_profile(img)
            except Exception as e:
                print(f"Error loading image: {e}")
                
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
            
            # Enforce null inferred_grid for static images and subframes to prevent engine bloat
            if proposed.get("type") in ["static_image", "preview"] or proposed.get("is_subframe"):
                proposed["inferred_grid"] = None
            
            # DETERMINISTIC IDENTIFIER & NAME FROM FILEPATH
            # e.g. "rafaelmatos/epic-rpg-world/characters/skeleton.png"
            filename_with_ext = os.path.basename(rel_path)
            deterministic_name = os.path.splitext(filename_with_ext)[0]
            
            # Create a 100% unique identifier by retaining the full path AND extension (sanitizing the dot)
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
                "color_profile": color_profile if color_profile else {
                    "color_space": "",
                    "palette": [],
                    "dominant_colors": [],
                    "transparent": False
                },
                "ai_audit": {
                    "pass1_model": "gemini-flash-latest",
                    "pass1_timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
                }
            }
            if proposed.get("num_frames") and proposed["num_frames"] > 1:
                asset_dict["animation_profile"] = {
                    "num_frames": proposed["num_frames"],
                    "base_frame_duration": 0.1,
                    "loop_type": "forward"
                }
            
            proposals.append(asset_dict)
            print(f"-> Success! Synthesized asset: {asset_dict['identifier']}")
            
            with open(PROPOSALS_PATH, 'w', encoding='utf-8') as f:
                json.dump(proposals, f, indent=2)
            
        except Exception as e:
            print(f"-> Error parsing API response: {e}")
            
        time.sleep(2)
        
    print(f"\nBatch complete! Wrote {len(proposals)} total proposals. Run build_viewer_data.py to hydrate the UI.")

if __name__ == "__main__":
    main()
