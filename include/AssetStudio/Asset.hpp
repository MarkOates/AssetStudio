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
      std::vector<std::string> categories;
      std::vector<std::string> tags;
      int related_assset_group_id;
      std::string from_pack;
      Asset(int id=0, std::string identifier="[unset-identifier]", std::string type="[unset-type]", std::string description="[unset-description]", AllegroFlare::FrameAnimation::Animation* animation={});
      ~Asset();

   };
}



