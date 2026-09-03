## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2025-02-23 - Bolt: Refactor PoE usage sensor
**Learning:** The HA core frequently evaluates property getters (e.g. `native_value`, `extra_state_attributes`) for sensor state representations. Iterating over long arrays inside these methods repeatedly incurs redundant O(N) operations.
**Action:** For sensor classes pulling from large list structures, implement a single-pass `_update_state` calculation method during data ingestion (e.g., in `__init__` and `_handle_coordinator_update`), caching the computed results in static attributes.
