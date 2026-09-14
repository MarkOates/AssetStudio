import json

raw_json = """{
  "catalog_proposal": {
    "type": "animation_frames",
    "perspective": "3/4_isometric",
    "num_frames": 17,
    "cell_dimensions": {"width": 96, "height": 64},
    "is_subframe": false,
    "is_icon": false,
    "inferred_grid": {
      "columns": 17,
      "rows": 1,
      "cell_width": 96,
      "cell_height": 64,
      "contains_multiple_animations": false,
      "inferred_animations": [
        {
          "name": "open",
          "row": 0,
          "start_frame": 0,
          "frame_count": 17,
          "inference_reasoning": [
            {
              "rule": "Rule 13: Visual Grid Deduction",
              "rationale": "Horizontal strip of 17 frames depicting a book opening sequence."
            }
          ]
        }
      ]
    }
  },
  "theme_profile": {
    "description": "A pixel art animation sequence showing a magical book opening from a closed state with glowing orange runes to a fully open green-paged tome.",
    "tags": ["book", "magic", "spellbook", "grimoire", "animation", "item", "open", "tweened"],
    "style": "Pixel Art",
    "color_descriptors": ["dark charcoal", "amber orange", "muted sage green"]
  },
  "inference_reasoning": []
}"""
data = json.loads(raw_json)

proposal = {
    "identifier": "synthetic/gemini/tweens/book-openning_tweened.png",
    "name": "book-openning_tweened",
    "asset_pack_identifier": "gemini/tweens",
    "type": data["catalog_proposal"]["type"],
    "is_subframe": data["catalog_proposal"]["is_subframe"],
    "is_icon": data["catalog_proposal"]["is_icon"],
    "visibility": "public",
    "sheet_row_number": None,
    "resource": {
        "type": data["catalog_proposal"]["type"],
        "source_files": ["/Assets/gemini/tweens/book-openning_tweened.png"],
        "cell_dimensions": data["catalog_proposal"]["cell_dimensions"],
        "inferred_grid": data["catalog_proposal"].get("inferred_grid")
    },
    "animation_profile": {
        "num_frames": data["catalog_proposal"]["num_frames"],
        "base_frame_duration": 0.05
    },
    "theme_profile": data["theme_profile"]
}

with open('scripts/ai_subagent_proposals.json', 'r') as f:
    proposals = json.load(f)

proposals.append(proposal)

with open('scripts/ai_subagent_proposals.json', 'w') as f:
    json.dump(proposals, f, indent=2)
