#!/bin/bash
set -e

echo "Installing dependencies..."
pip install -r requirements_test.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
# even if Home Assistant pins older versions.
echo "Force reinstalling aiodns and pycares..."
pip install --force-reinstall aiodns==3.6.1 pycares==4.11.0

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
pytest

echo "Running flake8..."
flake8 .

echo "Running bandit..."
bandit -c .bandit.yaml -r .

echo "All checks passed!"
