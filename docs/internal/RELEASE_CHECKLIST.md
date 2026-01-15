# Release Checklist

This document outlines the steps to be taken before a new release of the Meraki Home Assistant Integration.

## Pre-Release

- [ ] All code has been merged into the `beta` branch.
- [ ] All required tests have passed.
- [ ] The `manifest.json` file has been updated with the new version number.
- [ ] The `CHANGELOG.md` file has been updated with the latest changes.

## Release

- [ ] A new release is created on GitHub with the new version number.
- [ ] The release notes are copied from the `CHANGELOG.md` file.
- [ ] The release is published.

## Post-Release

- [ ] The `main` branch is updated from the `beta` branch.
