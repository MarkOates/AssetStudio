#pragma once


#include <lib/nlohmann/json.hpp>
#include <AssetStudio/GameProgressAndStateInfo.hpp>


namespace AssetStudio
{
  void to_json(nlohmann::json& j, const GameProgressAndStateInfo& object);
  void from_json(const nlohmann::json& j, GameProgressAndStateInfo& object);
}


