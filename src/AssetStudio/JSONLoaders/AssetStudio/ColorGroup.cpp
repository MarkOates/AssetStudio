

#include <AssetStudio/JSONLoaders/AssetStudio/ColorGroup.hpp>
#include <AssetStudio/JSONLoaders/AssetStudio/ColorFilters/General.hpp>
#include <AllegroFlare/Logger.hpp>


namespace AssetStudio
{


void to_json(nlohmann::json& j, const ColorGroup& object)
{
   j = nlohmann::json{
      { "color_ids", object.color_ids },
      { "general_filter", object.general_filter },
   };
}

void from_json(const nlohmann::json& j, ColorGroup& object)
{
   try
   {
      j.at("color_ids").get_to(object.color_ids);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_error(
         "AssetStudio::JSONLoaders::AssetStudio::ColorGroup::from_json",
         "When attempting to parse the key \"color_ids\", this error thrown by nlohmann::json: \""
            + std::string(e.what()) + "\"."
      );
   }

   try
   {
      j.at("general_filter").get_to(object.general_filter);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_error(
         "AssetStudio::JSONLoaders::AssetStudio::ColorGroup::from_json",
         "When attempting to parse the key \"general_filter\", this error thrown by nlohmann::json: \""
            + std::string(e.what()) + "\"."
      );
   }
}


} // namespace AssetStudio



