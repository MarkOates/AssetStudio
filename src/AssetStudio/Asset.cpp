

#include <AssetStudio/Asset.hpp>




namespace AssetStudio
{


Asset::Asset(int id, std::string identifier, std::string type, std::string description, AllegroFlare::FrameAnimation::Animation* animation, int cell_width, int cell_height, ALLEGRO_BITMAP* bitmap, std::string asset_pack_identifier, std::string intra_pack_identifier)
   : id(id)
   , identifier(identifier)
   , type(type)
   , description(description)
   , animation(animation)
   , cell_width(cell_width)
   , cell_height(cell_height)
   , bitmap(bitmap)
   , asset_pack_identifier(asset_pack_identifier)
   , intra_pack_identifier(intra_pack_identifier)
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


