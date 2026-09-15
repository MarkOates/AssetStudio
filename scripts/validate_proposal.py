import json
import sys

def validate_schema(data):
    errors = []
    
    if not isinstance(data, dict):
        return ["Root must be a JSON object"]
        
    # --- catalog_proposal ---
    if "catalog_proposal" not in data:
        errors.append("Missing 'catalog_proposal' object")
    elif not isinstance(data["catalog_proposal"], dict):
        errors.append("'catalog_proposal' must be an object")
    else:
        prop = data["catalog_proposal"]
        if "type" not in prop or not isinstance(prop["type"], str):
            errors.append("catalog_proposal missing 'type' or not a string")
        if "perspective" not in prop or not isinstance(prop["perspective"], str):
            errors.append("catalog_proposal missing 'perspective' or not a string")
        if "num_frames" not in prop or not isinstance(prop["num_frames"], int):
            errors.append("catalog_proposal missing 'num_frames' or not an integer")
            
        if "cell_dimensions" not in prop:
            errors.append("catalog_proposal missing 'cell_dimensions'")
        elif prop["cell_dimensions"] is not None:
            if not isinstance(prop["cell_dimensions"], dict):
                errors.append("'cell_dimensions' must be null or an object")
            else:
                for k in ["width", "height"]:
                    if k not in prop["cell_dimensions"]:
                        errors.append(f"cell_dimensions missing '{k}'")
                    elif prop["cell_dimensions"][k] is not None and not isinstance(prop["cell_dimensions"][k], int):
                        errors.append(f"cell_dimensions '{k}' must be null or integer")
                        
        if "is_subframe" not in prop or not isinstance(prop["is_subframe"], bool):
            errors.append("catalog_proposal missing 'is_subframe' or not a boolean")
        if "is_icon" not in prop or not isinstance(prop["is_icon"], bool):
            errors.append("catalog_proposal missing 'is_icon' or not a boolean")
            
        if "inferred_grid" not in prop:
            errors.append("catalog_proposal missing 'inferred_grid'")
        elif prop["inferred_grid"] is not None:
            if not isinstance(prop["inferred_grid"], dict):
                errors.append("'inferred_grid' must be null or an object")
            else:
                for k in ["columns", "rows"]:
                    if k not in prop["inferred_grid"]:
                        errors.append(f"inferred_grid missing '{k}'")
                    elif not isinstance(prop["inferred_grid"][k], int):
                        errors.append(f"inferred_grid '{k}' must be an integer")
            
    # --- theme_profile ---
    if "theme_profile" not in data:
        errors.append("Missing 'theme_profile' object")
    elif not isinstance(data["theme_profile"], dict):
        errors.append("'theme_profile' must be an object")
    else:
        theme = data["theme_profile"]
        if "description" not in theme or not isinstance(theme["description"], str):
            errors.append("theme_profile missing 'description' or not a string")
        if "tags" not in theme or not isinstance(theme["tags"], list):
            errors.append("theme_profile missing 'tags' or not a list")
        if "style" not in theme or not isinstance(theme["style"], str):
            errors.append("theme_profile missing 'style' or not a string")
        if "color_descriptors" not in theme or not isinstance(theme["color_descriptors"], list):
            errors.append("theme_profile missing 'color_descriptors' or not a list")

    # --- inference_reasoning ---
    if "inference_reasoning" not in data:
        errors.append("Missing 'inference_reasoning' array")
    elif not isinstance(data["inference_reasoning"], list):
        errors.append("'inference_reasoning' must be an array")
    else:
        for idx, item in enumerate(data["inference_reasoning"]):
            if not isinstance(item, dict):
                errors.append(f"inference_reasoning[{idx}] must be an object")
            else:
                if "rule" not in item or not isinstance(item["rule"], str):
                    errors.append(f"inference_reasoning[{idx}] missing 'rule' or not a string")
                if "rationale" not in item or not isinstance(item["rationale"], str):
                    errors.append(f"inference_reasoning[{idx}] missing 'rationale' or not a string")
        
    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_proposal.py <json_file>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            data = json.loads(content)
            
        errors = validate_schema(data)
        if errors:
            print("❌ Validation Failed:")
            for err in errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            print("✅ JSON is perfectly valid against the Inference Schema.")
            sys.exit(0)
            
    except json.JSONDecodeError as e:
        print(f"❌ INVALID JSON SYNTAX: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR reading file: {e}")
        sys.exit(1)
