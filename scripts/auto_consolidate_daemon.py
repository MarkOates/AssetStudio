import os
import json
import time
import fcntl
import datetime
import re
from validate_proposal import validate_schema

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
                        match = re.search(r'Analyze: /Users/markoates/Assets/(.+)', prompt)
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

def run_daemon():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proposals_path = os.path.join(base_dir, 'scripts', 'ai_subagent_proposals.json')
    brain_dir = get_brain_dir()
    
    print("🤖 Auto-Consolidate Daemon Started! Monitoring for subagent completions...")
    
    while True:
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
                        audit_block["pass1_model"] = "subagent-strict-json-harriet1"
                        audit_block["pass1_timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                        
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
                                "cell_dimensions": proposed.get("cell_dimensions", None),
                                "inferred_grid": proposed.get("inferred_grid", None),
                            },
                            "animation_profile": {
                                "num_frames": proposed.get("num_frames", 1),
                                "base_frame_duration": 0.1
                            } if proposed.get("num_frames", 1) > 1 else None,
                            "theme_profile": proposal_data.get("theme_profile", {}),
                            "inference_reasoning": proposal_data.get("inference_reasoning", []),
                            "ai_audit": audit_block
                        }
                        
                        new_proposals.append(asset_dict)
                        processed_paths.add(target_path)
                        print(f"✅ Daemon instantly consolidated: {target_path}")

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
                    
                print(f"💾 Daemon securely saved {len(new_proposals)} new proposals to database!")
                
                # Auto-trigger the UI rebuild
                os.system(f"{os.path.join(base_dir, 'scripts', 'rebuild_ui_data.sh')} > /dev/null 2>&1")
                print("🔄 Daemon automatically triggered UI Rebuild!")
                
            except Exception as e:
                print(f"❌ Daemon write error: {e}")
                
        time.sleep(5)

if __name__ == "__main__":
    run_daemon()
