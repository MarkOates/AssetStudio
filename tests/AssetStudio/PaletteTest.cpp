
#include <gtest/gtest.h>

#include <AssetStudio/Palette.hpp>
#include <AllegroFlare/Testing/WithAllegroRenderingFixture.hpp>
#include <allegro5/allegro_color.h>



class AssetStudio_PaletteTestWithAllegroRenderingFixture
   : public AllegroFlare::Testing::WithAllegroRenderingFixture
{};


TEST(AssetStudio_PaletteTest, can_be_created_without_blowing_up)
{
   AssetStudio::Palette palette;
}


TEST_F(AssetStudio_PaletteTestWithAllegroRenderingFixture, CAPTURE__build__builds_a_palette_from_a_bitap)
{
   ALLEGRO_COLOR clear_color = al_color_html("#777777");

   // Remove ALLEGRO_MAG_LINEAR flag (so zooming does not blur)
   al_set_new_bitmap_flags(al_get_new_bitmap_flags() & ~ALLEGRO_MAG_LINEAR);

   AllegroFlare::BitmapBin &bitmap_bin = get_bitmap_bin_ref();
   std::string bitmap_identifier = "sprite_strip_images/robo-soldier3.png";
   ALLEGRO_BITMAP *bitmap = bitmap_bin[bitmap_identifier];

   AssetStudio::Palette palette = AssetStudio::Palette::build(bitmap);

   AllegroFlare::Placement2D bitmap_placement;
   bitmap_placement.position.x = 1920/3*2;
   bitmap_placement.position.y = 1080/2;
   bitmap_placement.size.x = al_get_bitmap_width(bitmap);
   bitmap_placement.size.y = al_get_bitmap_width(bitmap);
   bitmap_placement.align.x = 0.5;
   bitmap_placement.align.y = 0.5;
   bitmap_placement.scale.x = 8;
   bitmap_placement.scale.y = 8;

   AllegroFlare::Placement2D palette_placement;
   palette_placement.position.x = 1920/3;
   palette_placement.position.y = 1080/2;
   palette_placement.size.x = 120;
   palette_placement.size.y = 100;
   palette_placement.align.x = 0.5;
   palette_placement.align.y = 0.5;
   palette_placement.scale.x = 2;
   palette_placement.scale.y = 2;

   //
   // Render
   //

   // Setup
   clear_with_color(clear_color);

   // Draw the image
   bitmap_placement.start_transform();
   al_draw_bitmap(bitmap, 0, 0, 0);
   bitmap_placement.restore_transform();

   // Draw the palette
   palette_placement.start_transform();
   palette.draw();
   palette_placement.restore_transform();

   // Flip
   al_flip_display();
   al_rest(2);
}


