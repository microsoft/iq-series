#!/bin/sh
set -eu

if [ -n "${SEED_SCRIPT:-}" ]; then
    script_dir="$(mktemp -d)"
    printf '%s' "$SEED_SCRIPT" > "$script_dir/seed_data.py"
    printf '%s' "$SEED_REQUIREMENTS" > "$script_dir/requirements.txt"
else
    script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
fi

echo "Installing seeding dependencies..."
python3 -m pip install --disable-pip-version-check --no-cache-dir -q -r "$script_dir/requirements.txt"
exec python3 -u "$script_dir/seed_data.py" "$@"
