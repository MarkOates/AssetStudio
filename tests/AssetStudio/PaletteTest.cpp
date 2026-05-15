
#include <gtest/gtest.h>

#include <AssetStudio/Palette.hpp>
#include <AllegroFlare/Testing/WithAllegroRenderingFixture.hpp>
#include <AllegroFlare/Testing/WithInteractionFixture.hpp>
#include <allegro5/allegro_color.h>
#include <allegro5/allegro_primitives.h>



class AssetStudio_PaletteTestWithAllegroRenderingFixture : public AllegroFlare::Testing::WithAllegroRenderingFixture {};
class AssetStudio_PaletteWithInteractionFixture : public AllegroFlare::Testing::WithInteractionFixture {};


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
   //std::string bitmap_identifier = "sprite_strip_images/robo-soldier3.png";
   std::string bitmap_identifier = "storyboard-1-01-1165x500.png";
   ALLEGRO_BITMAP *bitmap = bitmap_bin[bitmap_identifier];

   AssetStudio::Palette palette = AssetStudio::Palette::build(bitmap);

   AllegroFlare::Placement2D bitmap_placement;
   bitmap_placement.position.x = 1920/3*2;
   bitmap_placement.position.y = 1080/2;
   bitmap_placement.size.x = al_get_bitmap_width(bitmap);
   bitmap_placement.size.y = al_get_bitmap_height(bitmap);
   bitmap_placement.align.x = 0.5;
   bitmap_placement.align.y = 0.5;
   bitmap_placement.scale.x = 1;
   bitmap_placement.scale.y = 1;

   AllegroFlare::Placement2D palette_placement;
   palette_placement.position.x = 1920/5;
   palette_placement.position.y = 1080/2;
   palette_placement.size.x = 120;
   palette_placement.size.y = 100;
   palette_placement.align.x = 0.5;
   palette_placement.align.y = 0.5;
   palette_placement.scale.x = 1;
   palette_placement.scale.y = 1;

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


TEST_F(AssetStudio_PaletteWithInteractionFixture, FOCUS__CAPTURE__will_work_with_the_expected_context)
{
   ALLEGRO_COLOR clear_color = al_color_html("#777777");
   ALLEGRO_FONT *font = get_small_font();

   // Remove ALLEGRO_MAG_LINEAR flag (so zooming does not blur)
   al_set_new_bitmap_flags(al_get_new_bitmap_flags() & ~ALLEGRO_MAG_LINEAR);

   AllegroFlare::BitmapBin &bitmap_bin = get_bitmap_bin_ref();
   //std::string bitmap_identifier = "sprite_strip_images/robo-soldier3.png";
   std::string bitmap_identifier = "storyboard-1-01-1165x500.png";
   ALLEGRO_BITMAP *bitmap = bitmap_bin[bitmap_identifier];
   ALLEGRO_BITMAP *paletted_bitmap_result = nullptr;

   std::pair<AssetStudio::IndexedBitmap, AssetStudio::Palette> indexed_bitmap_and_palette =
      AssetStudio::Palette::build_indexed_bitmap_and_palette(bitmap);
   auto &indexed_bitmap = indexed_bitmap_and_palette.first;
   auto &palette = indexed_bitmap_and_palette.second;

   AllegroFlare::Placement2D bitmap_placement;
   bitmap_placement.position.x = 1920/3*2;
   bitmap_placement.position.y = 1080/8*2;
   bitmap_placement.size.x = al_get_bitmap_width(bitmap);
   bitmap_placement.size.y = al_get_bitmap_height(bitmap);
   bitmap_placement.align.x = 0.5;
   bitmap_placement.align.y = 0.5;
   bitmap_placement.scale.x = 1;
   bitmap_placement.scale.y = 1;

   AllegroFlare::Placement2D bitmap2_placement;
   bitmap2_placement.position.x = 1920/3*2;
   bitmap2_placement.position.y = 1080/8*6;
   bitmap2_placement.size.x = al_get_bitmap_width(bitmap);
   bitmap2_placement.size.y = al_get_bitmap_height(bitmap);
   bitmap2_placement.align.x = 0.5;
   bitmap2_placement.align.y = 0.5;
   bitmap2_placement.scale.x = 1;
   bitmap2_placement.scale.y = 1;

   AllegroFlare::Placement2D palette_placement;
   palette_placement.position.x = 1920/5;
   palette_placement.position.y = 1080/2;
   palette_placement.size.x = 120;
   palette_placement.size.y = 300;
   palette_placement.align.x = 0.5;
   palette_placement.align.y = 0.5;
   palette_placement.scale.x = 2;
   palette_placement.scale.y = 2;

   struct PickInfo
   {
      bool valid = false;
      ALLEGRO_COLOR color;
      int x = 0;
      int y = 0;
      uint32_t palette_index = 0; 
   };

   std::function<PickInfo(ALLEGRO_BITMAP*, AllegroFlare::Placement2D&, float, float)> pick_color =
      [](ALLEGRO_BITMAP *bitmap, AllegroFlare::Placement2D &placement, float xx, float yy){
         PickInfo result;

         int bitmap_width = al_get_bitmap_width(bitmap);
         int bitmap_height = al_get_bitmap_height(bitmap);
         placement.transform_coordinates(&xx, &yy);
         int x = (int)xx;
         int y = (int)yy;

         result.x = x;
         result.y = y;

         if (x < 0 || y < 0 || x >= bitmap_width || y >= bitmap_height)
         {
            result.valid = false;
            return result;
         }

         result.valid = true;
         result.color = al_get_pixel(bitmap, x, y);

         return result;
      };

   std::function<uint32_t(AssetStudio::Palette&, ALLEGRO_COLOR)> find_color_index =
     [](AssetStudio::Palette &palette, ALLEGRO_COLOR color){
        return palette.find_index_by_color(color);
     };

   //
   // UI
   //

   AllegroFlare::Vec2D mouse_position = { 1020./2, 1080./2 };
   AllegroFlare::Vec2D mouse_position_on_bitmap = {};
   PickInfo mouse_over_color, picked_color;
  

   while(interactive_test_wait_for_event())
   {
      ALLEGRO_EVENT &current_event = *interactive_test_get_current_event();

      switch(current_event.type)
      {
         case ALLEGRO_EVENT_TIMER: {
            //
            // Update

            //mouse_position_on_bitmap = mouse_position;
            //bitmap_placement.transform_coordinates(&mouse_position_on_bitmap.x, &mouse_position_on_bitmap.y);

            //
            // Draw
            //
            clear_with_color(clear_color);

            // Draw the image (bitmap1)
            bitmap_placement.start_transform();
            al_draw_bitmap(bitmap, 0, 0, 0);
            bitmap_placement.restore_transform();

            // Draw the image (bitmap2)
            if (paletted_bitmap_result)
            {
               bitmap2_placement.start_transform();
               al_draw_bitmap(paletted_bitmap_result, 0, 0, 0);
               bitmap2_placement.restore_transform();
            }

            // Draw the palette
            palette_placement.start_transform();
            palette.draw(picked_color.palette_index, font);
            palette_placement.restore_transform();

            // Draw the UI
            draw_crosshair(mouse_position.x, mouse_position.y);
            draw_crosshair_blue(mouse_position_on_bitmap.x, mouse_position_on_bitmap.y);
         
            if (mouse_over_color.valid)
            {
               al_draw_filled_rectangle(20, 20, 60, 60, mouse_over_color.color);
            }
            if (picked_color.valid)
            {
               al_draw_filled_rectangle(20, 20+100, 80, 80+100, picked_color.color);
               al_draw_textf(font, ALLEGRO_COLOR{1, 1, 1, 1}, 20, 20+100, 0, "%d", picked_color.palette_index);
            }

            //
            // Finish Drawing
            //
            interactive_test_render_status();
            al_flip_display();
         } break;

         //// For example:
         //case ALLEGRO_FLARE_EVENT_PLAY_SOUND_EFFECT:
         //{
            //std::cout << "[AllegroFlare_Elements_MultiListTestWithAllegroRenderingFixture]: INFO: "
                      //<< "Play sound effect event was emitted. "
                      //<< std::endl;
         //}
         //break;

         case ALLEGRO_EVENT_MOUSE_AXES: {
            int x = current_event.mouse.x;
            int y = current_event.mouse.y;

            mouse_position.x = x;
            mouse_position.y = y;

            // Update the mouse position, and the position on the bitmap
            mouse_position_on_bitmap = mouse_position;
            bitmap_placement.transform_coordinates(&mouse_position_on_bitmap.x, &mouse_position_on_bitmap.y);

            // Refresh the "picked color"
            mouse_over_color =
               pick_color(bitmap, bitmap_placement, mouse_position_on_bitmap.x, mouse_position_on_bitmap.y);

            mouse_over_color.palette_index = find_color_index(palette, mouse_over_color.color);
         } break;

         case ALLEGRO_EVENT_MOUSE_BUTTON_DOWN: {
            if (mouse_over_color.valid)
            {
               picked_color = mouse_over_color;

               /*
               if (paletted_bitmap_result)
               {
                  al_destroy_bitmap(paletted_bitmap_result);
                  paletted_bitmap_result = nullptr;
               }

               paletted_bitmap_result = AssetStudio::Palette::create_bitmap_from_indexed_bitmap_and_palette(
                  &indexed_bitmap,
                  &palette
               );
               */

               /*
               // Build (or rebuild) the result bitmap
               if (paletted_bitmap_result)
               {
                  al_destroy_bitmap(paletted_bitmap_result);
                  paletted_bitmap_result = nullptr;
               }


               paletted_bitmap_result = AssetStudio::Palette::create_bitmap_from_indexed_bitmap_and_palette(
                  &indexed_bitmap,
                  &palette
               );
               */
            }
         } break;

         case ALLEGRO_EVENT_KEY_DOWN: {
            bool shift = current_event.keyboard.modifiers & ALLEGRO_KEYMOD_SHIFT;
            bool option = current_event.keyboard.modifiers & ALLEGRO_KEYMOD_ALT;
            bool command = current_event.keyboard.modifiers & ALLEGRO_KEYMOD_COMMAND;

            bool palette_modified = false;

            if (shift && option && command)
            {
               switch(current_event.keyboard.keycode)
               {
                  case ALLEGRO_KEY_1: { // Dial 1, counter-clockwise
                     if (!picked_color.valid) break;
                     auto &color = *palette.find_color_by_index(picked_color.palette_index);
                     color.rotate_hue(-1./64);
                     palette_modified = true;
                  } break;
                  case ALLEGRO_KEY_2: { // Dial 1, clockwise
                     if (!picked_color.valid) break;
                     auto &color = *palette.find_color_by_index(picked_color.palette_index);
                     color.rotate_hue(1./64);
                     palette_modified = true;
                  } break;
               }
            }

            if (palette_modified)
            {
               if (paletted_bitmap_result)
               {
                  al_destroy_bitmap(paletted_bitmap_result);
                  paletted_bitmap_result = nullptr;
               }

               paletted_bitmap_result = AssetStudio::Palette::create_bitmap_from_indexed_bitmap_and_palette(
                  &indexed_bitmap,
                  &palette
               );
            }
         } break;
      }
   }

   // Cleanup
   if (paletted_bitmap_result)
   {
      al_destroy_bitmap(paletted_bitmap_result);
      paletted_bitmap_result = nullptr;
   }
}


