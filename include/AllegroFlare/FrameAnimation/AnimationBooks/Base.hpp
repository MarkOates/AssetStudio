#pragma once


#include <AllegroFlare/FrameAnimation/Animation.hpp>
#include <map>
#include <string>


namespace AllegroFlare
{
   namespace FrameAnimation
   {
      namespace AnimationBooks
      {
         class Base
         {
         public:
            static constexpr char* TYPE = (char*)"AllegroFlare/FrameAnimation/AnimationBooks/Base";

         private:
            std::string type;
            std::map<std::string, AllegroFlare::FrameAnimation::Animation> dictionary;

         protected:


         public:
            Base(std::string type=AllegroFlare::FrameAnimation::AnimationBooks::Base::TYPE);
            ~Base();

            std::string get_type() const;
            std::map<std::string, AllegroFlare::FrameAnimation::Animation> &get_dictionary_ref();
            void add_animation(std::string identifier="[unset-identifier]", AllegroFlare::FrameAnimation::Animation* animation=nullptr);
            bool animation_exists(std::string name="[unset-name]");
            AllegroFlare::FrameAnimation::Animation find_animation_by_name(std::string name="[unset-name]");
            bool is_type(std::string possible_type="");
         };
      }
   }
}



