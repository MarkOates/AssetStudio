import json, sys
vdata=json.load(open('web/viewer_data.json'))
p=set([e['identifier'] for e in json.load(open('scripts/ai_catalog_proposals.json'))] + [e['identifier'] for e in json.load(open('scripts/ai_subagent_proposals.json'))])
remaining=[u['context']['file'] for u in vdata.get('errors',[]) if u['type']=='UncataloguedFile' and f"synthetic/{u['context']['file'].replace('.','_')}" not in p]
batch = remaining[:20]
for file in batch:
  print(file)
