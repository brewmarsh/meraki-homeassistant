#!/bin/bash
set -e

# Install dependencies
pip install --upgrade pip
pip install -r requirements_dev.txt

# Run tests
pytest --cov=custom_components.meraki_ha tests/
