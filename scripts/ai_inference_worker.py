import os
import json
import time
import google.generativeai as genai
from PIL import Image

# Setup Paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = os.path.join(BASE_DIR, 'web', 'viewer_data.json')
CACHE_PATH = os.path.join(BASE_DIR, 'scripts', 'ai_cache.json')

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY environment variable not found.")
    exit(1)
genai.configure(api_key=api_key)

def load_cache():
    if os.path.exists(CACHE_PATH):
        try:
            with open(CACHE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=2)

def extract_color_profile(img):
    img = img.convert("RGBA")
    # maxcolors=1000 ensures if there are <1000 colors, it counts them exactly
    colors = img.getcolors(maxcolors=1000)
    
    def rgba_to_hex(r, g, b, a):
        if a == 255:
            return f"#{r:02x}{g:02x}{b:02x}"
        return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
        
    if colors and len(colors) <= 32:
        colors.sort(reverse=True, key=lambda x: x[0])
        palette = [rgba_to_hex(*c[1]) for c in colors]
        return {
            "color_space": f"{len(colors)}-color exact",
            "palette": palette,
            "is_exact_palette": True,
            "palette_swappable": True
        }
    else:
        # Too many colors. Let's just find the dominant 4 via quantization.
        try:
            quantized = img.quantize(colors=4, method=Image.MEDIANCUT).convert("RGBA")
            q_colors = quantized.getcolors(4)
            if q_colors:
                q_colors.sort(reverse=True, key=lambda x: x[0])
                palette = [rgba_to_hex(*c[1]) for c in q_colors]
            else:
                palette = []
        except Exception:
            palette = []
            
        return {
            "color_space": "full-color",
            "palette": palette[:4],
            "is_exact_palette": False,
            "palette_swappable": False
        }

def main():
    print("Loading Viewer Data...")
    with open(VIEWER_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    pending_assets = [a for a in data.get('assets', []) if a.get('needs_ai_inference') == True]
    print(f"Found {len(pending_assets)} assets needing inference.")
    
    if not pending_assets:
        print("Nothing to do.")
        return
        
    # PROCESS BATCH OF 10
    batch = pending_assets[:10]
    print(f"Starting batch process for {len(batch)} assets...")
    
    cache = load_cache()
    
    for idx, asset in enumerate(batch):
        print(f"\n--- [{idx+1}/{len(batch)}] Processing: {asset['identifier']} ({asset['name']}) ---")
        
        file_hash = asset.get('resource', {}).get('hash')
        if not file_hash:
            print("Error: Asset has no hash. Skipping.")
            continue
            
        source_files = asset.get('resource', {}).get('source_files', [])
        if not source_files:
            print("Error: Asset has no source files. Skipping.")
            continue
            
        virtual_url = source_files[0]
        physical_path = os.path.join(ASSETS_DIR, virtual_url[len("/Assets/"):])
        
        if not os.path.exists(physical_path):
            print(f"Error: Physical file missing at {physical_path}. Skipping.")
            continue
            
        print(f"Loading Image: {physical_path}")
        try:
            img = Image.open(physical_path)
            color_profile = extract_color_profile(img)
        except Exception as e:
            print(f"Error loading image (might not be an image): {e}")
            continue
        
        system_instruction = """You are an expert game asset cataloger and data engineer.
Given an image and its file path, you must analyze it using the following Formalized Heuristic Rules:

**Formalized Rules for Asset Inference:**
* **Rule 1: Strip Suffix Matching** - If the filename matches `_strip<N>`, it is a `animation_frames` with exactly `<N>` frames.
* **Rule 2: Embedded Resolution** - If the filename states a resolution like `16x16px`, these are likely the cell or tile dimensions.
* **Rule 3: Action Signatures** - Action verbs like `idle`, `walk`, `run`, `attack`, `jump`, `death` indicate character/entity animations.
* **Rule 4: Multi-File Sequences** - Filenames ending in sequential numbers (e.g., `frame0000`) denote a `multi_file` animation.
* **Rule 5: Tileset Geography** - Filenames containing `tileset`, `terrain`, `grid` indicate environment Tilemaps.
* **Rule 6: Parallax Backgrounds** - Wide aspect ratios or keywords like `sky`, `mountains`, `layers/`, `far`, `mid` indicate Background layers.
* **Rule 7: UI & HUD** - Keywords `gui`, `ui`, `border`, `cursor`, `icon` indicate interface elements.
* **Rule 8: Visual Effects (VFX)** - Keywords like `fx1_`, `explosion`, `spark`, `impact` denote particle/VFX assets.
* **Rule 9: Mockups & Previews** - Files containing `mockup`, `preview`, `sample` are valid `preview` or `showcase` assets and must be cataloged, never ignored.
* **Rule 10: Variant Tagging** - Suffixes like `_shadow`, `_outline`, `100%`, `_c1` are variant modifiers that belong in tags.
* **Rule 11: Alternative Reasoning** - If you cannot find a specific rule that fits perfectly, state your own logical reasoning here.

You MUST output ONLY valid JSON matching this exact schema:
{
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

        print("Calling Gemini Vision API (gemini-flash-latest)...")
        
        model = genai.GenerativeModel(
            model_name="gemini-flash-latest",
            system_instruction=system_instruction,
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"Analyze this game asset. It is of type '{asset['type']}', its original name is '{asset['name']}', and its file path is '{virtual_url}'."
        
        try:
            response = model.generate_content([prompt, img])
            result_data = json.loads(response.text)
            
            # Inject our perfectly computed color profile
            result_data["color_profile"] = color_profile
            
            cache[file_hash] = result_data
            save_cache(cache)
            print(f"-> Success! Cached {asset['identifier']}")
            
        except Exception as e:
            print(f"-> Error during API call or parsing: {e}")
            
        # Small delay to respect rate limits
        time.sleep(2)
        
    print("\nBatch complete! Run build_viewer_data.py to hydrate the UI.")

if __name__ == "__main__":
    main()
