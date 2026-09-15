import json
import os
import subprocess
import time

targets = [
    "untiedgames/mechanical-pixel-art-gui/extracted/mechanical_pixel_art_gui/window/violet/panel_bottom_right.png",
    "elvgames/topdown-rpg-sprites-2/extracted/Character Sprites 2 - Fantasy Dreamland/RPG Maker VX Ace/sv_actors/Character_047_Battler.png",
    "elvgames/spear-item-icons-32x32-pixelart/extracted/Spear Item Icons/Spears Purple/Spear_Purple 20.png",
    "untiedgames/zombie-pack-pixel-art-monsters/extracted/Zombie Pack/style_C/PNG/zombie_J/die/frame0020.png",
    "untiedgames/super-pixel-projectiles-pack-2/extracted/Super Pixel Projectiles Pack 2/PNG/pj2_scifi_missile_small_blue/frame0008.png",
    "finalbossblues/time-elements-character-core-set/extracted/assets/frontextra/frontextra4_c5.png",
    "itchabop/8bit-inventory/extracted/Sprites/Apple.png",
    "untiedgames/super-pixel-objects-and-items/extracted/super_pixel_objects_and_items/PNG/gem_B_orange_large/outline_black_outside/frame0004.png",
    "kazzter-k/sci-fi-icon-pack/extracted/Modern and Sci-Fi Icons/Icons/Individual Icons/icon_41.png",
    "elvgames/farming-game-world/extracted/Farming Game World/RPG Maker/RPG Maker MV/enemies/RPG_Monster_027_2.png",
    "elvgames/platformer-tileset-08/extracted/Platformer Series - Tileset #08/Enemies/Enemy 016/Enemy_016.png",
    "untiedgames/super-pixel-item-pickups-fantasy-pack-1/extracted/Super Pixel Item Pickups Fantasy Pack 1/PNG/fp1_gem_red/frame0027.png",
    "szadiart/world-and-dungeon/extracted/Open World And Cave Dungeon/Destructive objects/Crate C/crate-C-destr-anim-01.png",
    "rafaelmatos/epic-rpg-world-pack-ancient-ruins/extracted/EPIC RPG World Pack - Ancient Ruins V 1.9.1/Tilesets/grass2 to blood.png",
    "butterymilk/tiny-wonder-rpg-icons/extracted/Tiny Wonder RPG Icons Pack/sliced sprite sheets/items/items8.png",
    "runninblood/asset-pack/extracted/RunninBloods_HUGE_16x16_Asset_Pack_V2/Tiles/Seperate_files_tiles/16x16_Tile_pack_tileset_329.png",
    "untiedgames/super-pixel-sci-fi-ui-futura-max/extracted/Super Pixel Sci-Fi UI - Futura Max/window_theme_sliced/window_theme_dark_gray_sliced/window_bottom_right.png",
    "untiedgames/super-pixel-sci-fi-ui-futura-max/extracted/Super Pixel Sci-Fi UI - Futura Max/controller_glyphs/controller_glyphs_small_yellow_highlighted/stick_blank.png",
    "untiedgames/candy-pixel-art-gui/extracted/candy_pixel_art_gui/icons/outlined/orange/cash_coin_B.png",
    "untiedgames/wills-magic-pixel-particle-effects/extracted/wills_magic_pixel_particle_effects/square_burst/frames/frame0047.png",
    "cleancutgames/pixelart-parallax-woods/extracted/Pixelart_Parallax_Woods_Pack/Pixelart_Parallax_Woods_Pack/bg_plant_4_1.png",
    "almostapixel/smallburg-mine/extracted/assets/character/run/hairstyles/spikey/character_run_hairstyles_spikey_green.png",
    "untiedgames/mega-monster-pack/extracted/mega_monster_pack/spirit_mini/PNG/idle/frame0006.png",
    "untiedgames/royal-rpg-pixel-art-gui/extracted/royal_rpg_pixel_art_gui/icons/simple/light/folder.png",
    "finalbossblues/animated-npc-sprites-pack/extracted/npc-animations/individual_frames/children/child6_right (1).png",
    "elvgames/knight-fantasy-rpg-character-sprites/extracted/Farm Game Knight Character Sprites/Characters/Knight_74/Knight_74_Dead.png",
    "untiedgames/mechanical-pixel-art-gui/extracted/mechanical_pixel_art_gui/premade/256x1024/window/dark/vertical_rule_B.png",
    "untiedgames/zombie-pack-pixel-art-monsters/extracted/Zombie Pack/style_E/PNG/zombie_A/die/frame0003.png",
    "untiedgames/super-pixel-ice-cavern-tileset/extracted/super_pixel_ice_cavern/style_D/PNG/shadows_A_top_left.png",
    "untiedgames/super-pixel-fantasy-fx-pack-1/extracted/Super Pixel Fantasy FX Pack 1/PNG/fanfx1_magic_burst_B_small_blue/frame0013.png",
    "untiedgames/mechanical-pixel-art-gui/extracted/mechanical_pixel_art_gui/window/green/subpanel_center.png",
    "anokolisa/sidescroller-pixelart-sprites-asset-pack-forest-16x16/extracted/Legacy-Fantasy - High Forest 2.3/Mob/Boar/Walk/Walk-Base-Sheet.png",
    "almostapixel/smallburg-plantscraft-pack/extracted/assets/farming/crops/ground/eggplant/eggplant_seedpacket_icon.png",
    "untiedgames/wills-pixel-explosions/extracted/wills_pixel_explosions/round_explosion_small_multi/style_D/PNG/frame0022.png",
    "runninblood/16x16-top-down-rpg/extracted/RunninBloods_HUGE_16x16_Top-Down-Tileset_V2/Seperate_File_Tiles/Tiles2_220.png",
    "untiedgames/super-pixel-sci-fi-ui-futura-max/extracted/Super Pixel Sci-Fi UI - Futura Max/icons/outlined/green/share.png",
    "untiedgames/zombie-pack-pixel-art-monsters/extracted/Zombie Pack/style_B/PNG/zombie_B/attack_A/frame0012.png",
    "untiedgames/wills-magic-pixel-particle-effects/extracted/wills_magic_pixel_particle_effects/implosion_A/frames/frame0022.png",
    "alb-pixel-store/tiny-rangers-forest-assets/extracted/Tiny Ranger Forest/Enemies/Enemy 34/enemy_34_dead.png",
    "untiedgames/mechanical-pixel-art-gui/extracted/mechanical_pixel_art_gui/premade/128x1024/window/yellow/header_panel_A.png",
    "elvgames/ra-enemies-03/extracted/Monsters Asset Pack 03 - Rogue Adventure/Enemy_017_D.png",
    "untiedgames/wills-magic-pixel-particle-effects/extracted/wills_magic_pixel_particle_effects/fire_B/frames/frame0116.png",
    "chierit/livelynpcs-victorian-steampunk/extracted/LivelyNPCs_victorian_steampunk/individual sprites/steambot_02/steambot_02_04.png",
    "rafaelmatos/epic-rpg-world-pack-old-prison-asset-tileset/extracted/EPIC RPG World Pack - Old Prison V1.6.2/Props/atlas props - individual sprites/barrel - color scheme 2 - 22 silver.png",
    "untiedgames/super-pixel-objects-2021-edition/extracted/Super Pixel Objects 2021 Edition/PNG/outline_light/collectible_club_small_green/frame0006.png",
    "elvgames/fantasy-dreamland-caves/extracted/Caves - Fantasy Dreamland/RPG Maker MZ (16x16)/characters/FD_Caves_Minerals01.png",
    "elvgames/farming-game-world/extracted/Farming Game World/Characters/Knight_01/Knight_01_Pickaxe_Left.png",
    "elvgames/farming-game-world/extracted/Farming Game World/RPG Maker/RPG Maker MV/tilesets/FG_Forest_Summer_C.png",
    "untiedgames/super-pixel-sci-fi-ui-futura-max/extracted/Super Pixel Sci-Fi UI - Futura Max/controller_glyphs/controller_glyphs_small_violet/ps_dpad_horizontal.png",
    "untiedgames/zombie-pack-pixel-art-monsters/extracted/Zombie Pack/style_B/PNG/zombie_D/crawl_die/frame0028.png"
]

subagents = []
for i, target in enumerate(targets):
    prompt = f"You MUST use the view_file tool on this exact path FIRST to see its dimensions and frames: /Users/markoates/Assets/{target}. Then follow your system instructions to output the JSON catalog proposal."
    subagents.append({
        "Model": "flash_lite",
        "Role": f"Visual Inferencer {i+1}",
        "TypeName": "visual_inferencer_v2",
        "Prompt": prompt
    })

with open("batch.json", "w") as f:
    json.dump({"Subagents": subagents, "toolAction": "Spawning batch", "toolSummary": "Spawn batch"}, f)
