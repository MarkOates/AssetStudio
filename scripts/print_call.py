import sys
import json

paths = sys.stdin.read().strip().split('\n')
subagents = []
for i, path in enumerate(paths):
    if not path.strip(): continue
    abs_path = "/Users/markoates/Assets/" + path.strip()
    subagents.append({
        "Model": "flash_lite",
        "Role": f"VI{i+1}",
        "TypeName": "visual_inferencer_v2",
        "Prompt": f"Analyze: {abs_path}"
    })

print(json.dumps({"Subagents": subagents, "toolAction": "Spawning batch", "toolSummary": "Spawn 50"}))
