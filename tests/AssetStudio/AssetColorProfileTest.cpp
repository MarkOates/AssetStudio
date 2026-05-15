
#include <gtest/gtest.h>

#include <AssetStudio/AssetColorProfile.hpp>


TEST(AssetStudio_AssetColorProfileTest, can_be_created_without_blowing_up)
{
   AssetStudio::AssetColorProfile asset_color_profile;
}


TEST(AssetStudio_AssetColorProfileTest, run__returns_the_expected_response)
{
   AssetStudio::AssetColorProfile asset_color_profile;
   std::string expected_string = "Hello World!";
   EXPECT_EQ(expected_string, asset_color_profile.run());
}


