
#include <gtest/gtest.h>

#include <AssetStudio/Testing/Comparison/AssetStudio/ColorGroup.hpp>


TEST(AssetStudio_Testing_Comparison_AssetStudio_ColorGroupTest,
   PrintTo__with_a_ColorGroup__will_output_as_expected)
{
   std::stringstream ss;
   AssetStudio::ColorGroup object;

   PrintTo(object, &ss);

   std::string expected_output = "ColorGroup(color_ids: \"\", )";
   std::string actual_output = ss.str();
   EXPECT_EQ(expected_output, actual_output);
}


TEST(AssetStudio_Testing_Comparison_AssetStudio_ColorGroupTest,
   equality_operator__works_with_google_test_EXPECT_statement)
{
   AssetStudio::ColorGroup object;
   AssetStudio::ColorGroup other_object;

   EXPECT_EQ(object, other_object);
}


