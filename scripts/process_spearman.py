import json
import os
import hashlib

def get_file_hash(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "hash_error"

physical_path = "/Users/markoates/Assets/dreamir/elves-pack/extracted/Elves_Pack/Elf_Spearman/Elf_Spearman_Idle/Elf_Spearman_Idle6.png"
json_str = '''{"catalog_proposal": {"type": "multi_file_animation", "perspective": "side", "num_frames": 1, "cell_dimensions": {"width": 110, "height": 80}, "is_subframe": true, "is_icon": false, "inferred_grid": null}, "theme_profile": {"description": "A pixel art animation frame depicting an armored elven spearman standing in an idle stance, equipped with a long spear, a dark shield, full plate armor, and green tunic.", "tags": ["elf", "spearman", "soldier", "warrior", "idle", "spear", "shield", "plate armor", "fantasy", "pixel art"], "style": "16-bit side-scroller pixel art", "color_descriptors": ["dark slate grey", "forest green", "metallic silver", "wood brown"]}, "inference_reasoning": [{"rule": "Rule 4: Multi-File Sequences", "rationale": "The filename 'Elf_Spearman_Idle6.png' ends with sequential number '6' within the 'Elf_Spearman_Idle' directory, identifying it as an individual subframe of a multi-file animation sequence."}, {"rule": "Rule 3: Action Signatures", "rationale": "The keyword 'Idle' in both the directory name and filename indicates this frame belongs to an idle character animation sequence."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The character sprite is drawn in profile for a side-scrolling perspective."}]}'''

rel_path = physical_path.replace("/Users/markoates/Assets/", "")
vendor = rel_path.split("/")[0]
pack = rel_path.split("/")[2] if "extracted" in rel_path else rel_path.split("/")[1]
name = os.path.splitext(os.path.basename(rel_path))[0]

data = json.loads(json_str)
proposed = data["catalog_proposal"]

safe_rel_path = rel_path.replace('.', '_')
deterministic_id = f"synthetic/{safe_rel_path}"

asset_dict = {
    "identifier": deterministic_id,
    "name": name,
    "asset_pack_identifier": f"{vendor}/{pack}",
    "type": proposed["type"],
    "perspective": proposed.get("perspective", "unknown"),
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
    "theme_profile": data.get("theme_profile", {}),
    "inference_reasoning": data.get("inference_reasoning", []),
    "color_profile": {
        "color_space": "unknown",
        "palette": [],
        "is_exact_palette": False,
        "palette_swappable": False
    },
    "ai_audit": {
        "pass1_model": "subagent-strict-json",
        "pass1_timestamp": "2026-09-13T01:36:00-04:00"
    }
}

out_file = 'scripts/ai_subagent_proposals.json'
existing = []
if os.path.exists(out_file):
    with open(out_file, 'r', encoding='utf-8') as f:
        existing = json.load(f)

existing.append(asset_dict)

# Atomic save
tmp_path = out_file + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(existing, f, indent=2)
os.rename(tmp_path, out_file)

print(f"Appended final spearman subagent to ai_subagent_proposals.json")
