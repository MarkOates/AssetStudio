#pragma once


#include <AssetStudio/Asset.hpp>
#include <string>
#include <vector>


namespace AssetStudio
{
   class AssetGroup
   {
   private:

   protected:


   public:
      int id;
      std::string name;
      std::string description;
      std::vector<AssetStudio::Asset> assets;
      std::vector<std::string> categories;
      std::vector<std::string> tags;
      std::string from_pack;
      AssetGroup();
      ~AssetGroup();

   };
}



