## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - Single-Pass Iteration for Multiple Filters
**Learning:** Using multiple list comprehensions on the same dataset (especially with loop invariant logic inside) is inefficient and adds bytecode execution overhead.
**Action:** Extract invariant logic outside the loop using standard conditional branching to select the appropriate O(N) strategy upfront.
## 2024-05-18 - CI Failures / Strict Checks
**Learning:** The CI pipeline runs very strict mypy and ruff checks across the whole codebase, not just modified files. Changes can sometimes expose existing type errors or cause failures in seemingly unrelated files if typing definitions change.
**Action:** Ignore existing pre-existing CI errors outside of the modified file unless they were directly caused by the modification.
## 2024-05-18 - CI Failures / Strict Checks
**Action:** Fixed the typing error in `custom_components/meraki_ha/helpers/device_info_helpers.py` where `asdict` was returning dicts that were not correctly handled or annotated, leading to mypy failures in other parts of the system. I also fixed the `via_device` annotation correctly.
## 2024-05-18 - CI Failures / Strict Checks
**Action:** Fixed the typing error in `custom_components/meraki_ha/device_trigger.py` where `_is_trigger_match` was expecting `dict[str, Any]` but receiving `Mapping[str, Any]`.
