#pragma once


#include <AssetStudio/ColorGroup.hpp>
#include <ostream>


namespace AssetStudio
{
   bool operator==(const ColorGroup& object, const ColorGroup& other_object);
   void PrintTo(const ColorGroup& object, ::std::ostream* os);
}


