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

# The 8 successful subagent responses
responses = [
    # bottle
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-alchemy-rpg-icon-pack/extracted/Pixeltiers_Alchemy_RPG_Icon_Pack_3/bottles and vials/bottle_middle_007.png",
        '''{"catalog_proposal": {"type": "static_image", "perspective": "ui_overlay", "num_frames": 1, "cell_dimensions": {"width": 16, "height": 16}, "is_subframe": false, "is_icon": true, "inferred_grid": null}, "theme_profile": {"description": "A 16x16 pixel art RPG inventory icon of a medium glass potion bottle sealed with a cork and filled with glowing emerald green liquid.", "tags": ["potion", "bottle", "vial", "alchemy", "icon", "item", "green potion", "magic", "16x16", "inventory"], "style": "16-bit RPG pixel art", "color_descriptors": ["emerald green", "mint green", "teal", "cork brown", "glass light blue", "white highlight"]}, "inference_reasoning": [{"rule": "Rule 12: Icons & Small Graphics", "rationale": "The asset is a 16x16 pixel standalone graphic representing an inventory potion item, so is_icon is flagged as true."}, {"rule": "Rule 14: Type Definitions", "rationale": "The file is a standalone static image containing no animation data, categorizing it as static_image."}, {"rule": "Rule 11: Alternative Reasoning", "rationale": "Although the filename ends in a sequential number (_007), visual comparison with other files in the directory confirms the numbering represents distinct potion color variants rather than sequential animation frames, so is_subframe is false."}, {"rule": "Rule 7: UI & HUD", "rationale": "The asset originates from an RPG inventory icon pack designed for user interfaces and inventory menus."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The icon is rendered for inventory and HUD menus, classifying its perspective as ui_overlay."}]}'''
    ),
    # axe
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/axes/axe_39.png",
        '''{"catalog_proposal": {"type": "static_image", "perspective": "ui_overlay", "num_frames": 1, "cell_dimensions": {"width": 16, "height": 16}, "is_subframe": false, "is_icon": true, "inferred_grid": null}, "theme_profile": {"description": "A 16x16 pixel art RPG item icon of a heavy copper or bronze battleaxe with a wide blade and a wooden handle.", "tags": ["axe", "battleaxe", "weapon", "copper", "bronze", "item", "icon", "rpg", "equipment", "melee"], "style": "16x16 fantasy RPG pixel art", "color_descriptors": ["copper", "bronze", "dark brown", "black"]}, "inference_reasoning": [{"rule": "Rule 2: Embedded Resolution", "rationale": "The directory path specifies '16x16', matching the 16x16 pixel dimensions of the image."}, {"rule": "Rule 7: UI & HUD", "rationale": "The path includes 'icon-pack', indicating an inventory item or interface element."}, {"rule": "Rule 12: Icons & Small Graphics", "rationale": "The asset is a 16x16 standalone graphic representing a weapon item, flagging is_icon as true."}, {"rule": "Rule 14: Type Definitions", "rationale": "The asset is a single static graphic without animation frames, typed as static_image."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "Item icons in RPG inventory systems are presented as UI graphics, giving it a ui_overlay perspective."}]}'''
    ),
    # splash
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_splash_small_dark_blue/frame0009.png",
        '''{"catalog_proposal": {"type": "multi_file_animation", "perspective": "side", "num_frames": 1, "cell_dimensions": {"width": 36, "height": 34}, "is_subframe": true, "is_icon": false, "inferred_grid": null}, "theme_profile": {"description": "Frame 9 of a small pixel art splash effect in dark blue, showing settling surface ripples and a dispersing central droplet.", "tags": ["fx", "vfx", "splash", "water", "small", "dark_blue", "liquid", "subframe", "pixel_art"], "style": "16-bit retro pixel art VFX", "color_descriptors": ["dark blue", "cyan", "sky blue"]}, "inference_reasoning": [{"rule": "Rule 4: Multi-File Sequences", "rationale": "Filename 'frame0009.png' is part of a numbered sequence (frame0000 to frame0010), identifying it as a single subframe of a multi_file_animation."}, {"rule": "Rule 8: Visual Effects (VFX)", "rationale": "The asset path contains 'fx1_splash', which identifies it as a visual effect/particle animation of a water splash."}, {"rule": "Rule 10: Variant Tagging", "rationale": "The path segment 'small_dark_blue' specifies scale and color variants, which are tagged accordingly."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The horizontal water line and upward splash trajectory depict a side-view 2D perspective."}]}'''
    ),
    # lamp
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-props-mansion-pack-1/extracted/Super Pixel Props - Mansion Pack 1/PNG/lamp_tall_gold_off.png",
        '''{"catalog_proposal": {"type": "static_image", "perspective": "side", "num_frames": 1, "cell_dimensions": {"width": 32, "height": 96}, "is_subframe": false, "is_icon": false, "inferred_grid": null}, "theme_profile": {"description": "A tall pixel art floor lamp with an ornate golden metallic stand, unlit brown shade, and dangling green pull tassels.", "tags": ["lamp", "floor lamp", "furniture", "interior", "prop", "lighting", "gold", "light off", "mansion", "decor"], "style": "16-bit retro pixel art", "color_descriptors": ["golden bronze", "muted brown", "soft teal green"]}, "inference_reasoning": [{"rule": "Rule 14: Type Definitions", "rationale": "The asset is a standalone single-frame image of an interior prop (tall floor lamp) with no animation frames or grid structure, classifying it as a static_image."}, {"rule": "Rule 10: Variant Tagging", "rationale": "The filename contains descriptor tokens 'tall', 'gold', and state indicator 'off', which denote material and unlit state variants captured in tags."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The lamp is drawn straight-on in a side perspective typical of 2D side-scrolling platformers or side-view games."}]}'''
    ),
    # chef
    (
        "/Users/markoates/Assets/finalbossblues/quirky-npcs/extracted/quirky_npcs/fullcolor/3x(RMMVMZ)/ironchef_walk.png",
        '''{"catalog_proposal": {"type": "multi_directional_sprite", "perspective": "top_down", "num_frames": 12, "cell_dimensions": {"width": 138, "height": 144}, "is_subframe": false, "is_icon": false, "inferred_grid": {"columns": 3, "rows": 4, "cell_width": 138, "cell_height": 144, "contains_multiple_animations": false, "inferred_animations": [{"name": "walk", "row": 0, "start_frame": 0, "frame_count": 3, "inference_reasoning": [{"rule": "Rule 15: Multi-Directional Character Sheets", "rationale": "Row 0 depicts the south-facing walk cycle for the Iron Chef."}]}, {"name": "walk", "row": 1, "start_frame": 3, "frame_count": 3, "inference_reasoning": [{"rule": "Rule 15: Multi-Directional Character Sheets", "rationale": "Row 1 depicts the west-facing walk cycle for the Iron Chef."}]}, {"name": "walk", "row": 2, "start_frame": 6, "frame_count": 3, "inference_reasoning": [{"rule": "Rule 15: Multi-Directional Character Sheets", "rationale": "Row 2 depicts the east-facing walk cycle for the Iron Chef."}]}, {"name": "walk", "row": 3, "start_frame": 9, "frame_count": 3, "inference_reasoning": [{"rule": "Rule 15: Multi-Directional Character Sheets", "rationale": "Row 3 depicts the north-facing walk cycle for the Iron Chef."}]}]}}, "theme_profile": {"description": "A 4-directional 3-frame walk cycle sprite sheet featuring an 'Iron Chef' character: a knight clad in full plate armor wearing a tall chef's hat, an orange tabard apron, and oven mitts.", "tags": ["iron chef", "knight", "chef", "cook", "armor", "plate armor", "chef hat", "apron", "walk", "walk cycle", "character", "npc", "pixel art", "quirky", "rpg maker"], "style": "16-bit retro pixel art scaled 3x for RPG Maker MV/MZ", "color_descriptors": ["steel gray", "bright orange", "pure white", "shadowed charcoal", "warm red-orange"]}, "inference_reasoning": [{"rule": "Rule 3: Action Signatures", "rationale": "The filename contains the action verb 'walk', indicating character movement/walking animations."}, {"rule": "Rule 13: Visual Grid Deduction", "rationale": "Visual inspection of the 414x576 image confirms a 3-column by 4-row grid structure, yielding exact 138x144 pixel cells for each frame in this 3x scaled RPG Maker MV/MZ asset."}, {"rule": "Rule 15: Multi-Directional Character Sheets", "rationale": "The 3x4 grid depicts the same walking animation cycle rendered across four cardinal directions (Row 0: South/Down, Row 1: West/Left, Row 2: East/Right, Row 3: North/Up), designating this asset as a multi_directional_sprite with contains_multiple_animations set to false."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The character is rendered in a top-down 2D RPG perspective with slight forward tilt and cast ground contact shadows under the feet."}]}'''
    ),
    # dust
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_impact_dust_small_brown/frame0002.png",
        '''{"catalog_proposal": {"type": "multi_file_animation", "perspective": "side", "num_frames": 1, "cell_dimensions": {"width": null, "height": null}, "is_subframe": true, "is_icon": false, "inferred_grid": null}, "theme_profile": {"description": "A pixel art dust puff impact effect billowing upward and outward in earthy brown tones.", "tags": ["fx", "vfx", "impact", "dust", "smoke", "particle", "brown"], "style": "16-bit retro pixel art VFX", "color_descriptors": ["earthy brown", "tan", "warm ochre"]}, "inference_reasoning": [{"rule": "Rule 4: Multi-File Sequences", "rationale": "The filename 'frame0002.png' ends in a sequential number indicating a single subframe in a multi-file animation sequence."}, {"rule": "Rule 8: Visual Effects (VFX)", "rationale": "The folder name 'fx1_impact_dust_small_brown' includes the prefix 'fx1_' and keyword 'impact', identifying it as a particle visual effect."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The dust particles billow upward from a flat horizontal plane, characteristic of a 2D side perspective."}]}'''
    ),
    # wooden door
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Props/animated/doors2/wooden doors2-vertical-leftwards-opening.png",
        '''{"catalog_proposal": {"type": "animation_frames", "perspective": "top_down", "num_frames": 10, "cell_dimensions": {"width": 128, "height": 160}, "is_subframe": false, "is_icon": false, "inferred_grid": {"columns": 10, "rows": 1, "cell_width": 128, "cell_height": 160, "contains_multiple_animations": false, "inferred_animations": [{"name": "opening", "row": 0, "start_frame": 0, "frame_count": 10, "inference_reasoning": [{"rule": "Rule 3: Action Signatures", "rationale": "Filename indicates 'opening' action for a vertical wooden crypt/dungeon door."}, {"rule": "Rule 13: Visual Grid Deduction", "rationale": "Visual analysis confirms a 10-frame horizontal sequence showing the door swinging open leftwards."}]}]}}, "theme_profile": {"description": "An animated sprite sequence of a dark wooden vertical crypt door swinging open towards the left in a top-down RPG perspective.", "tags": ["crypt", "dungeon", "wooden door", "animated door", "opening", "gate", "props", "rpg"], "style": "16-bit dark fantasy pixel art", "color_descriptors": ["dark slate blue", "deep navy", "charcoal black"]}, "inference_reasoning": [{"rule": "Rule 3: Action Signatures", "rationale": "Filename contains action verb 'opening', indicating an environmental interactive prop animation."}, {"rule": "Rule 13: Visual Grid Deduction", "rationale": "Image dimensions 1280x160 divide precisely into 10 frames of 128x160 pixels arranged horizontally in 1 row."}, {"rule": "Rule 14: Type Definitions", "rationale": "Asset is a discrete 1D strip of animation frames representing a single continuous door-opening action."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The asset is depicted in a top-down RPG perspective designed for a vertical doorway opening into the scene."}]}'''
    ),
    # crystals
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-the-depths-of-the-mountain/extracted/Epic RPG World - The dephs of the Mountain V1.2/Props/Static/Props-individual sprites/Crystals2-improved refraction_16.png",
        '''{"catalog_proposal": {"type": "sprite_sheet_cell", "perspective": "top_down", "num_frames": 1, "cell_dimensions": {"width": 64, "height": 64}, "is_subframe": false, "is_icon": false, "inferred_grid": null}, "theme_profile": {"description": "A cluster of glowing red crystalline mineral shards with refractive highlights emerging from a dark rocky base.", "tags": ["crystal", "gem", "mineral", "red", "ore", "cave", "prop", "static", "glowing", "refraction"], "style": "16-bit dark fantasy pixel art with radiant glow", "color_descriptors": ["bright crimson", "ruby red", "warm orange", "dark charcoal", "soft red glow"]}, "inference_reasoning": [{"rule": "Rule 14: Type Definitions", "rationale": "Located in 'Props/Static/Props-individual sprites/', this asset is an individual prop extracted from a larger sprite sheet collection, classifying it as a sprite_sheet_cell."}, {"rule": "Rule 10: Variant Tagging", "rationale": "The '_16' suffix indicates variant index 16 of the 'Crystals2-improved refraction' static prop series rather than a sequential animation frame."}, {"rule": "Rule 16: Perspective Analysis", "rationale": "The asset is depicted from an elevated 3/4 high-angle view suited for top-down 2D RPG cave and dungeon environments."}]}'''
    )
]

output_proposals = []

for physical_path, json_str in responses:
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
            "pass1_timestamp": "2026-09-13T01:35:00-04:00"
        }
    }
    
    output_proposals.append(asset_dict)

out_file = 'scripts/ai_subagent_proposals.json'
existing = []
if os.path.exists(out_file):
    with open(out_file, 'r', encoding='utf-8') as f:
        existing = json.load(f)

existing.extend(output_proposals)

# Atomic save
tmp_path = out_file + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(existing, f, indent=2)
os.rename(tmp_path, out_file)

print(f"Successfully appended {len(output_proposals)} assets to ai_subagent_proposals.json")
