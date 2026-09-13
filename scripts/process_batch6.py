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

batch6_responses = [
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/SENGOKU ADVENTURE TILESET/DAY/GROUND 7.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "top_down",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Ground tile with grass detail from Sengoku Adventure Tileset (Day)",
            "tags": ["ground", "tileset", "sengoku", "day", "grass", "nature", "dirt", "top-down"],
            "style": "pixel art",
            "color_descriptors": ["brown", "tan", "green", "olive"]
          },
          "inference_reasoning": [
            {"rule": "File path and visual content", "rationale": "Located in Sengoku Adventure Tileset DAY folder, representing a ground tile with grass patches in top-down perspective."},
            {"rule": "Dimensions and type", "rationale": "Single static tile image typical of 16x16 top-down RPG tilesets."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/finalbossblues/quirky-npcs/extracted/quirky_npcs/fullcolor/3x(RMMVMZ)/foodboys.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "front",
            "num_frames": 3,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": {"rows": 4, "columns": 3}
          },
          "theme_profile": {
            "description": "Pixel art sprite sheet featuring animated food characters including a burger, sausage, pickle, and taco with 3-frame idle animations.",
            "tags": ["pixel-art", "food", "characters", "npc", "quirky-npcs", "animation", "burger", "taco", "sausage", "pickle"],
            "style": "pixel art",
            "color_descriptors": ["full color", "vibrant", "detailed shading"]
          },
          "inference_reasoning": [
            {"rule": "Grid layout detection", "rationale": "The image is arranged in a 4x3 grid with each row representing a different food character and each column representing an animation frame."},
            {"rule": "Character classification", "rationale": "Depicts anthropomorphic food items (burger, sausage, pickle, taco) styled as quirky NPCs."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-alchemy-rpg-icon-pack/extracted/Pixeltiers_Alchemy_RPG_Icon_Pack_3/ingredients/birds_nest.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "ui_overlay",
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
            "description": "A pixel art icon of a bird's nest, suitable for alchemy, crafting, and RPG inventory items.",
            "tags": [
              "alchemy",
              "rpg",
              "icon",
              "ingredient",
              "birds_nest",
              "nest",
              "nature",
              "crafting"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "brown",
              "dark brown",
              "amber"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Single standalone icon file from an alchemy RPG icon pack",
              "rationale": "The asset is a single image file representing an inventory item/ingredient (bird's nest) formatted for UI display."
            },
            {
              "rule": "Pixel art style classification",
              "rationale": "Visual inspection reveals clear low-resolution pixel art characteristic of RPG icon sets."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/hats and helmets/hat_052.png",
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
            "description": "A 16x16 pixel art icon of a brown hat with a white band.",
            "tags": [
              "hat",
              "headwear",
              "equipment",
              "rpg",
              "pixel_art",
              "clothing"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "brown",
              "white",
              "dark outline"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Standalone Inventory Icon Detection",
              "rationale": "The file is located in a hats and helmets asset folder and measures 16x16 pixels, representing a single equipable item icon."
            },
            {
              "rule": "Perspective & Style Analysis",
              "rationale": "The hat is rendered in a clean 16x16 pixel art style with a front-facing perspective, featuring distinct shading and a white accent band."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/meds and drugs/meds_002.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A single 16x16 pixel art icon of a blue and white capsule pill.",
            "tags": ["pill", "capsule", "medicine", "drug", "item", "health", "pixel art"],
            "style": "pixel art",
            "color_descriptors": ["blue", "white", "gold/brown shading", "dark outline"]
          },
          "inference_reasoning": [
            {
              "rule": "Single item asset classification",
              "rationale": "The image is a standalone 16x16 pixel art graphic representing an inventory item (capsule pill)."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/swords/sword_18.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "isometric",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A 16x16 pixel art icon of a glowing green sword with a gold hilt and ornate guard.",
            "tags": ["sword", "weapon", "rpg", "pixel-art", "green", "gold", "item"],
            "style": "pixel art",
            "color_descriptors": ["green", "yellow", "gold", "brown", "white", "black"]
          },
          "inference_reasoning": [
            {
              "rule": "Single standalone icon file format",
              "rationale": "The file is an isolated 16x16 sprite representing a sword inventory icon."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/seethingswarm/catset/extracted/catset_assets/catset_gifs/cat01_gifs/cat01_ledgeclimb_12fps.gif",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "side",
            "num_frames": 6,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Cat ledge climb animation frames showing a brown cat pulling itself up.",
            "tags": ["cat", "animation", "ledgeclimb", "pixel_art"],
            "style": "pixel art",
            "color_descriptors": ["brown", "tan", "black"]
          },
          "inference_reasoning": [
            {
              "rule": "File extension and naming (.gif, ledgeclimb)",
              "rationale": "The asset is an animated GIF depicting a cat climbing a ledge, categorized as animation_frames."
            },
            {
              "rule": "Visual perspective",
              "rationale": "The cat is viewed from the side as it climbs upward."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/ansimuz/food-items-icons/extracted/Items-Food-Files/SPRITES/058-carrot.png",
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
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A pixel art carrot food item icon with vibrant orange body and green leafy top.",
            "tags": [
              "food",
              "carrot",
              "vegetable",
              "item",
              "icon",
              "pixel_art",
              "ansimuz"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "orange",
              "green",
              "brown"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Single sprite detection",
              "rationale": "The image is a standalone single item sprite file from an icon pack."
            },
            {
              "rule": "Perspective & Icon analysis",
              "rationale": "It represents an inventory item rendered in a side/slightly angled profile suitable for UI or pickup display."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/shirts/shirt_015.png",
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
            "description": "A 16x16 pixel art icon of an olive green t-shirt/shirt from a modern RPG asset pack.",
            "tags": [
              "shirt",
              "clothing",
              "apparel",
              "rpg",
              "item",
              "icon",
              "pixel art"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "olive green",
              "dark outline",
              "white highlight"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset categorization and visual inspection",
              "rationale": "The asset is a standalone 16x16 pixel art graphic located in an icon set's shirts directory, depicting a front-facing garment item suitable for inventory UI."
            }
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch6_responses:
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

print(f"Successfully appended batch 6 (9 items). Total items now: {len(existing)}")
