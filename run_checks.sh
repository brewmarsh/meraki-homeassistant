#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements_test.txt

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

# echo "Running tests..."
# pytest

echo "Running pip-audit..."
pip-audit

echo "Running ruff..."
ruff check .

echo "Running bandit..."
bandit -c .bandit.yaml -r .

echo "All checks passed!"
