#pragma once


#include <AssetStudio/Color.hpp>
#include <AssetStudio/Palette.hpp>
#include <allegro5/allegro.h>
#include <map>
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
      void draw();
      static bool sort_by_luminance(AssetStudio::Color& a=dummy_color, AssetStudio::Color& b=dummy_color);
   };
}



