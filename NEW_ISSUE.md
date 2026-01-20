**Title:** `feat: Consolidated Logic from Legacy PRs`

**Body:**

This issue consolidates the features and fixes from several legacy pull requests to align with the new architectural standards defined in `AGENTS.md`.

### Harvested Logic Checklist

- [ ] **Port MT30 Sensor Logic (from PR #45)**
  - **Task:** Integrate the logic for supporting Meraki MT30 environmental sensors.
  - **Original Files:** `const.py`, `sensor.py`
  - **Notes:** This was a compliant implementation and can be ported with minimal changes.

- [ ] **Fix Config Flow to use Selectors (from PR #52)**
  - **Task:** Refactor the `config_flow.py` to use `homeassistant.helpers.selector` instead of raw `Voluptuous` types.
  - **Original Files:** `config_flow.py`
  - **Notes:** This is a mandatory change for compliance with modern Home Assistant standards.

- [ ] **Refactor Content Filtering Entity (from PR #61)**
  - **Task:** Re-implement the content filtering `Select` entity within the correct module to prevent name shadowing.
  - **Original Files:** `custom_components/meraki_ha/select.py`
  - **Required Changes:** The logic must be moved from the non-compliant `select.py` to a new file within the `custom_components/meraki_ha/meraki_select/` directory, as per the "Module Shadowing" rule in `AGENTS.md`.

### Action Items

1.  Implement the features listed above in a new branch targeting `beta`.
2.  Ensure all changes are fully compliant with `AGENTS.md`.
3.  Close the legacy PRs (#45, #52, #61) with a comment linking to this issue.
