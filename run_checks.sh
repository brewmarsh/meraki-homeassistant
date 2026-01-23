#!/bin/bash
set -e

echo "Installing dependencies..."
# Use uv as in CI
uv pip install --system --prerelease=allow -r requirements_dev.txt -r requirements_test.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
echo "Force reinstalling aiodns and pycares..."
uv pip uninstall --system pycares aiodns
uv pip install --system --no-cache-dir pycares==4.11.0 aiodns==3.6.1

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
python -m pytest

echo "Running ruff check..."
python -m ruff check --fix .

echo "Running ruff format..."
python -m ruff format .

echo "Running bandit..."
python -m bandit -c .bandit.yaml -r .

echo "All checks passed!"
