#pragma once


#include <AssetStudio/ColorFilters/General.hpp>
#include <cstdint>
#include <set>


namespace AssetStudio
{
   class ColorGroup
   {
   private:

   protected:


   public:
      std::set<uint32_t> color_ids;
      AssetStudio::ColorFilters::General general_filter;
      ColorGroup();
      ~ColorGroup();

   };
}



