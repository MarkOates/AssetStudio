

#include <AssetStudio/Database.hpp>




namespace AssetStudio
{


Database::Database()
   : assets()
   , asset_groups()
   , categories()
{
}


Database::~Database()
{
}


void Database::set_assets(std::map<std::string, AssetStudio::Asset*> assets)
{
   this->assets = assets;
}


void Database::set_asset_groups(std::vector<AssetStudio::AssetGroup*> asset_groups)
{
   this->asset_groups = asset_groups;
}


void Database::set_categories(std::vector<AssetStudio::Category*> categories)
{
   this->categories = categories;
}


std::map<std::string, AssetStudio::Asset*> Database::get_assets() const
{
   return assets;
}


std::vector<AssetStudio::AssetGroup*> Database::get_asset_groups() const
{
   return asset_groups;
}


std::vector<AssetStudio::Category*> Database::get_categories() const
{
   return categories;
}




} // namespace AssetStudio


