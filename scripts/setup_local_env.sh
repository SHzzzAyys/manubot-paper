#!/usr/bin/env bash

set -o errexit \
    -o nounset \
    -o pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_path="$repo_root/.venv"
requirements_path="$repo_root/requirements-local.txt"

echo "Repository root: $repo_root"
echo "Virtual environment: $venv_path"

python_cmd="${PYTHON:-python3}"

if [ ! -d "$venv_path" ]; then
  echo "Creating local virtual environment..."
  "$python_cmd" -m venv "$venv_path"
fi

source "$venv_path/bin/activate"

echo "Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing local requirements..."
python -m pip install -r "$requirements_path"

if command -v pandoc >/dev/null 2>&1; then
  echo "Pandoc detected: $(pandoc --version | head -n 1)"
else
  echo "WARNING: pandoc is not on PATH. Local HTML/PDF export will fail until pandoc is installed."
fi

echo
echo "Local environment is ready."
echo "Use it with:"
echo "  . .venv/bin/activate"
echo "  python scripts/validate_manuscript.py"
