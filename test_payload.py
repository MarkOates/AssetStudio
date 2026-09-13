import json

targets = [f"file_{i}.png" for i in range(81)]
subagents = []
for t in targets:
    subagents.append({
        "Model": "flash_lite",
        "Prompt": f"Analyze the following image using your `view_file` tool:\n{t}\nOutput ONLY valid JSON matching the schema.",
        "Role": f"Analyze {t}",
        "TypeName": "strict_json_cataloger"
    })

print(len(json.dumps(subagents)))
