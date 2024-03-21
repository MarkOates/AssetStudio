

#include <AssetStudio/Gameplay/Screen.hpp>

#include <AllegroFlare/BitmapBin.hpp>
#include <AllegroFlare/FrameAnimation/SpriteSheet.hpp>
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
      error_message << "[Screen::set_event_emitter]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::set_event_emitter: error: guard \"(!initialized)\" not met");
   }
   this->event_emitter = event_emitter;
   return;
}

void Screen::set_bitmap_bin(AllegroFlare::BitmapBin* bitmap_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[Screen::set_bitmap_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::set_bitmap_bin: error: guard \"(!initialized)\" not met");
   }
   this->bitmap_bin = bitmap_bin;
   return;
}

void Screen::set_font_bin(AllegroFlare::FontBin* font_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[Screen::set_font_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::set_font_bin: error: guard \"(!initialized)\" not met");
   }
   this->font_bin = font_bin;
   return;
}

void Screen::set_model_bin(AllegroFlare::ModelBin* model_bin)
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[Screen::set_model_bin]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::set_model_bin: error: guard \"(!initialized)\" not met");
   }
   this->model_bin = model_bin;
   return;
   return;
}

void Screen::load_level_by_identifier(std::string level_identifier)
{
   if (!(game_configuration))
   {
      std::stringstream error_message;
      error_message << "[Screen::load_level_by_identifier]: error: guard \"game_configuration\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::load_level_by_identifier: error: guard \"game_configuration\" not met");
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
   return;
}

void Screen::initialize()
{
   if (!((!initialized)))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"(!initialized)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"(!initialized)\" not met");
   }
   if (!(al_is_system_installed()))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"al_is_system_installed()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"al_is_system_installed()\" not met");
   }
   if (!(al_is_primitives_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"al_is_primitives_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"al_is_primitives_addon_initialized()\" not met");
   }
   if (!(al_is_font_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"al_is_font_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"al_is_font_addon_initialized()\" not met");
   }
   if (!(event_emitter))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"event_emitter\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"event_emitter\" not met");
   }
   if (!(bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"bitmap_bin\" not met");
   }
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"font_bin\" not met");
   }
   if (!(model_bin))
   {
      std::stringstream error_message;
      error_message << "[Screen::initialize]: error: guard \"model_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::initialize: error: guard \"model_bin\" not met");
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
      error_message << "[Screen::build_n_frames]: error: guard \"(num_frames > 1)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::build_n_frames: error: guard \"(num_frames > 1)\" not met");
   }
   if (!((start_frame_num >= 0)))
   {
      std::stringstream error_message;
      error_message << "[Screen::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::build_n_frames: error: guard \"(start_frame_num >= 0)\" not met");
   }
   if (!((each_frame_duration >= 0.0001)))
   {
      std::stringstream error_message;
      error_message << "[Screen::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::build_n_frames: error: guard \"(each_frame_duration >= 0.0001)\" not met");
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

void Screen::load_database_from_csv()
{
   std::string assets_folder = "/Users/markoates/Assets/";
   std::string assets_csv_filename = "assets_db.csv";
   assets_bitmap_bin.set_full_path(assets_folder);

   //AssetStudio::DatabaseCSVLoader

   //AllegroFlare::BitmapBin assets_bitmap_bin;
   //assets_bitmap_bin.set_full_path(ASSETS_FULL_PATH);
   AssetStudio::DatabaseCSVLoader loader;
   loader.set_assets_bitmap_bin(&assets_bitmap_bin);
   loader.set_csv_full_path(assets_folder + assets_csv_filename);
   loader.load();

   database.set_assets(loader.get_levels());

   // Initialize the animations
   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      asset->animation->initialize();
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
      asset->animation->initialize();
   }

   return;
}

void Screen::on_activate()
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[Screen::on_activate]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::on_activate: error: guard \"initialized\" not met");
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
      error_message << "[Screen::on_deactivate]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::on_deactivate: error: guard \"initialized\" not met");
   }
   //emit_hide_and_restore_size_input_hints_bar_event();
   return;
}

void Screen::update()
{
   float time_now = al_get_time();
   // Run "update" on all animations
   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      asset->animation->update();
      if (asset->animation->get_playmode() == AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE)
      {
         if (asset->animation->get_finished())
         {
            // Before resetting the animation, add some dealy so it is clear the animation playmode is not a loop
            float age_since_finished = time_now -  asset->animation->get_finished_at();
            if (age_since_finished >= 0.8f)
            {
               // Reset the animation to replay
               asset->animation->reset();
               asset->animation->start();
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

   float x = 300;
   float y = 200;
   float spacing_x = 300;
   int sprite_sheet_scale = 2;
   AllegroFlare::Placement2D placement;
   int asset_i = 0;
   ALLEGRO_COLOR ui_color = ALLEGRO_COLOR{0.1, 0.1, 0.143, 0.5};

   for (auto &asset_record : database.get_assets())
   {
      auto &asset = asset_record.second;
      placement.position.x = x + spacing_x * asset_i;
      placement.position.y = y;
      placement.size.x = asset->cell_width * sprite_sheet_scale;
      placement.size.y = asset->cell_height * sprite_sheet_scale;
      placement.scale.x = 3.0f;
      placement.scale.y = 3.0f;

      placement.start_transform();

      // Draw a frame rectangle indicating the dimensions of the asset
      al_draw_rectangle(0, 0, placement.size.x, placement.size.y, ui_color, 2.0);

      if (asset->animation->get_finished())
      {
         // If the animation is "finished", show a little placeholder circle indicating that the animation has 
         // reached its end
         al_draw_filled_circle(placement.size.x/2, placement.size.y/2, 6, ui_color);
      }
      else
      {
         asset->animation->draw();
      }
      placement.restore_transform();
      //placement.draw_box(al_color_name("dodgerblue"), false);

      asset_i++;
   }

   return;
}

void Screen::game_event_func(AllegroFlare::GameEvent* game_event)
{
   if (!(game_event))
   {
      std::stringstream error_message;
      error_message << "[Screen::game_event_func]: error: guard \"game_event\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::game_event_func: error: guard \"game_event\" not met");
   }
   // game_configuration->handle_game_event(game_event);
   return;
}

void Screen::primary_update_func(double time_now, double delta_time)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[Screen::primary_update_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::primary_update_func: error: guard \"initialized\" not met");
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
      error_message << "[Screen::primary_render_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::primary_render_func: error: guard \"initialized\" not met");
   }
   // Render stuff here
   render();
   return;
}

void Screen::virtual_control_button_up_func(AllegroFlare::Player* player, AllegroFlare::VirtualControllers::Base* virtual_controller, int virtual_controller_button_num, bool is_repeat)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[Screen::virtual_control_button_up_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::virtual_control_button_up_func: error: guard \"initialized\" not met");
   }
   // TODO: this function
   return;
}

void Screen::virtual_control_button_down_func(AllegroFlare::Player* player, AllegroFlare::VirtualControllers::Base* virtual_controller, int virtual_controller_button_num, bool is_repeat)
{
   if (!(initialized))
   {
      std::stringstream error_message;
      error_message << "[Screen::virtual_control_button_down_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::virtual_control_button_down_func: error: guard \"initialized\" not met");
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
      error_message << "[Screen::virtual_control_axis_change_func]: error: guard \"initialized\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::virtual_control_axis_change_func: error: guard \"initialized\" not met");
   }
   // TODO: this function
   return;
}

ALLEGRO_FONT* Screen::obtain_font()
{
   if (!(font_bin))
   {
      std::stringstream error_message;
      error_message << "[Screen::obtain_font]: error: guard \"font_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Screen::obtain_font: error: guard \"font_bin\" not met");
   }
   return font_bin->auto_get("Inter-Regular.ttf -32");
}


} // namespace Gameplay
} // namespace AssetStudio


