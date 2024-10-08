

#include <AssetStudio/DatabaseCSVLoader.hpp>

#include <AllegroFlare/CSVParser.hpp>
#include <AllegroFlare/FrameAnimation/SpriteSheet.hpp>
#include <AllegroFlare/FrameAnimation/SpriteStripAssembler.hpp>
#include <AllegroFlare/Logger.hpp>
#include <AllegroFlare/UsefulPHP.hpp>
#include <algorithm>
#include <cstdlib>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>


namespace AssetStudio
{


DatabaseCSVLoader::DatabaseCSVLoader(AllegroFlare::BitmapBin* assets_bitmap_bin)
   : AllegroFlare::CSVParser()
   , assets_bitmap_bin(assets_bitmap_bin)
   , csv_full_path("[unset-csv_full_path]")
   , assets({})
   , sprite_sheets({})
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


std::map<std::string, AssetStudio::Asset*> DatabaseCSVLoader::get_assets()
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::get_assets]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::get_assets]: error: guard \"loaded\" not met");
   }
   return assets;
}

bool DatabaseCSVLoader::level_exists(std::string level_identifier)
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::level_exists]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::level_exists]: error: guard \"loaded\" not met");
   }
   return (assets.find(level_identifier) != assets.end());
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

std::vector<std::string> DatabaseCSVLoader::comma_separated_quoted_strings_to_vector_of_strings(std::string comma_separated_quoted_strings)
{
   std::vector<std::string> result;
   std::stringstream ss(comma_separated_quoted_strings);
   std::string current_element;
   bool in_quotes = false;

   // Parse the CSV list character by character
   for (char ch : comma_separated_quoted_strings)
   {
      if (ch == '"')
      {
         // Toggle quotes state
         in_quotes = !in_quotes;
      }
      else if (ch == ',' && !in_quotes)
      {
         // Found a comma outside quotes, push the current element
         result.push_back(current_element);
         current_element.clear(); // Reset for the next element
      }
      else if (in_quotes)
      {
         current_element += ch;
      }
   }

   // Push the last element if it's not empty
   if (!current_element.empty())
   {
      result.push_back(current_element);
   }

   return result;
}

std::vector<std::string> DatabaseCSVLoader::comma_separated_strings_to_vector_of_strings(std::string comma_separated_strings)
{
   // NOTE: Does not account for nested strings
   return tokenize(comma_separated_strings, ',');
}

std::pair<bool, uint32_t> DatabaseCSVLoader::str_to_playmode(std::string playmode_string)
{
   if (playmode_string == "once")
   {
      return { true, AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE };
   }
   else if (playmode_string == "loop")
   {
      return { true, AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_LOOP };
   }
   else if (playmode_string == "ping_pong_forward")
   {
      return { true, AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_PING_PONG };
   }

   return { false, 0 };
}

AssetStudio::Asset* DatabaseCSVLoader::find_level(std::string level_identifier)
{
   if (!(loaded))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::find_level]: error: guard \"loaded\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::find_level]: error: guard \"loaded\" not met");
   }
   if (!(level_exists(level_identifier)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::find_level]: error: guard \"level_exists(level_identifier)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::find_level]: error: guard \"level_exists(level_identifier)\" not met");
   }
   return assets[level_identifier];
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

AllegroFlare::FrameAnimation::SpriteSheet* DatabaseCSVLoader::create_sprite_sheet_from_individual_images(std::vector<std::string> individual_frame_image_filenames, int cell_width, int cell_height, int sprite_sheet_scale)
{
   if (!(assets_bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::create_sprite_sheet_from_individual_images]: error: guard \"assets_bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::create_sprite_sheet_from_individual_images]: error: guard \"assets_bitmap_bin\" not met");
   }
   if (!((!individual_frame_image_filenames.empty())))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::create_sprite_sheet_from_individual_images]: error: guard \"(!individual_frame_image_filenames.empty())\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::create_sprite_sheet_from_individual_images]: error: guard \"(!individual_frame_image_filenames.empty())\" not met");
   }
   // TODO: Consider caching the created result_sprite_sheet;

   std::vector<ALLEGRO_BITMAP*> bitmaps;
   for (auto &individual_frame_image_filename : individual_frame_image_filenames)
   {
      bitmaps.push_back(assets_bitmap_bin->auto_get(individual_frame_image_filename));
   }

   AllegroFlare::FrameAnimation::SpriteStripAssembler sprite_strip_assembler;
   sprite_strip_assembler.set_bitmaps(bitmaps);
   sprite_strip_assembler.assemble();
   ALLEGRO_BITMAP* sprite_strip = sprite_strip_assembler.get_sprite_strip();

   // Given the newly assembled sprite_strip (aka atlas), build the sprite_sheet
   AllegroFlare::FrameAnimation::SpriteSheet *result_sprite_sheet =
      new AllegroFlare::FrameAnimation::SpriteSheet(sprite_strip, cell_width, cell_height, sprite_sheet_scale);

   // Cleanup
   al_destroy_bitmap(sprite_strip);
   // Cleanup the individual frame images in the bin here
   for (auto &individual_frame_image_filename : individual_frame_image_filenames)
   {
      // TODO: This could wierdly clobber, consider checking all the image frames do *not* already exist in the
      // bin at the beginning of the method before continuing.
      assets_bitmap_bin->destroy(individual_frame_image_filename);
   }

   return result_sprite_sheet;
}

AllegroFlare::FrameAnimation::SpriteSheet* DatabaseCSVLoader::obtain_sprite_sheet(std::string filename, int cell_width, int cell_height, int sprite_sheet_scale)
{
   if (!(assets_bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::obtain_sprite_sheet]: error: guard \"assets_bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::obtain_sprite_sheet]: error: guard \"assets_bitmap_bin\" not met");
   }
   // TODO: Guard after assets_bitmap_bin is initialized

   //std::map<std::tuple<filename, int, int, int>, AllegroFlare::FrameAnimation::SpriteSheet*> cache;
   std::tuple<std::string, int, int, int> sprite_sheet_key(filename, cell_width, cell_height, sprite_sheet_scale);
   if (sprite_sheets.find(sprite_sheet_key) == sprite_sheets.end())
   {
      // Create sprite sheet
      ALLEGRO_BITMAP* sprite_sheet_atlas = al_clone_bitmap(
            assets_bitmap_bin->auto_get(filename)
         );
      AllegroFlare::FrameAnimation::SpriteSheet *result_sprite_sheet =
         new AllegroFlare::FrameAnimation::SpriteSheet(sprite_sheet_atlas, cell_width, cell_height, sprite_sheet_scale);

      al_destroy_bitmap(sprite_sheet_atlas);

      // Add the sprite sheet to the list of sprite sheets
      sprite_sheets[sprite_sheet_key] = result_sprite_sheet;
   }

   return sprite_sheets[sprite_sheet_key];

   //ALLEGRO_BITMAP* sprite_sheet_atlas = al_clone_bitmap(
         //assets_bitmap_bin->auto_get(filename)
         ////assets_bitmap_bin.auto_get("grotto_escape_pack/Base pack/graphics/player.png")
      //);
   //AllegroFlare::FrameAnimation::SpriteSheet *result_sprite_sheet =
      //new AllegroFlare::FrameAnimation::SpriteSheet(sprite_sheet_atlas, cell_width, cell_height, sprite_sheet_scale);

   //al_destroy_bitmap(sprite_sheet_atlas);

   //return result_sprite_sheet;
}

std::vector<AllegroFlare::FrameAnimation::Frame> DatabaseCSVLoader::build_n_frames(uint32_t num_frames, uint32_t start_frame_num, float each_frame_duration)
{
   if (!((num_frames >= 1)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(num_frames >= 1)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(num_frames >= 1)\" not met");
   }
   if (!((start_frame_num >= 0)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(start_frame_num >= 0)\" not met");
   }
   if (!((each_frame_duration >= 0.0001)))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::build_n_frames]: error: guard \"(each_frame_duration >= 0.0001)\" not met");
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
      error_message << "[AssetStudio::DatabaseCSVLoader::load]: error: guard \"(!loaded)\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::load]: error: guard \"(!loaded)\" not met");
   }
   if (!(assets_bitmap_bin))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::DatabaseCSVLoader::load]: error: guard \"assets_bitmap_bin\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::DatabaseCSVLoader::load]: error: guard \"assets_bitmap_bin\" not met");
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
   // TODO: Report hidden assets at end of loading process
   std::set<std::string> hidden_assets;
   for (std::map<std::string, std::string> &extracted_row : csv_parser.extract_all_rows())
   {
      std::string visibility = validate_key_and_return(&extracted_row, "visibility");
      std::string identifier = validate_key_and_return(&extracted_row, "identifier");

      // Skip over "hidden" assets
      if (visibility == "hidden")
      {
         // Store the hidden asset identifier to report at the end what assets are hidden for debugging
         hidden_assets.insert(identifier);
         continue;
      }

      // Extract the data here
      //std::string identifier = validate_key_and_return(&extracted_row, "identifier");
      //std::string status = validate_key_and_return(&extracted_row, "status");
      std::string asset_pack_identifier = validate_key_and_return(&extracted_row, "asset_pack_identifier");
      std::string intra_pack_identifier = validate_key_and_return(&extracted_row, "intra_pack_identifier");
      int id = toi(validate_key_and_return(&extracted_row, "id"));
      int cell_width = toi(validate_key_and_return(&extracted_row, "cell_width"));
      int cell_height = toi(validate_key_and_return(&extracted_row, "cell_height"));
      //std::string image_filename = validate_key_and_return(&extracted_row, "image_filename");
      std::string playmode = validate_key_and_return(&extracted_row, "playmode");
      std::string type = validate_key_and_return(&extracted_row, "type");
      float align_x = toi(validate_key_and_return(&extracted_row, "align_x"));
      float align_y = toi(validate_key_and_return(&extracted_row, "align_y"));
      float anchor_x = toi(validate_key_and_return(&extracted_row, "anchor_x"));
      float anchor_y = toi(validate_key_and_return(&extracted_row, "anchor_y"));

      std::string image_filename = validate_key_and_return(&extracted_row, "image_filename");
      std::string images_list_raw = validate_key_and_return(&extracted_row, "images_list");



      // Load the frame data

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



      // Load the image (or images) data

      std::string full_path_to_image_file = "[unprocessed]";
      AllegroFlare::FrameAnimation::SpriteSheet* sprite_sheet = nullptr;
      bool using_single_image_file = false;
      int sprite_sheet_scale = 2;

      if (image_filename.empty() && images_list_raw.empty())
      {
         AllegroFlare::Logger::throw_error(
            "AssetStudio::DatabaseCSVLoader::load",
            "foofoo231"
         );
      }
      else if (!image_filename.empty() && !images_list_raw.empty())
      {
         AllegroFlare::Logger::throw_error(
            "AssetStudio::DatabaseCSVLoader::load",
            "foofoo456"
         );
      }
      else if (!image_filename.empty())
      {
         full_path_to_image_file = asset_pack_identifier + "/extracted/" + image_filename;

         sprite_sheet = obtain_sprite_sheet(full_path_to_image_file, cell_width, cell_height, sprite_sheet_scale);
         using_single_image_file = true;
      }
      else if (!images_list_raw.empty())
      {
         // TODO: Handle this case:
         // TODO: Split
         //std::string full_path_to_image_file = asset_pack_identifier + "/extracted/" + image_filename;
         std::vector<std::string> images_list = comma_separated_strings_to_vector_of_strings(images_list_raw);

         //std::cout << "*** images_list detected ***" << std::endl;
         //std::cout << "  - images_list.size(): " << images_list.size() << std::endl;
         //std::cout << "  - frame_data.size(): " << frame_data.size() << std::endl;
         //std::cout << "  - images_list_raw: ###" << images_list_raw << "###" << std::endl;

         if (images_list.size() != frame_data.size())
         {
            AllegroFlare::Logger::throw_error(
               "AssetStudio::DatabaseCSVLoader::load",
               "When processing asset \"" + identifier + "\", the number of images in "
                  "the \"images_list\" (" + std::to_string(images_list.size()) + ") was not the same as the "
                  "\"frame_data\"'s \"num_frames\" "
                  "(" + std::to_string(frame_data.size()) + ")"
            );
         }

         //AllegroFlare::Logger::warn_from(
            //"AssetStudio::DatabaseCSVLoader::load",
            //"When processing asset \"" + identifier + "\", an \"images_list\" was supplied. This feature is "
               //"not yet implemented (you should add it in now, tho). For now, skipping this asset."
         //);

         // Build the extended path_to_image_file
         for (auto &image_list_item : images_list)
         {
            image_list_item = asset_pack_identifier + "/extracted/" + image_list_item;
         }

         sprite_sheet = create_sprite_sheet_from_individual_images(
               images_list,
               cell_width,
               cell_height,
               sprite_sheet_scale
            );
         using_single_image_file = false;
         //continue;
           //asset_pack_identifier + "/extracted/" + image_filename;
         //AllegroFlare::Logger::throw_error(
            //"AssetStudio::DatabaseCSVLoader::load",
            //"foofoo2"
         //);
      }
      //std::string full_path_to_image_file = asset_pack_identifier + "/extracted/" + image_filename;



      // Parse the "playmode"

      std::pair<bool, uint32_t> playmode_parsed_data =
            { true, AllegroFlare::FrameAnimation::Animation::PLAYMODE_FORWARD_ONCE };

      if (!playmode.empty())
      {
         playmode_parsed_data = str_to_playmode(playmode);
      }
      //else
      //{
         std::cout << "- identifier: \"" << identifier << "\"" << std::endl;
         std::cout << "    playmode: \"" << playmode << "\" -> " << playmode_parsed_data.second << std::endl;
      //}

      if (playmode_parsed_data.first == false)
      {
         AllegroFlare::Logger::throw_error(
            "AssetStudio::DatabaseCSVLoader::load",
            "Unrecognized playmode \"" + playmode + "\" when loading row " + std::to_string(row_i) + "."
         );
      }


      // Build the sprite sheet
      //AllegroFlare::FrameAnimation::SpriteSheet* sprite_sheet =
         //obtain_sprite_sheet(full_path_to_image_file, cell_width, cell_height, 2);

      // Build the animation
      AllegroFlare::FrameAnimation::Animation *animation =
         new AllegroFlare::FrameAnimation::Animation(
            sprite_sheet,
            identifier,
            frame_data,
            playmode_parsed_data.second
         );

      // Load the data into the asset
      AssetStudio::Asset *asset = new AssetStudio::Asset;
      asset->id = id;
      asset->identifier = identifier;
      asset->animation = animation;
      asset->cell_width = cell_width;
      asset->cell_height = cell_height;
      asset->align_x = align_x;
      asset->align_y = align_y;
      asset->anchor_x = anchor_x;
      asset->anchor_y = anchor_y;
      asset->asset_pack_identifier= asset_pack_identifier;
      asset->intra_pack_identifier= intra_pack_identifier;
      asset->type = type;

      assets.insert({ asset->identifier, asset });

      // If it's an "icon_set", then also build unique assets for each icon
      int icon_id = 1;
      if (type == "icon_set")
      {
         std::cout << "Building \"icon_set\" for \"" << identifier << "\"" << std::endl;
         //ALLEGRO_BITMAP *get_cell(int index);
         //ALLEGRO_BITMAP *get_atlas();
         //int get_num_sprites();

         for (int i=0; i<sprite_sheet->get_num_sprites(); i++)
         {
            std::string icon_identifier = identifier + "-icon_" + std::to_string(icon_id);
            // TODO: See if icon_identifier clashes

            AssetStudio::Asset *icon_asset = new AssetStudio::Asset;
            icon_asset->id = id + i + 10000; // TODO: Figure out some way to create unique names and ids from icons
            icon_asset->identifier = icon_identifier;
            //icon_asset->animation = animation;
            icon_asset->bitmap = sprite_sheet->get_cell(i);
            icon_asset->cell_width = cell_width;
            icon_asset->cell_height = cell_height;
            icon_asset->type = "icon";

            assets.insert({ icon_asset->identifier, icon_asset });

            icon_id++;
         }
      }
      
      //ALLEGRO_BITMAP *get_cell(int index);
      //ALLEGRO_BITMAP *get_atlas();
      //int get_num_sprites();
      
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

      assets.insert({ identifier, level });

      */
      row_i++;
   }

   loaded = true;
   return;
}

std::vector<std::string> DatabaseCSVLoader::split(std::string string, char delimiter)
{
   std::vector<std::string> elems;
   auto result = std::back_inserter(elems);
   std::stringstream ss(string);
   std::string item;
   while (std::getline(ss, item, delimiter)) { *(result++) = item; }
   return elems;
}

std::vector<std::string> DatabaseCSVLoader::tokenize(std::string str, char delim)
{
   std::vector<std::string> tokens = split(str, delim);
   for (auto &token : tokens) token = trim(token);
   return tokens;
}

std::string DatabaseCSVLoader::trim(std::string s)
{
   // ltrim
   s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int c) {return !std::isspace(c);}));
   // rtrim
   s.erase(std::find_if(s.rbegin(), s.rend(), [](int c) {return !std::isspace(c);}).base(), s.end());
   return s;
}


} // namespace AssetStudio


