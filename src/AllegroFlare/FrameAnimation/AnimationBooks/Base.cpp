

#include <AllegroFlare/FrameAnimation/AnimationBooks/Base.hpp>

#include <AllegroFlare/Errors.hpp>


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


