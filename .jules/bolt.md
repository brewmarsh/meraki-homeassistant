## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-07-27 - [Home Assistant Property Caching]
**Learning:** Home Assistant executes property getters like `native_value` and `extra_state_attributes` very frequently. Performing O(N) filtering inside these methods causes hidden performance penalties, especially when multiple properties re-filter the same data.
**Action:** Pre-calculate and cache required data subsets (like a list of offline devices) in update hooks (e.g. `_compute_device_cache`) so that property getters only execute O(1) reads (e.g. `len(cache)`).
