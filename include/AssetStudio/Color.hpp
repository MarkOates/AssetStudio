#pragma once


#include <AssetStudio/Color.hpp>
#include <allegro5/allegro.h>
#include <cstdint>
#include <tuple>


namespace AssetStudio
{
   class Color
   {
   private:

   protected:


   public:
      uint32_t id;
      ALLEGRO_COLOR al_color;
      float luminance;
      float hue;
      float saturation;
      float lightness;
      float chroma;
      Color();
      ~Color();

      static AssetStudio::Color build(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static float calculate_luminance(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static std::tuple<float, float, float> calculate_hue_saturation_lightness(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static float calculate_chroma(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
   };
}



