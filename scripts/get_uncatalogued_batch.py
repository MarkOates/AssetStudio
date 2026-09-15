import json
import sys
import os

def get_next_batch(n_items):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    viewer_data_path = os.path.join(base_dir, 'web', 'viewer_data.json')
    proposals_path = os.path.join(base_dir, 'scripts', 'ai_subagent_proposals.json')

    # Load uncatalogued paths
    with open(viewer_data_path, 'r', encoding='utf-8') as f:
        viewer_data = json.load(f)
    
    uncatalogued = [
        e["context"]["file"] for e in viewer_data.get("errors", []) 
        if e.get("type") == "UncataloguedFile" and "file" in e.get("context", {})
    ]

    # Load already proposed paths
    proposed_paths = set()
    if os.path.exists(proposals_path):
        with open(proposals_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.strip():
                proposals = json.loads(content)
                for p in proposals:
                    if "resource" in p and "source_files" in p["resource"]:
                        for sf in p["resource"]["source_files"]:
                            proposed_paths.add(sf.replace("/Assets/", ""))

    # Find fresh targets
    fresh_targets = []
    for target in uncatalogued:
        if target not in proposed_paths:
            fresh_targets.append(target)
            if len(fresh_targets) >= n_items:
                break

    for target in fresh_targets:
        print(target)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    get_next_batch(n)
