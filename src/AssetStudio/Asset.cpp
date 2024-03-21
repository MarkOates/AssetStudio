

#include <AssetStudio/Asset.hpp>




namespace AssetStudio
{


Asset::Asset(int id, std::string identifier, std::string description, AllegroFlare::FrameAnimation::Animation* animation)
   : id(id)
   , identifier(identifier)
   , description(description)
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


