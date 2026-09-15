import os
import json
import fcntl
import datetime
import re
import argparse
from validate_proposal import validate_schema

from inject_metadata import extract_color_profile, compute_file_hash
from PIL import Image

def get_brain_dir():
    return os.path.expanduser("~/.gemini/antigravity-cli/brain")

def extract_payload_from_transcript(transcript_path):
    last_json_content = None
    target_path = None
    
    if not os.path.exists(transcript_path):
        return None, None
        
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    step = json.loads(line)
                    # Extract target path from initial prompt
                    if step.get("source") == "USER_EXPLICIT" and step.get("type") == "USER_INPUT":
                        prompt = step.get("content", "")
                        match = re.search(r'Analyze: /Users/markoates/(?:Assets|Repos/AssetStudio)/(.+)', prompt)
                        if match:
                            target_path = match.group(1).strip()
                            
                    # Extract JSON from send_message tool call
                    if step.get("source") == "MODEL" and step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = step.get("tool_calls", [])
                        for call in tool_calls:
                            if call.get("name") == "send_message":
                                args = call.get("args", {})
                                msg = args.get("Message", "")
                                if "{" in msg and "}" in msg:
                                    last_json_content = msg
                except:
                    pass
    except:
        pass
        
    if last_json_content and target_path:
        start_idx = last_json_content.find('{')
        end_idx = last_json_content.rfind('}') + 1
        raw_json_str = last_json_content[start_idx:end_idx]
        try:
            parsed = json.loads(raw_json_str)
            return target_path, parsed
        except:
            pass
            
    return None, None

def process_all_transcripts(run_id=None, orchestrator=None, orchestrator_model=None):
    import uuid
    if not run_id:
        run_id = uuid.uuid4().hex[:8]
        print(f"🆕 Auto-generated Run ID: {run_id}")

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proposals_path = os.path.join(base_dir, 'scripts', 'ai_subagent_proposals.json')
    brain_dir = get_brain_dir()
    
    print("🔍 Scanning transcript logs for completed subagents...")
    
    # Load currently consolidated paths so we don't process duplicates
    processed_paths = set()
    if os.path.exists(proposals_path):
        try:
            with open(proposals_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.strip():
                    proposals = json.loads(content)
                    for p in proposals:
                        if "resource" in p and "source_files" in p["resource"]:
                            for sf in p["resource"]["source_files"]:
                                processed_paths.add(sf.replace("/Assets/", ""))
        except:
            pass
            
    new_proposals = []
    
    # Scan all subagent transcripts in the brain directory
    if os.path.exists(brain_dir):
        for subdir in os.listdir(brain_dir):
            transcript_path = os.path.join(brain_dir, subdir, ".system_generated", "logs", "transcript_full.jsonl")
            
            target_path, proposal_data = extract_payload_from_transcript(transcript_path)
            
            if target_path and target_path not in processed_paths:
                # Validate and format
                errors = validate_schema(proposal_data)
                if not errors:
                    vendor = target_path.split('/')[0]
                    pack = target_path.split('/')[1]
                    deterministic_id = f"synthetic/{target_path.replace('.', '_')}"
                    
                    proposed = proposal_data.get("catalog_proposal", {})
                    
                    audit_block = proposal_data.get("ai_audit", {})
                    audit_block["pass1_model"] = "subagent-strict-json-harriet3"
                    audit_block["pass1_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                    if run_id:
                        audit_block["run_id"] = run_id
                    if orchestrator:
                        audit_block["orchestrator_agent"] = orchestrator
                    if orchestrator_model:
                        audit_block["orchestrator_agent_model"] = orchestrator_model
                    
                    # Deterministic Metadata Extraction
                    full_disk_path = os.path.join("/Users/markoates/Assets", target_path)
                    computed_hash = compute_file_hash(full_disk_path) if os.path.exists(full_disk_path) else None
                    color_profile = None
                    actual_width, actual_height = None, None
                    if os.path.exists(full_disk_path) and target_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        try:
                            with Image.open(full_disk_path) as img:
                                color_profile = extract_color_profile(img)
                                actual_width, actual_height = img.size
                        except:
                            pass
                    
                    theme_profile = proposal_data.get("theme_profile", {})
                    if color_profile:
                        theme_profile["color_profile"] = color_profile
                        
                    inferred_grid = proposed.get("inferred_grid")
                    cell_dimensions = proposed.get("cell_dimensions")
                    
                    if actual_width and actual_height:
                        cols = 1
                        rows = 1
                        if inferred_grid:
                            cols = inferred_grid.get("columns", 1)
                            rows = inferred_grid.get("rows", 1)
                        elif proposed.get("type") == "animation_frames":
                            num_frames = proposed.get("num_frames") or 1
                            if num_frames > 1:
                                if actual_width > actual_height:
                                    cols = num_frames
                                    rows = 1
                                else:
                                    cols = 1
                                    rows = num_frames
                                    
                        if cols > 0 and rows > 0:
                            cell_dimensions = {
                                "width": int(actual_width / cols),
                                "height": int(actual_height / rows)
                            }
                    
                    asset_dict = {
                        "identifier": deterministic_id,
                        "name": os.path.basename(target_path),
                        "asset_pack_identifier": f"{vendor}/{pack}",
                        "type": proposed.get("type", "static_image"),
                        "is_subframe": proposed.get("is_subframe", False),
                        "is_icon": proposed.get("is_icon", False),
                        "visibility": "public",
                        "sheet_row_number": None,
                        "blacklisted_type": None,
                        "resource": {
                            "type": proposed.get("type", "static_image"),
                            "source_files": [f"/Assets/{target_path}"],
                            "cell_dimensions": cell_dimensions,
                            "inferred_grid": inferred_grid,
                            "hash": computed_hash
                        },
                        "animation_profile": {
                            "num_frames": proposed.get("num_frames") or 1,
                            "base_frame_duration": 0.1
                        } if (proposed.get("num_frames") or 1) > 1 else None,
                        "theme_profile": theme_profile,
                        "inference_reasoning": proposal_data.get("inference_reasoning", []),
                        "ai_audit": audit_block
                    }
                    
                    new_proposals.append(asset_dict)
                    processed_paths.add(target_path)
                    print(f"✅ Extracted and validated: {target_path}")

    # If we found new valid proposals, lock and append to database
    if new_proposals:
        try:
            with open(proposals_path, 'a+') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.seek(0)
                content = f.read()
                existing = json.loads(content) if content.strip() else []
                existing.extend(new_proposals)
                f.seek(0)
                f.truncate()
                json.dump(existing, f, indent=2)
                fcntl.flock(f, fcntl.LOCK_UN)
                
            print(f"💾 Securely merged {len(new_proposals)} new proposals into ai_subagent_proposals.json!")
        except Exception as e:
            print(f"❌ Write error: {e}")
    else:
        print("No new valid subagent proposals found to process.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", type=str, help="Run hash ID")
    parser.add_argument("--orchestrator", type=str, help="Orchestrator agent name")
    parser.add_argument("--orchestrator-model", type=str, help="Orchestrator model")
    args = parser.parse_args()
    process_all_transcripts(run_id=args.run_id, orchestrator=args.orchestrator, orchestrator_model=args.orchestrator_model)
