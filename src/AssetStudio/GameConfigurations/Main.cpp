

#include <AssetStudio/GameConfigurations/Main.hpp>

#include <AllegroFlare/Achievement.hpp>
#include <AllegroFlare/DialogTree/NodeBankFactory.hpp>
#include <AllegroFlare/EventNames.hpp>
#include <AllegroFlare/GameEventDatas/AchievementUnlocked.hpp>
#include <AllegroFlare/GameProgressAndStateInfos/Base.hpp>
#include <AllegroFlare/Runners/Complete.hpp>
#include <AssetStudio/Gameplay/Level.hpp>
#include <AssetStudio/Gameplay/Screen.hpp>
#include <functional>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>


namespace AssetStudio
{
namespace GameConfigurations
{


Main::Main()
   : AllegroFlare::GameConfigurations::Complete(AssetStudio::GameConfigurations::Main::TYPE)
{
}


Main::~Main()
{
}


std::vector<std::tuple<std::string, AllegroFlare::Achievement*, bool, bool>> Main::build_achievements()
{
   return {};
}

AllegroFlare::Screens::Gameplay* Main::create_primary_gameplay_screen(AllegroFlare::Runners::Complete* runner)
{
   if (!(runner))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::GameConfigurations::Main::create_primary_gameplay_screen]: error: guard \"runner\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::GameConfigurations::Main::create_primary_gameplay_screen]: error: guard \"runner\" not met");
   }
   // TODO: Find some way to remove the Runners::Complete dependency, consider injecting
   // the bin dependencies individually into this method

   AssetStudio::Gameplay::Screen *result = new AssetStudio::Gameplay::Screen;

   result->set_font_bin(runner->get_font_bin());
   result->set_bitmap_bin(runner->get_bitmap_bin());
   result->set_model_bin(runner->get_model_bin());
   result->set_event_emitter(runner->get_event_emitter());
   result->set_game_configuration(this);

   result->initialize();
   return result;
}

std::vector<AllegroFlare::Elements::StoryboardPages::Base *> Main::create_intro_logos_storyboard_pages()
{
   //AllegroFlare::StoryboardPageFactory page_factory;
   //page_factory.set_font_bin(font_bin);
   //page_factory.set_bitmap_bin(bitmap_bin);
   //page_factory.set_model_bin(model_bin);
   //page_factory.create_clubcatt_logo_page(),
   //page_factory.create_image_page(bitmap_bin->operator[]("clubcatt-website-01.jpg")),
   return {};
}

std::vector<AllegroFlare::Elements::StoryboardPages::Base *> Main::create_intro_storyboard_pages()
{
   //AllegroFlare::Logger::throw_error(
      //"AllegroFlare::GameConfigurations::Base::create_intro_storyboard_pages",
      //"Not implemented in the base class. This method must be implemented in the derived class"
   //);
   //AllegroFlare::StoryboardPageFactory page_factory;
   //page_factory.set_font_bin(font_bin);
   //page_factory.set_bitmap_bin(bitmap_bin);
   //page_factory.set_model_bin(model_bin);

   //std::vector<AllegroFlare::Elements::StoryboardPages::Base *> result =
   //{
      //page_factory.create_image_with_advancing_text_page(
         //"storyboard-1-01-1165x500.png",
         //"Once upon a time, in a magical kingdom ruled by a wise and just queen, a young hero sets out on a "
            //"journey to prove himself and save his people from a terrible curse."
      //),
      //page_factory.create_image_with_advancing_text_page(
         //"storyboard-2-01-1165x500.png",
         //"With the help of his trusty sidekick and a band of unlikely allies, he must navigate treacherous "
            //"terrain and battle fierce foes."
      //),
      //page_factory.create_advancing_text_page(
        //"And achieve his goal to save the kingdom."
      //),
   //};
   return {};
}

std::vector<std::pair<std::string, std::string>> Main::build_title_screen_menu_options()
{
   //AllegroFlare::Logger::throw_error(
      //"AllegroFlare::GameConfigurations::Base::build_title_screen_menu_options",
         //"Not implemented in the base class. This method must be implemented in the derived class"
   //);
   std::vector<std::pair<std::string, std::string>> options = {
      //{ "Continue",          "continue_from_last_save" },       // TODO: If game session is saved and valid
      //{ "Load a Saved Game", "goto_load_a_saved_game_screen" }, // TODO: If game session is saved and valid,
                                                                // and the game supports save slots
      { "Start New Game",    "start_new_game" },                // TODO: If the game session has not begun
      //{ "Achievements",      "goto_achievements_screen" },
      //{ "Settings",          "goto_settings_screen" },
      //{ "Version",           "goto_version_screen" },
      //{ "Credits",           "goto_credits_screen" },           // TODO: If game has been won
      { "Quit",              "quit" },
   };
   return options;
}

void Main::load_audio_controller(AllegroFlare::AudioController* audio_controller)
{
   if (!(audio_controller))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::GameConfigurations::Main::load_audio_controller]: error: guard \"audio_controller\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::GameConfigurations::Main::load_audio_controller]: error: guard \"audio_controller\" not met");
   }
   // An example of how to load a sound effect track:
   audio_controller->set_and_load_sound_effect_elements({
      //{ "menu_move", { "ci-menu_move-01.ogg", false, "restart" } },
      //{ "menu_select", { "ci-menu_choice-01.ogg", false, "restart" } },
   });

   // How to play a sound effect:
   // event_emitter->emit_play_music_track_event("menu_select");

   //// An example of how to load a music track:
   //audio_controller.set_and_load_music_track_elements({
      ////{ "intro_music", { "wanderer-01.ogg", true, "ignore" } },
   //});

   // How to play a music track:
   // event_emitter->emit_play_music_track_event("intro_music");
   return;
}

void Main::load_last_played_session_or_start_new(AllegroFlare::GameSession* game_session)
{
   if (!(game_session))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::GameConfigurations::Main::load_last_played_session_or_start_new]: error: guard \"game_session\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::GameConfigurations::Main::load_last_played_session_or_start_new]: error: guard \"game_session\" not met");
   }
   // TODO: This method
   //AllegroFlare::GameProgressAndStateInfos::Base *game_progress_and_state_info =
     //game_session->get_game_progress_and_state_info();
   return;
}

void Main::setup_new_game_progress_and_state_info(AllegroFlare::GameSession* game_session)
{
   if (!(game_session))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::GameConfigurations::Main::setup_new_game_progress_and_state_info]: error: guard \"game_session\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::GameConfigurations::Main::setup_new_game_progress_and_state_info]: error: guard \"game_session\" not met");
   }
   // TODO: This method
   //AllegroFlare::Logger::throw_error(
      //"AllegroFlare::GameConfigurations::Base::setup_new_game_progress_and_state_info",
      //"Not implemented in the base class. This method must be implemented in the derived class"
   //);
   //AllegroFlare::GameProgressAndStateInfos::Base *game_progress_and_state_info =
     //game_session->get_game_progress_and_state_info();
   return;
}

std::vector<AllegroFlare::LoadASavedGame::SaveSlots::Base*> Main::build_save_slots_for_load_a_saved_game_screen()
{
   /*
   std::vector<AllegroFlare::LoadASavedGame::SaveSlots::Base*> result = {
      new AllegroFlare::LoadASavedGame::SaveSlots::Empty(), // TODO: Fill this list with items from save file
      new AllegroFlare::LoadASavedGame::SaveSlots::Empty(),
      new AllegroFlare::LoadASavedGame::SaveSlots::Empty(),
   };
   return result;
   */
   return {};
}

void Main::handle_game_event(AllegroFlare::GameEvent* game_event)
{
   //// TODO: Handle top-level game events here
   //if (game_event->is_type(AllegroFlare::GameEventDatas::ScreenActivated::NAME))
   //{
      //AllegroFlare::GameEventDatas::ScreenActivated* as =
        //static_cast<AllegroFlare::GameEventDatas::ScreenActivated*>(game_event->get_data());

      //// TODO: Handle game-specific logic for a after a screen switch
   //}
   if (game_event->get_type() == AllegroFlare::GameEventDatas::AchievementUnlocked::NAME)
   {
      if (game_event->get_data()->is_type(AllegroFlare::GameEventDatas::AchievementUnlocked::TYPE))
      {
         AllegroFlare::GameEventDatas::AchievementUnlocked *as =
            static_cast<AllegroFlare::GameEventDatas::AchievementUnlocked *>(game_event->get_data());
         // TODO: Handle saving progress of achievements. Something like below.
         // See this guide:
         // https://docs.google.com/document/d/1QdDVa6giZOmGbF61dgom1ZJ_Ev5OFvZEM2Bc453RjGw/edit
         //mark_achievement_as_unlocked_and_save_progress(as->get_achievement_identifier());
      }
      else
      {
         throw std::runtime_error("Gameplay/Runner/game_event_func: unexpected AchievementUnlocked event data type");
      }
   }
   return;
}

std::vector<std::pair<std::string, std::string>> Main::build_level_list_for_level_select_screen_by_identifier(std::string identifier)
{
   std::vector<std::pair<std::string, std::string>> result = {
      //{ "Forest Village 1", "forest_village_1" },
      //{ "Forest Village 2", "forest_village_2" },
      //{ "Forest", "forest_1" },
      //{ "Crystal Cave", "crystal_cave_1" },
      //{ "Desert Town", "desert_town_3" },
      //{ "Town 2", "town_2" },
      //{ "Cave 1", "cave_1" },
      //{ "Town 1", "town_1" },
   };
   return result;
}

AllegroFlare::DialogTree::NodeBank Main::build_dialog_bank_by_identifier(std::string identifier)
{
   // TODO: Test this contains the expected nodes
   AllegroFlare::DialogTree::NodeBank result_node_bank;

   // TODO: Consider joining the system nodes outside of the LevelFactory
   AllegroFlare::DialogTree::NodeBank system_node_bank =
      AllegroFlare::DialogTree::NodeBankFactory::build_common_system_dialogs_node_bank();
   result_node_bank.merge(&system_node_bank);

   return result_node_bank;
}

AllegroFlare::Levels::Base* Main::load_level_by_identifier(std::string identifier)
{
   // TODO: Replace void* with a better type (once the design is clear)
   AssetStudio::Gameplay::Level *result = new AssetStudio::Gameplay::Level();

   std::map<std::string, std::function<void()>> items_map = {
      { "", [](){
         AllegroFlare::Logger::warn_from(
            "AssetStudio::GameConfigurations::Main::load_level_by_identifier",
            "Loading a completely blank empty level."
         );
         // TODO: Add warning: loading an empty level
      }},
      { "forest_village_1", [](){
         //result->set_background_image_identifier("maps/forest-village-1.png");
      }},
      //{ "forest_village_2", [result](){
         //result->set_background_image_identifier("maps/forest-village-2.png");
      //}},
      //{ "forest_1", [result](){
         //result->set_background_image_identifier("maps/forest-1.png");
      //}},
      //{ "crystal_cave_1", [result](){
         //result->set_background_image_identifier("maps/crystal-cave-1.png");
      //}},
      //{ "desert_town_3", [result](){
         //result->set_background_image_identifier("maps/desert-town-3.png");
      //}},
      //{ "town_2", [result](){
         //result->set_background_image_identifier("maps/town-2.png");
      //}},
      //{ "cave_1", [result](){
         //result->set_background_image_identifier("maps/rpg-fit-backgrounds-ex-101.png");
      //}},
      //{ "town_1", [result](){
         //result->set_background_image_identifier("maps/rpg-fit-backgrounds-x2-01.png");
      //}},
   };

   // locate and call the function to handle the item
   if (items_map.count(identifier) == 0)
   {
      bool item_handled = false;
      //if (unrecognized_key_callback_func)
      //{
         //item_handled = unrecognized_key_callback_func();
      //}

      if (!item_handled)
      {
         // item not found
         std::stringstream error_message;
         error_message << "[AssetStudio::GameConfigurations::Main::load_level]: error: Cannot load the item with the identifier \""
                       << identifier << "\", it does not exist.";
         throw std::runtime_error(error_message.str());
      }
   }
   else
   {
      // call the item
      items_map[identifier]();
   }

   return result;
}


} // namespace GameConfigurations
} // namespace AssetStudio


