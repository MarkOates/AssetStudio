#pragma once


#include <AssetStudio/Palette.hpp>
#include <allegro5/allegro.h>
#include <map>


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
      std::map<ALLEGRO_COLOR, int> colors;
      AssetStudio::Palette::PropertyTags tags;

   protected:


   public:
      Palette();
      ~Palette();

      static AssetStudio::Palette build(ALLEGRO_BITMAP* bitmap=nullptr);
      void draw();
   };
}



