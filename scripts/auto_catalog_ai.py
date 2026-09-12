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
    
    # We want to process 10 files. Let's just grab the first 10.
    batch = uncat_files[:10]
    print(f"Found {len(uncat_files)} uncatalogued files. Processing {len(batch)}...")
    
    proposals = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
    
    system_instruction = """You are an expert game asset cataloger and data engineer.
Given an image and its file path, analyze it using the Formalized Heuristic Rules to generate a catalog override.

**Formalized Rules for Asset Inference:**
* **Rule 1: Strip Suffix Matching** - If the filename matches `_strip<N>`, it is a `sprite_sheet_slice` with exactly `<N>` frames.
* **Rule 2: Embedded Resolution** - If the filename states a resolution like `16x16px`, these are likely the cell or tile dimensions.
* **Rule 3: Action Signatures** - Action verbs like `idle`, `walk`, `run`, `attack`, `jump`, `death` indicate character/entity animations.
* **Rule 4: Multi-File Sequences** - Filenames ending in sequential numbers denote a `multi_file` animation. You must flag `is_subframe: true` because it is part of a sequence.
* **Rule 5: Tileset Geography** - Filenames containing `tileset`, `terrain`, `grid` indicate environment Tilemaps.
* **Rule 6: Parallax Backgrounds** - Wide aspect ratios or keywords like `sky`, `mountains`, `layers/`, `far`, `mid` indicate Background layers.
* **Rule 7: UI & HUD** - Keywords `gui`, `ui`, `border`, `cursor`, `icon` indicate interface elements.
* **Rule 8: Visual Effects (VFX)** - Keywords like `fx1_`, `explosion`, `spark`, `impact` denote particle/VFX assets.
* **Rule 9: Mockups & Previews** - Files containing `mockup`, `preview`, `sample` are valid `preview` assets and must be cataloged.
* **Rule 10: Variant Tagging** - Suffixes like `_shadow`, `_outline`, `100%`, `_c1` are variant modifiers that belong in tags.
* **Rule 11: Alternative Reasoning** - If you cannot find a specific rule that fits perfectly, state your own logical reasoning here.

You MUST output ONLY valid JSON matching this exact schema:
{
  "catalog_proposal": {
    "name": "a unique concise name for the asset, usually derived from filename",
    "type": "sprite_sheet_slice | multi_file | static_image | preview",
    "num_frames": 1,
    "cell_dimensions": {"width": null, "height": null},
    "is_subframe": false
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
        generation_config={"response_mime_type": "application/json"}
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
                
        prompt = f"Analyze this uncatalogued game asset. Its file path is '{rel_path}'."
        
        try:
            if img:
                response = model.generate_content([prompt, img])
            else:
                response = model.generate_content([prompt])
                
            result_data = json.loads(response.text)
            
            # Construct the full asset override structure
            parts = rel_path.split('/')
            vendor = parts[0]
            pack = parts[1]
            proposed = result_data["catalog_proposal"]
            name = proposed["name"]
            
            asset_dict = {
                "identifier": f"synthetic/{vendor}/{pack}/{name}",
                "name": name,
                "asset_pack_identifier": f"{vendor}/{pack}",
                "type": proposed["type"],
                "is_subframe": proposed.get("is_subframe", False),
                "visibility": "public",
                "sheet_row_number": None,
                "resource": {
                    "type": proposed["type"],
                    "source_files": [f"/Assets/{rel_path}"],
                    "cell_dimensions": proposed.get("cell_dimensions"),
                    "hash": get_file_hash(physical_path)
                },
                "theme_profile": result_data.get("theme_profile", {}),
                "color_profile": color_profile if color_profile else {
                    "color_space": "",
                    "palette": [],
                    "is_exact_palette": False,
                    "palette_swappable": False
                }
            }
            
            # Optionally inject inference reasoning into theme_profile for debugging
            asset_dict["theme_profile"]["inference_reasoning"] = result_data.get("inference_reasoning", [])
            
            proposals.append(asset_dict)
            
            with open(PROPOSALS_PATH, 'w', encoding='utf-8') as f:
                json.dump(proposals, f, indent=2)
                
            print(f"-> Success! Synthesized asset: {asset_dict['identifier']}")
            
        except Exception as e:
            print(f"-> Error during API call or parsing: {e}")
            
        time.sleep(2)
        
    print(f"\nBatch complete! Wrote {len(proposals)} total proposals. Run build_viewer_data.py to hydrate the UI.")

if __name__ == "__main__":
    main()
