

#include <AssetStudio/Palette.hpp>

#include <AssetStudio/Color.hpp>
#include <AssetStudio/Comparison/ALLEGRO_COLOR.hpp>
#include <allegro5/allegro_primitives.h>
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace AssetStudio
{


AssetStudio::Color Palette::dummy_color = AssetStudio::Color::build(ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});


Palette::Palette()
   : raw_colors()
   , colors()
   , tags(PropertyTags::UNDEF)
{
}


Palette::~Palette()
{
}


AssetStudio::Palette Palette::build(ALLEGRO_BITMAP* bitmap)
{
   if (!(bitmap))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::build]: error: guard \"bitmap\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::build]: error: guard \"bitmap\" not met");
   }
   if (!(al_get_current_display()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::build]: error: guard \"al_get_current_display()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::build]: error: guard \"al_get_current_display()\" not met");
   }
   AssetStudio::Palette result;
   ALLEGRO_COLOR pixel;

   al_lock_bitmap(bitmap, ALLEGRO_PIXEL_FORMAT_ANY, ALLEGRO_LOCK_READONLY);
   int width = al_get_bitmap_width(bitmap);
   int height = al_get_bitmap_height(bitmap);

   for (int y=0; y<height; y++)
   {
      for (int x=0; x<width; x++)
      {
         pixel = al_get_pixel(bitmap, x, y);
         result.raw_colors[pixel]++;
      }
   }

   for (auto &raw_color : result.raw_colors)
   {
      result.colors.push_back(AssetStudio::Color::build(raw_color.first));
   }

   al_unlock_bitmap(bitmap);

   return result;
}

void Palette::draw()
{
   if (!(al_is_primitives_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::draw]: error: guard \"al_is_primitives_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::draw]: error: guard \"al_is_primitives_addon_initialized()\" not met");
   }
   int x = 0;
   int y = 0;
   int columns = 6;
   int spacing_x = 20;
   int spacing_y = 20;
   int box_w = 18;
   int box_h = 18;

   int column = 0;
   int row = 0;

   for (auto &color : colors)
   {
      int x1 = x + spacing_x * column;
      int y1 = y + spacing_y * row;
      int x2 = x1 + box_w;
      int y2 = y1 + box_h;

      al_draw_filled_rectangle(x1, y1, x2, y2, color.al_color);

      column++;
      if (column > columns)
      {
         column = 0;
         row++;
      }
   }
   return;
}

bool Palette::sort_by_luminance(AssetStudio::Color& color_a, AssetStudio::Color& color_b)
{
   // TODO
   return true;
}


} // namespace AssetStudio


