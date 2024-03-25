

#include <AllegroFlare/FrameAnimation/SpriteStripAssembler.hpp>

#include <AllegroFlare/Logger.hpp>
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace AllegroFlare
{
namespace FrameAnimation
{


SpriteStripAssembler::SpriteStripAssembler()
   : bitmaps({})
   , sprite_strip(nullptr)
   , assembled("")
{
}


SpriteStripAssembler::~SpriteStripAssembler()
{
}


void SpriteStripAssembler::set_bitmaps(std::vector<ALLEGRO_BITMAP*> bitmaps)
{
   if (get_initialized()) throw std::runtime_error("[SpriteStripAssembler::set_bitmaps]: error: guard \"get_initialized()\" not met.");
   this->bitmaps = bitmaps;
}


std::vector<ALLEGRO_BITMAP*> SpriteStripAssembler::get_bitmaps() const
{
   return bitmaps;
}


bool SpriteStripAssembler::get_initialized()
{
   return assembled;
}

ALLEGRO_BITMAP* SpriteStripAssembler::get_sprite_strip()
{
   if (!(assembled))
   {
      std::stringstream error_message;
      error_message << "[SpriteStripAssembler::get_sprite_strip]: error: guard \"assembled\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("SpriteStripAssembler::get_sprite_strip: error: guard \"assembled\" not met");
   }
   return sprite_strip;
}

void SpriteStripAssembler::assemble()
{
   if (!((!bitmaps.empty())))
   {
      std::stringstream error_message;
      error_message << "[SpriteStripAssembler::assemble]: error: guard \"(!bitmaps.empty())\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("SpriteStripAssembler::assemble: error: guard \"(!bitmaps.empty())\" not met");
   }
   // Validate all bitmaps are not nullptr
   for (auto &bitmap : bitmaps)
   {
      if (bitmap == nullptr)
      {
         AllegroFlare::Logger::throw_error(
            "AllegroFlare::FrameAnimation::SpriteStripAssembler::assemble"
            "One of the bitmaps cannot be a nullptr."
         );
      }
   }

   // Validate all bitmaps have the same dimension (based on the inital images dimension)
   int cell_width = al_get_bitmap_width(bitmaps[0]);
   int cell_height = al_get_bitmap_height(bitmaps[0]);
   // TODO: Validate dimensions here

   // Create the bitmap
   sprite_strip = al_create_bitmap(cell_width * bitmaps.size(), cell_height);

   // Draw each bitmap onto the target
   al_set_target_bitmap(sprite_strip);
   al_clear_to_color(ALLEGRO_COLOR{0, 0, 0, 0});
   int i=0;
   for (auto &bitmap : bitmaps)
   {
      al_draw_bitmap(bitmap, i * cell_width, 0, 0);
   }

   assembled = true;
   return;
}


} // namespace FrameAnimation
} // namespace AllegroFlare


