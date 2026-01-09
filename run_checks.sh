#!/bin/bash
set -e

# ============================================
# Check for uv package manager FIRST
# ============================================
if ! command -v uv &> /dev/null; then
    echo "============================================"
    echo "uv is not installed - installing with pip..."
    echo "============================================"
    pip install uv

    # Verify installation worked
    if ! command -v uv &> /dev/null; then
        echo ""
        echo "ERROR: Failed to install uv with pip."
        echo ""
        echo "Try installing manually:"
        echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
        echo "  brew install uv  (macOS)"
        echo ""
        echo "See: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
    echo "✅ uv installed successfully!"
    echo ""
fi

echo "============================================"
echo "Running local checks (mirrors CI pipeline)"
echo "============================================"
echo ""
echo "Using uv package manager..."
echo "Installing/syncing dependencies (including dev)..."
uv sync --all-extras --frozen 2>/dev/null || uv sync --all-extras

# Use uv run to execute commands in the virtual environment
RUFF="uv run ruff"
BANDIT="uv run bandit"
MYPY="uv run mypy"
PYTEST="uv run pytest"

echo ""
echo "1/5 Running ruff check..."
$RUFF check custom_components/meraki_ha/ tests/

echo ""
echo "2/5 Running ruff format check..."
$RUFF format --check custom_components/meraki_ha/ tests/

echo ""
echo "3/5 Running bandit security check..."
$BANDIT -r custom_components/meraki_ha/ -c pyproject.toml -q

echo ""
echo "4/5 Running mypy type check..."
$MYPY custom_components/meraki_ha/ tests/

echo ""
echo "5/5 Running pytest..."
$PYTEST tests/ -x -q --ignore=tests/test_e2e_web_ui.py

echo ""
echo "============================================"
echo "✅ All checks passed!"
echo "============================================"
