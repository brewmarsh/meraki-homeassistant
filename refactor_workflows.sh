#!/bin/bash

# Exit on error
set -e

# Create validate-code.yml
cat > .github/workflows/validate-code.yml << EOL
name: Validate Code

on:
  push:
    branches: ['main', 'beta']
  pull_request:
    branches: ['main', 'beta']

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Set up Python 3.13
        id: setup-python
        uses: actions/setup-python@v6
        with:
          python-version: '3.13'
      - name: Cache pip dependencies
        uses: actions/cache@v4
        with:
          path: ./.venv
          key: \${{ runner.os }}-pip-\${{ steps.setup-python.outputs.python-version }}-\${{ hashFiles('**/requirements_dev.txt') }}
          restore-keys: |
            \${{ runner.os }}-pip-\${{ steps.setup-python.outputs.python-version }}-
      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          python -m pip install --upgrade pip
          pip install -r requirements_dev.txt
      - name: Archive venv
        run: tar -czf venv.tar.gz .venv
      - name: Upload venv artifact
        uses: actions/upload-artifact@v4
        with:
          name: venv
          path: venv.tar.gz

  ruff:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Download venv artifact
        uses: actions/download-artifact@v4
        with:
          name: venv
      - name: Extract venv
        run: tar -xzf venv.tar.gz
      - name: Run ruff
        run: |
          source .venv/bin/activate
          ruff check .
          ruff format --check .

  mypy:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Download venv artifact
        uses: actions/download-artifact@v4
        with:
          name: venv
      - name: Extract venv
        run: tar -xzf venv.tar.gz
      - name: Run mypy
        run: |
          source .venv/bin/activate
          mypy custom_components/meraki_ha/ tests/

  bandit:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Download venv artifact
        uses: actions/download-artifact@v4
        with:
          name: venv
      - name: Extract venv
        run: tar -xzf venv.tar.gz
      - name: Run bandit
        run: |
          source .venv/bin/activate
          bandit -r custom_components/meraki_ha/ -c .bandit.yaml

  pip-audit:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Download venv artifact
        uses: actions/download-artifact@v4
        with:
          name: venv
      - name: Extract venv
        run: tar -xzf venv.tar.gz
      - name: Run pip-audit
        run: |
          source .venv/bin/activate
          pip-audit --ignore-vuln PYSEC-2020-49 --ignore-vuln PYSEC-2022-42969 --ignore-vuln GHSA-g7vv-2v7x-gj9p

  pytest:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - name: Download venv artifact
        uses: actions/download-artifact@v4
        with:
          name: venv
      - name: Extract venv
        run: tar -xzf venv.tar.gz
      - name: Run tests with coverage
        run: |
          source .venv/bin/activate
          pytest --cov=custom_components.meraki_ha --cov-report=xml tests/
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v5
        with:
          token: \${{ secrets.CODECOV_TOKEN }}
          slug: brewmarsh/meraki-homeassistant
          files: ./coverage.xml

  validate-hacs:
    runs-on: 'ubuntu-latest'
    steps:
      - uses: actions/checkout@v5
      - name: HACS validation
        uses: 'hacs/action@main'
        with:
          category: 'integration'
EOL

# Create deploy-hacs.yml
cat > .github/workflows/deploy-hacs.yml << EOL
name: Deploy to HACS

on:
  pull_request:
    types: [closed]
    branches:
      - main
      - beta

jobs:
  version:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == true
    permissions:
      contents: write
      pull-requests: read
    outputs:
      new_version: \${{ steps.increment.outputs.new_version }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
          ref: \${{ github.base_ref }}

      - name: Set up Python and Node.js
        uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install bump2version
          npm install

      - name: Increment Version
        id: increment
        env:
          PR_TITLE: \${{ github.event.pull_request.title }}
        run: |
          if [[ "\${{ github.base_ref }}" == "beta" ]]; then
            bump2version --allow-dirty beta
          else
            increment_type="patch" # Default increment type
            if [[ "\$PR_TITLE" == *"[major]"* ]]; then
              increment_type="major"
            elif [[ "\$PR_TITLE" == *"[minor]"* ]]; then
              increment_type="minor"
            fi
            bump2version --allow-dirty \$increment_type
          fi
          new_version=\$(grep -oP '"version": "\K[^"]+' custom_components/meraki_ha/manifest.json)
          echo "new_version=\$new_version" >> "\$GITHUB_OUTPUT"

      - name: Update package.json version
        if: steps.increment.outputs.new_version != ''
        run: |
          echo "Synchronizing package.json version to: \${{ steps.increment.outputs.new_version }}"
          npm version \${{ steps.increment.outputs.new_version }} --no-git-tag-version --allow-same-version

      - name: Generate Changelog
        if: steps.increment.outputs.new_version != ''
        run: |
          npx conventional-changelog -p angular -i CHANGELOG.md -s
          # Generate release notes for the current version
          npx conventional-changelog -p angular -r 1 > RELEASE_NOTES.md

      - name: Commit and push changes
        if: steps.increment.outputs.new_version != ''
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'chore(release): update version to \${{ steps.increment.outputs.new_version }} and CHANGELOG'
          file_pattern: 'custom_components/meraki_ha/manifest.json CHANGELOG.md package.json .bumpversion.cfg package-lock.json'
          commit_user_name: "github-actions[bot]"
          commit_user_email: "github-actions[bot]@users.noreply.github.com"
          commit_author: "github-actions[bot] <github-actions[bot]@users.noreply.github.com>"
          branch: \${{ github.base_ref }}

      - name: Upload Release Notes
        if: steps.increment.outputs.new_version != ''
        uses: actions/upload-artifact@v4
        with:
          name: release-notes
          path: RELEASE_NOTES.md

  release:
    runs-on: ubuntu-latest
    needs: version
    if: needs.version.outputs.new_version != ''
    permissions:
      contents: write
    steps:
      - name: Download Release Notes
        uses: actions/download-artifact@v4
        with:
          name: release-notes

      - name: Create Release
        uses: softprops/action-gh-release@v2
        with:
          tag_name: 'v\${{ needs.version.outputs.new_version }}'
          name: 'Release v\${{ needs.version.outputs.new_version }}'
          body_path: 'RELEASE_NOTES.md'
          draft: false
          prerelease: \${{ github.base_ref == 'beta' }}
EOL

# Rename files
git mv .github/workflows/build-runner-image.yaml .github/workflows/tool-build-runner.yml
git mv .github/workflows/mkdocs-deploy.yaml .github/workflows/deploy-docs.yml
git mv .github/workflows/jules.yml .github/workflows/agent-jules.yml

# Update deploy-docs.yml
sed -i 's/name: Deploy MkDocs/name: Deploy Documentation/g' .github/workflows/deploy-docs.yml

# Update jules.yaml
cat > .github/jules.yaml << EOL
# .github/jules.yaml
instructions: "ALL Pull Requests must target the beta branch unless explicitly told otherwise."
project_context:
  primary_branch: main
  development_branch: beta
  coding_standards: 'Follow Home Assistant Core integration standards (PEP8, async/await).'
  ignored_errors: 'Ignore all errors not related to the meraki_ha integration.'
EOL

# Delete old files
git rm .github/workflows/beta-ci.yaml
git rm .github/workflows/main-ci.yaml
git rm .github/workflows/beta-version-update.yaml
git rm .github/workflows/production-version-update.yaml
git rm .github/workflows/beta-release.yml
git rm .github/workflows/hassfest.yaml
