
#include <gtest/gtest.h>

#include <AssetStudio/JSONLoaders/AssetStudio/ColorFilters/General.hpp>
#include <AssetStudio/Testing/Comparison/AssetStudio/ColorFilters/General.hpp>


TEST(AssetStudio_JSONLoaders_AssetStudio_ColorFilters_GeneralTest,
   to_json__returns_the_object_as_json_with_the_expected_values)
{
   AssetStudio::ColorFilters::General general;
   nlohmann::json j = general;

   std::string expected_values =
R"({
  "hue_rotation": 0.0,
  "rgb_multiplier": 1.0,
  "saturation_multiplier": 1.0
})";

   std::string actual_values = j.dump(2);
   EXPECT_EQ(expected_values, actual_values);
}


TEST(AssetStudio_JSONLoaders_AssetStudio_ColorFilters_GeneralTest,
   from_json__loads_json_data_into_the_object)
{
   AssetStudio::ColorFilters::General general;

   std::string json =
R"({
  "hue_rotation": 0.0,
  "rgb_multiplier": 1.0,
  "saturation_multiplier": 1.0
})";

   nlohmann::json parsed_json = nlohmann::json::parse(json);
   parsed_json.get_to(general);

   AssetStudio::ColorFilters::General expected;

   EXPECT_EQ(expected, general);
}



