import json
import sys
import os
import fcntl
import datetime
from validate_proposal import validate_schema

def consolidate_batch(batch_json_path):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proposals_path = os.path.join(base_dir, 'scripts', 'ai_subagent_proposals.json')
    
    with open(batch_json_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)
        
    new_proposals = []
    
    for item in batch_data:
        rel_path = item["path"]
        data = item["proposal"]
        
        # 1. Validate
        errors = validate_schema(data)
        if errors:
            print(f"❌ Validation failed for {rel_path}: {errors}")
            continue
            
        # 2. Format
        vendor = rel_path.split('/')[0]
        pack = rel_path.split('/')[1]
        deterministic_name = os.path.basename(rel_path)
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        
        proposed = data.get("catalog_proposal", {})
        
        audit_block = data.get("ai_audit", {})
        audit_block["pass1_model"] = "subagent-strict-json-harriet1"
        audit_block["pass1_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
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
            "theme_profile": data.get("theme_profile", {}),
            "inference_reasoning": data.get("inference_reasoning", []),
            "ai_audit": audit_block
        }
        
        new_proposals.append(asset_dict)
        print(f"✅ Validated and formatted {rel_path}")
        
    if not new_proposals:
        print("No valid proposals to consolidate.")
        return
        
    # Race-condition proof file append
    with open(proposals_path, 'a+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        content = f.read()
        if content.strip():
            existing = json.loads(content)
        else:
            existing = []
            
        existing.extend(new_proposals)
        
        f.seek(0)
        f.truncate()
        json.dump(existing, f, indent=2)
        fcntl.flock(f, fcntl.LOCK_UN)
        
    print(f"✅ Successfully consolidated {len(new_proposals)} proposals into ai_subagent_proposals.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 consolidate_batch.py <batch_json_path>")
        sys.exit(1)
        
    consolidate_batch(sys.argv[1])
