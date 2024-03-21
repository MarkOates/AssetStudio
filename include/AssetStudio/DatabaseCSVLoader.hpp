#pragma once


#include <AllegroFlare/BitmapBin.hpp>
#include <AllegroFlare/CSVParser.hpp>
#include <AssetStudio/Asset.hpp>
#include <map>
#include <string>


namespace AssetStudio
{
   class DatabaseCSVLoader : public AllegroFlare::CSVParser
   {
   private:
      AllegroFlare::BitmapBin* assets_bitmap_bin;
      std::string csv_full_path;
      std::map<std::string, AssetStudio::Asset*> levels;
      bool loaded;

   protected:


   public:
      DatabaseCSVLoader(AllegroFlare::BitmapBin* assets_bitmap_bin=nullptr);
      ~DatabaseCSVLoader();

      void set_assets_bitmap_bin(AllegroFlare::BitmapBin* assets_bitmap_bin);
      void set_csv_full_path(std::string csv_full_path);
      AllegroFlare::BitmapBin* get_assets_bitmap_bin() const;
      std::string get_csv_full_path() const;
      std::map<std::string, AssetStudio::Asset*> get_levels();
      bool level_exists(std::string level_identifier="[unset-level_identifier]");
      static int toi(std::string value="[unset-value]");
      static float tof(std::string value="[unset-value]");
      AssetStudio::Asset* find_level(std::string level_identifier="[unset-level_identifier]");
      static std::string validate_key_and_return(std::map<std::string, std::string>* extracted_row=nullptr, std::string key="[unset-key]");
      void load();
   };
}



