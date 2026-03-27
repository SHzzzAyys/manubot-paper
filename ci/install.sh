#!/usr/bin/env bash

## install.sh: install the local/CI Python environment using venv and pip.

set -o errexit \
    -o pipefail

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r ci/requirements-ci.txt

if [ "${SPELLCHECK:-}" = "true" ]; then
  bash ci/install-spellcheck.sh
fi
