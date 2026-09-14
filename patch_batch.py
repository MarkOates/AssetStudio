content = open('scripts/batch_final.py').read()

new_process_asset = """
def process_asset(rel_path):
    physical_path = os.path.join(ASSETS_DIR, rel_path)
    
    if not os.path.exists(physical_path):
        return None
        
    ext = os.path.splitext(physical_path)[1].lower()
    asset_extensions = ('.png', '.gif', '.jpg', '.jpeg', '.wav', '.ogg', '.mp3')
    
    if ext not in asset_extensions:
        filename_with_ext = os.path.basename(rel_path)
        deterministic_name = os.path.splitext(filename_with_ext)[0]
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        parts = rel_path.split('/')
        vendor = parts[0]
        if len(parts) > 1:
            pack = parts[1] if parts[1] != "extracted" else parts[0]
        else:
            pack = "unknown"
            
        return {
            "identifier": deterministic_id,
            "name": deterministic_name,
            "asset_pack_identifier": f"{vendor}/{pack}",
            "type": "blacklisted_file",
            "is_subframe": False,
            "is_icon": False,
            "visibility": "hidden",
            "sheet_row_number": None,
            "blacklisted_type": ext if ext else "unknown",
            "resource": {
                "type": "blacklisted_file",
                "source_files": [f"/Assets/{rel_path}"]
            },
            "theme_profile": {
                "description": "Blacklisted file type skipped during AI evaluation.",
                "tags": [ext.strip('.') if ext else "unknown", "blacklisted"],
                "style": "None",
                "color_descriptors": []
            }
        }
        
    img = None
    color_profile = None
    if ext in ('.png', '.jpg', '.jpeg', '.gif'):
        try:
            img = Image.open(physical_path)
            color_profile = extract_color_profile(img)
        except Exception:
            pass
            
    prompt = f"Analyze this uncatalogued game asset visually. The image is {img.width}x{img.height} pixels. Its file path is '{rel_path}'." if img else f"Analyze this uncatalogued game asset. Its file path is '{rel_path}'."
    
    try:
        if img:
            response = model.generate_content([prompt, img])
        else:
            response = model.generate_content([prompt])
            
        result_data = json.loads(response.text)
        
        parts = rel_path.split('/')
        vendor = parts[0]
        if len(parts) > 1:
            pack = parts[1] if parts[1] != "extracted" else parts[0]
        else:
            pack = "unknown"
            
        proposed = result_data["catalog_proposal"]
        
        if proposed.get("type") in ["static_image", "preview"] or proposed.get("is_subframe"):
            proposed["inferred_grid"] = None
        
        filename_with_ext = os.path.basename(rel_path)
        deterministic_name = os.path.splitext(filename_with_ext)[0]
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        
        asset_dict = {
            "identifier": deterministic_id,
            "name": deterministic_name,
            "asset_pack_identifier": f"{vendor}/{pack}",
            "type": proposed.get("type", "static_image"),
            "is_subframe": proposed.get("is_subframe", False),
            "is_icon": proposed.get("is_icon", False),
            "visibility": "public",
            "sheet_row_number": None,
            "blacklisted_type": None,
            "resource": {
                "type": proposed.get("type", "static_image"),
                "source_files": [f"/Assets/{rel_path}"],
                "cell_dimensions": proposed.get("cell_dimensions", None),
                "inferred_grid": proposed.get("inferred_grid", None),
            },
            "animation_profile": {
                "num_frames": proposed.get("num_frames", 1),
                "base_frame_duration": 0.1
            } if proposed.get("num_frames", 1) > 1 else None,
            "theme_profile": result_data.get("theme_profile", {}),
            "inference_reasoning": result_data.get("inference_reasoning", []),
            "ai_metadata": {
                "pass1_model": "gemini-3.5-flash-lite",
                "pass1_timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        }
        
        if img and proposed.get("inferred_grid") and not proposed.get("is_subframe"):
            if "cell_dimensions" in asset_dict["resource"] and asset_dict["resource"]["cell_dimensions"]:
                # Keep inferred
                pass
            else:
                asset_dict["resource"]["cell_dimensions"] = {"width": img.width, "height": img.height}
                
        if color_profile:
            asset_dict["theme_profile"]["color_profile"] = color_profile
            
        return asset_dict
        
    except Exception as e:
        print(f"Error processing {rel_path}: {e}")
        return None
"""

import re
content = re.sub(r'def process_asset\(rel_path\):.*?(?=\n\n|$)', new_process_asset, content, flags=re.DOTALL)
with open('scripts/batch_final.py', 'w') as f:
    f.write(content)
print("Patched batch_final.py")
