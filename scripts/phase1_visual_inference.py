import os
import json
import hashlib
import time
import datetime
import concurrent.futures
import google.generativeai as genai
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = os.path.join(BASE_DIR, 'web', 'viewer_data.json')
PROPOSALS_PATH = os.path.join(BASE_DIR, 'scripts', 'ai_subagent_proposals.json')

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
            palette = [rgba_to_hex(*c[1]) for c in colors[:16]]
            return {
                "color_space": "sRGB",
                "palette": palette,
                "dominant_colors": palette[:3],
                "transparent": True
            }
        return None
    except Exception:
        return None

def get_file_hash(filepath):
    if not os.path.exists(filepath): return None
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

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
    * **Rule 16: Perspective Analysis** - You MUST deduce the camera perspective of the asset (e.g., top_down, 3/4_isometric, side_scroller, ui_overlay, unknown) and provide your reasoning in the inference_reasoning array.

You MUST output ONLY valid JSON matching this exact schema:
{
  "catalog_proposal": {
    "type": "animation_frames | multi_directional_sprite | multi_file_animation | static_image | preview | sprite_sheet | sprite_sheet_cell | tileset | sound_effect | music | pixel_font | ttf_font | 3d_model | text",
    "perspective": "top_down | 3/4_isometric | side | ui_overlay | unknown",
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
    model_name="gemini-3.5-flash-lite",
    system_instruction=system_instruction,
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.0
    }
)


def process_asset(rel_path):
    physical_path = os.path.join(ASSETS_DIR, rel_path)
    
    if not os.path.exists(physical_path):
        return None
        
    ext = os.path.splitext(physical_path)[1].lower()
    asset_extensions = ('.png', '.gif', '.jpg', '.jpeg', '.wav', '.ogg', '.mp3')
    
    if ext not in asset_extensions:
        filename_with_ext = os.path.basename(rel_path)
        deterministic_name = os.path.splitext(filename_with_ext)[0]
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        parts = rel_path.split('/')
        vendor = parts[0]
        if len(parts) > 1:
            pack = parts[1] if parts[1] != "extracted" else parts[0]
        else:
            pack = "unknown"
            
        return {
            "identifier": deterministic_id,
            "name": deterministic_name,
            "asset_pack_identifier": f"{vendor}/{pack}",
            "type": "blacklisted_file",
            "is_subframe": False,
            "is_icon": False,
            "visibility": "hidden",
            "sheet_row_number": None,
            "blacklisted_type": ext if ext else "unknown",
            "resource": {
                "type": "blacklisted_file",
                "source_files": [f"/Assets/{rel_path}"]
            },
            "theme_profile": {
                "description": "Blacklisted file type skipped during AI evaluation.",
                "tags": [ext.strip('.') if ext else "unknown", "blacklisted"],
                "style": "None",
                "color_descriptors": []
            }
        }
        
    img = None
    color_profile = None
    if ext in ('.png', '.jpg', '.jpeg', '.gif'):
        try:
            img = Image.open(physical_path)
            color_profile = extract_color_profile(img)
        except Exception:
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
        if len(parts) > 1:
            pack = parts[1] if parts[1] != "extracted" else parts[0]
        else:
            pack = "unknown"
            
        proposed = result_data["catalog_proposal"]
        
        if proposed.get("type") in ["static_image", "preview"] or proposed.get("is_subframe"):
            proposed["inferred_grid"] = None
        
        filename_with_ext = os.path.basename(rel_path)
        deterministic_name = os.path.splitext(filename_with_ext)[0]
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        
        
        audit_block = result_data.get("ai_audit", {})
        audit_block["pass1_model"] = "gemini-3.5-flash-lite"
        audit_block["pass1_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        asset_dict = {
            "identifier": deterministic_id,
            "name": deterministic_name,
            "asset_pack_identifier": f"{vendor}/{pack}",
            "type": proposed.get("type", "static_image"),
            "is_subframe": proposed.get("is_subframe", False),
            "is_icon": proposed.get("is_icon", False),
            "visibility": "public",
            "sheet_row_number": None,
            "blacklisted_type": None,
            "resource": {
                "type": proposed.get("type", "static_image"),
                "source_files": [f"/Assets/{rel_path}"],
                "cell_dimensions": proposed.get("cell_dimensions", None),
                "inferred_grid": proposed.get("inferred_grid", None),
            },
            "animation_profile": {
                "num_frames": proposed.get("num_frames", 1),
                "base_frame_duration": 0.1
            } if proposed.get("num_frames", 1) > 1 else None,
            "theme_profile": result_data.get("theme_profile", {}),
            "inference_reasoning": result_data.get("inference_reasoning", []),
            "ai_audit": audit_block
        }
        
        if img and proposed.get("inferred_grid") and not proposed.get("is_subframe"):
            if "cell_dimensions" in asset_dict["resource"] and asset_dict["resource"]["cell_dimensions"]:
                # Keep inferred
                pass
            else:
                asset_dict["resource"]["cell_dimensions"] = {"width": img.width, "height": img.height}
                
        if color_profile:
            asset_dict["theme_profile"]["color_profile"] = color_profile
            
        return asset_dict
        
    except Exception as e:
        print(f"Error processing {rel_path}: {e}")
        return None


def main():
    print("Finding ALL remaining uncatalogued files...")
    with open(VIEWER_DATA_PATH, 'r', encoding='utf-8') as f:
        vdata = json.load(f)
        
    proposals = set()
    for fp in ['scripts/ai_catalog_proposals.json', 'scripts/ai_subagent_proposals.json']:
        if os.path.exists(fp):
            with open(fp, 'r', encoding='utf-8') as f:
                for p in json.load(f):
                    proposals.add(p['identifier'])
                    
    uncat_files = [e['context']['file'] for e in vdata.get('errors', []) if e['type'] == 'UncataloguedFile']
    remaining = [u for u in uncat_files if f"synthetic/{u.replace('.', '_')}" not in proposals]
    
    targets = remaining
    
    print(f"Starting concurrent processing of {len(targets)} assets with 9 workers...")
    
    results = []
    
    # Process concurrently
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = {executor.submit(process_asset, t): t for t in targets}
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            completed += 1
            res = future.result()
            if res:
                results.append(res)
                print(f"[{completed}/{len(targets)}] Processed {res['name']}")
                
    duration = time.time() - start_time
    print(f"Finished processing {len(results)} assets in {duration:.1f} seconds ({(duration/len(results)):.2f}s per asset).")
    
    existing = []
    if os.path.exists(PROPOSALS_PATH):
        with open(PROPOSALS_PATH, 'r', encoding='utf-8') as f:
            existing = json.load(f)
            
    existing.extend(results)
    
    tmp_path = PROPOSALS_PATH + '.tmp'
    with open(tmp_path, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)
    os.rename(tmp_path, PROPOSALS_PATH)
    
    print(f"Appended {len(results)} assets to {PROPOSALS_PATH}")

if __name__ == "__main__":
    main()
