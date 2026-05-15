
#include <gtest/gtest.h>

#include <AssetStudio/ColorStudio.hpp>


TEST(AssetStudio_ColorStudioTest, can_be_created_without_blowing_up)
{
   AssetStudio::ColorStudio color_studio;
}


TEST(AssetStudio_ColorStudioTest, run__returns_the_expected_response)
{
   AssetStudio::ColorStudio color_studio;
   std::string expected_string = "Hello World!";
   EXPECT_EQ(expected_string, color_studio.run());
}


