#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements_dev.txt -r requirements_test.txt

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running ruff check..."
ruff check --fix .

echo "Running ruff format..."
ruff format .

echo "Running mypy..."
mypy --ignore-missing-imports custom_components/meraki_ha/ tests/

echo "Running bandit..."
bandit -r custom_components/meraki_ha/ -c .bandit.yaml

echo "Running tests..."
pytest

echo "All checks passed!"
