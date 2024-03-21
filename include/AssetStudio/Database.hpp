#pragma once


#include <AssetStudio/Asset.hpp>
#include <AssetStudio/AssetGroup.hpp>
#include <AssetStudio/Category.hpp>
#include <map>
#include <string>
#include <vector>


namespace AssetStudio
{
   class Database
   {
   private:
      std::map<std::string, AssetStudio::Asset*> assets;
      std::vector<AssetStudio::AssetGroup*> asset_groups;
      std::vector<AssetStudio::Category*> categories;

   protected:


   public:
      Database();
      ~Database();

      void set_assets(std::map<std::string, AssetStudio::Asset*> assets);
      void set_asset_groups(std::vector<AssetStudio::AssetGroup*> asset_groups);
      void set_categories(std::vector<AssetStudio::Category*> categories);
      std::map<std::string, AssetStudio::Asset*> get_assets() const;
      std::vector<AssetStudio::AssetGroup*> get_asset_groups() const;
      std::vector<AssetStudio::Category*> get_categories() const;
   };
}



