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

      void set_bitmap_filename(std::string bitmap_filename);
      void set_color_groups(std::vector<AssetStudio::ColorGroup> color_groups);
      std::string get_bitmap_filename() const;
      std::vector<AssetStudio::ColorGroup> get_color_groups() const;
      void save_json_file(std::string file_path=DEFAULT_ARGUMENT_FILE_PATH);
      void load_json_file(std::string file_path=DEFAULT_ARGUMENT_FILE_PATH);
   };
}



