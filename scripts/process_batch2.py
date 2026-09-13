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

batch2_responses = [
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/200% Icons/icon_73.png",
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
            "description": "A pixel art cursor or pointer arrow icon with warm fiery red, orange, and yellow color tones.",
            "tags": [
              "icon",
              "cursor",
              "pointer",
              "arrow",
              "ui",
              "fire"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "red",
              "orange",
              "yellow",
              "white"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Icon source path categorization",
              "rationale": "Located in User Interface Icons/Separated Icons/200% Icons/"
            },
            {
              "rule": "Visual content identification",
              "rationale": "Depicts a cursor arrow or pointer icon with fiery warm colors."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/swords/sword_53.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "ui_overlay",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A 16x16 pixel art bronze or copper sword icon, suitable for RPG inventory or weapon display.",
            "tags": ["sword", "weapon", "bronze", "copper", "rpg", "item", "inventory", "pixel-art", "16x16"],
            "style": "pixel art",
            "color_descriptors": ["bronze", "copper", "brown", "dark brown", "golden brown"]
          },
          "inference_reasoning": [
            {"rule": "Icon detection", "rationale": "The asset is a standalone 16x16 item icon representing a sword."},
            {"rule": "Perspective classification", "rationale": "Oriented diagonally for inventory/UI display."},
            {"rule": "Theme profiling", "rationale": "Earthy copper and bronze tones indicate a low-tier or metallic RPG weapon."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/swords/sword_139.png",
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
            "description": "A 16x16 pixel art icon of a golden sword/dagger weapon with a dark hilt.",
            "tags": [
              "sword",
              "weapon",
              "rpg",
              "item",
              "icon",
              "gold",
              "blade"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "gold",
              "brown",
              "grey",
              "black"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "File path and dimensions check",
              "rationale": "The file is located in the swords subdirectory of a 16x16 RPG icon pack and measures 16x16 pixels."
            },
            {
              "rule": "Visual content analysis",
              "rationale": "The image depicts a single static inventory item icon of a weapon."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/rafaelmatos/epic-rpg-world-the-depths-of-the-mountain/extracted/Epic RPG World - The dephs of the Mountain V1.2/Props/Static/Props-individual sprites/Crystals5-improved refraction_1.png",
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
            "description": "A glowing red and pink crystal prop with improved refraction effects, suitable for dungeon, cave, or mountain environments.",
            "tags": ["crystal", "gem", "prop", "cave", "dungeon", "mountain", "red", "glowing", "refraction"],
            "style": "pixel art",
            "color_descriptors": ["red", "pink", "magenta", "dark purple/grey"]
          },
          "inference_reasoning": [
            {"rule": "Static prop classification", "rationale": "Filename and asset path indicate an individual static prop sprite for a crystal."},
            {"rule": "Perspective determination", "rationale": "Viewed from a side/front-on angle typical of 2D platformer or top-down RPG props."},
            {"rule": "Theme identification", "rationale": "Part of the Epic RPG World - The Depths of the Mountain pack, featuring subterranean crystalline elements."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_explosion_small_orange/frame0001.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "unknown",
            "num_frames": 11,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A small orange pixel art explosion animation effect featuring bright yellow and white core with orange and red edges.",
            "tags": ["explosion", "fx", "pixel-art", "orange", "fire", "combat", "effect"],
            "style": "pixel-art",
            "color_descriptors": ["orange", "yellow", "white", "red"]
          },
          "inference_reasoning": [
            {"rule": "Multi-file animation sequence detection", "rationale": "The asset is part of a numbered sequence of individual PNG files (frame0000.png to frame0010.png) in a dedicated directory."},
            {"rule": "Standard asset pack dimensions", "rationale": "Untied Games Super Pixel Effects Pack 1 standard small explosion frames are sized at 32x32 pixels."},
            {"rule": "Perspective and type classification", "rationale": "Particle/explosion effects are flat 2D overlays without a specific perspective orientation."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/SENGOKU ADVENTURE TILESET/NIGHT/NIGHT PLAYER WALK YELLOW 5.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "top_down",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": True,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A single frame (frame 5) of a character walk animation in a yellow tunic and dark trousers, viewed from behind in a night-themed Sengoku adventure pixel art style.",
            "tags": ["sengoku", "adventure", "player", "walk", "yellow", "night", "character", "pixel art", "animation frame"],
            "style": "pixel art",
            "color_descriptors": ["yellow", "brown", "dark blue", "skin tone"]
          },
          "inference_reasoning": [
            {"rule": "Filename sequence and naming pattern (WALK YELLOW 5.png)", "rationale": "Indicates this is an individual frame of a multi-file animation sequence."},
            {"rule": "Perspective and character sprite design", "rationale": "Top-down / RPG overworld sprite style depicting a character walking."},
            {"rule": "Color palette and theme", "rationale": "Yellow top and dark garments matching the night Sengoku adventure tileset aesthetics."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/200% Icons/icon_80.png",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "front",
            "num_frames": 1,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art icon of a campfire with flames and logs",
            "tags": ["campfire", "fire", "flame", "ui", "icon", "survival", "hot"],
            "style": "pixel art",
            "color_descriptors": ["red", "orange", "yellow", "dark red"]
          },
          "inference_reasoning": [
            {"rule": "Icon Category", "rationale": "Located in User Interface Icons directory and sized as an icon."},
            {"rule": "Visual Content", "rationale": "Depicts a campfire with glowing flames over wood logs."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/SENGOKU ADVENTURE TILESET/NIGHT/NIGHT POT.png",
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
            "description": "A dark ceramic pot or jar asset from a Sengoku adventure night tileset.",
            "tags": ["pot", "jar", "container", "furniture", "sengoku", "night"],
            "style": "pixel art",
            "color_descriptors": ["dark brown", "black", "muted gray"]
          },
          "inference_reasoning": [
            {"rule": "Static object detection", "rationale": "The image contains a single standalone pot object with no animation frames or sprite sheet grid."},
            {"rule": "Perspective classification", "rationale": "The pot is shown from a top-down or slight side angle typical of RPG tilesets."},
            {"rule": "Theme identification", "rationale": "The filename 'NIGHT POT.png' and dark color palette fit the Sengoku Adventure night tileset theme."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/ansimuz/super-grotto-escape-godot-project/extracted/SuperGrottoEscape/Fx/Shock/explosion-d4.png",
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
            "description": "A single blue circular shockwave ring effect frame.",
            "tags": ["shockwave", "explosion", "fx", "blue", "ring"],
            "style": "pixel art",
            "color_descriptors": ["blue", "cyan", "transparent"]
          },
          "inference_reasoning": [
            {"rule": "Type determination", "rationale": "Single static image file representing one frame of a shock effect animation."},
            {"rule": "Perspective", "rationale": "Side-scrolling platformer FX asset."},
            {"rule": "Dimensions", "rationale": "Standard pixel art sprite dimensions for small shockwave/explosion effects."}
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch2_responses:
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

print(f"Successfully appended batch 2 (9 items). Total items now: {len(existing)}")
