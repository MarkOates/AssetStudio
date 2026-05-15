

#include <AssetStudio/Color.hpp>

#include <algorithm>
#include <allegro5/allegro_color.h>
#include <cmath>


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

void Color::multiply_rgb(float multiplier)
{
   uint32_t previous_id = id;
   *this = build(ALLEGRO_COLOR{
      al_color.r * multiplier,
      al_color.g * multiplier,
      al_color.b * multiplier,
      al_color.a
   });
   id = previous_id;
   return;
}

void Color::multiply_saturation(float multiplier)
{
   uint32_t previous_id = id;

   // Calculate and clamp new saturation (0.0 - 1.0)
   float new_sat = this->saturation * multiplier;
   if (new_sat < 0.0f) new_sat = 0.0f;
   if (new_sat > 1.0f) new_sat = 1.0f;

   // Convert HSL back to ALLEGRO_COLOR
   ALLEGRO_COLOR new_al_color;
   al_color_hsl_to_rgb(this->hue, new_sat, this->lightness, 
                       &new_al_color.r, &new_al_color.g, &new_al_color.b);
   new_al_color.a = this->al_color.a;

   // Rebuild the object
   *this = build(new_al_color);
   id = previous_id;
}

void Color::rotate_hue(float unit_offset)
{
   uint32_t previous_id = id;
   // Calculate new hue (0.0 - 360.0)
   float new_hue = std::fmod(this->hue + (unit_offset * 360.0f), 360.0f);
   if (new_hue < 0.0f) new_hue += 360.0f;

   // Convert HSL back to ALLEGRO_COLOR
   ALLEGRO_COLOR new_al_color;
   al_color_hsl_to_rgb(new_hue, this->saturation, this->lightness, 
                       &new_al_color.r, &new_al_color.g, &new_al_color.b);
   new_al_color.a = this->al_color.a;

   // Rebuild the object
   *this = build(new_al_color);
   id = previous_id;
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


