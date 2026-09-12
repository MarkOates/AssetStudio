import os
import json
import google.generativeai as genai
from PIL import Image

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

def test_file(physical_path):
    print(f"\n=======================")
    print(f"Testing: {physical_path}")
    
    img = None
    color_profile = None
    if physical_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        try:
            img = Image.open(physical_path)
            color_profile = extract_color_profile(img)
        except Exception as e:
            print(f"Image load error: {e}")
            
    system_instruction = """You are an expert game asset cataloger and data engineer.
Given a file path (and optionally an image), analyze it using the following Formalized Heuristic Rules:

**Formalized Rules for Asset Inference:**
* **Rule 1: Strip Suffix Matching** - If the filename matches `_strip<N>`, it is a `animation_frames` with exactly `<N>` frames.
* **Rule 2: Embedded Resolution** - If the filename states a resolution like `16x16px`, these are likely the cell or tile dimensions.
* **Rule 3: Action Signatures** - Action verbs like `idle`, `walk`, `run`, `attack`, `jump`, `death` indicate character/entity animations.
* **Rule 4: Multi-File Sequences** - Filenames ending in sequential numbers (e.g., `frame0000`) denote a `multi_file` animation.
* **Rule 5: Tileset Geography** - Filenames containing `tileset`, `terrain`, `grid` or paths containing `tilesets/` indicate environment Tilemaps.
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
    "style": "Invent a creative style descriptor based on the asset, or leave blank if not applicable."
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
    
    prompt = f"Analyze this game asset. Its file path is '{physical_path}'."
    
    try:
        if img:
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content([prompt])
            
        result_data = json.loads(response.text)
        if color_profile:
            result_data["color_profile"] = color_profile
            
        print(json.dumps(result_data, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")

test_file("/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/SENGOKU ADVENTURE TILESET/NIGHT/NIGHT GROUND TOP 5.png")
test_file("/Users/markoates/Assets/ansimuz/super-grotto-escape-godot-project/extracted/SuperGrottoEscape/UI/Pixel.ttf")

