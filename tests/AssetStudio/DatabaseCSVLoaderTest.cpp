
#include <gtest/gtest.h>

#include <AssetStudio/DatabaseCSVLoader.hpp>


#define ASSETS_DB_CSV_FILENAME "/Users/markoates/Assets/assets_db.csv"


TEST(AssetStudio_DatabaseCSVLoaderTest, can_be_created_without_blowing_up)
{
   AssetStudio::DatabaseCSVLoader loader;
}


TEST(Robieo_CSVToLevelLoaderTest, load__will_not_blow_up)
{
   AssetStudio::DatabaseCSVLoader loader;
   loader.set_csv_full_path(ASSETS_DB_CSV_FILENAME);
   loader.load();
   SUCCEED();
}


TEST(Robieo_CSVToLevelLoaderTest, load__when_loading_from_the_source_data__will_create_the_expected_records)
{
   AssetStudio::DatabaseCSVLoader loader;
   loader.set_csv_full_path(ASSETS_DB_CSV_FILENAME);
   loader.load();

   EXPECT_EQ(true, loader.level_exists("grotto_walk"));
}


/*
TEST(Robieo_CSVToLevelLoaderTest, load__when_loading_from_the_source_data__will_load_records_with_the_expected_data)
{
   Robieo::CSVToLevelLoader loader;
   loader.set_csv_full_path(ASSETS_DB_CSV_FILENAME);
   loader.load();

   ASSERT_EQ(true, loader.level_exists("02-level-4-11"));

   Robieo::Gameplay::Level actual_level = loader.find_level("02-level-4-11");

   EXPECT_EQ("3. Forest", actual_level.get_title());
   EXPECT_EQ("level-4-13.obj", actual_level.get_world_model_obj_filename());
   EXPECT_EQ("level-4-13.png", actual_level.get_world_model_texture_filename());

   ASSERT_EQ(1, actual_level.get_tile_maps_ref().size());
   auto &tile_map = actual_level.get_tile_maps_ref()[0];
   //actual_level.get_tile_maps_ref().size());
   //EXPECT_EQ("the_cave.png", actual_level.get_tile_map_tile_elevation_bitmap_filename());
   //EXPECT_EQ("the_cave-type.png", actual_level.get_tile_map_tile_type_bitmap_filename());

   //EXPECT_EQ(AllegroFlare::Vec2D(22, 28), actual_level.get_tile_map_origin_offset());
   //EXPECT_EQ(10.0, actual_level.get_tile_map_ceiling_height());
   //EXPECT_EQ(0.0, actual_level.get_tile_map_groundlevel_height());
   //EXPECT_EQ(-2.0, actual_level.get_tile_map_floor_height());

   EXPECT_EQ("robot-holly_jolly", actual_level.get_song_to_perform_identifier());
   EXPECT_EQ(15.0, actual_level.get_song_to_perform_duration_sec());
}


TEST(Robieo_CSVToLevelLoaderTest, load__on_production_csv__will_not_blow_up)
{
   Robieo::CSVToLevelLoader loader;
   loader.set_csv_full_path(ASSETS_DB_CSV_FILENAME);
   loader.load();
   SUCCEED();
}
*/


