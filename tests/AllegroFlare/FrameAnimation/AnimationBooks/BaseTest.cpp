
#include <gtest/gtest.h>

#include <AllegroFlare/FrameAnimation/AnimationBooks/Base.hpp>


class AnimationBooksBaseTestClass : public AllegroFlare::FrameAnimation::AnimationBooks::Base
{
public:
   AnimationBooksBaseTestClass()
      : AllegroFlare::FrameAnimation::AnimationBooks::Base("AnimationBooksBaseTestClass")
   {}
};


TEST(AllegroFlare_FrameAnimation_AnimationBooks_BaseTest, can_be_created_without_blowing_up)
{
   AllegroFlare::FrameAnimation::AnimationBooks::Base base;
}


TEST(AllegroFlare_FrameAnimation_AnimationBooks_BaseTest, TYPE__has_the_expected_value)
{
   EXPECT_STREQ(
     "AllegroFlare/FrameAnimation/AnimationBooks/Base",
     AllegroFlare::FrameAnimation::AnimationBooks::Base::TYPE
   );
}


TEST(AllegroFlare_FrameAnimation_AnimationBooks_BaseTest, type__has_the_expected_value_matching_TYPE)
{
   AllegroFlare::FrameAnimation::AnimationBooks::Base base;
   EXPECT_EQ(AllegroFlare::FrameAnimation::AnimationBooks::Base::TYPE, base.get_type());
}


TEST(AllegroFlare_FrameAnimation_AnimationBooks_BaseTest, derived_classes_will_have_the_expected_type)
{
   AnimationBooksBaseTestClass test_class;
   EXPECT_EQ("AnimationBooksBaseTestClass", test_class.get_type());
}


