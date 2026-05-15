

#include <AssetStudio/Filesystem.hpp>

#include <filesystem>
#include <iostream>
#include <sstream>
#include <stdexcept>


namespace AssetStudio
{


Filesystem::Filesystem()
{
}


Filesystem::~Filesystem()
{
}


bool Filesystem::exists_as_file(std::string file_path)
{
   if (!(file_path != DEFAULT_ARGUMENT_FILE_PATH))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Filesystem::exists_as_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Filesystem::exists_as_file]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met");
   }
   return std::filesystem::exists(file_path) && std::filesystem::is_regular_file(file_path);
}

bool Filesystem::exists_as_directory(std::string file_path)
{
   if (!(file_path != DEFAULT_ARGUMENT_FILE_PATH))
   {
      std::stringstream error_message;
      error_message << "[AssetStudio::Filesystem::exists_as_directory]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met.";
      std::cerr << "\033[1;31m" << error_message.str() << " An exception will be thrown to halt the program.\033[0m" << std::endl;
      throw std::runtime_error("[AssetStudio::Filesystem::exists_as_directory]: error: guard \"file_path != DEFAULT_ARGUMENT_FILE_PATH\" not met");
   }
   return std::filesystem::exists(file_path) && std::filesystem::is_directory(file_path);
}


} // namespace AssetStudio


