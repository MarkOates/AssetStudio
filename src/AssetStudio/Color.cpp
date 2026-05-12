

#include <AssetStudio/Color.hpp>

#include <algorithm>
#include <allegro5/allegro_color.h>


namespace AssetStudio
{


Color::Color()
   : id(0)
   , al_color(ALLEGRO_COLOR{0.5, 0.5, 0.5, 1.0})
   , luminance(0.0f)
   , hue(0.0f)
   , saturation(0.0f)
   , lightness(0.0f)
   , chroma(0.0f)
{
}


Color::~Color()
{
}


AssetStudio::Color Color::build(ALLEGRO_COLOR al_color)
{
   AssetStudio::Color result;
   result.al_color = al_color;
   result.luminance = calculate_luminance(al_color);
   std::tie(result.hue, result.saturation, result.lightness) = calculate_hue_saturation_lightness(al_color);
   result.chroma = calculate_chroma(al_color);
   return result;
}

float Color::calculate_luminance(ALLEGRO_COLOR al_color)
{
   return 0.299 * al_color.r
        + 0.587 * al_color.g
        + 0.114 * al_color.b;
}

std::tuple<float, float, float> Color::calculate_hue_saturation_lightness(ALLEGRO_COLOR al_color)
{
   float h, s, l;
   al_color_rgb_to_hsl(al_color.r, al_color.g, al_color.b, &h, &s, &l);
   return {h, s, l};
}

float Color::calculate_chroma(ALLEGRO_COLOR al_color)
{
   float max_val = std::max({al_color.r, al_color.g, al_color.b});
   float min_val = std::min({al_color.r, al_color.g, al_color.b});
   return max_val - min_val;
}


} // namespace AssetStudio


