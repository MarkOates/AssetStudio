import os
import json
import hashlib
import time
import google.generativeai as genai

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = os.path.join(BASE_DIR, 'web', 'viewer_data.json')
BLUEPRINTS_PATH = os.path.join(BASE_DIR, 'scripts', 'structural_blueprints.json')

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def main():
    print("Loading Viewer Data to find UncataloguedFiles...")
    with open(VIEWER_DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    errors = data.get('errors', [])
    uncat_files = [e['context']['file'] for e in errors if e['type'] == 'UncataloguedFile']
    
    # Group uncatalogued files by their parent directory
    directories = {}
    for f in uncat_files:
        d = os.path.dirname(f)
        if d not in directories:
            directories[d] = []
        directories[d].append(f)
        
    print(f"Found {len(uncat_files)} uncatalogued files across {len(directories)} directories.")
    
    blueprints = {}
    if os.path.exists(BLUEPRINTS_PATH):
        try:
            with open(BLUEPRINTS_PATH, 'r', encoding='utf-8') as f:
                blueprints = json.load(f)
        except Exception:
            pass
            
    system_instruction = """You are an expert game asset data architect. 
I am giving you a list of physical files located in a specific directory (and optionally, the text content of any metadata files found there).
Your job is to mathematically deduce how these raw files should be grouped into parent assets.

**Reasoning Rules for Structural Inference:**
* **Rule 1: GraphicallySimilar** - Files with sequentially numbered names (e.g. frame01, frame02) or obvious visual sequences should be bundled into a single `multi_file` asset.
* **Rule 2: ProvidedVendorFile** - If there is a metadata file (.txt, .json, .csv) provided by the vendor, you MUST use its definitions to deduce sub-assets, bounding boxes, or sequence groupings.
* **Rule 11: Alternative Reasoning** - If neither of the above apply perfectly, state your own logical reasoning.

You MUST output ONLY valid JSON matching this exact schema:
{
  "parent_assets": [
    {
      "name": "derived_parent_name (e.g. fx1_splash)",
      "type": "multi_file_animation | animation_frames | multi_directional_sprite | static_file | sprite_sheet | sprite_sheet_cell | tileset | sound_effect | music | pixel_font | ttf_font | 3d_model | text",
      "source_files": ["array of exact file paths that belong to this asset"],
      "num_frames": 1,
      "cell_dimensions": {"width": null, "height": null},
      "start_offset": {"x": 0, "y": 0},
      "inference_reasoning": [
        {
          "rule": "Rule X: Name of Rule",
          "rationale": "Explicit reason why this rule applies to this asset grouping."
        }
      ]
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
    
    # Let's process just the first 5 directories as a test batch
    dir_list = list(directories.keys())[:5]
    
    for idx, directory in enumerate(dir_list):
        if directory in blueprints:
            print(f"Skipping {directory} (already cached)")
            continue
            
        print(f"\n--- [{idx+1}/{len(dir_list)}] Architecting Directory: {directory} ---")
        files_in_dir = directories[directory]
        
        # Look for metadata files in this physical directory
        physical_dir = os.path.join(ASSETS_DIR, directory)
        metadata_contents = ""
        if os.path.exists(physical_dir):
            for fname in os.listdir(physical_dir):
                if fname.lower().endswith(('.txt', '.json', '.xml', '.csv')):
                    meta_path = os.path.join(physical_dir, fname)
                    try:
                        with open(meta_path, 'r', encoding='utf-8') as mf:
                            metadata_contents += f"\n--- CONTENTS OF {fname} ---\n{mf.read(2000)}\n" # Read up to 2KB
                    except Exception:
                        pass
        
        prompt = f"Directory: '{directory}'\nFiles:\n" + "\n".join(files_in_dir)
        if metadata_contents:
            prompt += f"\n\nFound Metadata Files:\n{metadata_contents}"
            
        try:
            response = model.generate_content([prompt])
            result_data = json.loads(response.text)
            
            # Inject audit metadata into Pass 2 assets
            for pa in result_data.get("parent_assets", []):
                pa["ai_audit"] = {
                    "pass2_model": "gemini-flash-latest",
                    "pass2_timestamp": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat()
                }
            
            blueprints[directory] = result_data["parent_assets"]
            
            temp_path = BLUEPRINTS_PATH + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(blueprints, f, indent=2)
            os.rename(temp_path, BLUEPRINTS_PATH)
                
            print(f"-> Success! Synthesized {len(result_data['parent_assets'])} parent assets.")
            
        except Exception as e:
            print(f"-> Error during API call or parsing: {e}")
            
        time.sleep(2)
        
    print(f"\nBatch complete! Wrote structural blueprints.")

if __name__ == "__main__":
    main()
