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

batch4_responses = [
    (
        "/Users/markoates/Assets/alb-pixel-store/little-robo-adventure-world-4-asset/extracted/LittleRobo Adventure World 4/Enemies/Enemy 25/enemy_25_glide1.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Small robotic enemy gliding with an antenna and glowing eye or sensor.",
            "tags": ["enemy", "robot", "glide", "pixel-art", "little-robo"],
            "style": "pixel art",
            "color_descriptors": ["brown", "white", "red", "dark brown"]
          },
          "inference_reasoning": [
            {"rule": "Rule filename inspection", "rationale": "Filename contains glide1, indicating an animation frame or pose of a gliding robot enemy."},
            {"rule": "Rule visual inspection", "rationale": "Shows a standalone single sprite graphic of a small robot."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Props/atlas props - individual sprites/vase color scheme 5 - 1.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A dark brownish-grey clay vase prop with a hollow dark interior for a crypt environment.",
            "tags": ["prop", "vase", "urn", "crypt", "container", "pot"],
            "style": "pixel art",
            "color_descriptors": ["brown", "grey", "dark"]
          },
          "inference_reasoning": [
            {
              "rule": "Standalone prop identification",
              "rationale": "The image is an individually extracted sprite representing a single container prop."
            },
            {
              "rule": "Perspective classification",
              "rationale": "The view shows the side profile of the vase with a slight top-down angle revealing its opening."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/ansimuz/food-items-icons/extracted/Items-Food-Files/PNG/items-food-preview-x1.png",
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
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art food items icon preview sheet containing various baked goods, sweets, meats, fast food, fruits, vegetables, and seafood.",
            "tags": [
              "food",
              "icons",
              "pixel-art",
              "items",
              "ansimuz"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "colorful",
              "vibrant",
              "multi-colored"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Type Inference",
              "rationale": "The image is a preview sheet showcasing a collection of food icons, categorized as a static image overview."
            },
            {
              "rule": "Perspective Inference",
              "rationale": "The icons are presented in a top-down / iconographic perspective typical of RPG item inventories."
            },
            {
              "rule": "Cell Dimensions Inference",
              "rationale": "Ansimuz pixel art asset packs standardly use 16x16 pixel grid cells for item icons."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/dreamir/elves-pack/extracted/Elves_Pack/Elf_Mage/Elf_Mage_Spell_1NoEffeckt/Elf_Mage_Spell_8.png",
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
            "description": "An elf mage character casting a spell, holding a wooden staff topped with a glowing blue orb.",
            "tags": ["elf", "mage", "spell", "magic", "staff", "pixel-art", "fantasy", "character"],
            "style": "pixel-art",
            "color_descriptors": ["green", "brown", "blonde", "blue"]
          },
          "inference_reasoning": [
            {
              "rule": "Directory and filename pattern indicate a multi-file animation sequence.",
              "rationale": "The file is named Elf_Mage_Spell_8.png inside the Elf_Mage_Spell_1NoEffeckt directory, representing a single frame of a spellcasting animation."
            },
            {
              "rule": "Visual analysis of perspective and character design.",
              "rationale": "The character is shown from a side/three-quarters perspective, characteristic of 2D RPG sprite packs."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/SENGOKU ADVENTURE TILESET/DAY/HOUSE 2 DOOR.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A wooden door tile with vertical planks and a latch from the Sengoku Adventure Tileset daytime house collection.",
            "tags": ["sengoku", "adventure", "tileset", "door", "house", "wood", "day", "pixel_art"],
            "style": "pixel art",
            "color_descriptors": ["brown", "dark brown", "amber", "tan"]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Type Inference",
              "rationale": "The image is a single static graphic representing a closed wooden door tile."
            },
            {
              "rule": "Perspective Inference",
              "rationale": "The door is viewed head-on from a straight-on front perspective."
            },
            {
              "rule": "Dimensions Inference",
              "rationale": "Standard tile size for Sengoku Adventure Tileset is 16x16 pixels."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/100% Icons/icon_119.png",
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
            "description": "A grey metallic gear or cog icon used for settings, options, or configuration in user interfaces.",
            "tags": [
              "gear",
              "cog",
              "settings",
              "options",
              "interface",
              "icon"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "grey",
              "blue-grey",
              "dark outline"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Icon Classification",
              "rationale": "The asset is located in an interface icons directory and depicts a standard UI symbol (a gear/cog)."
            },
            {
              "rule": "Dimensions & Type",
              "rationale": "It is a single static image file representing a standalone user interface icon."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/100% Icons/icon_79.png",
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
            "description": "A pixel art bullet cartridge icon in copper and bronze tones.",
            "tags": [
              "icon",
              "ui",
              "bullet",
              "ammo",
              "weapon",
              "pixel_art"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "copper",
              "brown",
              "dark"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Icon path analysis",
              "rationale": "The file is located in the User Interface Icons separated icons directory."
            },
            {
              "rule": "Visual content identification",
              "rationale": "The image depicts a standard firearm bullet cartridge."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/jackets and vests/vest_002.png",
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
            "description": "A dark tactical vest or leather jacket armor piece for modern RPG characters.",
            "tags": ["vest", "jacket", "armor", "clothing", "equipment", "rpg", "modern"],
            "style": "pixel art",
            "color_descriptors": ["dark grey", "black", "brown", "steel"]
          },
          "inference_reasoning": [
            {"rule": "Static image asset", "rationale": "The image is a single standalone icon file."},
            {"rule": "Icon classification", "rationale": "It represents an inventory item (vest/jacket) sized 16x16 pixels."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/ansimuz/super-grotto-escape-godot-project/extracted/SuperGrottoEscape/Comtraption/SpikeBlock/block.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "side",
            "num_frames": 2,
            "cell_dimensions": {
              "width": 16,
              "height": 16
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": {
              "columns": 2,
              "rows": 1
            }
          },
          "theme_profile": {
            "description": "Spike block hazard from Super Grotto Escape with blue metallic body and two animation frames showing extended or retracted spikes.",
            "tags": [
              "spike",
              "block",
              "trap",
              "hazard",
              "platform",
              "pixel-art"
            ],
            "style": "pixel-art",
            "color_descriptors": [
              "blue",
              "dark blue",
              "cyan"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Scene configuration",
              "rationale": "SpikeBlock.tscn defines hframes = 2 and a 16x16 collision shape (extents 8, 8), confirming a 2-frame 16x16 sprite sheet."
            },
            {
              "rule": "Game perspective",
              "rationale": "Super Grotto Escape is a side-scrolling platformer game."
            }
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch4_responses:
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
            "pass1_timestamp": "2026-09-13T03:02:00-04:00"
        }
    }
    existing.append(asset_dict)

with open(json_path, 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Successfully appended batch 4 (9 items). Total items now: {len(existing)}")
