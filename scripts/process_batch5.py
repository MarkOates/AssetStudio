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

batch5_responses = [
    (
        "/Users/markoates/Assets/dreamir/elves-pack/extracted/Elves_Pack/Elf_Mage/Elf_Mage_Spell_1/Elf_Mage_Spell_1.png",
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
            "description": "Elf Mage casting a spell holding a staff with a blue magical orb, wearing green and brown robes with blonde hair.",
            "tags": [
              "elf",
              "mage",
              "spell",
              "magic",
              "staff",
              "fantasy",
              "pixel-art"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "green",
              "brown",
              "blue",
              "gold",
              "blonde"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Multi-file animation frame",
              "rationale": "Filename indicates part of a multi-file spell casting animation sequence."
            },
            {
              "rule": "Side perspective",
              "rationale": "Character is shown in a side/three-quarters profile view characteristic of 2D platformer/RPG sprite packs."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/axes/axe_24.png",
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
            "description": "A 16x16 pixel art icon of a double-bladed battle axe with a brown wooden handle and glowing green/yellow metal blades.",
            "tags": ["axe", "weapon", "battle-axe", "rpg", "item", "icon", "pixel-art"],
            "style": "pixel-art",
            "color_descriptors": ["green", "yellow", "brown", "black", "white"]
          },
          "inference_reasoning": [
            {
              "rule": "File path and visual inspection indicate a standalone RPG weapon icon.",
              "rationale": "The image is located in an axe pack directory, measures 16x16 pixels, and depicts a single static weapon icon suitable for inventory systems."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/untiedgames/world-map-pixel-art-tileset/extracted/world_map/pieces/terrain/terrain_edge_east_A_f3.png",
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
            "description": "World map terrain edge tile showing a landmass transitioning eastward into coastal water.",
            "tags": ["world_map", "terrain", "edge", "east", "land", "water", "pixel_art"],
            "style": "pixel art",
            "color_descriptors": ["green", "brown", "tan", "cyan", "blue", "dark_blue"]
          },
          "inference_reasoning": [
            {
              "rule": "File path and naming convention identify world map terrain pieces.",
              "rationale": "The path 'world_map/pieces/terrain/terrain_edge_east_A_f3.png' designates an eastern terrain edge piece for a world map tileset."
            },
            {
              "rule": "Visual inspection shows distinct terrain strata from land to deep water.",
              "rationale": "The image clearly depicts green land grading into rocky/clifftop terrain, beach/shallow water, and deep blue water on the right edge."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/ansimuz/gothicvania-cemetery/extracted/gothicvania-cemetery-files/GIFS/misc/enemy-death.gif",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "side",
            "num_frames": 6,
            "cell_dimensions": {"width": 32, "height": 32},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Pixel art animation of an enemy death effect showing a rising orange and yellow flame/soul in the GothicVania Cemetery style.",
            "tags": ["gothicvania", "cemetery", "enemy-death", "animation", "pixel-art", "effect", "fire", "soul"],
            "style": "retro pixel art",
            "color_descriptors": ["orange", "yellow", "white"]
          },
          "inference_reasoning": [
            {
              "rule": "File path and format analysis",
              "rationale": "The file is an animated GIF located in the GothicVania Cemetery asset pack under GIFS/misc/enemy-death.gif, indicating a multi-frame animation sequence for an enemy death effect."
            },
            {
              "rule": "Visual content inspection",
              "rationale": "Visual inspection shows a pixel art flame/soul dissipation effect typical of side-scrolling platformer games."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-modern-rpg-icon-set/extracted/Pixeltiers_16x16_Modern_RPG_Update_3/shirts/shirt_161.png",
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
            "description": "A 16x16 pixel art icon of a sleeveless shirt or vest in a modern RPG style.",
            "tags": [
              "shirt",
              "vest",
              "clothing",
              "apparel",
              "rpg",
              "item",
              "icon",
              "modern"
            ],
            "style": "pixel art",
            "color_descriptors": [
              "grey",
              "olive",
              "muted green"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Asset categorization",
              "rationale": "The image is a standalone 16x16 pixel art graphic representing an inventory item of clothing (shirt/vest)."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/finalbossblues/quirky-npcs/extracted/quirky_npcs/tf_color/3x(RMMVMZ)/ironchef.png",
        {
          "catalog_proposal": {
            "type": "animation_frames",
            "perspective": "front",
            "num_frames": 12,
            "cell_dimensions": {
              "width": 32,
              "height": 32
            },
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": {
              "rows": 4,
              "cols": 3
            }
          },
          "theme_profile": {
            "description": "An armored knight chef sprite sheet featuring 12 animation frames showing standing, holding a frying pan, and stirring in a pot.",
            "tags": [
              "knight",
              "chef",
              "armor",
              "cooking",
              "pixel-art",
              "character",
              "npc"
            ],
            "style": "pixel-art",
            "color_descriptors": [
              "steel grey",
              "orange",
              "white",
              "charcoal"
            ]
          },
          "inference_reasoning": [
            {
              "rule": "Grid Structure",
              "rationale": "The image is organized into a 4 row by 3 column grid representing 12 animation frames of the knight chef character."
            },
            {
              "rule": "Character Design",
              "rationale": "The character combines medieval knight plate armor with culinary elements like an apron and a chef-hat styled helmet."
            }
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/helmets/helmet_181.png",
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
            "description": "A horned helmet RPG icon with gold, brown, and horn details.",
            "tags": ["helmet", "armor", "icon", "rpg", "horns", "viking", "fantasy"],
            "style": "pixel_art",
            "color_descriptors": ["brown", "gold", "white", "black", "purple"]
          },
          "inference_reasoning": [
            {"rule": "Asset Type", "rationale": "It is a standalone 16x16 icon image representing an inventory equipment item."},
            {"rule": "Perspective", "rationale": "The helmet is displayed from a direct front-facing perspective."},
            {"rule": "Is Icon", "rationale": "Sized and styled as an RPG inventory icon."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeltier/pixeltiers-16x16-rpg-icon-pack/extracted/Pixeltiers_16x16_RPG_Pack_Update_8/swords/sword_175.png",
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
            "description": "A 16x16 pixel art icon of a curved dagger or short sword with a dark hilt and light blade.",
            "tags": ["sword", "dagger", "weapon", "blade", "rpg", "item", "icon", "pixel art"],
            "style": "pixel art",
            "color_descriptors": ["dark grey", "silver", "gold/yellow highlights", "black"]
          },
          "inference_reasoning": [
            {"rule": "File path and size", "rationale": "Located in swords directory of a 16x16 RPG icon pack, single image file."},
            {"rule": "Visual content", "rationale": "Shows a single standalone curved blade weapon icon suitable for inventory UI overlays."}
          ]
        }
    ),
    (
        "/Users/markoates/Assets/pixeljad/megabundle/extracted/MEGA BUNDLE 12 ASSET PACKS/TINY VOLCANO TILESET/ABOUT ME PIXELJAD ITCHIO.gif",
        {
          "catalog_proposal": {
            "type": "static_image",
            "perspective": "ui_overlay",
            "num_frames": 1,
            "cell_dimensions": {"width": 0, "height": 0},
            "is_subframe": False,
            "is_icon": False,
            "inferred_grid": None
          },
          "theme_profile": {
            "description": "Artist 'About Me' promotional banner card with portrait and social links",
            "tags": ["banner", "about_me", "artist_credit", "ui", "portrait", "pixeljad"],
            "style": "pixel_art",
            "color_descriptors": ["brown", "beige", "teal", "skin_tone", "dark_brown"]
          },
          "inference_reasoning": [
            {"rule": "Asset Type Rule", "rationale": "The image is a static promotional/credits banner card with text and an artist avatar."},
            {"rule": "Perspective Rule", "rationale": "It functions as a UI graphic or bio banner rather than an in-game tile or sprite."},
            {"rule": "Theme Rule", "rationale": "Features artist credits, portrait, and social media/portfolio icons in pixel art style."}
          ]
        }
    )
]

json_path = "/Users/markoates/Repos/AssetStudio/scripts/ai_subagent_proposals.json"

with open(json_path, 'r') as f:
    existing = json.load(f)

for physical_path, data in batch5_responses:
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

print(f"Successfully appended batch 5 (9 items). Total items now: {len(existing)}")
