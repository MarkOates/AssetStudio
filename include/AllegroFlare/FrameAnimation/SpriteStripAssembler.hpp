#pragma once


#include <allegro5/allegro.h>
#include <vector>


namespace AllegroFlare
{
   namespace FrameAnimation
   {
      class SpriteStripAssembler
      {
      private:
         std::vector<ALLEGRO_BITMAP*> bitmaps;
         ALLEGRO_BITMAP* sprite_strip;
         bool assembled;

      protected:


      public:
         SpriteStripAssembler();
         ~SpriteStripAssembler();

         void set_bitmaps(std::vector<ALLEGRO_BITMAP*> bitmaps);
         std::vector<ALLEGRO_BITMAP*> get_bitmaps() const;
         bool get_initialized();
         ALLEGRO_BITMAP* get_sprite_strip();
         void assemble();
      };
   }
}



