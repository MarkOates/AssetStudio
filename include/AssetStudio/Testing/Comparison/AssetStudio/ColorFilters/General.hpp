#pragma once


#include <AssetStudio/ColorFilters/General.hpp>
#include <ostream>


namespace AssetStudio::ColorFilters
{
   bool operator==(const General& object, const General& other_object);
   void PrintTo(const General& object, ::std::ostream* os);
}


