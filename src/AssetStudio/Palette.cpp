

#include <AssetStudio/Palette.hpp>

#include <AssetStudio/Color.hpp>
#include <AssetStudio/Comparison/ALLEGRO_COLOR.hpp>
#include <algorithm>
#include <allegro5/allegro.h>
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
   , sorting(Sorting::UNDEF)
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

   uint32_t id = 1;
   for (auto &raw_color : result.raw_colors)
   {
      result.colors.push_back(AssetStudio::Color::build(raw_color.first));
      result.colors.back().id = id;
      id++;
   }

   al_unlock_bitmap(bitmap);

   // NOTE: Palette is implicitly ordered by reverse-luminance (from the Comparison/ALLEGRO_COLOR header). You might
   // consider ordering differently.

   return result;
}

std::pair<AssetStudio::IndexedBitmap, AssetStudio::Palette> Palette::build_indexed_bitmap_and_palette(ALLEGRO_BITMAP* bitmap)
{
   if (!(bitmap))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::build_indexed_bitmap_and_palette]: error: guard \"bitmap\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::build_indexed_bitmap_and_palette]: error: guard \"bitmap\" not met");
   }
   if (!(al_get_current_display()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::build_indexed_bitmap_and_palette]: error: guard \"al_get_current_display()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::build_indexed_bitmap_and_palette]: error: guard \"al_get_current_display()\" not met");
   }
   std::pair<AssetStudio::IndexedBitmap, AssetStudio::Palette> result_;
   AssetStudio::Palette &result = result_.second;
   AssetStudio::IndexedBitmap &result_bitmap = result_.first;

   int width = al_get_bitmap_width(bitmap);
   int height = al_get_bitmap_height(bitmap);
   result_bitmap.width = width;
   result_bitmap.height = height;
   result_bitmap.pixels.resize(width * height);

   std::map<ALLEGRO_COLOR, uint16_t> color_to_index;
   uint16_t next_id = 0;

   al_lock_bitmap(bitmap, ALLEGRO_PIXEL_FORMAT_ANY, ALLEGRO_LOCK_READONLY);

   for (int y = 0; y < height; y++)
   {
      for (int x = 0; x < width; x++)
      {
         ALLEGRO_COLOR pixel = al_get_pixel(bitmap, x, y);
         
         //  Check if color exists in our temporary map
         auto it = color_to_index.find(pixel);
         if (it == color_to_index.end())
         {
             // New color
             color_to_index[pixel] = next_id;
             result_bitmap.pixels[x + y * width] = next_id;
             
             // Store in palette result
             AssetStudio::Color new_color = AssetStudio::Color::build(pixel);
             new_color.id = next_id;
             result.colors.push_back(new_color);
             
             next_id++;
         }
         else
         {
             // Existing color
             result_bitmap.pixels[x + y * width] = it->second;
         }
         
         // Maintain initial list
         result.raw_colors[pixel]++;
      }
   }

   al_unlock_bitmap(bitmap);
   return result_;
}

void Palette::draw(uint32_t picked_id)
{
   if (!(al_is_primitives_addon_initialized()))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Palette::draw]: error: guard \"al_is_primitives_addon_initialized()\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Palette::draw]: error: guard \"al_is_primitives_addon_initialized()\" not met");
   }
   // TODO: guard for al_draw_text

   float frame_stroke_thickness = 2.0f;
   float o = 0.5;
   ALLEGRO_COLOR frame_color_a{o, o, o, o};
   ALLEGRO_COLOR frame_color_b{0, 0, 0, o};
   ALLEGRO_COLOR text_color{1, 1, 1, 1};

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
      //if (font) al_draw_textf(font, text_color, x1, y1, 0, "%d", color.id);
      if (picked_id != 0 && color.id == picked_id)
      {
         float s = frame_stroke_thickness;
         al_draw_rectangle(x1-s*0, y1-s*0, x2+s*0, y2+s*0, frame_color_a, s);
         al_draw_rectangle(x1-s*1, y1-s*1, x2+s*1, y2+s*1, frame_color_b, s);
      }

      column++;
      if (column > columns)
      {
         column = 0;
         row++;
      }
   }
   return;
}

uint32_t Palette::find_index_by_color(ALLEGRO_COLOR al_color)
{
   for (auto &color : colors) if (color.al_color == al_color) return color.id;
   return 0;
}

void Palette::sort_by_luminance()
{
   std::sort(colors.begin(), colors.end(), compare_by_luminance);
   sorting = Sorting::LUMINANCE;
   return;
}

void Palette::sort_by_id()
{
   std::sort(colors.begin(), colors.end(), compare_by_id);
   sorting = Sorting::ID;
   return;
}

bool Palette::compare_by_luminance(AssetStudio::Color& a, AssetStudio::Color& b)
{
   if (a.luminance != b.luminance) return a.luminance > b.luminance;
   return std::tie(a.al_color.r, a.al_color.g, a.al_color.b, a.al_color.a)
      > std::tie(b.al_color.r, b.al_color.g, b.al_color.b, b.al_color.a);
}

bool Palette::compare_by_id(AssetStudio::Color& a, AssetStudio::Color& b)
{
   // id should always be unique. If not, there's a problem.
   return a.id > b.id;
}


} // namespace AssetStudio


