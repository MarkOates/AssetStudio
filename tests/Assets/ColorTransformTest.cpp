
#include <gtest/gtest.h>

#include <Assets/ColorTransform.hpp>


TEST(Assets_ColorTransformTest, can_be_created_without_blowing_up)
{
   Assets::ColorTransform color_transform;
}


TEST(Assets_ColorTransformTest, run__returns_the_expected_response)
{
   Assets::ColorTransform color_transform;
   std::string expected_string = "Hello World!";
   EXPECT_EQ(expected_string, color_transform.run());
}


