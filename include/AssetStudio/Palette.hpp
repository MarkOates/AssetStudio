#pragma once


#include <AssetStudio/Color.hpp>
#include <AssetStudio/IndexedBitmap.hpp>
#include <AssetStudio/Palette.hpp>
#include <allegro5/allegro.h>
#include <cstdint>
#include <map>
#include <utility>
#include <vector>


namespace AssetStudio
{
   class Palette
   {
   private:
      enum class PropertyTags
      {
         UNDEF = 0,
         HAS_ALPHA,
      };
      enum class Sorting
      {
         UNDEF = 0,
         ID,
         LUMINANCE,
      };
      std::map<ALLEGRO_COLOR, int> raw_colors;
      std::vector<AssetStudio::Color> colors;
      AssetStudio::Palette::Sorting sorting;
      AssetStudio::Palette::PropertyTags tags;
      static AssetStudio::Color dummy_color;

   protected:


   public:
      Palette();
      ~Palette();

      static AssetStudio::Palette build(ALLEGRO_BITMAP* bitmap=nullptr);
      static std::pair<AssetStudio::Palette, AssetStudio::IndexedBitmap> build_indexted_bitmap_and_palette(ALLEGRO_BITMAP* bitmap=nullptr);
      void draw(uint32_t picked_id=0);
      uint32_t find_index_by_color(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      void sort_by_luminance();
      void sort_by_id();
      static bool compare_by_luminance(AssetStudio::Color& a=dummy_color, AssetStudio::Color& b=dummy_color);
      static bool compare_by_id(AssetStudio::Color& a=dummy_color, AssetStudio::Color& b=dummy_color);
   };
}



