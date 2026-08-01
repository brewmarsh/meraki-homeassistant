## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-08-01 - O(N) operations in HA Sensor properties
**Learning:** Property getters like `native_value` and `extra_state_attributes` in Home Assistant sensors are evaluated frequently. Including O(N) operations (e.g. list comprehension or summing counts over lists) within these properties degrades performance and can block the main loop.
**Action:** Pre-calculate and cache the results of O(N) operations during coordinator data updates (in a `_compute_device_cache()` method) to provide O(1) property access.
