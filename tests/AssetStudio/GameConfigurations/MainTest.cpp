
#include <gtest/gtest.h>

#include <AssetStudio/GameConfigurations/Main.hpp>


TEST(AssetStudio_GameConfigurations_MainTest, can_be_created_without_blowing_up)
{
   AssetStudio::GameConfigurations::Main main_configuration;
}


TEST(AssetStudio_GameConfigurations_MainTest, load_level_by_identifier__will_not_blow_up)
{
   AssetStudio::GameConfigurations::Main main_configuration;
   AllegroFlare::Levels::Base* level = main_configuration.load_level_by_identifier("forest_village_1");
   EXPECT_NE(nullptr, level);
}


