#pragma once


#include <AssetStudio/ColorGroup.hpp>
#include <string>
#include <vector>


namespace AssetStudio
{
   class AssetColorProfile
   {
   public:
      static constexpr const char* DEFAULT_ARGUMENT_FILE_PATH = "[unset-file_path]";

   private:
      std::string bitmap_filename;
      std::vector<AssetStudio::ColorGroup> color_groups;

   protected:


   public:
      AssetColorProfile();
      ~AssetColorProfile();

      void load_from_json_file(std::string file_path=DEFAULT_ARGUMENT_FILE_PATH);
   };
}



