import json, os, glob, hashlib
base_dir = '/Users/markoates/.gemini/antigravity-cli/brain'
def get_file_hash(filepath):
    h = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return "hash_error"

out_file = 'scripts/ai_subagent_proposals.json'
existing = []
if os.path.exists(out_file):
    with open(out_file, 'r', encoding='utf-8') as f:
        existing = json.load(f)

existing_ids = set(e['identifier'] for e in existing)
output_proposals = []

for cid in os.listdir(base_dir):
    transcript_path = os.path.join(base_dir, cid, '.system_generated', 'logs', 'transcript_full.jsonl')
    if not os.path.exists(transcript_path):
        transcript_path = os.path.join(base_dir, cid, '.system_generated', 'logs', 'transcript.jsonl')
    
    if not os.path.exists(transcript_path): continue
    
    image_path = None
    json_output = None
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
            except: continue
            if data.get('source') == 'USER_EXPLICIT' and 'Analyze the following image' in data.get('content', ''):
                content = data['content']
                for l in content.split('\n'):
                    if '/Users/markoates/Assets/' in l:
                        image_path = l.strip()
            
            if data.get('source') == 'MODEL' and 'catalog_proposal' in data.get('content', ''):
                content = data['content']
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0]
                try:
                    json_output = json.loads(content)
                except:
                    pass
    
    if image_path and json_output:
        rel_path = image_path.replace("/Users/markoates/Assets/", "")
        vendor = rel_path.split("/")[0]
        pack = rel_path.split("/")[2] if "extracted" in rel_path else rel_path.split("/")[1]
        name = os.path.splitext(os.path.basename(rel_path))[0]
        
        proposed = json_output.get("catalog_proposal", {})
        safe_rel_path = rel_path.replace('.', '_')
        deterministic_id = f"synthetic/{safe_rel_path}"
        
        if deterministic_id not in existing_ids:
            asset_dict = {
                "identifier": deterministic_id,
                "name": name,
                "asset_pack_identifier": f"{vendor}/{pack}",
                "type": proposed.get("type", "unknown"),
                "perspective": proposed.get("perspective", "unknown"),
                "is_subframe": proposed.get("is_subframe", False),
                "is_icon": proposed.get("is_icon", False),
                "visibility": "public",
                "sheet_row_number": None,
                "resource": {
                    "type": proposed.get("type", "unknown"),
                    "source_files": [f"/Assets/{rel_path}"],
                    "cell_dimensions": proposed.get("cell_dimensions"),
                    "inferred_grid": proposed.get("inferred_grid"),
                    "hash": get_file_hash(image_path)
                },
                "theme_profile": json_output.get("theme_profile", {}),
                "inference_reasoning": json_output.get("inference_reasoning", []),
                "color_profile": {
                    "color_space": "unknown",
                    "palette": [],
                    "is_exact_palette": False,
                    "palette_swappable": False
                },
                "ai_audit": {
                    "pass1_model": "antigravity-flash-lite-batch81",
                    "pass1_timestamp": "2026-09-13T03:14:00-04:00"
                }
            }
            output_proposals.append(asset_dict)
            existing_ids.add(deterministic_id)

print(f"Extracted {len(output_proposals)} NEW assets")
if output_proposals:
    existing.extend(output_proposals)
    with open(out_file + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)
    os.rename(out_file + '.tmp', out_file)
    print(f"Saved to {out_file}")
