
#include <gtest/gtest.h>

#include <AssetStudio/Testing/Comparison/AssetStudio/ColorFilters/General.hpp>


TEST(AssetStudio_Testing_Comparison_AssetStudio_ColorFilters_GeneralTest,
   PrintTo__with_an_AssetStudio_ColorFilters_General__will_output_as_expected)
{
   std::stringstream ss;
   AssetStudio::ColorFilters::General object;

   PrintTo(object, &ss);

   std::string expected_output =
      "AssetStudio::ColorFilters::General(hue_rotation: \"0\", saturation_multiplier: \"1\", rgb_multiplier: \"1\", )";
   std::string actual_output = ss.str();
   EXPECT_EQ(expected_output, actual_output);
}


TEST(AssetStudio_Testing_Comparison_AssetStudio_ColorFilters_GeneralTest,
   equality_operator__works_with_google_test_EXPECT_statement)
{
   AssetStudio::ColorFilters::General object;
   AssetStudio::ColorFilters::General other_object;

   EXPECT_EQ(object, other_object);
}


