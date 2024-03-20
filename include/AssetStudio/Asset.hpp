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
      std::string name;
      std::string description;
      AllegroFlare::FrameAnimation::Animation animation;
      std::vector<std::string> categories;
      std::vector<std::string> tags;
      int related_assset_group_id;
      std::string from_pack;
      Asset(int id=0, std::string name="[unset-name]", std::string description="[unset-description]", AllegroFlare::FrameAnimation::Animation animation={});
      ~Asset();

   };
}



