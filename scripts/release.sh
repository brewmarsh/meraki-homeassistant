#!/bin/bash
#
# This script is the single source of truth for versioning.
# It uses the latest git tag to forcibly synchronize versions in configuration files,
# then calls bump-my-version to increment the version.
#
# Usage:
#   ./scripts/release.sh <part>
#
#   <part>: 'beta' to increment the patch version for a beta release.
#           'patch' to finalize a release (removes beta suffix).
#
set -euo pipefail

# --- Configuration ---
MANIFEST_FILE="custom_components/meraki_ha/manifest.json"
BUMP_CONFIG_FILE=".bumpversion.toml"

# --- Functions ---
function error_exit() {
  echo "Error: ${1}" >&2
  exit 1
}

# --- Main Script ---
# 1. Validate input
if [[ $# -ne 1 ]]; then
  error_exit "Usage: $0 <part>. Part must be 'beta' or 'patch'."
fi
PART="${1}"

# 2. Get the current version from .bumpversion.toml as the source of truth.
# This allows manual version jumps to be respected by the release process.
echo "Reading current version from ${BUMP_CONFIG_FILE}..."
VERSION=$(grep "^current_version =" "${BUMP_CONFIG_FILE}" | sed -E 's/current_version = "(.*)"/\1/')
if [[ -z "${VERSION}" ]]; then
  echo "Warning: Could not read version from ${BUMP_CONFIG_FILE}. Falling back to git tags."
  LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null) || error_exit "Failed to get latest git tag and no version found in config."
  VERSION="${LATEST_TAG#v}"
fi
echo "Current version identified as: ${VERSION}"

# Normalize bare version numbers (e.g., 112 -> 112.0.0)
if [[ "$VERSION" =~ ^[0-9]+$ ]]; then
  CLEAN_VERSION="${VERSION}.0.0"
  echo "Normalized version $VERSION to $CLEAN_VERSION for SemVer compatibility."
  VERSION=$CLEAN_VERSION
fi

# Normalize version numbers with missing components (e.g., 112.1 -> 112.1.0)
if [[ "$VERSION" =~ ^[0-9]+\.[0-9]+$ ]]; then
  CLEAN_VERSION="${VERSION}.0"
  echo "Normalized version $VERSION to $CLEAN_VERSION for SemVer compatibility."
  VERSION=$CLEAN_VERSION
fi

# Normalize version strings missing dots and build number (e.g., 112-beta -> 112.0.0-beta.1)
if [[ "$VERSION" =~ ^[0-9]+-[a-z]+$ ]]; then
  CLEAN_VERSION=$(echo "$VERSION" | sed -E 's/([0-9]+)-([a-z]+)/\1.0.0-\2.1/')
  echo "Normalized version $VERSION to $CLEAN_VERSION for tool compatibility."
  VERSION=$CLEAN_VERSION
fi

# 3. Force-synchronize version in manifest.json
echo "Syncing version in ${MANIFEST_FILE} to ${VERSION}..."
if ! jq --arg version "${VERSION}" '.version = $version' "${MANIFEST_FILE}" > "${MANIFEST_FILE}.tmp"; then
  error_exit "jq command failed to update ${MANIFEST_FILE}"
fi
mv "${MANIFEST_FILE}.tmp" "${MANIFEST_FILE}"
echo "Successfully synced ${MANIFEST_FILE}"

# 4. Force-synchronize version in .bumpversion.toml
echo "Syncing version in ${BUMP_CONFIG_FILE} to ${VERSION}..."
# Using a temp file for sed to be safe, as in-place editing can be tricky.
# We ensure the version string is double-quoted to maintain valid TOML syntax.
sed "s/^current_version = .*/current_version = \"${VERSION}\"/" "${BUMP_CONFIG_FILE}" > "${BUMP_CONFIG_FILE}.tmp"
mv "${BUMP_CONFIG_FILE}.tmp" "${BUMP_CONFIG_FILE}"
echo "Successfully synced ${BUMP_CONFIG_FILE}"

# 5. Determine which part to bump
BUMP_PART=""
case "${PART}" in
  beta)
    BUMP_PART="build"
    ;;
  patch)
    BUMP_PART="release"
    ;;
  *)
    error_exit "Invalid part '${PART}'. Must be 'beta' or 'patch'."
    ;;
esac

# 6. Run bump-my-version
echo "Running bump-my-version to bump the '${BUMP_PART}' part..."
# Using --allow-dirty because we have modified the files. The CI will commit them.
bump-my-version bump "${BUMP_PART}" --current-version "${VERSION}" --allow-dirty
echo "Version bump successful. New version has been written to files."
