

#include <AssetStudio/AssetGroup.hpp>




namespace AssetStudio
{


AssetGroup::AssetGroup()
   : id(0)
   , name("[unset-name]")
   , description("[unset-description]")
   , assets({})
   , categories()
   , tags()
   , from_pack("[unset-description]")
{
}


AssetGroup::~AssetGroup()
{
}




} // namespace AssetStudio


