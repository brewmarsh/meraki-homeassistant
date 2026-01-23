#!/bin/bash
set -e

echo "Installing uv..."
pip install uv

echo "Installing dependencies..."
uv pip install --system --prerelease=allow -r requirements_dev.txt --overrides requirements_overrides.txt

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
python -m pytest

echo "Running ruff..."
python -m ruff check .

echo "Running bandit..."
python -m bandit -c .bandit.yaml -r .

echo "All checks passed!"