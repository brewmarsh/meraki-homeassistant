#!/bin/bash
set -e

echo "Running tests..."
pytest

echo "Running flake8..."
flake8 .

echo "Running bandit..."
bandit -r .

echo "All checks passed!"
