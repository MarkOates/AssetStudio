

#include <AssetStudio/DatabaseCSVLoader.hpp>

#include <AllegroFlare/CSVParser.hpp>
#include <AllegroFlare/FrameAnimation/SpriteSheet.hpp>
#include <AllegroFlare/Logger.hpp>
#include <AllegroFlare/UsefulPHP.hpp>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>


namespace AssetStudio
{


DatabaseCSVLoader::DatabaseCSVLoader(AllegroFlare::BitmapBin* assets_bitmap_bin)
   : AllegroFlare::CSVParser()
   , assets_bitmap_bin(assets_bitmap_bin)
   , csv_full_path("[unset-csv_full_path]")
   , levels({})
   , loaded(false)
{
}


DatabaseCSVLoader::~DatabaseCSVLoader()
{
}


void DatabaseCSVLoader::set_assets_bitmap_bin(AllegroFlare::BitmapBin* assets_bitmap_bin)
{
   this->assets_bitmap_bin = assets_bitmap_bin;
}


void DatabaseCSVLoader::set_csv_full_path(std::string csv_full_path)
{
   this->csv_full_path = csv_full_path;
}


AllegroFlare::BitmapBin* DatabaseCSVLoader::get_assets_bitmap_bin() const
{
   return assets_bitmap_bin;
}


std::string DatabaseCSVLoader::get_csv_full_path() const
{
   return csv_full_path;
}


std::map<std::string, AssetStudio::Asset*> DatabaseCSVLoader::get_levels()
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::get_levels]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::get_levels: error: guard \"loaded\" not met");
   }
   return levels;
}

bool DatabaseCSVLoader::level_exists(std::string level_identifier)
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::level_exists]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::level_exists: error: guard \"loaded\" not met");
   }
   return (levels.find(level_identifier) != levels.end());
}

int DatabaseCSVLoader::toi(std::string value)
{
   if (value.empty()) return 0;
   if (value[0] == '+') value.erase(0, 1); // Pop front on the '+' sign
   return std::atoi(value.c_str());
}

float DatabaseCSVLoader::tof(std::string value)
{
   if (value.empty()) return 0;
   if (value[0] == '+') value.erase(0, 1); // Pop front on the '+' sign
   return std::stof(value.c_str());
}

AssetStudio::Asset* DatabaseCSVLoader::find_level(std::string level_identifier)
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::find_level]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::find_level: error: guard \"loaded\" not met");
   }
   if (!(level_exists(level_identifier)))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::find_level]: error: guard \"level_exists(level_identifier)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::find_level: error: guard \"level_exists(level_identifier)\" not met");
   }
   return levels[level_identifier];
}

std::string DatabaseCSVLoader::validate_key_and_return(std::map<std::string, std::string>* extracted_row, std::string key)
{
   if (extracted_row->count(key) == 0)
   {
      std::vector<std::string> valid_keys;
      for (const auto& pair : *extracted_row) valid_keys.push_back(pair.first);

      std::stringstream ss;
      ss << "[";
      for (auto &valid_key : valid_keys)
      {
         ss << "\"" << valid_key << "\", ";
      }
      ss << "]";

      AllegroFlare::Logger::throw_error(
         "Robieo::CSVToLevelLoader::validate_key_and_return",
         "key \"" + key + "\" does not exist. The following keys are present: " + ss.str() + "."
      );
   }
   return extracted_row->operator[](key);
}

AllegroFlare::FrameAnimation::SpriteSheet* DatabaseCSVLoader::obtain_sprite_sheet(std::string filename, int cell_width, int cell_height, int sprite_sheet_scale)
{
   if (!(assets_bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::obtain_sprite_sheet]: error: guard \"assets_bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::obtain_sprite_sheet: error: guard \"assets_bitmap_bin\" not met");
   }
   // TODO: Guard after assets_bitmap_bin is initialized

   ALLEGRO_BITMAP* sprite_sheet_atlas = al_clone_bitmap(
         assets_bitmap_bin->auto_get(filename)
         //assets_bitmap_bin.auto_get("grotto_escape_pack/Base pack/graphics/player.png")
      );
   AllegroFlare::FrameAnimation::SpriteSheet *result_sprite_sheet =
      new AllegroFlare::FrameAnimation::SpriteSheet(sprite_sheet_atlas, cell_width, cell_height, sprite_sheet_scale);

   al_destroy_bitmap(sprite_sheet_atlas);

   return result_sprite_sheet;
}

std::vector<AllegroFlare::FrameAnimation::Frame> DatabaseCSVLoader::build_n_frames(uint32_t num_frames, uint32_t start_frame_num, float each_frame_duration)
{
   if (!((num_frames > 1)))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::build_n_frames]: error: guard \"(num_frames > 1)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::build_n_frames: error: guard \"(num_frames > 1)\" not met");
   }
   if (!((start_frame_num >= 0)))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::build_n_frames: error: guard \"(start_frame_num >= 0)\" not met");
   }
   if (!((each_frame_duration >= 0.0001)))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::build_n_frames: error: guard \"(each_frame_duration >= 0.0001)\" not met");
   }
   std::vector<AllegroFlare::FrameAnimation::Frame> result;
   for (uint32_t i=0; i<num_frames; i++)
   {
      result.push_back({ start_frame_num + i, each_frame_duration });
   }
   return result;
}

std::vector<AllegroFlare::FrameAnimation::Frame> DatabaseCSVLoader::build_frames_from_hash(std::string frame_data_hash)
{
   AllegroFlare::Logger::throw_error(
      "AssetStudio::DatabaseCSVLoader::build_frames_from_hash",
      "This feature is not yet supported."
   );

   std::vector<AllegroFlare::FrameAnimation::Frame> result;
   return result;
}

void DatabaseCSVLoader::load()
{
   if (!((!loaded)))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::load]: error: guard \"(!loaded)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::load: error: guard \"(!loaded)\" not met");
   }
   if (!(assets_bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[DatabaseCSVLoader::load]: error: guard \"assets_bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("DatabaseCSVLoader::load: error: guard \"assets_bitmap_bin\" not met");
   }
   // Obtain the content from the file and parse it to extractable data
   std::string content = AllegroFlare::php::file_get_contents(csv_full_path);
   if (content.empty()) throw std::runtime_error("empty file content");
   AllegroFlare::CSVParser csv_parser;
   csv_parser.set_raw_csv_content(content);
   csv_parser.parse();
   csv_parser.assemble_column_headers(3);

   // Load the parsed data to Level objects
   int first_physical_row = csv_parser.get_num_header_rows();
   int row_i = first_physical_row;
   for (std::map<std::string, std::string> &extracted_row : csv_parser.extract_all_rows())
   {
      // Extract the data here
      std::string identifier = validate_key_and_return(&extracted_row, "identifier");
      int id = toi(validate_key_and_return(&extracted_row, "id"));
      int cell_width = toi(validate_key_and_return(&extracted_row, "cell_width"));
      int cell_height = toi(validate_key_and_return(&extracted_row, "cell_height"));
      std::string image_filename = validate_key_and_return(&extracted_row, "image_filename");

      std::string frame_data__in_hash = validate_key_and_return(&extracted_row, "frame_data__in_hash");
      std::string frame_data__build_n_frames__num_frames =
         validate_key_and_return(&extracted_row, "frame_data__build_n_frames__num_frames");
      std::string frame_data__build_n_frames__start_from_frame =
         validate_key_and_return(&extracted_row, "frame_data__build_n_frames__start_from_frame");
      std::string frame_data__build_n_frames__each_frame_duration =
         validate_key_and_return(&extracted_row, "frame_data__build_n_frames__each_frame_duration");

      bool using_build_n_frames_frame_data = 
         !(
               frame_data__build_n_frames__num_frames.empty()
            && frame_data__build_n_frames__start_from_frame.empty()
            && frame_data__build_n_frames__each_frame_duration.empty()
         );
      bool using_in_hash_frame_data = !frame_data__in_hash.empty();

      std::vector<AllegroFlare::FrameAnimation::Frame> frame_data;

      if (using_build_n_frames_frame_data && using_in_hash_frame_data)
      {
         AllegroFlare::Logger::throw_error(
            "AssetStudio::DatabaseCSVLoader::load",
            "When loading row " + std::to_string(row_i) + ", both \"build_n_frames\" and \"in_hash\" sections "
               "contain data. Either one section or the other should be used, but not both."
         );
      }
      else if (!using_build_n_frames_frame_data && !using_in_hash_frame_data)
      {
         // NOTE: Assuming this is a tileset
         // TODO: Consider outputting an "info", "warning", or maybe guarding with a type==tileset or something.
         //AllegroFlare::Logger::throw_error(
            //"AssetStudio::DatabaseCSVLoader::load",
            //"When loading row " + std::to_string(row_i) + ", both \"build_n_frames\" and \"in_hash\" sections are "
               //"empty. Expecting some data there."
         //);
      }
      else if (using_build_n_frames_frame_data)
      {
         frame_data = build_n_frames(
               toi(frame_data__build_n_frames__num_frames), // TODO: Test this int
               toi(frame_data__build_n_frames__start_from_frame), // TODO: Test this int
               tof(frame_data__build_n_frames__each_frame_duration) // TODO: Test this float
            );
      }
      else if (using_in_hash_frame_data)
      {
         frame_data = build_frames_from_hash(frame_data__in_hash);
      }
      else
      {
         AllegroFlare::Logger::throw_error(
            "AssetStudio::DatabaseCSVLoader::load",
            "Weird error 2324jfgasodjifas."
         );
      }

      // Build the animation
      AllegroFlare::FrameAnimation::Animation *animation =
         new AllegroFlare::FrameAnimation::Animation(
            obtain_sprite_sheet(image_filename, cell_width, cell_height, 2),
            identifier,
            frame_data,
            AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_PING_PONG
         );

      // Load the data into the asset
      AssetStudio::Asset *asset = new AssetStudio::Asset;
      asset->id = id;
      asset->identifier = identifier;
      asset->animation = animation;

      //asset->cell_width = cell_width;
      //asset->cell_height = cell_height;
      // Build up the animation
      //asset->name = image_filename;
      //asset->description = description;

      levels.insert({ identifier, asset });
      
      /*
      // Pull out the variables
      std::string identifier =
         validate_key_and_return(&extracted_row, "identifier");
      std::string title =
         validate_key_and_return(&extracted_row, "title");
      std::string world_model_obj_filename =
         validate_key_and_return(&extracted_row, "world__model_obj_filename");
      std::string world_model_texture_filename =
         validate_key_and_return(&extracted_row, "world__model_texture_filename");
      std::string environment_model_obj_filename =
         validate_key_and_return(&extracted_row, "environment__model_obj_filename");
      std::string environment_model_texture_filename =
         validate_key_and_return(&extracted_row, "environment__model_texture_filename");

      std::string background_music_identifier =
         validate_key_and_return(&extracted_row, "background_music_identifier");
      std::string song_to_perform_identifier =
         validate_key_and_return(&extracted_row, "song_to_perform__identifier");
      float song_to_perform_duration_sec =
         tof(validate_key_and_return(&extracted_row, "song_to_perform__duration_sec"));

      float primary_light_spin =
         tof(validate_key_and_return(&extracted_row, "primary_light__spin"));
      float primary_light_tilt_time_of_day =
         tof(validate_key_and_return(&extracted_row, "primary_light__tilt_time_of_day"));



      // Pass along the variables to the result object
      Robieo::Gameplay::Level level;
      level.set_title(title);

      level.set_world_model_obj_filename(world_model_obj_filename);
      level.set_world_model_texture_filename(world_model_texture_filename);


      if (!environment_model_obj_filename.empty())
      {
         AllegroFlare::Logger::info_from(
            "Robieo::CSVToLevelLoader::load",
            "environment obj model for level detected: \"" + environment_model_obj_filename + "\""
         );
         level.set_environment_model_obj_filename(environment_model_obj_filename);
         level.set_environment_model_texture_filename(environment_model_texture_filename);
      }



      {
      level.get_tile_maps_ref().push_back({});
      auto &tile_map = level.get_tile_maps_ref().back();

      std::string tile_map_tile_elevation_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_ground_floor__tile_elevation_bitmap_filename");
      std::string tile_map_tile_type_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_ground_floor__tile_type_bitmap_filename");
      //std::cout << "tile_map_tile_elevation_bitmap_filename: " << tile_map_tile_elevation_bitmap_filename << std::endl;
      //std::cout << "tile_map_tile_type_bitmap_filename: " << tile_map_tile_type_bitmap_filename << std::endl;

      int tile_map_origin_offset_x = toi(validate_key_and_return(&extracted_row, "tile_map_ground_floor__origin_offset__x"));
      int tile_map_origin_offset_y = toi(validate_key_and_return(&extracted_row, "tile_map_ground_floor__origin_offset__y"));
      float tile_map_ceiling_height = tof(validate_key_and_return(&extracted_row, "tile_map_ground_floor__ceiling_height"));
      float tile_map_groundlevel_height = tof(validate_key_and_return(&extracted_row, "tile_map_ground_floor__groundlevel_height"));
      float tile_map_floor_height = tof(validate_key_and_return(&extracted_row, "tile_map_ground_floor__floor_height"));

      tile_map.set_tile_elevation_bitmap_filename(tile_map_tile_elevation_bitmap_filename);
      tile_map.set_tile_type_bitmap_filename(tile_map_tile_type_bitmap_filename);
      tile_map.set_origin_offset({ (float)tile_map_origin_offset_x, (float)tile_map_origin_offset_y });
      tile_map.set_ceiling_height(tile_map_ceiling_height);
      tile_map.set_groundlevel_height(tile_map_groundlevel_height);
      tile_map.set_floor_height(tile_map_floor_height);
      }





      {
        //int num = 1;
      //level.get_tile_maps_ref().push_back({});
      //auto &tile_map = level.get_tile_maps_ref()[0];

      std::string tile_map_tile_elevation_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_floor2__tile_elevation_bitmap_filename");
      std::string tile_map_tile_type_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_floor2__tile_type_bitmap_filename");

      //std::cout << "tile_map_tile_elevation_bitmap_filename: " << tile_map_tile_elevation_bitmap_filename << std::endl;
      //std::cout << "tile_map_tile_type_bitmap_filename: " << tile_map_tile_type_bitmap_filename << std::endl;

         // TODO: Better validation
         if (!tile_map_tile_elevation_bitmap_filename.empty())
         {

         level.get_tile_maps_ref().push_back({});
         auto &tile_map = level.get_tile_maps_ref().back();
         int tile_map_origin_offset_x = toi(validate_key_and_return(&extracted_row, "tile_map_floor2__origin_offset__x"));
         int tile_map_origin_offset_y = toi(validate_key_and_return(&extracted_row, "tile_map_floor2__origin_offset__y"));
         float tile_map_ceiling_height = tof(validate_key_and_return(&extracted_row, "tile_map_floor2__ceiling_height"));
         float tile_map_groundlevel_height = tof(validate_key_and_return(&extracted_row, "tile_map_floor2__groundlevel_height"));
         float tile_map_floor_height = tof(validate_key_and_return(&extracted_row, "tile_map_floor2__floor_height"));

         tile_map.set_tile_elevation_bitmap_filename(tile_map_tile_elevation_bitmap_filename);
         tile_map.set_tile_type_bitmap_filename(tile_map_tile_type_bitmap_filename);
         tile_map.set_origin_offset({ (float)tile_map_origin_offset_x, (float)tile_map_origin_offset_y });
         tile_map.set_ceiling_height(tile_map_ceiling_height);
         tile_map.set_groundlevel_height(tile_map_groundlevel_height);
         tile_map.set_floor_height(tile_map_floor_height);
         }
      }




      {
        //int num = 1;
      //level.get_tile_maps_ref().push_back({});
      //auto &tile_map = level.get_tile_maps_ref()[0];

      std::string tile_map_tile_elevation_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_basement1__tile_elevation_bitmap_filename");
      std::string tile_map_tile_type_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_basement1__tile_type_bitmap_filename");

      //std::cout << "tile_map_tile_elevation_bitmap_filename: " << tile_map_tile_elevation_bitmap_filename << std::endl;
      //std::cout << "tile_map_tile_type_bitmap_filename: " << tile_map_tile_type_bitmap_filename << std::endl;

         // TODO: Better validation
         if (!tile_map_tile_elevation_bitmap_filename.empty())
         {

         level.get_tile_maps_ref().push_back({});
         auto &tile_map = level.get_tile_maps_ref().back();
         int tile_map_origin_offset_x = toi(validate_key_and_return(&extracted_row, "tile_map_basement1__origin_offset__x"));
         int tile_map_origin_offset_y = toi(validate_key_and_return(&extracted_row, "tile_map_basement1__origin_offset__y"));
         float tile_map_ceiling_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement1__ceiling_height"));
         float tile_map_groundlevel_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement1__groundlevel_height"));
         float tile_map_floor_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement1__floor_height"));

         tile_map.set_tile_elevation_bitmap_filename(tile_map_tile_elevation_bitmap_filename);
         tile_map.set_tile_type_bitmap_filename(tile_map_tile_type_bitmap_filename);
         tile_map.set_origin_offset({ (float)tile_map_origin_offset_x, (float)tile_map_origin_offset_y });
         tile_map.set_ceiling_height(tile_map_ceiling_height);
         tile_map.set_groundlevel_height(tile_map_groundlevel_height);
         tile_map.set_floor_height(tile_map_floor_height);
         }
      }




      {
        //int num = 1;
      //level.get_tile_maps_ref().push_back({});
      //auto &tile_map = level.get_tile_maps_ref()[0];

      std::string tile_map_tile_elevation_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_basement2__tile_elevation_bitmap_filename");
      std::string tile_map_tile_type_bitmap_filename =
         validate_key_and_return(&extracted_row, "tile_map_basement2__tile_type_bitmap_filename");

      //std::cout << "tile_map_tile_elevation_bitmap_filename: " << tile_map_tile_elevation_bitmap_filename << std::endl;
      //std::cout << "tile_map_tile_type_bitmap_filename: " << tile_map_tile_type_bitmap_filename << std::endl;

         // TODO: Better validation
         if (!tile_map_tile_elevation_bitmap_filename.empty())
         {

         level.get_tile_maps_ref().push_back({});
         auto &tile_map = level.get_tile_maps_ref().back();
         int tile_map_origin_offset_x = toi(validate_key_and_return(&extracted_row, "tile_map_basement2__origin_offset__x"));
         int tile_map_origin_offset_y = toi(validate_key_and_return(&extracted_row, "tile_map_basement2__origin_offset__y"));
         float tile_map_ceiling_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement2__ceiling_height"));
         float tile_map_groundlevel_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement2__groundlevel_height"));
         float tile_map_floor_height = tof(validate_key_and_return(&extracted_row, "tile_map_basement2__floor_height"));

         tile_map.set_tile_elevation_bitmap_filename(tile_map_tile_elevation_bitmap_filename);
         tile_map.set_tile_type_bitmap_filename(tile_map_tile_type_bitmap_filename);
         tile_map.set_origin_offset({ (float)tile_map_origin_offset_x, (float)tile_map_origin_offset_y });
         tile_map.set_ceiling_height(tile_map_ceiling_height);
         tile_map.set_groundlevel_height(tile_map_groundlevel_height);
         tile_map.set_floor_height(tile_map_floor_height);
         }
      }





      //level.set_tile_elevation_bitmap_filename(tile_map_tile_elevation_bitmap_filename);
      //level.set_tile_map_tile_type_bitmap_filename(tile_map_tile_type_bitmap_filename);
      //level.set_tile_map_origin_offset({ (float)tile_map_origin_offset_x, (float)tile_map_origin_offset_y });
      //level.set_tile_map_ceiling_height(tile_map_ceiling_height);
      //level.set_tile_map_groundlevel_height(tile_map_groundlevel_height);
      //level.set_tile_map_floor_height(tile_map_floor_height);

      level.set_primary_light_spin(primary_light_spin);
      level.set_primary_light_tilt_time_of_day(primary_light_tilt_time_of_day);


      level.set_background_music_identifier(background_music_identifier);
      level.set_song_to_perform_identifier(song_to_perform_identifier);
      level.set_song_to_perform_duration_sec(song_to_perform_duration_sec);

      levels.insert({ identifier, level });

      */
      row_i++;
   }

   loaded = true;
   return;
}


} // namespace AssetStudio


