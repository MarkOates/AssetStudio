

#include <AssetStudio/AssetColorProfile.hpp>

#include <AllegroFlare/Logger.hpp>
#include <AllegroFlare/UsefulPHP.hpp>
#include <AssetStudio/Filesystem.hpp>
#include <AssetStudio/JSONLoaders/AssetStudio/ColorGroup.hpp>
#include <iostream>
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


void AssetColorProfile::load_from_json_file(std::string file_path)
{
   if (!(file_path != DEFAULT_ARGUMENT_FILE_PATH))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::AssetColorProfile::load_from_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::AssetColorProfile::load_from_json_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met");
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


