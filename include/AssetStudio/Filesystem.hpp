#pragma once


#include <string>


namespace AssetStudio
{
   class Filesystem
   {
   public:
      static constexpr const char* DEFAULT_ARGUMENT_FILE_PATH = "[unset-file_path]";

   private:

   protected:


   public:
      Filesystem();
      ~Filesystem();

      static bool exists_as_file(std::string file_path=DEFAULT_ARGUMENT_FILE_PATH);
      static bool exists_as_directory(std::string file_path=DEFAULT_ARGUMENT_FILE_PATH);
   };
}



