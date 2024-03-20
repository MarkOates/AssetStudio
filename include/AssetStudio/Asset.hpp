#pragma once


#include <AllegroFlare/FrameAnimation/Animation.hpp>
#include <AllegroFlare/FrameAnimation/Book.hpp>
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
      std::vector<std::string> categories;
      std::vector<std::string> tags;
      int related_assset_group_id;
      std::string from_pack;
      AllegroFlare::FrameAnimation::Book* animation_book;
      AllegroFlare::FrameAnimation::Animation animation;
      Asset();
      ~Asset();

   };
}



