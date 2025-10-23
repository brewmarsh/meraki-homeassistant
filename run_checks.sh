#!/bin/bash
set -e

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
pytest

echo "Running flake8..."
flake8 .

echo "Running bandit..."
bandit -c .bandit.yaml -r .

echo "All checks passed!"
