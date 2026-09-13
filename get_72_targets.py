import json, os
with open('web/viewer_data.json', 'r', encoding='utf-8') as f:
    vdata = json.load(f)
proposals = set()
for fp in ['scripts/ai_catalog_proposals.json', 'scripts/ai_subagent_proposals.json']:
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            for p in json.load(f):
                proposals.add(p['identifier'])
uncat_files = [e['context']['file'] for e in vdata.get('errors', []) if e['type'] == 'UncataloguedFile']
remaining = [u for u in uncat_files if f"synthetic/{u.replace('.', '_')}" not in proposals]
targets = remaining[-72:]
for t in targets:
    print(t)
