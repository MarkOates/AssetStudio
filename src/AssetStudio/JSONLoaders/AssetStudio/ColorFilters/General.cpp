

#include <AssetStudio/JSONLoaders/AssetStudio/ColorFilters/General.hpp>
#include <AllegroFlare/Logger.hpp>


namespace AssetStudio::ColorFilters
{


void to_json(nlohmann::json& j, const General& v)
{
   j = nlohmann::json{
      { "hue_rotation", v.hue_rotation },
      { "saturation_multiplier", v.saturation_multiplier},
      { "rgb_multiplier", v.rgb_multiplier},
   };
}

void from_json(const nlohmann::json& j, General& v)
{
   try
   {
      j.at("hue_rotation").get_to(v.hue_rotation);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_error(
         "AssetStudio::JSONLoaders::AssetStudio::ColorFilters::General::from_json",
         "When attempting to parse the key \"hue_rotation\", this error thrown by nlohmann::json: \""
            + std::string(e.what()) + "\"."
      );
   }

   try
   {
      j.at("saturation_multiplier").get_to(v.saturation_multiplier);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_error(
         "AssetStudio::JSONLoaders::AssetStudio::ColorFilters::General::from_json",
         "When attempting to parse the key \"saturation_multiplier\", this error thrown by nlohmann::json: \""
            + std::string(e.what()) + "\"."
      );
   }

   try
   {
      j.at("rgb_multiplier").get_to(v.rgb_multiplier);
   }
   catch (std::exception &e)
   {
      AllegroFlare::Logger::throw_error(
         "AssetStudio::JSONLoaders::AssetStudio::ColorFilters::General::from_json",
         "When attempting to parse the key \"rgb_multiplier\", this error thrown by nlohmann::json: \""
            + std::string(e.what()) + "\"."
      );
   }
}


} // namespace AssetStudio::ColorFilters



