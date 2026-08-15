## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-08-15 - [O(1) property access for Home Assistant Sensors]
**Learning:** In Home Assistant, properties like `native_value` and `extra_state_attributes` are evaluated frequently on the main event loop. Performing O(N) operations inside these properties can cause performance issues.
**Action:** Always pre-calculate O(N) operations within `_update_state` or `_handle_coordinator_update` methods, which only run when new data arrives. Store the result in standard attributes like `_attr_native_value` for O(1) property access.
## 2026-08-15 - [Mypy Strict TypedDict assignments]
**Learning:** When using typed dictionaries or kwargs that are strictly typed in Home Assistant definitions (e.g., `DeviceInfo`), avoid passing `None` directly if the type doesn't allow it. For instance, `via_device` expects `tuple[str, str]` and not `tuple[str, str] | None` according to mypy in newer versions. Setting it via kwarg to `None` causes a mypy `typeddict-item` error.
**Action:** Initialize the `DeviceInfo` object first and add optional items (like `via_device`) dynamically to the dictionary (e.g. `info["via_device"] = (...)`) only if they are present.
