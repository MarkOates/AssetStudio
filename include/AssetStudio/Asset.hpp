#pragma once


#include <AllegroFlare/FrameAnimation/Animation.hpp>
#include <string>
#include <vector>


namespace AssetStudio
{
   class Asset
   {
   private:

   protected:


   public:
      int id;
      std::string identifier;
      std::string type;
      std::string description;
      AllegroFlare::FrameAnimation::Animation* animation;
      int cell_width;
      int cell_height;
      std::vector<std::string> categories;
      std::vector<std::string> tags;
      int related_assset_group_id;
      std::string from_pack;
      Asset(int id=0, std::string identifier="[unset-identifier]", std::string type="[unset-type]", std::string description="[unset-description]", AllegroFlare::FrameAnimation::Animation* animation={}, int cell_width=0, int cell_height=0);
      ~Asset();

   };
}



