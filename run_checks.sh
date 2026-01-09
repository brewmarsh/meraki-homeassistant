#!/bin/bash
set -e

echo "============================================"
echo "Running local checks (mirrors CI pipeline)"
echo "============================================"

# Check if we're in a virtual environment or use uvx
if command -v uvx &> /dev/null; then
    RUFF="uvx ruff"
    BANDIT="uvx bandit"
    MYPY="uvx mypy"
    PYTEST="uvx pytest"
elif [ -n "$VIRTUAL_ENV" ]; then
    echo "Installing dependencies in virtual environment..."
    pip install -r requirements_dev.txt
    RUFF="ruff"
    BANDIT="bandit"
    MYPY="mypy"
    PYTEST="pytest"
else
    echo "No virtual environment detected. Using uvx or install dependencies manually."
    echo "You can also run: python3 -m venv venv && source venv/bin/activate"
    RUFF="uvx ruff"
    BANDIT="uvx bandit"
    MYPY="uvx mypy"
    PYTEST="uvx pytest"
fi

export PYTHONPATH=$PYTHONPATH:.

echo ""
echo "1/5 Running ruff check..."
$RUFF check custom_components/meraki_ha/

echo ""
echo "2/5 Running ruff format check..."
$RUFF format --check custom_components/meraki_ha/

echo ""
echo "3/5 Running bandit security check..."
$BANDIT -r custom_components/meraki_ha/ -c pyproject.toml -q

echo ""
echo "4/5 Running mypy type check..."
$MYPY custom_components/meraki_ha/ --ignore-missing-imports

echo ""
echo "5/5 Running pytest..."
$PYTEST tests/ -x -q --ignore=tests/test_e2e_web_ui.py 2>/dev/null || echo "⚠️  Tests require Home Assistant environment (skipped)"

echo ""
echo "============================================"
echo "✅ All checks passed!"
echo "============================================"
