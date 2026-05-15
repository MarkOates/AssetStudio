

#include <AssetStudio/Testing/Comparison/AssetStudio/ColorFilters/General.hpp>


namespace AssetStudio::ColorFilters
{


bool operator==(const General& object, const General& other_object)
{
   if (object.hue_rotation != other_object.hue_rotation) return false;
   if (object.saturation_multiplier != other_object.saturation_multiplier) return false;
   if (object.rgb_multiplier != other_object.rgb_multiplier) return false;
   return true;
}


void PrintTo(const General& object, ::std::ostream* os)
{
   *os << "AssetStudio::ColorFilters::General("
       << "hue_rotation: \"" << object.hue_rotation<< "\", "
       << "saturation_multiplier: \"" << object.saturation_multiplier << "\", "
       << "rgb_multiplier: \"" << object.rgb_multiplier << "\", "
       << ")";
}


}


