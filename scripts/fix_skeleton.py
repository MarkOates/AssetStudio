import json

path = "scripts/ai_catalog_proposals.json"
with open(path, "r") as f:
    data = json.load(f)

# Keep everything except the 5 synthetic assets we generated
data = [d for d in data if "skeleton_variation1" not in d["name"]]
with open(path, "w") as f:
    json.dump(data, f, indent=2)
