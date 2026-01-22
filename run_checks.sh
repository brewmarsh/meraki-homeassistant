#!/bin/bash
set -e

# Ensure uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv could not be found, installing..."
    pip install uv
fi

echo "Installing dependencies..."
uv pip install --system --prerelease=allow -r requirements_test.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
# even if Home Assistant pins older versions.
echo "Force reinstalling aiodns and pycares..."
uv pip install --system --force-reinstall aiodns==3.6.1 pycares==4.11.0

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
# Run pytest as a module to ensure it uses the correct environment
python -m pytest

echo "Running flake8..."
python -m flake8 .

echo "Running bandit..."
# Check if bandit is installed
if ! python -m bandit --version &> /dev/null; then
    echo "Bandit not found, installing..."
    uv pip install --system bandit
fi
python -m bandit -c .bandit.yaml -r .

echo "All checks passed!"
