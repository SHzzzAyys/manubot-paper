#!/usr/bin/env bash

set -o errexit \
    -o nounset \
    -o pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_path="$repo_root/.venv"

if [ ! -x "$venv_path/bin/manubot" ]; then
  echo "Local .venv is missing Manubot. Run scripts/setup_local_env.sh first." >&2
  exit 1
fi

export TZ=Etc/UTC
export LC_ALL=en_US.UTF-8
export PATH="$venv_path/bin:$PATH"

cd "$repo_root"

manubot process \
  --content-directory=content \
  --output-directory=output \
  --cache-directory=ci/cache \
  --skip-citations \
  --log-level=INFO
