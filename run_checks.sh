#!/bin/bash
set -e

echo "Installing uv..."
pip install uv

echo "Installing dependencies..."
uv pip install --system --prerelease=allow -r requirements_test.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
# even if Home Assistant pins older versions.
echo "Force reinstalling aiodns and pycares..."
uv pip install --system --force-reinstall aiodns==3.6.1 pycares==4.11.0

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
python -m pytest

echo "Running ruff..."
python -m ruff check .

echo "Running bandit..."
python -m bandit -c .bandit.yaml -r .

echo "All checks passed!"
