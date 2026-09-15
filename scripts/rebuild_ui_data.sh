#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Step 1: Rebuilding viewer data JSON payload..."
python3 "$SCRIPT_DIR/build_viewer_data.py"

echo "Viewer rebuild pipeline complete."
