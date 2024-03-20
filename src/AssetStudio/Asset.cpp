

#include <AssetStudio/Asset.hpp>




namespace AssetStudio
{


Asset::Asset(int id, std::string name, std::string description, AllegroFlare::FrameAnimation::Book* animation_book, AllegroFlare::FrameAnimation::Animation animation)
   : id(id)
   , name(name)
   , description(description)
   , animation_book(animation_book)
   , animation(animation)
   , categories()
   , tags()
   , related_assset_group_id(0)
   , from_pack("[unset-description]")
{
}


Asset::~Asset()
{
}




} // namespace AssetStudio


