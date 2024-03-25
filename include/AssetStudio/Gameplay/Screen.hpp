#pragma once


#include <AllegroFlare/BitmapBin.hpp>
#include <AllegroFlare/EventEmitter.hpp>
#include <AllegroFlare/FontBin.hpp>
#include <AllegroFlare/FrameAnimation/Frame.hpp>
#include <AllegroFlare/FrameAnimation/SpriteSheet.hpp>
#include <AllegroFlare/GameEvent.hpp>
#include <AllegroFlare/ModelBin.hpp>
#include <AllegroFlare/Placement2D.hpp>
#include <AllegroFlare/Player.hpp>
#include <AllegroFlare/Screens/Gameplay.hpp>
#include <AllegroFlare/VirtualControllers/Base.hpp>
#include <AssetStudio/Database.hpp>
#include <AssetStudio/GameConfigurations/Main.hpp>
#include <AssetStudio/Gameplay/Level.hpp>
#include <allegro5/allegro.h>
#include <cstdint>
#include <string>
#include <vector>


namespace AssetStudio
{
   namespace Gameplay
   {
      class Screen : public AllegroFlare::Screens::Gameplay
      {
      public:
         static constexpr char* TYPE = (char*)"AssetStudio/Gameplay/Screen";

      private:
         AllegroFlare::EventEmitter* event_emitter;
         AllegroFlare::BitmapBin* bitmap_bin;
         AllegroFlare::FontBin* font_bin;
         AllegroFlare::ModelBin* model_bin;
         AllegroFlare::BitmapBin assets_bitmap_bin;
         AssetStudio::Database database;
         ALLEGRO_BITMAP* sprite_sheet_atlas;
         AllegroFlare::FrameAnimation::SpriteSheet* sprite_sheet;
         AssetStudio::GameConfigurations::Main* game_configuration;
         AllegroFlare::Placement2D scrollarea_placement;
         std::string current_level_identifier;
         AssetStudio::Gameplay::Level* current_level;
         bool initialized;

      protected:


      public:
         Screen(AllegroFlare::EventEmitter* event_emitter=nullptr, AllegroFlare::BitmapBin* bitmap_bin=nullptr, AllegroFlare::FontBin* font_bin=nullptr, AllegroFlare::ModelBin* model_bin=nullptr, AllegroFlare::BitmapBin assets_bitmap_bin={}, AssetStudio::GameConfigurations::Main* game_configuration=nullptr);
         virtual ~Screen();

         void set_game_configuration(AssetStudio::GameConfigurations::Main* game_configuration);
         AssetStudio::GameConfigurations::Main* get_game_configuration() const;
         void set_event_emitter(AllegroFlare::EventEmitter* event_emitter=nullptr);
         void set_bitmap_bin(AllegroFlare::BitmapBin* bitmap_bin=nullptr);
         void set_font_bin(AllegroFlare::FontBin* font_bin=nullptr);
         void set_model_bin(AllegroFlare::ModelBin* model_bin=nullptr);
         virtual void load_level_by_identifier(std::string level_identifier="[unset-level_identifier]") override;
         void initialize();
         std::vector<AllegroFlare::FrameAnimation::Frame> build_n_frames(uint32_t num_frames=1, uint32_t start_frame_num=0, float each_frame_duration=0.08f);
         AllegroFlare::FrameAnimation::SpriteSheet* obtain_sprite_sheet(std::string filename="[unset-filename]", int cell_width=16, int cell_height=16, int sprite_sheet_scale=2);
         std::string infer_asssets_folder_location();
         void load_database_from_csv();
         void load_database_and_build_assets();
         virtual void on_activate() override;
         virtual void on_deactivate() override;
         void update();
         void render();
         virtual void game_event_func(AllegroFlare::GameEvent* game_event=nullptr) override;
         virtual void primary_update_func(double time_now=0.0f, double delta_time=1.0f) override;
         virtual void primary_render_func() override;
         virtual void key_char_func(ALLEGRO_EVENT* ev=nullptr) override;
         virtual void virtual_control_button_up_func(AllegroFlare::Player* player=nullptr, AllegroFlare::VirtualControllers::Base* virtual_controller=nullptr, int virtual_controller_button_num=0, bool is_repeat=false) override;
         virtual void virtual_control_button_down_func(AllegroFlare::Player* player=nullptr, AllegroFlare::VirtualControllers::Base* virtual_controller=nullptr, int virtual_controller_button_num=0, bool is_repeat=false) override;
         virtual void virtual_control_axis_change_func(ALLEGRO_EVENT* ev=nullptr) override;
         ALLEGRO_FONT* obtain_font();
         ALLEGRO_FONT* obtain_font_for_asset_identifier();
         ALLEGRO_FONT* obtain_small_font();
      };
   }
}



