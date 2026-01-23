#!/bin/bash
set -e

echo "Installing uv..."
pip install uv

echo "Upgrading build tools..."
uv pip install --system --upgrade pip setuptools "wheel>=0.46.2"

echo "Installing dependencies..."
uv pip install --system --prerelease=allow -r requirements_dev.txt

# Force reinstall aiodns and pycares to match Python 3.13 compatibility requirements
# even if Home Assistant pins older versions.
echo "Force reinstalling aiodns and pycares..."
uv pip uninstall --system pycares aiodns
uv pip install --system --no-cache-dir aiodns==3.6.1 pycares==4.11.0

export PYTHONPATH=$PYTHONPATH:.
echo "PYTHONPATH: $PYTHONPATH"

echo "Running tests..."
python -m pytest

echo "Running ruff..."
python -m ruff check .

echo "Running bandit..."
python -m bandit -c .bandit.yaml -r .

echo "Running pip-audit..."
export PIP_AUDIT_IGNORE_VULN='GHSA-6mq8-rvhq-8wgg GHSA-69f9-5gxw-wvc2 GHSA-6jhg-hg63-jvvf GHSA-g84x-mcqj-x9qq GHSA-fh55-r93g-j68g GHSA-54jq-c3m8-4m76 GHSA-jj3x-wxrx-4x23 GHSA-mqqc-3gqh-h2x8 PYSEC-2020-49 PYSEC-2022-42969 GHSA-g7vv-2v7x-gj9p GHSA-mq77-rv97-285m GHSA-pp3g-xmm4-5cw9 GHSA-9548-qrrj-x5pj GHSA-hx9q-6w63-j58v GHSA-79v4-65xg-pq4g GHSA-cpwx-vrp4-4pq7 GHSA-9hjg-9r4m-mvj7 GHSA-8qf3-x8v5-2pj8 GHSA-w476-p2h3-79g9 GHSA-pqhf-p39g-3x64 GHSA-pq67-6m6q-mj2v GHSA-gm62-xv2j-4w53 GHSA-2xpw-w6gg-jr37 GHSA-38jv-5279-wg99 GHSA-8rrh-rw8j-w5fx'

IGNORE_ARGS=""
for vul in $PIP_AUDIT_IGNORE_VULN; do
  IGNORE_ARGS="$IGNORE_ARGS --ignore-vuln $vul"
done
python -m pip_audit -r custom_components/meraki_ha/requirements.txt -l $IGNORE_ARGS

echo "All checks passed!"
