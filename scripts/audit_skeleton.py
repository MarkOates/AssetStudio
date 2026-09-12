import json
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

system_instruction = """You are an expert game asset cataloger and computer vision AI.
You are given an image (a sprite sheet) and its filename. 
DO NOT just rely on the filename. You must visually analyze the image data.
1. Visually count the number of columns and rows in the grid.
2. Determine if this sheet contains a single animation sequence, or MULTIPLE different animations (e.g., idle on row 1, walk on row 2).
3. If it contains multiple animations, propose how we should break it apart (e.g., what are the cell dimensions, and how many frames per animation?).

Output your analysis as a structured JSON object containing your visual reasoning and your proposed slicing strategy.
"""

def main():
    rel_path = "rafaelmatos/epic-rpg-world-asset-pack-crypt/extracted/EPIC RPG World Pack - Crypt V.1.5.1/Characters/Skeleton/skeleton-variation1-all animations.png"
    physical_path = os.path.join('/Users/markoates/Assets', rel_path)
    
    img = Image.open(physical_path)
    
    model = genai.GenerativeModel(
        model_name="gemini-flash-latest", # Use Pro for advanced visual counting/reasoning
        system_instruction=system_instruction,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.0
        }
    )
    
    prompt = f"Analyze this image. The image is {img.width}x{img.height} pixels. Filename: '{rel_path}'."
    response = model.generate_content([prompt, img])
    
    print("\n--- AI VISUAL ANALYSIS ---")
    print(response.text)

if __name__ == "__main__":
    main()
