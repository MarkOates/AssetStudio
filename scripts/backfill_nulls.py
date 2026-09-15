import json
import os

files = [
    "scripts/ai_subagent_proposals.json",
    "scripts/ai_catalog_proposals.json"
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
        
    with open(file_path, "r") as f:
        data = json.load(f)
        
    updated = False
    for item in data:
        if "ai_audit" not in item:
            item["ai_audit"] = {}
            
        audit = item["ai_audit"]
        
        # Check and set null for older rows
        if "run_id" not in audit:
            audit["run_id"] = None
            updated = True
        if "orchestrator_agent" not in audit:
            audit["orchestrator_agent"] = None
            updated = True
        if "orchestrator_agent_model" not in audit:
            audit["orchestrator_agent_model"] = None
            updated = True
            
    if updated:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Backfilled nulls in {file_path}")
    else:
        print(f"No backfill needed for {file_path}")
