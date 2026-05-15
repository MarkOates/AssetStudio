#pragma once


#include <lib/nlohmann/json.hpp>
#include <AssetStudio/ColorFilters/General.hpp>


namespace AssetStudio::ColorFilters
{
  void to_json(nlohmann::json& j, const General& object);
  void from_json(const nlohmann::json& j, General& object);
}


