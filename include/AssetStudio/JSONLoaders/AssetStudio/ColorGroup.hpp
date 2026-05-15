#pragma once


#include <lib/nlohmann/json.hpp>
#include <AssetStudio/ColorGroup.hpp>


namespace AssetStudio
{
  void to_json(nlohmann::json& j, const ColorGroup& object);
  void from_json(const nlohmann::json& j, ColorGroup& object);
}


