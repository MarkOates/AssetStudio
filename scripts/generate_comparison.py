import json
import os

with open('scripts/canary_expensive.json') as f:
    exp = json.load(f)
with open('scripts/canary_cheap.json') as f:
    chp = json.load(f)

md = "# Raw JSON Output Comparison\n\n"

for asset_key in exp.keys():
    e_val = exp[asset_key]
    c_val = chp.get(asset_key, {})
    
    md += f"## {asset_key}\n\n"
    
    md += "| Field | 💰 Expensive (3.8 Flash) | 🪙 Cheap (3.5 Flash Lite) |\n"
    md += "| --- | --- | --- |\n"
    
    # Theme Profile
    e_theme = e_val.get("theme_profile", {})
    c_theme = c_val.get("theme_profile", {})
    md += f"| **Description** | {e_theme.get('description', '')} | {c_theme.get('description', '')} |\n"
    md += f"| **Tags** | {', '.join(e_theme.get('tags', []))} | {', '.join(c_theme.get('tags', []))} |\n"
    md += f"| **Style** | {e_theme.get('style', '')} | {c_theme.get('style', '')} |\n"
    md += f"| **Colors** | {', '.join(e_theme.get('color_descriptors', []))} | {', '.join(c_theme.get('color_descriptors', []))} |\n"
    
    # Inference Reasoning
    e_reas = e_val.get("inference_reasoning", [])
    c_reas = c_val.get("inference_reasoning", [])
    
    e_reas_str = "<br>".join([f"**{r.get('rule')}**: {r.get('rationale')}" for r in e_reas])
    c_reas_str = "<br>".join([f"**{r.get('rule')}**: {r.get('rationale')}" for r in c_reas])
    md += f"| **Reasoning** | {e_reas_str} | {c_reas_str} |\n\n"

with open('/Users/markoates/.gemini/antigravity-cli/brain/9b10f025-657a-4016-852c-e88bb214a4a4/canary_side_by_side.md', 'w') as f:
    f.write(md)
print("Done")
