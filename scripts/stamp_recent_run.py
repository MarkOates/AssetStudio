import json

with open("scripts/ai_subagent_proposals.json", "r") as f:
    data = json.load(f)

# Update the last 48 items (the ones just completed)
for item in data[-48:]:
    if "ai_audit" not in item:
        item["ai_audit"] = {}
    item["ai_audit"]["orchestrator_agent_model"] = "gemini-3.1-pro"

with open("scripts/ai_subagent_proposals.json", "w") as f:
    json.dump(data, f, indent=2)

print("Updated last 48 assets with orchestrator_agent_model.")
