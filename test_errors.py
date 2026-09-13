import json

with open('web/viewer_data.json', 'r') as f:
    data = json.load(f)

resolved_files = set()
for a in data['assets']:
    if a['identifier'].startswith('synthetic/'):
        for sf in a['resource']['source_files']:
            rel = sf.replace('/Assets/', '', 1)
            resolved_files.add(rel)

filtered_errors = []
for err in data['errors']:
    if err['type'] == 'UncataloguedFile' and err['context'].get('file') in resolved_files:
        continue
    filtered_errors.append(err)

print(f"Original errors: {len(data['errors'])}")
print(f"Filtered errors: {len(filtered_errors)}")
