import json

with open('scripts/ai_catalog_proposals.json', 'r') as f:
    proposals = json.load(f)

print(f"Total proposals before: {len(proposals)}")

# Remove any proposal where the type is "multi_file" or "sprite_sheet_slice"
new_proposals = [p for p in proposals if p['type'] not in ['multi_file', 'sprite_sheet_slice']]

print(f"Total proposals after: {len(new_proposals)}")
print(f"Purged: {len(proposals) - len(new_proposals)}")

with open('scripts/ai_catalog_proposals.json', 'w') as f:
    json.dump(new_proposals, f, indent=2)
