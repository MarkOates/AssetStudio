# Inference Policy

Inference within the `AssetStudio` workflow is a multi-step, standardized process designed to categorize and architect game assets. Whether performed by direct API batch scripts, autonomous subagents, or programmatic Python rules, all inference MUST conform to the schema and guidelines outlined below.

## The Two Phases of Inference

The system processes raw uncatalogued assets through two distinct phases of inference.

### Phase 1: Initial Visual Inference (`scripts/phase1_visual_inference.py`)
In this phase, individual asset files (like a single `.png`) are analyzed visually and contextually to determine their raw technical properties.
* **Objective:** Produce a `catalog_proposal` and `theme_profile` for the raw file.
* **Mechanism:** Driven by the **16 Formalized Rules for Asset Inference**.
* **Output Schema:**
  ```json
  {
    "catalog_proposal": {
      "type": "animation_frames | static_image | etc...",
      "perspective": "top_down | side | etc...",
      "num_frames": 1,
      "cell_dimensions": {"width": 32, "height": 32},
      "is_subframe": false,
      "is_icon": false,
      "inferred_grid": null
    },
    "theme_profile": {
      "description": "...",
      "tags": [],
      "style": "...",
      "color_descriptors": []
    }
  }
  ```

### Phase 2: Structural Inference (`scripts/phase2_structural_inference.py`)
Once individual files are cataloged, this phase analyzes the entire directory structure and any provided vendor metadata files to group raw files into cohesive parent assets.
* **Objective:** Architect multi-file animations, atlases, or sets into logical groups.
* **Mechanism:** Driven by the **Reasoning Rules for Structural Inference** (e.g., *Rule 1: GraphicallySimilar*, *Rule 2: ProvidedVendorFile*).
* **Output Schema:** Produces `parent_assets` arrays that bundle multiple `source_files` and provide a structural `type` and `start_offset`.

---

## The Two Execution Strategies

The AssetStudio pipeline supports two distinct execution paths for AI inference, depending on the scale and complexity of the task:

1. **Google AI API (The Batch Script)**
   * **Mechanism:** Executed via `scripts/phase1_visual_inference.py`. This is a rigid, headless Python script that brute-forces direct REST API calls using the Google AI SDK (`google-generativeai`).
   * **Use Case:** High-volume, high-speed batch processing. It uses standard thread pools to process hundreds of thousands of files rapidly. It does not use external tools or conversational agents.

2. **Antigravity Orchestrated Subagents (The Agentic Workflow)**
   * **Mechanism:** The primary Antigravity AI orchestrator spawns and manages autonomous subagents dynamically (e.g., using the `visual_inferencer` custom profile).
   * **Use Case:** Tactical analysis requiring tooling. Unlike the raw API, subagents operate inside the workspace and have access to read-tools (like `view_file` or `search_web`), allowing them to investigate obscure assets or read local context before returning their payload to the orchestrator.

---

## Subagent Dispatch & Validation Workflow

When utilizing autonomous subagents to perform inference tasks asynchronously, the following strict workflow MUST be adhered to:

### 1. Subagent Dispatch & Tool Restrictions
* The orchestrator agent may dispatch multiple subagents concurrently to parallelize visual analysis across many assets.
* Subagents MUST be spawned using a highly restricted custom profile (e.g., `visual_inferencer`) rather than generic research templates.
* **Model Constraints:** Subagents should be invoked using the `flash_lite` model for speed, cost-efficiency, and strict adherence to rules without conversational deviation.
* **Tool Restrictions:** The subagent must have `enable_write_tools` and `enable_subagent_tools` set to `false` so it cannot modify the filesystem, write artifacts, or spawn its own agents. Read-only web searches are permitted (`enable_mcp_tools: true`) only as a fallback for identifying obscure assets.
* Each subagent must be explicitly instructed to respond with **strictly formatted, raw JSON** and nothing else.

### 2. Schema Validation Requirements
* The parent agent MUST NOT passively accept and "fix" malformed JSON (or "almost JSON") returned by a subagent.
* Before accepting a subagent's proposal, the response must be structurally validated against the schema. 
* This validation MUST be performed by writing the output to a temporary file and executing the **`scripts/validate_proposal.py`** script against it.
* If a subagent returns invalid JSON or fails the schema validation, the parent agent must reject the payload, reply to the subagent with the exact validation errors, and instruct it to output the correct response.

### 3. Concurrency, State Consolidation, & UI Sync (The Auto-Process Pipeline)
* Individual subagents MUST NOT write their results directly to the database themselves. Doing so will cause race conditions and file corruption.
* **The `auto_process.sh` Pipeline:** To streamline the consolidation and UI update without triggering constant unique command approvals, the orchestrator MUST run `bash scripts/auto_process.sh` after sweeping timeouts. 
* **Granular Context & What the Script Does:**
  * **Extraction:** It runs `scripts/process_all_transcripts.py`, which programmatically extracts the raw JSON directly from each subagent's `transcript.jsonl`. This avoids hallucination or truncation by the orchestrator.
  * **Audit Injection & Run ID:** The script automatically generates a unique 8-character hex `run_id` (so the orchestrator doesn't have to pass it dynamically) and injects the `"big-boss"` orchestrator name and model into the `ai_audit` block.
  * **File Locking:** The Python script appends the data to `scripts/ai_subagent_proposals.json` using an OS-level file lock (`fcntl.flock`) to prevent concurrent access corruption.
  * **UI Rebuild:** Finally, the bash script automatically runs `scripts/rebuild_ui_data.sh` to recompile `web/viewer_data.json` so the frontend updates immediately.
* **Batch Optimization Note:** Because the rebuild script takes a significant amount of time, the orchestrator should start up the next batch of subagents *before* running `auto_process.sh` (if there are any to deploy). This allows the next batch of asynchronous AI inference to process concurrently while the system compiles the UI payload.

## Starting the Viewer Server
To view the generated UI data in the frontend web application, run the following command in the root of the workspace:
```bash
python3 serve.py
```

### 5. Timeout Sweep Protocol
* To prevent orphaned background processes and infinite UI loading states caused by API rate limits or network drops, the orchestrator agent MUST enforce a strict **6-minute** timeout policy on all spawned subagents.
* *Context for Orchestrator:* While the hard kill limit is 6 minutes, subagents typically finish their analysis within **1 to 2 minutes**. The orchestrator should schedule periodic check-in timers (e.g., every 90 seconds) using `TimerCondition: 'never'` to wake up and check if the agents are finished, rather than waiting the full 6 minutes for every batch.
* **CRITICAL: Single Consolidation Rule:** The orchestrator MUST NOT run `auto_process.sh` until ALL subagents in the batch are either completely finished or have been killed at the 6-minute mark. Running it multiple times per batch will generate multiple `run_id`s, breaking the audit trail. `auto_process.sh` must be executed exactly ONCE at the absolute end of the batch.
* When executing the 6-minute sweep (or if an agent has hung), the orchestrator MUST use `manage_subagents` to list all currently running agents and forcefully kill any that have exceeded the timeout.

### 6. Orchestrator Reporting
* At the conclusion of each batch, the orchestrator MUST output a clear report to the user.
* The report MUST include:
  * The unique `run_id` generated for the batch.
  * The number of tasks that successfully merged into the database.
  * The number of tasks that failed or timed out.
  * Any interesting edge cases, anomalies, or notable reasoning that arose during the subagent swarm execution.

---

## Programmatic Metadata Extraction

While semantic and structural categorization is handled by AI models, strict quantitative metadata MUST be calculated deterministically using standard libraries (e.g., Python's `Pillow` or `hashlib`) prior to catalog injection.
* **Color Profiles**: The `color_profile` block (including exact dominant hex codes and palette extraction) is calculated programmatically using direct image processing, ensuring the AI does not hallucinate exact color values.
* **Cryptographic Hashes & Dimensions**: File hashes (`hash`) and physical bounds must be computed programmatically rather than inferred.

---

## The Audit Trail Standardization

To maintain strict traceability between the two different execution strategies, every inference proposal MUST include an `ai_audit` object when committed to the database. The previously fragmented `ai_metadata` block is deprecated in favor of a unified `ai_audit` schema.

When utilizing Antigravity Orchestrated Subagents, the subagents are not required to generate or format the `ai_audit` block themselves. The Orchestrator Agent (or its consolidation script) handles this transparently by automatically injecting the `ai_audit` metadata during the final database write.

All inference engines (or their orchestrators) must append the following block:
```json
"ai_audit": {
    "pass1_model": "<execution_environment_identifier>",
    "pass1_timestamp": "<iso_8601_timestamp>",
    "run_id": "<8_to_12_char_hex_hash>",
    "orchestrator_agent": "big-boss",
    "orchestrator_agent_model": "<e.g. gemini-3.1-pro>"
}
```
*(For Phase 2 inferences, use `pass2_model` and `pass2_timestamp`.)*

**Valid Execution Environment Identifiers:**
* **Google AI API Scripts:** Must cite the raw model name (e.g., `"gemini-3.5-flash-lite"` or `"gemini-flash-latest"`).
* **Antigravity Orchestrator:** Must cite the specific subagent profile codename injected by the orchestrator (e.g., `"subagent-strict-json-harriet1"`). The orchestrator itself (named `"big-boss"`) must inject its own model identifier (e.g., `"gemini-3.1-pro"`) and a unique `run_id` hash for the batch.
* **Programmatic/Deterministic:** Must cite the tool name (e.g., `"Tween Generator"`).

## Inference Reasoning Requirement
Every piece of inference logic must be backed by explicit reasoning. An `inference_reasoning` array must be generated for all deductions, citing the specific rule used:
```json
"inference_reasoning": [
  {
    "rule": "Rule 16: Perspective Analysis",
    "rationale": "The asset is drawn straight-on in a side perspective."
  }
]
```

---

## The 16 Formalized Rules for Asset Inference

* **Rule 1: Strip Suffix Matching** - If the filename matches `_strip<N>`, it is `animation_frames` with exactly `<N>` frames.
* **Rule 2: Embedded Resolution** - If the filename states a resolution like `16x16px`, these are likely the cell or tile dimensions.
* **Rule 3: Action Signatures** - Action verbs like `idle`, `walk`, `run`, `attack`, `jump`, `death` indicate character/entity animations.
* **Rule 4: Multi-File Sequences** - Filenames ending in sequential numbers denote a `multi_file_animation`. You must flag `is_subframe: true` because it is part of a sequence.
* **Rule 5: Environment/Tilesets** - Filenames with `tileset`, `map`, `bg`, `layer` are usually environmental. 
* **Rule 6: Parallax Backgrounds** - Wide aspect ratios or keywords like `sky`, `mountains`, `layers/`, `far`, `mid` indicate Background layers.
* **Rule 7: UI & HUD** - Keywords `gui`, `ui`, `border`, `cursor`, `icon` indicate interface elements.
* **Rule 8: Visual Effects (VFX)** - Keywords like `fx1_`, `explosion`, `spark`, `impact` denote particle/VFX assets.
* **Rule 9: Mockups & Previews** - Files containing `mockup`, `preview`, `sample` are valid `preview` assets and must be cataloged.
* **Rule 10: Variant Tagging** - Suffixes like `_shadow`, `_outline`, `100%`, `_c1` are variant modifiers that belong in tags.
* **Rule 11: Alternative Reasoning** - If you cannot find a specific rule that fits perfectly, state your own logical reasoning here.
* **Rule 12: Icons & Small Graphics** - If the asset is a very small standalone graphic (like 16x16 or 32x32) representing an item, weapon, material, or UI element, you must flag `is_icon: true`.
* **Rule 13: Visual Grid Deduction** - You MUST visually analyze sprite sheets. Do not just rely on the filename. Count the columns and rows to deduce exact pixel dimensions. If a single sheet contains MULTIPLE distinct animations on different rows, you MUST return a separate proposal for each animation sequence.
* **Rule 14: Type Definitions** - 
    - `animation_frames`: A discrete animation sequence, typically arranged as a 1D strip of frames.
    - `multi_directional_sprite`: A 2D grid containing the same animation rendered from multiple cardinal directions.
    - `sprite_sheet`: A 2D atlas containing multiple distinct animations or an atlas of distinct items.
    - `sprite_sheet_cell`: A single static asset intended to be extracted from a larger sheet.
    - `tileset`: An environmental grid of map tiles intended to be assembled in a level editor.
    - `multi_file_animation`: A single frame image belonging to a sequentially numbered directory of frames.
    - `static_image`: A standalone image containing no animation data.
    - `preview`: Vendor promotional art or layout mockups.
    - `sound_effect` / `music`: Audio files.
    - `pixel_font` / `ttf_font`: Typography files.
    - `3d_model`: 3D object files.
    - `text`: Documentation, license, or readme files.
* **Rule 15: Multi-Directional Character Sheets** - Character sprites arranged in grids where each row represents the same animation sequence from a different cardinal direction MUST be typed as `multi_directional_sprite` and interpreted as a single animation entity.
* **Rule 16: Perspective Analysis** - You MUST deduce the camera perspective of the asset (e.g., top_down, 3/4_isometric, side_scroller, ui_overlay, unknown) and provide your reasoning in the inference_reasoning array.
