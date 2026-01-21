#!/bin/bash
set -e

echo "Installing dependencies..."
pip install "numpy>=1.26.0"
pip install -r requirements_test.txt

echo "Forcing DNS stack versions..."
pip install --force-reinstall "aiodns==3.6.1" "pycares==4.11.0"

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
pytest

echo "Running flake8..."
flake8 .

echo "Running bandit..."
bandit -c .bandit.yaml -r .

echo "All checks passed!"
