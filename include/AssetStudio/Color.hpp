#pragma once


#include <allegro5/allegro.h>
#include <tuple>


namespace AssetStudio
{
   class Color
   {
   private:

   protected:


   public:
      ALLEGRO_COLOR al_color;
      float luminance;
      float hue;
      float saturation;
      float lightness;
      float chroma;
      Color();
      ~Color();

      void build(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static float calculate_luminance(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static std::tuple<float, float, float> calculate_hue_saturation_lightness(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
      static float calculate_chroma(ALLEGRO_COLOR al_color=ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0});
   };
}



