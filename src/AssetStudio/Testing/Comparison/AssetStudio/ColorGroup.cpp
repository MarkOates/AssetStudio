

#include <AssetStudio/Testing/Comparison/AssetStudio/ColorGroup.hpp>
#include <AssetStudio/Testing/Comparison/AssetStudio/ColorFilters/General.hpp>



#include <set>
#include <string>
#include <sstream>

namespace
{
   std::string escape_quotes(const std::string& input)
   {
      std::string result;

      for (char c : input)
      {
         if (c == '"')
         {
            result += "\\\"";
         }
         else
         {
            result += c;
         }
      }

      return result;
   }

   std::string set_to_quoted_csv(const std::set<std::string>& values)
   {
      std::ostringstream oss;
      bool first = true;

      for (const auto& val : values)
      {
         if (!first)
         {
            oss << ",";
         }

         oss << "\"" << escape_quotes(val) << "\"";
         first = false;
      }

      return oss.str();
   }

   std::string set_to_quoted_csv(const std::set<uint32_t>& values)
   {
      std::ostringstream oss;
      bool first = true;

      for (uint32_t val : values)
      {
         if (!first)
         {
            oss << ",";
         }

         oss << "\"" << val << "\"";
         first = false;
      }

      return oss.str();
   }
}


namespace AssetStudio
{


bool operator==(const ColorGroup& object, const ColorGroup& other_object)
{
   if (object.color_ids != other_object.color_ids) return false;
   if (object.general_filter != other_object.general_filter) return false;
   return true;
}


void PrintTo(const ColorGroup& object, ::std::ostream* os)
{
   *os << "ColorGroup("
       << "color_ids: \"" << set_to_quoted_csv(object.color_ids) << "\", "
       << ")";
}


}


