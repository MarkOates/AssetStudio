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

batch3_responses = [
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/100% Icons/icon_51.png",
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
            "description": "A pixel art UI icon featuring the letters DEF with a downward-pointing blue chevron or arrow above it, representing defense status or stat reduction.",
            "tags": [
              "ui",
              "icon",
              "defense",
              "def",
              "stat",
              "pixel-art",
              "blue",
              "arrow"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "cyan",
              "blue",
              "black",
              "white"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Icon Type Determination",
              "rationale": "The asset is a standalone user interface icon depicting stat abbreviation 'DEF' with a directional indicator, intended for game UI overlays."
            },
            {
              "rule": "Perspective Classification",
              "rationale": "Flat 2D UI graphic designed for interface overlays rather than in-world perspective."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/kazzter-k/interface-icons/extracted/User Interface Icons/Separated Icons/200% Icons/icon_163.png",
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
            "description": "Red fast-backward media control icon with a vertical line and two left-pointing arrows",
            "tags": [
              "ui",
              "icon",
              "media",
              "fast-backward",
              "skip",
              "red",
              "interface"
            ],
            "style": "pixel_art",
            "color_descriptors": [
              "red",
              "dark_red",
              "black"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "UI Icon Identification",
              "rationale": "The asset depicts a standard media player skip/fast-backward symbol with a vertical bar and left-facing triangles, rendered in pixel art style."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_splash_small_red/frame0009.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": True,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Frame 9 of a small red splash pixel effect animation.",
            "tags": ["splash", "effect", "red", "pixel-art", "animation"],
            "style": "pixel art",
            "color_descriptors": ["red", "dark red", "transparent"]
          },
          "inference_reasoning": [
            {"rule": "Directory and filename structure", "rationale": "Located in fx1_splash_small_red/frame0009.png, indicating a multi-file animation sequence."},
            {"rule": "Visual content", "rationale": "Shows small red splash droplets dissolving or settling."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/venoxxx/dungeon-toolkit-2d-platformer/extracted/toolkit/items.png",
        {
          "catalog_proposal": {
            "type": "sprite_sheet_cell",
            "perspective": "ui_overlay",
            "num_frames": 1,
            "cell_dimensions": {"width": 16, "height": 16},
            "is_subframe": False,
            "is_icon": True,
            "inferred_grid": {"columns": 5, "rows": 4}
          },
          "theme_profile": {
            "description": "Inventory items, collectibles, and pickup particle effects including mushrooms, gems, feathers, and glowing amulets in a pixel art dungeon crawler style.",
            "tags": ["items", "collectibles", "inventory", "pixel-art", "dungeon", "ui", "icons", "pickup"],
            "style": "16-bit pixel art",
            "color_descriptors": ["red", "blue", "gold", "pink", "white", "gray", "brown"]
          },
          "inference_reasoning": [
            {
              "rule": "Grid and content analysis",
              "rationale": "The image contains multiple rows of collectible inventory items and small sprite/particle animations laid out in a grid format with 16x16 pixel cell alignment."
            },
            {
              "rule": "Item categorization",
              "rationale": "The top rows depict various inventory icons (mushroom, gems, fruit, feathers, coins), while the lower rows show pickup or spawn animations and particle effects."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_energy_shield_small_green/frame0016.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "side",
            "num_frames": 20,
            "cell_dimensions": {
              "width": 32,
              "height": 32
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art animation frame sequence representing a small green energy shield effect.",
            "tags": [
              "pixel art",
              "energy shield",
              "green",
              "sci-fi",
              "vfx",
              "effect",
              "animation"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "green",
              "lime",
              "yellow-green",
              "white"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Directory Structure",
              "rationale": "The asset is part of a folder containing 20 sequential frame files (frame0000.png to frame0019.png), confirming a multi_file_animation."
            },
            {
              "rule": "Visual Content",
              "rationale": "Visual inspection reveals a glowing green energy barrier or shield bubble/ring."
            },
            {
              "rule": "Style and Perspective",
              "rationale": "Classic 2D pixel art style designed for side-scrolling video game effects and VFX."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/world-map-pixel-art-tileset/extracted/world_map/pieces/terrain/grass_corner_southeast_f3.png",
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
            "description": "Pixel art grass terrain tile representing a southeast corner piece for a world map tileset.",
            "tags": ["terrain", "grass", "corner", "southeast", "world-map", "pixel-art", "tileset"],
            "style": "pixel art",
            "color_descriptors": ["green", "dark green"]
          },
          "inference_reasoning": [
            {"rule": "File path and naming convention", "rationale": "Path includes world_map/pieces/terrain/grass_corner_southeast_f3.png indicating a terrain corner piece."},
            {"rule": "Visual analysis", "rationale": "Displays a grass terrain tile with border shading typical of top-down world maps."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/super-pixel-effects-pack-1/extracted/Super Pixel Effects Pack 1/PNG/fx1_electric_zap_small_violet/frame0002.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "unknown",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 32,
              "height": 32
            },
            "is_subframe": True,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A single frame of a small pixel art electric zap effect featuring violet, pink, and cyan sparks and energy crackles.",
            "tags": [
              "electric",
              "zap",
              "effect",
              "violet",
              "lightning",
              "pixel-art",
              "magic",
              "animation"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "violet",
              "pink",
              "cyan",
              "yellow",
              "white"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "File path pattern recognition",
              "rationale": "The path contains 'fx1_electric_zap_small_violet/frame0002.png', indicating it is part of a multi-file animation sequence for a small electric zap effect."
            },
            {
              "rule": "Visual content analysis",
              "rationale": "The image displays pixel-art lightning/spark effects with bright core energy and surrounding particle dots."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/TINY FOREST/WATER GROUND NIGHT 2.png",
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
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "A pixel art water and waterfall tile styled for a nighttime forest environment, featuring dark blue cascading water and cyan foam highlights.",
            "tags": [
              "water",
              "waterfall",
              "ground",
              "night",
              "tile",
              "pixel-art",
              "tiny-forest"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "dark blue",
              "cyan",
              "midnight blue",
              "teal"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset Type Classification",
              "rationale": "The image is a standalone file representing a single water/waterfall tile graphic, classified as a static image."
            },
            {
              "rule": "Perspective Identification",
              "rationale": "The vertical cascading flow of the waterfall indicates a side-scrolling platformer perspective."
            },
            {
              "rule": "Grid and Dimensions",
              "rationale": "Tiny Forest asset pack uses standard 16x16 pixel grid building blocks."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/dreamir/elves-pack/extracted/Elves_Pack/Elf_Spearman/Elf_Spearman_BlockNoEffeckt/Elf_Spearman_Block5.png",
        {
          "catalog_proposal": {
            "type": "multi_file_animation",
            "perspective": "side",
            "num_frames": 1,
            "cell_dimensions": {
              "width": 64,
              "height": 64
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art sprite of an Elf Spearman in dark armor holding a spear and raising a large green shield in a blocking stance.",
            "tags": [
              "elf",
              "spearman",
              "warrior",
              "shield",
              "block",
              "pixel_art",
              "armor"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "dark grey",
              "green",
              "brown",
              "silver"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Filename and directory structure analysis",
              "rationale": "The path contains 'Elf_Spearman_BlockNoEffeckt/Elf_Spearman_Block5.png', indicating it is part of a multi-file blocking animation sequence for an elf spearman unit."
            },
            {
              "rule": "Visual content inspection",
              "rationale": "The sprite depicts a humanoid elf warrior in armor holding a spear and raising a large green shield, characteristic of a defensive block stance from a side-scrolling perspective."
            }
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch3_responses:
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
            "pass1_timestamp": "2026-09-13T03:01:00-04:00"
        }
    }
    existing.append(asset_dict)

with open(json_path, 'w') as f:
    json.dump(existing, f, indent=2)

print(f"Successfully appended batch 3 (9 items). Total items now: {len(existing)}")
