import os
import hashlib
from PIL import Image

def extract_color_profile(img):
    try:
        img = img.convert("RGBA")
        colors = img.getcolors(maxcolors=1000)
        
        def rgba_to_hex(r, g, b, a):
            if a == 255: return f"#{r:02x}{g:02x}{b:02x}"
            return f"#{r:02x}{g:02x}{b:02x}{a:02x}"
            
        if colors and len(colors) <= 32:
            colors.sort(reverse=True, key=lambda x: x[0])
            palette = [rgba_to_hex(*c[1]) for c in colors[:16]]
            return {
                "color_space": "sRGB",
                "palette": palette,
                "dominant_colors": palette[:3],
                "transparent": True
            }
        return None
    except Exception:
        return None

def compute_file_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()
