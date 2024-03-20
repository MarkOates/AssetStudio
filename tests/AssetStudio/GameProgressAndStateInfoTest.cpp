
#include <gtest/gtest.h>

#include <AssetStudio/GameProgressAndStateInfo.hpp>


TEST(AssetStudio_GameProgressAndStateInfoTest, can_be_created_without_blowing_up)
{
   AssetStudio::GameProgressAndStateInfo game_progress_and_state_info;
}


TEST(AssetStudio_GameProgressAndStateInfoTest, TYPE__has_the_expected_value)
{
   EXPECT_STREQ(
     "AssetStudio/GameProgressAndStateInfo",
     AssetStudio::GameProgressAndStateInfo::TYPE
   );
}


TEST(AssetStudio_GameProgressAndStateInfoTest, type__has_the_expected_value_matching_TYPE)
{
   AssetStudio::GameProgressAndStateInfo game_progress_and_state_info;
   EXPECT_EQ(AssetStudio::GameProgressAndStateInfo::TYPE, game_progress_and_state_info.get_type());
}


