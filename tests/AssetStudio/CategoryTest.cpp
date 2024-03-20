
#include <gtest/gtest.h>

#include <AssetStudio/Category.hpp>


TEST(AssetStudio_CategoryTest, can_be_created_without_blowing_up)
{
   AssetStudio::Category category;
}


TEST(AssetStudio_CategoryTest, run__returns_the_expected_response)
{
   AssetStudio::Category category;
   std::string expected_string = "Hello World!";
   EXPECT_EQ(expected_string, category.run());
}


