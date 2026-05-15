
#include <gtest/gtest.h>

#include <AssetStudio/IndexedPalette.hpp>


TEST(AssetStudio_IndexedPaletteTest, can_be_created_without_blowing_up)
{
   AssetStudio::IndexedPalette indexed_palette;
}


TEST(AssetStudio_IndexedPaletteTest, run__returns_the_expected_response)
{
   AssetStudio::IndexedPalette indexed_palette;
   std::string expected_string = "Hello World!";
   EXPECT_EQ(expected_string, indexed_palette.run());
}


