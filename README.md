# AssetStudio

**Domain Overview: AssetStudio**
AssetStudio is an automated, AI-driven pipeline designed to extract, analyze, and catalog raw game assets (such as sprite sheets, tilesets, UI elements, and VFX). The system processes raw archives and turns them into a structured, searchable catalog.

**Key Systems & Policies:**

1. **Extraction Policy (Data Integrity First)**
   - Archives are processed under strict read-only constraints in `/Users/markoates/Assets/` to preserve original files.
   - Extractions happen flatly into a dedicated `extracted/` subdirectory for each pack.
   - Extraction state and permissibility are managed meticulously via a `packs.json` database, enforcing file-locking and automation safety flags (like `can_be_extracted_by_automation`).

2. **Inference Pipeline**
   - **Phase 1 (Visual Inference):** Analyzes individual asset files (e.g., a `.png`) to deduce technical properties (like dimensions, frames, type) and themes based on **16 Formalized Rules** (handling things like `_strip<N>` naming conventions, grid deductions, and camera perspectives).
   - **Phase 2 (Structural Inference):** Analyzes directory structures and vendor metadata to group individual files into cohesive parent assets (like multi-file animations or atlases).

3. **Execution & Agentic Workflow**
   - Inference can run via high-volume Google AI API batch scripts (`scripts/phase1_visual_inference.py`) or via **Antigravity Orchestrated Subagents**.
   - Subagents are strictly controlled: they use fast models (`flash_lite`), have no filesystem write access, and must output strictly validated JSON proposals.
   - Database writes are handled safely via a consolidation pipeline (`scripts/auto_process.sh`) that extracts subagent transcripts, applies an `ai_audit` trail, uses OS-level file locking, and triggers a frontend UI rebuild.
