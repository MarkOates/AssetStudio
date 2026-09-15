import json
import sys
import os
import re

def extract_payloads(transcript_paths, output_batch_path):
    batch_data = []
    
    for path in transcript_paths:
        if path.startswith("file://"):
            path = path[7:]
            
        if not os.path.exists(path):
            print(f"Transcript not found: {path}")
            continue
            
        last_json_content = None
        
        # Read the FULL JSONL transcript to avoid truncated fields
        full_path = path.replace('transcript.jsonl', 'transcript_full.jsonl')
        if not os.path.exists(full_path):
            full_path = path # fallback
            
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    step = json.loads(line)
                    if step.get("source") == "MODEL" and step.get("type") == "PLANNER_RESPONSE":
                        tool_calls = step.get("tool_calls", [])
                        for call in tool_calls:
                            if call.get("name") == "send_message":
                                args = call.get("args", {})
                                msg = args.get("Message", "")
                                if "{" in msg and "}" in msg:
                                    last_json_content = msg
                except Exception as e:
                    pass
                    
        if last_json_content:
            # Clean up the string to extract just the JSON block
            start_idx = last_json_content.find('{')
            end_idx = last_json_content.rfind('}') + 1
            raw_json_str = last_json_content[start_idx:end_idx]
            
            try:
                parsed_json = json.loads(raw_json_str)
                # We need to know which file this belonged to.
                # Assuming the subagent was given the path in its prompt, 
                # we can extract it from the USER_INPUT step in the same transcript.
                target_path = None
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        step = json.loads(line)
                        if step.get("source") == "USER_EXPLICIT" and step.get("type") == "USER_INPUT":
                            prompt = step.get("content", "")
                            match = re.search(r'Analyze: /Users/markoates/Assets/(.+)', prompt)
                            if match:
                                target_path = match.group(1).strip()
                                break
                
                if target_path:
                    batch_data.append({
                        "path": target_path,
                        "proposal": parsed_json
                    })
                    print(f"✅ Extracted payload for {target_path}")
                else:
                    print(f"❌ Could not determine target path for transcript {path}")
            except Exception as e:
                print(f"❌ Failed to parse JSON from {path}: {e}")
        else:
            print(f"❌ No JSON payload found in {path}")
            
    with open(output_batch_path, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, indent=2)
        
    print(f"\nSuccessfully extracted {len(batch_data)} payloads to {output_batch_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 extract_payloads.py <output_batch_json> <transcript1.jsonl> [transcript2.jsonl ...]")
        sys.exit(1)
        
    output_path = sys.argv[1]
    transcripts = sys.argv[2:]
    extract_payloads(transcripts, output_path)
