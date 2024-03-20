

#include <AssetStudio/Asset.hpp>




namespace AssetStudio
{


Asset::Asset()
   : id(0)
   , name("[unset-name]")
   , description("[unset-description]")
   , categories()
   , tags()
   , related_assset_group_id(0)
   , from_pack("[unset-description]")
   , animation_book(nullptr)
   , animation()
{
}


Asset::~Asset()
{
}




} // namespace AssetStudio


