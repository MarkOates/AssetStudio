#pragma once


#include <cstdint>
#include <vector>


namespace AssetStudio
{
   class IndexedBitmap
   {
   private:

   protected:


   public:
      uint32_t width;
      uint32_t height;
      std::vector<uint16_t> pixels;
      IndexedBitmap();
      ~IndexedBitmap();

   };
}



