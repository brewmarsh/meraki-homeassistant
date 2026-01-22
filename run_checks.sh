#!/bin/bash
set -e

echo "Installing dependencies..."
uv pip install --system --prerelease=allow -r requirements_dev.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
echo "Force reinstalling aiodns and pycares..."
uv pip uninstall pycares aiodns || true
uv pip install --system --force-reinstall aiodns==3.6.1 pycares==4.11.0

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running Ruff..."
ruff check .
ruff format --check .

echo "Running Mypy..."
mypy --ignore-missing-imports custom_components/meraki_ha/ tests/

echo "Running Bandit..."
bandit -c .bandit.yaml -r custom_components/meraki_ha/

echo "Running Tests..."
python -m pytest

echo "All checks passed!"
