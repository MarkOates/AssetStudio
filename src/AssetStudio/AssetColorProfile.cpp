

#include <AssetStudio/AssetColorProfile.hpp>

#include <AllegroFlare/Logger.hpp>
#include <AllegroFlare/UsefulPHP.hpp>
#include <AssetStudio/Filesystem.hpp>
#include <AssetStudio/JSONLoaders/AssetStudio/ColorGroup.hpp>
#include <iostream>
#include <lib/nlohmann/json.hpp>
#include <sstream>
#include <stdexcept>


namespace AssetStudio
{


AssetColorProfile::AssetColorProfile()
   : bitmap_filename("[unset-filename]")
   , color_groups()
{
}


AssetColorProfile::~AssetColorProfile()
{
}


void AssetColorProfile::set_bitmap_filename(std::string bitmap_filename)
{
   this->bitmap_filename = bitmap_filename;
}


void AssetColorProfile::set_color_groups(std::vector<AssetStudio::ColorGroup> color_groups)
{
   this->color_groups = color_groups;
}


std::string AssetColorProfile::get_bitmap_filename() const
{
   return bitmap_filename;
}


std::vector<AssetStudio::ColorGroup> AssetColorProfile::get_color_groups() const
{
   return color_groups;
}


void AssetColorProfile::save_json_file(std::string file_path)
{
   if (!(file_path != DEFAULT_ARGUMENT_FILE_PATH))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::AssetColorProfile::save_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::AssetColorProfile::save_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met");
   }
   if (AssetStudio::Filesystem::exists_as_directory(file_path))
   {
      AllegroFlare::Logger::throw_error(
         THIS_CLASS_AND_METHOD_NAME,
         "Cannot save the json file named \"" + file_path + "\". The location already exists as a folder."
      );
   }

   nlohmann::json j;
   j["color_groups"] = color_groups;
   j["bitmap_filename"] = bitmap_filename;

   std::string contents = j.dump(3);

   AllegroFlare::php::file_put_contents(file_path, contents);

   return;
}

void AssetColorProfile::load_json_file(std::string file_path)
{
   if (!(file_path != DEFAULT_ARGUMENT_FILE_PATH))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::AssetColorProfile::load_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::AssetColorProfile::load_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met");
   }
   if (!AssetStudio::Filesystem::exists_as_file(file_path))
   {
      AllegroFlare::Logger::throw_missing_file_error(
         THIS_CLASS_AND_METHOD_NAME,
         file_path
      );
   }

   std::string file_content = AllegroFlare::php::file_get_contents(file_path);
   nlohmann::json j;

   try
   {
      j = nlohmann::json::parse(file_content);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_missing_file_error(
         THIS_CLASS_AND_METHOD_NAME,
         "Exception caught when trying to load \"" + file_path + "\": " + e.what()
      );
   }

      //color_groups = nlohmann::json::parse(file_content);

   return;
}


} // namespace AssetStudio


