

#include <AssetStudio/Database.hpp>

#include <AllegroFlare/Errors.hpp>


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


bool Database::asset_exists(std::string identifier)
{
   return (assets.count(identifier) > 0);
}

AssetStudio::Asset* Database::find_asset_by_identifier(std::string identifier)
{
   if (assets.count(identifier) == 0)
   {
      AllegroFlare::Errors::throw_error(
            "AssetStudio::Database::find_asset_by_identifier",
            "No asset exists with the identifier \"" + identifier+ "\""
         );
   }
   return assets[identifier];
}

AllegroFlare::FrameAnimation::Animation* Database::find_animation_by_identifier(std::string identifier)
{
   if (!asset_exists(identifier))
   {
      AllegroFlare::Errors::throw_error(
            "AssetStudio::Database::find_animation_by_identifier",
            "No asset exists for identifier \"" + identifier+ "\" to evaluate for an animation."
         );
   }
   AssetStudio::Asset* asset = find_asset_by_identifier(identifier);
   if (!asset->animation)
   {
      AllegroFlare::Errors::throw_error(
            "AssetStudio::Database::find_animation_by_identifier",
            "The asset \"" + identifier+ "\" exists but does not contain an animation."
         );
   }
   return asset->animation;
}


} // namespace AssetStudio


