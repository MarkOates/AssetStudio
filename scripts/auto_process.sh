#!/bin/bash
python3 scripts/process_all_transcripts.py --orchestrator big-boss --orchestrator-model gemini-3.1-pro
bash scripts/rebuild_ui_data.sh
