

#include <AssetStudio/Gameplay/Screen.hpp>

#include <AllegroFlare/BitmapBin.hpp>
#include <AllegroFlare/FrameAnimation/SpriteSheet.hpp>
#include <AllegroFlare/SystemInfo.hpp>
#include <AllegroFlare/VirtualControllers/GenericController.hpp>
#include <AssetStudio/DatabaseCSVLoader.hpp>
#include <AssetStudio/GameConfigurations/Main.hpp>
#include <AssetStudio/Gameplay/Level.hpp>
#include <allegro5/allegro_color.h>
#include <allegro5/allegro_primitives.h>
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace AssetStudio
{
namespace Gameplay
{


Screen::Screen(AllegroFlare::EventEmitter* event_emitter, AllegroFlare::BitmapBin* bitmap_bin, AllegroFlare::FontBin* font_bin, AllegroFlare::ModelBin* model_bin, AllegroFlare::BitmapBin assets_bitmap_bin, AssetStudio::GameConfigurations::Main* game_configuration)
   : AllegroFlare::Screens::Gameplay()
   , event_emitter(event_emitter)
   , bitmap_bin(bitmap_bin)
   , font_bin(font_bin)
   , model_bin(model_bin)
   , assets_bitmap_bin(assets_bitmap_bin)
   , database()
   , sprite_sheet_atlas(nullptr)
   , sprite_sheet(nullptr)
   , game_configuration(game_configuration)
   , scrollarea_placement({})
   , current_level_identifier("[unset-current_level]")
   , current_level(nullptr)
   , initialized(false)
{
}


Screen::~Screen()
{
}


void Screen::set_game_configuration(AssetStudio::GameConfigurations::Main* game_configuration)
{
   this->game_configuration = game_configuration;
}


AssetStudio::GameConfigurations::Main* Screen::get_game_configuration() const
{
   return game_configuration;
}


void Screen::set_event_emitter(AllegroFlare::EventEmitter* event_emitter)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::set_event_emitter]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::set_event_emitter]: error: guard \"(!initialized)\" not met");
   }
   this->event_emitter = event_emitter;
   return;
}

void Screen::set_bitmap_bin(AllegroFlare::BitmapBin* bitmap_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::set_bitmap_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::set_bitmap_bin]: error: guard \"(!initialized)\" not met");
   }
   this->bitmap_bin = bitmap_bin;
   return;
}

void Screen::set_font_bin(AllegroFlare::FontBin* font_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::set_font_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::set_font_bin]: error: guard \"(!initialized)\" not met");
   }
   this->font_bin = font_bin;
   return;
}

void Screen::set_model_bin(AllegroFlare::ModelBin* model_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::set_model_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::set_model_bin]: error: guard \"(!initialized)\" not met");
   }
   this->model_bin = model_bin;
   return;
   return;
}

bool Screen::load_level_by_identifier(std::string level_identifier)
{
   if (!(game_configuration))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::load_level_by_identifier]: error: guard \"game_configuration\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::load_level_by_identifier]: error: guard \"game_configuration\" not met");
   }
   // Destroy the current level
   if (current_level)
   {
      // TODO: Shutdown current level
      delete current_level;
   }

   // Load the new level
   AllegroFlare::Levels::Base *loaded_level = game_configuration->load_level_by_identifier(level_identifier);
   if (loaded_level)
   {
      // TODO: Consider how to have this level loading mechanism removed, specifically the dependency on the configuration
      // For now, confirm the type, and cast
      if (!loaded_level->is_type(AssetStudio::Gameplay::Level::TYPE))
      {
         throw std::runtime_error("Loaded level not of expected type");
      }
      current_level_identifier = level_identifier;
      current_level = static_cast<AssetStudio::Gameplay::Level*>(loaded_level);
   }
   return true;
}

void Screen::initialize()
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"(!initialized)\" not met");
   }
   if (!(al_is_system_installed()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_system_installed()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_system_installed()\" not met");
   }
   if (!(al_is_primitives_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_primitives_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_primitives_addon_initialized()\" not met");
   }
   if (!(al_is_font_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_font_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"al_is_font_addon_initialized()\" not met");
   }
   if (!(event_emitter))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"event_emitter\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"event_emitter\" not met");
   }
   if (!(bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"bitmap_bin\" not met");
   }
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"font_bin\" not met");
   }
   if (!(model_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::initialize]: error: guard \"model_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::initialize]: error: guard \"model_bin\" not met");
   }
   set_update_strategy(AllegroFlare::Screens::Base::UpdateStrategy::SEPARATE_UPDATE_AND_RENDER_FUNCS);

   load_database_from_csv();

   initialized = true;
   return;
}

std::vector<AllegroFlare::FrameAnimation::Frame> Screen::build_n_frames(uint32_t num_frames, uint32_t start_frame_num, float each_frame_duration)
{
   if (!((num_frames > 1)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(num_frames > 1)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(num_frames > 1)\" not met");
   }
   if (!((start_frame_num >= 0)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met");
   }
   if (!((each_frame_duration >= 0.0001)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met");
   }
   std::vector<AllegroFlare::FrameAnimation::Frame> result;
   for (uint32_t i=0; i<num_frames; i++)
   {
      result.push_back({ start_frame_num + i, each_frame_duration });
   }
   return result;
}

AllegroFlare::FrameAnimation::SpriteSheet* Screen::obtain_sprite_sheet(std::string filename, int cell_width, int cell_height, int sprite_sheet_scale)
{
   // TODO: Guard after assets_bitmap_bin is initialized
   //static std::map<std::string, AllegroFlare::FrameAnimation::SpriteSheet*> sprite_sheets = {
   //};

   ALLEGRO_BITMAP* sprite_sheet_atlas = al_clone_bitmap(
         assets_bitmap_bin.auto_get(filename)
         //assets_bitmap_bin.auto_get("grotto_escape_pack/Base pack/graphics/player.png")
      );
   //AllegroFlare::FrameAnimation::SpriteSheet *sprite_sheet =
   AllegroFlare::FrameAnimation::SpriteSheet *result_sprite_sheet =
      new AllegroFlare::FrameAnimation::SpriteSheet(sprite_sheet_atlas, cell_width, cell_height, sprite_sheet_scale);

   al_destroy_bitmap(sprite_sheet_atlas);

   return result_sprite_sheet;
}

std::string Screen::infer_asssets_folder_location()
{
   AllegroFlare::SystemInfo system_info;
   //std::vector<std::string> expected_possible_hostnames = {
      //"DESKTOP-NC9M1BH",            // Mark's Windows Laptop
      //"Marks-13-MacBook-Pro.local", // Mark's Mac Laptop used as desktop
      //"Marks-Mac-mini.local",       // Mark's MacMini
      // Marks-MacBook-Pro.local      // Mark's primary laptop
   //};
   std::string hostname = system_info.get_hostname();

   if (hostname == "Marks-MacBook-Pro.local")
   {
      return "/Volumes/markoates/Assets/";
   }

   return "/Users/markoates/Assets/";
}

void Screen::load_database_from_csv()
{
   std::string assets_folder = infer_asssets_folder_location();
   std::string assets_csv_filename = "assets_db.csv";
   assets_bitmap_bin.set_full_path(assets_folder);

   AssetStudio::DatabaseCSVLoader loader;
   loader.set_assets_bitmap_bin(&assets_bitmap_bin);
   loader.set_csv_full_path(assets_folder + assets_csv_filename);
   loader.load();

   database.set_assets(loader.get_assets());

   // Initialize the animations
   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      if (asset->animation) asset->animation->initialize();
   }

   return;
}

void Screen::load_database_and_build_assets()
{
   int asset_id = 0;
   std::string assets_folder = "/Users/markoates/Assets/";
   assets_bitmap_bin.set_full_path(assets_folder);

   //sprite_sheet_atlas = al_clone_bitmap(
         //assets_bitmap_bin.auto_get("grotto_escape_pack/Base pack/graphics/player.png")
      //);
   //AllegroFlare::FrameAnimation::SpriteSheet *sprite_sheet =
   //sprite_sheet =
      //new AllegroFlare::FrameAnimation::SpriteSheet(sprite_sheet_atlas, 16, 16, 2);
   //al_destroy_bitmap(atlas);

   /*
   database.set_assets({
      {
         "grotto_character",
         new AssetStudio::Asset(
            asset_id++,
            "grotto",
            "grotto character",
            new AllegroFlare::FrameAnimation::Animation(
               obtain_sprite_sheet("grotto_escape_pack/Base pack/graphics/player.png"), //sprite_sheet,
               "grotto_character",
               {
                  { 0, 0.2 },
                  { 1, 0.2 },
                  { 2, 0.2 },
               },
               AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_PING_PONG
            )
         ),
      },
      {
         "grotto_jump",
         new AssetStudio::Asset(
            asset_id++,
            "grotto",
            "grotto jump",
            new AllegroFlare::FrameAnimation::Animation(
               obtain_sprite_sheet("grotto_escape_pack/Base pack/graphics/player.png"), //sprite_sheet,
               "grotto_jump",
               {
                  { 4, 1.0 },
               },
               AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_PING_PONG
            )
         ),
      },
      {
         "explosion_h",
         new AssetStudio::Asset(
            asset_id++,
            "explosion_h",
            "a blow up",
            new AllegroFlare::FrameAnimation::Animation(
               obtain_sprite_sheet("Explosions Pack 7 files/Spritesheet/explosion-h.png", 32, 32),
               "explosion_h",
               build_n_frames(9),
               AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE
            )
         ),
      },
      {
         "explosion_e",
         new AssetStudio::Asset(
            asset_id++,
            "explosion_h",
            "a blow up",
            new AllegroFlare::FrameAnimation::Animation(
               obtain_sprite_sheet("Explosions Pack 7 files/Spritesheet/explosion-e.png", 48, 48),
               "explosion_h",
               build_n_frames(9),
               AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE
            )
         )
      },

         //obtain_sprite_sheet
      //Explosions Pack 7 files/Spritesheet/explosion-h.png


   });
   */

   // Initialize the animations
   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      if (asset->animation) asset->animation->initialize();
   }

   return;
}

void Screen::on_activate()
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::on_activate]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::on_activate]: error: guard \"initialized\" not met");
   }
   //emit_event_to_update_input_hints_bar();
   //emit_show_and_size_input_hints_bar_event();
   return;
}

void Screen::on_deactivate()
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::on_deactivate]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::on_deactivate]: error: guard \"initialized\" not met");
   }
   //emit_hide_and_restore_size_input_hints_bar_event();
   return;
}

void Screen::update()
{
   float time_now = al_get_time();

   // Do an auto-scroll on the scrollarea
   //scrollarea_placement.position.y -= 1.0f;

   // Run "update" on all animations
   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;

      // Update the animation (if present)
      if (asset->animation)
      {
         asset->animation->update();
         if (asset->animation->get_playmode() == AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE)
         {
            if (asset->animation->get_finished())
            {
               // Before resetting the animation, add some dealy so it is clear the animation playmode is not a loop
               float age_since_finished = time_now -  asset->animation->get_finished_at();
               if (age_since_finished >= 0.4f)
               {
                  // Reset the animation to replay
                  asset->animation->reset();
                  asset->animation->start();
               }
            }
         }
      }
   }
   return;
}

void Screen::render()
{
   ALLEGRO_FONT *font = obtain_font();
   //al_draw_text(font, ALLEGRO_COLOR{1, 1, 1, 1}, 1920/2, 1080/2 - 30, ALLEGRO_ALIGN_CENTER, "Hello");

   float spacing_x = 300;
   float spacing_y = 340;
   int num_columns = 6;

   float x = 1920 / 2 - (spacing_x * (num_columns - 1)) / 2;
   float y = 200;

   int sprite_sheet_scale = 2;
   AllegroFlare::Placement2D asset_placement;
   AllegroFlare::Placement2D frame_placement;
   int asset_i = 0;
   float ui_color_opacity = 0.5f;
   ALLEGRO_COLOR ui_color = ALLEGRO_COLOR{
         0.1f*ui_color_opacity,
         0.1f*ui_color_opacity,
         0.143f*ui_color_opacity,
         0.5f*ui_color_opacity
      };
   ALLEGRO_COLOR ui_color_light = ALLEGRO_COLOR{0.7, 0.7, 0.745, 1.0};
   ALLEGRO_COLOR ui_color_dark = ALLEGRO_COLOR{0.0, 0.0, 0.0, 0.1};

   float scale_x = 2.0f;
   float scale_y = 2.0f;

   int column_num = 0;
   int row_num = 0;

   // Build up the scrollarea_placement (TODO: Move this to an initialization)
   // TODO: Add scrollarea user controls
   //scrollarea_placement.position.y--;
   scrollarea_placement.size.x = 1920;
   scrollarea_placement.size.y = 1080;
   scrollarea_placement.align.x = 0;
   scrollarea_placement.align.y = 0;

   scrollarea_placement.start_transform();

   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      if (asset->type == "tileset") continue; // Skip over tilesets

      row_num = asset_i / num_columns;
      column_num = asset_i % num_columns;
      float xx = x + (spacing_x * column_num);
      float yy = y + (spacing_y * row_num);
      frame_placement.position.x = xx;
      frame_placement.position.y = yy;
      frame_placement.size.x = 256;
      frame_placement.size.y = 256;

      frame_placement.start_transform();
      al_draw_filled_rectangle(0, 0, frame_placement.size.x, frame_placement.size.y, ui_color_dark);
      {
         asset_placement.position.x = frame_placement.size.x/2;
         asset_placement.position.y = frame_placement.size.y/2;
         asset_placement.size.x = asset->cell_width * sprite_sheet_scale;
         asset_placement.size.y = asset->cell_height * sprite_sheet_scale;
         asset_placement.scale.x = scale_x;
         asset_placement.scale.y = scale_x;

         asset_placement.start_transform();
         //al_draw_rectangle(0, 0, frame_placement.size.x, frame_placement.size.y, ui_color, 1.0);

         // Draw a frame rectangle indicating the dimensions of the asset
         al_draw_rectangle(0, 0, asset_placement.size.x, asset_placement.size.y, ui_color, 2.0);

         if (asset->animation)
         {
            if (asset->animation->get_finished())
            {
               // If the animation is "finished", show a little placeholder circle indicating that the animation has 
               // reached its end
               al_draw_filled_circle(asset_placement.size.x/2, asset_placement.size.y/2, 6, ui_color);
            }
            else
            {
               asset->animation->draw();
            }
         }
         else if (asset->bitmap)
         {
            //al_draw_circle(asset_placement.size.x/2, asset_placement.size.y/2, 6, ui_color, 2.0f);
            al_draw_bitmap(asset->bitmap, 0, 0, 0);
            //al_draw_bitmap(
         }
         else
         {
            al_draw_text(
                  font,
                  ui_color_light,
                  asset_placement.size.x * 0.5f,
                  asset_placement.size.y * 0.5f,
                  ALLEGRO_ALIGN_CENTER,
                  "preview not available"
               );
         }

         asset_placement.restore_transform();

         // Draw info about the asset
         ALLEGRO_FONT *font = obtain_font_for_asset_identifier();
         ALLEGRO_FONT *small_font = obtain_small_font();

         // Draw asset identifier
         al_draw_text(
               font,
               ui_color_light,
               0,
               frame_placement.size.y + 8,
               ALLEGRO_ALIGN_LEFT,
               asset->intra_pack_identifier.c_str()
            );

         // Draw asset pack identifier
         al_draw_text(
               small_font,
               ui_color_light,
               0,
               frame_placement.size.y + 8 + 20,
               ALLEGRO_ALIGN_LEFT,
               asset->asset_pack_identifier.c_str()
            );

         // Draw asset type
         al_draw_text(
               small_font,
               ui_color_light,
               frame_placement.size.x,
               frame_placement.size.y + 8,
               ALLEGRO_ALIGN_RIGHT,
               asset->type.c_str()
            );

         // Draw asset dimensions
         al_draw_textf(
               small_font,
               ui_color_light,
               frame_placement.size.x,
               frame_placement.size.y + 8 + 20,
               ALLEGRO_ALIGN_RIGHT,
               "%dx%d", asset->cell_width, asset->cell_height
            );

         //al_draw_rectangle(0, 0, frame_placement.size.x, frame_placement.size.y, ui_color, 1.0);
      }
      al_draw_rectangle(0, 0, frame_placement.size.x, frame_placement.size.y, ui_color, 1.0);
      frame_placement.restore_transform();


      //asset_placement.draw_box(al_color_name("dodgerblue"), false);

      asset_i++;
   }
   scrollarea_placement.restore_transform();

   return;
}

void Screen::game_event_func(AllegroFlare::GameEvent* game_event)
{
   if (!(game_event))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::game_event_func]: error: guard \"game_event\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::game_event_func]: error: guard \"game_event\" not met");
   }
   // game_configuration->handle_game_event(game_event);
   return;
}

void Screen::primary_update_func(double time_now, double delta_time)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::primary_update_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::primary_update_func]: error: guard \"initialized\" not met");
   }
   // Update stuff here (take into account delta_time)
   update();
   return;
}

void Screen::primary_render_func()
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::primary_render_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::primary_render_func]: error: guard \"initialized\" not met");
   }
   // Render stuff here
   render();
   return;
}

void Screen::key_char_func(ALLEGRO_EVENT* ev)
{
   if (!(ev))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::key_char_func]: error: guard \"ev\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::key_char_func]: error: guard \"ev\" not met");
   }
   switch (ev->keyboard.keycode)
   {
      case ALLEGRO_KEY_UP:
      case ALLEGRO_KEY_PGUP:
         scrollarea_placement.position.y += 40.0f;
         //universe.move_camera_up();
      break;

      case ALLEGRO_KEY_DOWN:
      case ALLEGRO_KEY_PGDN:
         scrollarea_placement.position.y -= 40.0f;
         //universe.move_camera_down();
      break;

      case ALLEGRO_KEY_RIGHT:
         //universe.move_camera_right();
      break;

      case ALLEGRO_KEY_LEFT:
         //universe.move_camera_left();
      break;

      //case ALLEGRO_KEY_S: {
         //bool command_pressed = ev->keyboard.modifiers & ALLEGRO_KEYMOD_COMMAND;
         //if (command_pressed)
         //{
            //universe.save_score_to_filename();
            //handled = true;
         //}
      //} break;
      //case ALLEGRO_KEY_L: {
         //bool command_pressed = ev->keyboard.modifiers & ALLEGRO_KEYMOD_COMMAND;
         //if (command_pressed)
         //{
            //universe.load_score_from_filename();
            //handled = true;
         //}
      //} break;
   }
   return;
}

void Screen::virtual_control_button_up_func(AllegroFlare::Player* player, AllegroFlare::VirtualControllers::Base* virtual_controller, int virtual_controller_button_num, bool is_repeat)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::virtual_control_button_up_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::virtual_control_button_up_func]: error: guard \"initialized\" not met");
   }
   // TODO: this function
   return;
}

void Screen::virtual_control_button_down_func(AllegroFlare::Player* player, AllegroFlare::VirtualControllers::Base* virtual_controller, int virtual_controller_button_num, bool is_repeat)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::virtual_control_button_down_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::virtual_control_button_down_func]: error: guard \"initialized\" not met");
   }
   // TODO: this function
   using namespace AllegroFlare;
   //if (!is_processing_user_input()) return;

   if (virtual_controller_button_num == VirtualControllers::GenericController::BUTTON_RIGHT)
   {
      //player_velocity.x = 1;
      //chapter_select_element.rotate_carousel_right();
   }
   if (virtual_controller_button_num == VirtualControllers::GenericController::BUTTON_LEFT)
   {
      //player_velocity.x = -1;
      //chapter_select_element.rotate_carousel_left();
   }
   if (virtual_controller_button_num == VirtualControllers::GenericController::BUTTON_A
      || virtual_controller_button_num == VirtualControllers::GenericController::BUTTON_MENU
      )
   {
      //select_menu_option();
   }
   if (virtual_controller_button_num == VirtualControllers::GenericController::BUTTON_X)
   {
      //exit_screen();
   }
   //call_on_finished_callback_func(); // Consider technique to exit
   return;
}

void Screen::virtual_control_axis_change_func(ALLEGRO_EVENT* ev)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::virtual_control_axis_change_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::virtual_control_axis_change_func]: error: guard \"initialized\" not met");
   }
   // TODO: this function
   return;
}

ALLEGRO_FONT* Screen::obtain_font()
{
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::obtain_font]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::obtain_font]: error: guard \"font_bin\" not met");
   }
   return font_bin->auto_get("Inter-Regular.ttf -32");
}

ALLEGRO_FONT* Screen::obtain_font_for_asset_identifier()
{
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::obtain_font_for_asset_identifier]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::obtain_font_for_asset_identifier]: error: guard \"font_bin\" not met");
   }
   return font_bin->auto_get("Inter-Regular.ttf -18");
}

ALLEGRO_FONT* Screen::obtain_small_font()
{
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Gameplay::Screen::obtain_small_font]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Gameplay::Screen::obtain_small_font]: error: guard \"font_bin\" not met");
   }
   return font_bin->auto_get("Inter-Regular.ttf -13");
}


} // namespace Gameplay
} // namespace AssetStudio


