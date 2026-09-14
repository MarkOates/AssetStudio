import json
import os
import sys
from PIL import Image

ASSETS_DIR = '/Users/markoates/Assets'
VIEWER_DATA_PATH = 'web/viewer_data.json'
AI_PROPOSALS = 'scripts/ai_catalog_proposals.json'
OUT_DIR = os.path.join(ASSETS_DIR, 'gemini', 'tweens')
os.makedirs(OUT_DIR, exist_ok=True)

def tween_asset(identifier):
    with open(VIEWER_DATA_PATH, 'r', encoding='utf-8') as f:
        vdata = json.load(f)
        
    asset = next((a for a in vdata.get('assets', []) if a['identifier'] == identifier), None)
    if not asset:
        print(f"Asset {identifier} not found!")
        return
        
    src_file = asset['resource']['source_files'][0]
    # Remove /Assets/ prefix to get relative path
    rel_path = src_file.replace('/Assets/', '', 1)
    physical_path = os.path.join(ASSETS_DIR, rel_path)
    
    print(f"Loading {physical_path}")
    img = Image.open(physical_path).convert('RGBA')
    
    # We need to know cell dimensions
    grid = asset['resource'].get('inferred_grid') or {}
    w = grid.get('cell_width') or asset['resource']['cell_dimensions']['width']
    h = grid.get('cell_height') or asset['resource']['cell_dimensions']['height']
    cols = grid.get('columns') or (img.width // w)
    
    frames = []
    for i in range(cols):
        box = (i*w, 0, (i+1)*w, h)
        frames.append(img.crop(box))
        
    print(f"Extracted {len(frames)} frames. Generating tweens...")
    
    new_frames = []
    for i in range(len(frames) - 1):
        new_frames.append(frames[i])
        # Simple blend tween
        tween = Image.blend(frames[i], frames[i+1], alpha=0.5)
        new_frames.append(tween)
        
    new_frames.append(frames[-1])
    
    # Create new spritesheet
    new_w = w * len(new_frames)
    new_img = Image.new('RGBA', (new_w, h), (0, 0, 0, 0))
    for i, frame in enumerate(new_frames):
        new_img.paste(frame, (i*w, 0))
        
    out_name = asset['name'] + "_tweened"
    out_path = os.path.join(OUT_DIR, out_name + ".png")
    new_img.save(out_path)
    print(f"Saved tweened spritesheet to {out_path}")
    
    # Add to AI proposals
    proposal = {
        "identifier": f"synthetic/gemini/tweens/{out_name}.png",
        "name": out_name,
        "asset_pack_identifier": "gemini/tweens",
        "type": "animation_frames",
        "is_subframe": False,
        "is_icon": False,
        "visibility": "public",
        "sheet_row_number": None,
        "resource": {
            "type": "animation_frames",
            "source_files": [f"/Assets/gemini/tweens/{out_name}.png"],
            "cell_dimensions": {"width": w, "height": h},
            "inferred_grid": {
                "columns": len(new_frames),
                "rows": 1,
                "cell_width": w,
                "cell_height": h,
                "contains_multiple_animations": False,
                "inferred_animations": [
                    {
                        "name": "tweened_sequence",
                        "row": 0,
                        "start_frame": 0,
                        "frame_count": len(new_frames),
                        "inference_reasoning": [
                            {"rule": "Tween Generator", "rationale": "AI-blended intermediate frames."}
                        ]
                    }
                ]
            }
        },
        "animation_profile": {
            "num_frames": len(new_frames),
            "base_frame_duration": 0.05
        },
        "theme_profile": asset.get('theme_profile', {})
    }
    
    # Update AI_PROPOSALS
    ap_path = AI_PROPOSALS
    if os.path.exists(ap_path):
        with open(ap_path, 'r', encoding='utf-8') as f:
            proposals = json.load(f)
    else:
        proposals = []
        
    proposals.append(proposal)
    with open(ap_path, 'w', encoding='utf-8') as f:
        json.dump(proposals, f, indent=2)
        
    print("Injected tween asset into catalog proposals!")

if __name__ == '__main__':
    tween_asset(sys.argv[1])
