
#include <gtest/gtest.h>

#include <AssetStudio/AssetColorProfile.hpp>


TEST(AssetStudio_AssetColorProfileTest, can_be_created_without_blowing_up)
{
   AssetStudio::AssetColorProfile asset_color_profile;
}


TEST(AssetStudio_AssetColorProfileTest, DISABLED__load_json_file__with_a_bad_json_file__will_raise_an_exception)
{
   AssetStudio::AssetColorProfile asset_color_profile;
   asset_color_profile.load_json_file("file-that-does-not-exist.json");
}


TEST(AssetStudio_AssetColorProfileTest, save_json_file__will_save_the_json_content_to_a_file)
{
   AssetStudio::AssetColorProfile asset_color_profile;
   asset_color_profile.set_bitmap_filename("zip_zaps_graphics/kit_123/foobar_bitmap.png");
   asset_color_profile.save_json_file("AssetColorProfileTest__save_json_file.json");
}


