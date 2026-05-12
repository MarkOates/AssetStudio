#pragma once




namespace Assets
{
   class ColorTransform
   {
   private:
      float multiplier;
      float hue_rotation;

   protected:


   public:
      ColorTransform();
      ~ColorTransform();

      void process();
   };
}



