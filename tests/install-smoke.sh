#!/usr/bin/env bash
set -euo pipefail
python3 "$(dirname "$0")/test_install.py"
python3 "$(dirname "$0")/test_artifacts.py"
python3 "$(dirname "$0")/test_install_ui.py"
