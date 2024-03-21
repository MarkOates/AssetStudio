

#include <AssetStudio/Asset.hpp>




namespace AssetStudio
{


Asset::Asset(int id, std::string identifier, std::string type, std::string description, AllegroFlare::FrameAnimation::Animation* animation, int cell_width, int cell_height)
   : id(id)
   , identifier(identifier)
   , type(type)
   , description(description)
   , animation(animation)
   , cell_width(cell_width)
   , cell_height(cell_height)
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


