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

batch7_responses = [
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/underwear/bra_015.png",
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
            "description": "A 16x16 pixel art icon of a pink bra / underwear item.",
            "tags": ["underwear", "clothing", "bra", "rpg", "icon", "equipment"],
            "style": "pixel art",
            "color_descriptors": ["pink", "magenta", "coral", "black outline"]
          },
          "inference_reasoning": [
            {"rule": "Icon Analysis", "rationale": "The image is a single 16x16 standalone pixel art icon representing a piece of modern RPG underwear (bra)."},
            {"rule": "Perspective & Type", "rationale": "Front-facing static icon suitable for inventory or UI display."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-the-depths-of-the-mountain/extracted/Epic RPG World - The dephs of the Mountain V1.2/Props/Animated props/individual files/lightning-4tiles-frame16.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 64},
            "is_subframe": True,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A single frame of a vertical lightning bolt spanning four tiles, rendered in blue pixel art style for an underground mountain or cave setting.",
            "tags": ["lightning", "electricity", "prop", "animated", "magic", "mountain", "depths", "blue", "pixel art"],
            "style": "pixel art",
            "color_descriptors": ["blue", "light blue", "white"]
          },
          "inference_reasoning": [
            {"rule": "Filename analysis", "rationale": "The filename 'lightning-4tiles-frame16.png' indicates this is frame 16 of a 4-tile tall lightning animation."},
            {"rule": "Visual analysis", "rationale": "The image displays a vertical electrical discharge/lightning bolt with branching tendrils."},
            {"rule": "Grid and dimensions", "rationale": "Spans 4 tiles vertically in a 16x16 pixel grid system, resulting in a height of 64 pixels and width of 16 pixels."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Props/atlas props - individual sprites/coffin - vertical - 2.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 32,
              "height": 48
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A vertical stone coffin or crypt prop with carved ornamentation at the base, viewed from the front.",
            "tags": [
              "coffin",
              "crypt",
              "prop",
              "tomb",
              "stone",
              "vertical",
              "gothic",
              "horror"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "dark blue",
              "navy blue",
              "slate grey",
              "charcoal"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Classification",
              "rationale": "The image is a single static standalone prop sprite of a vertical coffin/crypt monument."
            },
            {
              "rule": "Perspective Identification",
              "rationale": "The prop is shown straight-on in a flat front-facing perspective."
            },
            {
              "rule": "Theme & Style Extraction",
              "rationale": "Dark blue/stone color palette with carved details fits the crypt and gothic RPG asset pack theme."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/seethingswarm/catset/extracted/catset_assets/catset_spritesheets/cat01_spritesheets/cat01_ledgegrab_strip5.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "side",
            "num_frames": 5,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": {"columns": 5, "rows": 1}
          },
          "theme_profile": {
            "description": "Pixel art horizontal strip of 5 animation frames showing a brown cat performing a ledge grab.",
            "tags": ["cat", "ledgegrab", "animation", "pixel-art", "platformer", "strip5"],
            "style": "Pixel art",
            "color_descriptors": ["brown", "tan", "dark outline"]
          },
          "inference_reasoning": [
            {
              "rule": "Filename inspection",
              "rationale": "Filename 'cat01_ledgegrab_strip5.png' explicitly denotes a 5-frame ledge grab animation strip."
            },
            {
              "rule": "Visual layout",
              "rationale": "Horizontal sequence of 5 distinct sprite states showing transition into a hanging/ledge-grab position."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/misc-weapons/weapon_65.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 16,
              "height": 16
            },
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A 16x16 pixel art magic staff weapon icon with a glowing blue crystal head, a red jewel connector, and a brown wooden handle.",
            "tags": ["weapon", "staff", "magic", "wand", "crystal", "rpg", "item"],
            "style": "pixel art",
            "color_descriptors": ["blue", "red", "brown", "black", "white"]
          },
          "inference_reasoning": [
            {
              "rule": "Dimensions and asset type",
              "rationale": "The file is located in a 16x16 RPG icon pack directory (misc-weapons) and has 16x16 dimensions, representing a single static item icon."
            },
            {
              "rule": "Perspective and category",
              "rationale": "Rendered from a diagonal side perspective typical of inventory icons in RPGs, depicting a magical weapon/staff."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/swords/sword_92.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 16,
              "height": 16
            },
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A 16x16 pixel art icon of a brown wooden or bronze sword viewed from a side/diagonal perspective.",
            "tags": ["sword", "weapon", "rpg", "item", "wooden", "brown", "blade"],
            "style": "pixel art",
            "color_descriptors": ["brown", "gold", "dark brown", "grey"]
          },
          "inference_reasoning": [
            {
              "rule": "Single item icon detection",
              "rationale": "The image is a standalone 16x16 pixel art inventory icon representing a sword."
            },
            {
              "rule": "Perspective classification",
              "rationale": "The sword is rendered diagonally from a side profile view typical of 2D RPG item icons."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/jackets and vests/vest_003.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 16,
              "height": 16
            },
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A 16x16 pixel art icon representing a brown leather vest or tactical garment with buckles.",
            "tags": [
              "vest",
              "armor",
              "leather",
              "clothing",
              "equipment",
              "rpg",
              "pixel art"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "brown",
              "dark brown",
              "tan",
              "grey"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Type Inference",
              "rationale": "The image is a standalone 16x16 graphic representing an inventory item/equipment piece."
            },
            {
              "rule": "Perspective Inference",
              "rationale": "The clothing item is depicted from a straight-on, symmetric front view."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/finalbossblues/quirky-npcs/extracted/quirky_npcs/tf_color/3x(RMMVMZ)/pigman.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "front",
            "num_frames": 12,
            "cell_dimensions": {
              "width": 48,
              "height": 48
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art sprite sheet of a pigman NPC with pink skin, snout, brown belt, and blue trousers, featuring multiple frames with neutral and roaring expressions.",
            "tags": [
              "pigman",
              "monster",
              "npc",
              "pixel-art",
              "sprite-sheet",
              "fantasy",
              "character"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "pink",
              "brown",
              "blue",
              "grey"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Type",
              "rationale": "The image contains multiple frames arranged in a grid showing character animations/expressions."
            },
            {
              "rule": "Perspective",
              "rationale": "The character faces forward towards the viewer."
            },
            {
              "rule": "Cell Dimensions & Frames",
              "rationale": "The sheet has 12 cells in a 4x3 arrangement with standard 48x48 pixel character dimensions for Quirky NPCs."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-alchemy-rpg-icon-pack/extracted/Pixeltiers_Alchemy_RPG_Icon_Pack_3/ingredients/strange_fruit_003.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "ui_overlay",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 32,
              "height": 32
            },
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art icon of a strange red fruit or berry cluster with a green stem, designed as an alchemy RPG crafting ingredient.",
            "tags": [
              "fruit",
              "alchemy",
              "item",
              "ingredient",
              "red",
              "berry",
              "pixel-art",
              "rpg"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "red",
              "orange",
              "yellow",
              "green",
              "black"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Standalone UI Icon Classification",
              "rationale": "The asset path under 'ingredients' and visual presentation as a standalone item indicate a UI overlay icon."
            },
            {
              "rule": "Theme & Subject Identification",
              "rationale": "The sprite depicts a bulbous red fruit with highlights and a green stem, matching alchemy RPG ingredient themes."
            }
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch7_responses:
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
            "pass1_timestamp": "2026-09-13T03:03:00-04:00"
        }
    }
    existing.append(asset_dict)

with open(json_path, 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Successfully appended batch 7 (9 items). Total items now: {len(existing)}")
