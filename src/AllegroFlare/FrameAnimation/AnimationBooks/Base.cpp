

#include <AllegroFlare/FrameAnimation/AnimationBooks/Base.hpp>

#include <AllegroFlare/Errors.hpp>
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace AllegroFlare
{
namespace FrameAnimation
{
namespace AnimationBooks
{


Base::Base(std::string type)
   : type(type)
   , dictionary({})
{
}


Base::~Base()
{
}


std::string Base::get_type() const
{
   return type;
}


std::map<std::string, AllegroFlare::FrameAnimation::Animation> &Base::get_dictionary_ref()
{
   return dictionary;
}


void Base::add_animation(std::string identifier, AllegroFlare::FrameAnimation::Animation* animation)
{
   if (!(animation))
   {
      std::stringstream error_message;
      error_message << "[Base::add_animation]: error: guard \"animation\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("Base::add_animation: error: guard \"animation\" not met");
   }
   if (animation_exists(identifier))
   {
      // TODO: Test this validation
      AllegroFlare::Errors::throw_error(
            "AllegroFlare::FrameAnimation::AnimationBooks::add_animation",
            "An animation already exists with the name \"" + identifier + "\". An animation cannot overwritten."
         );
   }
   dictionary[identifier] = *animation;
   return;
}

bool Base::animation_exists(std::string name)
{
   return (dictionary.count(name) > 0);
}

AllegroFlare::FrameAnimation::Animation Base::find_animation_by_name(std::string name)
{
   if (dictionary.count(name) == 0)
   {
      AllegroFlare::Errors::throw_error(
            "AllegroFlare::FrameAnimation::AnimationBooks::find_animation_by_name",
            "No animation exists for name \"" + name + "\""
         );
   }
   return dictionary[name];
}

bool Base::is_type(std::string possible_type)
{
   return (possible_type == get_type());
}


} // namespace AnimationBooks
} // namespace FrameAnimation
} // namespace AllegroFlare


