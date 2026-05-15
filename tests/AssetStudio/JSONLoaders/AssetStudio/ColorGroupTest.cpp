
#include <gtest/gtest.h>

#include <AssetStudio/JSONLoaders/AssetStudio/ColorGroup.hpp>
#include <AssetStudio/Testing/Comparison/AssetStudio/ColorGroup.hpp>


TEST(AssetStudio_JSONLoaders_AssetStudio_ColorGroupTest,
   to_json__returns_the_object_as_json_with_the_expected_values)
{
   AssetStudio::ColorGroup color_group;
   nlohmann::json j = color_group;

   std::string expected_values =
R"({
  "color_ids": [],
  "general_filter": {
    "hue_rotation": 0.0,
    "rgb_multiplier": 1.0,
    "saturation_multiplier": 1.0
  }
})";

   std::string actual_values = j.dump(2);
   EXPECT_EQ(expected_values, actual_values);
}


TEST(AssetStudio_JSONLoaders_AssetStudio_ColorGroupTest,
   from_json__loads_json_data_into_the_object)
{
   AssetStudio::ColorGroup color_group;

   std::string json =
R"({
  "color_ids": [1, 4, 5],
  "general_filter": {
    "hue_rotation": 0.0,
    "rgb_multiplier": 1.0,
    "saturation_multiplier": 1.0
  }
})";

   nlohmann::json parsed_json = nlohmann::json::parse(json);
   parsed_json.get_to(color_group);

   AssetStudio::ColorGroup expected;
   expected.color_ids = { 1, 4, 5 };

   //// TODO: add comparison
   EXPECT_EQ(expected, color_group);
}



