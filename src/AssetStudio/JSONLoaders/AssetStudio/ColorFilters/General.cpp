

#include <AssetStudio/JSONLoaders/AssetStudio/ColorFilters/General.hpp>


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
   j.at("hue_rotation").get_to(v.hue_rotation);
   j.at("saturation_multiplier").get_to(v.saturation_multiplier);
   j.at("rgb_multiplier").get_to(v.rgb_multiplier);
}


} // namespace AssetStudio::ColorFilters



