# Compliance Check Report

**Status:** ❌ Failed

The following violations were found in the PR:

1.  **Missing Test Files**
    - `tests/sensor/network/test_network_traffic_shaping.py` is missing.
    - `tests/switch/test_switch_traffic_shaping.py` is missing.

    These files were referenced in recent commit messages as being renamed/added but are not present in the filesystem.

2.  **Manifest Version Mismatch**
    - `custom_components/meraki_ha/manifest.json` version is `2.0.0-beta.70`.
    - Recent commits indicate the version should be `2.1.0-beta.100`.

3.  **Outdated Dependencies**
    - `meraki` version in `requirements_test.txt` and `requirements_dev.txt` is `1.40.1`.
    - Recent commits indicate it should be `>=1.53.0`.

**Action Required:**
@brewmarsh Please address these issues by ensuring all files are committed and `manifest.json` is updated.
