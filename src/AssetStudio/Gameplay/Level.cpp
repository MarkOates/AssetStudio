

#include <AssetStudio/Gameplay/Level.hpp>




namespace AssetStudio
{
namespace Gameplay
{


Level::Level()
   : AllegroFlare::Levels::Base(AssetStudio::Gameplay::Level::TYPE)
   , title("[unset-title]")
{
}


Level::~Level()
{
}


void Level::set_title(std::string title)
{
   this->title = title;
}


std::string Level::get_title() const
{
   return title;
}




} // namespace Gameplay
} // namespace AssetStudio


