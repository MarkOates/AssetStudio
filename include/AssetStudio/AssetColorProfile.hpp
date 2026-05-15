#pragma once


#include <string>


namespace AssetStudio
{
   class AssetColorProfile
   {
   private:
      std::string json_filename;

   protected:


   public:
      AssetColorProfile();
      ~AssetColorProfile();

      std::string run();
   };
}



