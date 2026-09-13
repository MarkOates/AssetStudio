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

batch1_responses = [
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Props/atlas props - individual sprites/tissue -vertical - 3.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A vertical stone pillar or wall segment prop from a crypt asset pack.",
            "tags": ["crypt", "prop", "stone", "pillar", "wall", "vertical", "dungeon"],
            "style": "pixel art",
            "color_descriptors": ["grey", "dark stone", "brownish grey"]
          },
          "inference_reasoning": [
            {
              "rule": "Static prop classification",
              "rationale": "The image is a single standalone prop sprite from an individual sprite atlas."
            },
            {
              "rule": "Perspective & dimensions",
              "rationale": "The asset depicts a vertical architectural element viewed from the side in pixel art style."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/legs/leg_34.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A pair of metallic steel or silver armor leggings or greaves.",
            "tags": ["armor", "legs", "greaves", "pants", "equipment", "rpg", "steel", "silver"],
            "style": "16x16 pixel art RPG icon",
            "color_descriptors": ["silver", "steel", "white", "blue-grey", "dark"]
          },
          "inference_reasoning": [
            {"rule": "Standalone item icon classification", "rationale": "The image is a single standalone inventory equipment icon representing armor legs/greaves in a 16x16 pixel art style viewed from the front."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-the-depths-of-the-mountain/extracted/Epic RPG World - The dephs of the Mountain V1.2/Props/Static/Props-individual sprites/Crystals1_10.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A glowing purple crystal prop from a mountain depths theme",
            "tags": ["crystal", "prop", "mountain", "purple", "glowing", "static"],
            "style": "pixel art",
            "color_descriptors": ["purple", "violet", "dark blue", "black"]
          },
          "inference_reasoning": [
            {"rule": "Image type", "rationale": "The asset is an individual static prop image representing a single crystal object."},
            {"rule": "Perspective", "rationale": "Rendered from a side/front perspective suitable for 2D platformers or RPGs."},
            {"rule": "Theme", "rationale": "Purple glowing crystal fits the 'depths of the mountain' magical/underground mining aesthetic."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/alb-pixel-store/little-robo-adventure-world-4-asset/extracted/LittleRobo Adventure World 4/Enemies/Enemy 24/tail.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 32,
              "height": 32
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A robotic enemy tail component consisting of a purple spherical node with yellow glowing lights and red-orange metallic armor plating.",
            "tags": [
              "enemy",
              "robot",
              "tail",
              "sci-fi",
              "pixel-art",
              "armor",
              "mechanical"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "purple",
              "yellow",
              "red",
              "orange",
              "dark grey"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Single standalone image file of a robot part",
              "rationale": "The image is an isolated static sprite representing a single robot tail component with no animation frames or grid layout."
            },
            {
              "rule": "Side profile orientation",
              "rationale": "The asset is viewed from the side, showing the profile of the armored tail structure."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/dreamir/elves-pack/extracted/Elves_Pack/Elf_Mage/Elf_Mage_Idle/Elf_Mage_Idle2.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 64, "height": 64},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art sprite of an Elf Mage holding a staff with a blue magical orb, wearing green robes and blonde hair, in an idle pose.",
            "tags": ["elf", "mage", "idle", "fantasy", "pixel-art", "staff", "magic", "green"],
            "style": "pixel art",
            "color_descriptors": ["green", "brown", "blue", "blonde", "tan"]
          },
          "inference_reasoning": [
            {"rule": "File path and naming convention", "rationale": "Path contains Elf_Mage_Idle indicating it is part of a multi-file animation sequence for an idle state."},
            {"rule": "Visual content analysis", "rationale": "Character is an elf mage with a staff, green robes, and blonde hair, consistent with fantasy elf mage character sprites."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_dash_large_brown/frame0001.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 96, "height": 48},
            "is_subframe": True,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Large brown dash or dust cloud special effect animation frame",
            "tags": ["dash", "effect", "dust", "brown", "pixel-art", "animation", "action"],
            "style": "pixel art",
            "color_descriptors": ["brown", "tan", "yellow", "light-blue"]
          },
          "inference_reasoning": [
            {"rule": "Multi-file animation sequence", "rationale": "File resides in an effect folder and is part of a numbered frame sequence (frame0001.png)."},
            {"rule": "Side perspective action effect", "rationale": "The dash/dust visual lines indicate horizontal movement suitable for side-scrolling games."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/aamatniekss/grasslands-era-of-fantasy-pixelart-asset-pack/extracted/EraOfFantasy_Grasslands_v2/Animation/Large_Cliff_Sand_Dirt_Grass/No_Shadow/Cliff_WorksForAll_No_Shadow_5.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "side",
            "num_frames": 6,
            "cell_dimensions": {"width": 32, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": {"columns": 6, "rows": 1}
          },
          "theme_profile": {
            "description": "Horizontal animation strip of a large cliff edge with sand, dirt, and grass elements, featuring no shadow.",
            "tags": ["cliff", "dirt", "grass", "sand", "animation", "terrain", "platformer", "pixel-art"],
            "style": "pixel-art",
            "color_descriptors": ["brown", "green", "teal", "earthy"]
          },
          "inference_reasoning": [
            {"rule": "Animation Directory Structure", "rationale": "Located in the Animation directory under Large_Cliff_Sand_Dirt_Grass/No_Shadow, indicating a horizontal sequence of animation frames for cliff terrain."},
            {"rule": "Horizontal Strip Layout", "rationale": "The image shows a sequence of 6 side-by-side repeating or animated frames depicting a cliff edge with grass and dirt."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/TINY BEACH/NIGHT TILESET/NIGHT - GROUND HOLE TOP LEFT.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "top_down",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 16,
              "height": 16
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Night ground hole top left tile from the Tiny Beach tileset",
            "tags": [
              "tileset",
              "ground",
              "hole",
              "night",
              "beach",
              "tiny_beach"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "dark blue",
              "navy",
              "midnight blue"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Filename and path analysis",
              "rationale": "The file is located in the Tiny Beach Night Tileset directory and named NIGHT - GROUND HOLE TOP LEFT.png, indicating a top-left corner tile for a ground hole."
            },
            {
              "rule": "Asset pack standards",
              "rationale": "Tiny Beach asset packs by PixelJad use 16x16 pixel art tiles designed for top-down retro games."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/helmets/helmet_172.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "An ornate fantasy helmet icon with small horns or wings, a central crest/gem, and metallic blue-grey plating.",
            "tags": ["helmet", "armor", "equipment", "rpg", "fantasy", "headgear", "horn"],
            "style": "pixel art 16x16",
            "color_descriptors": ["blue", "grey", "purple", "gold", "white"]
          },
          "inference_reasoning": [
            {"rule": "File path analysis", "rationale": "Located in a helmets directory within a 16x16 RPG icon pack."},
            {"rule": "Visual analysis", "rationale": "Single standalone 16x16 pixel art icon depicting a front-facing fantasy helmet with horns/wings and a crest."}
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch1_responses:
    rel_path = physical_path.replace("/Users/markoates/Assets/", "")
    vendor = rel_path.split("/")[0]
    pack = rel_path.split("/")[2] if "extracted" in rel_path else rel_path.split("/")[1]
    name = os.path.splitext(os.path.basename(rel_path))[0]
    
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
            "pass1_timestamp": "2026-09-13T03:00:00-04:00"
        }
    }
    existing.append(asset_dict)

with open(json_path, 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Successfully appended batch 1 (9 items). Total items now: {len(existing)}")
