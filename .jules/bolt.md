## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - Caching Property Lookups in Home Assistant Entities
**Learning:** Home Assistant entities frequently access property getters like `native_value` and `extra_state_attributes`. Performing O(N) operations (e.g., iterating over devices with `sum(1 for ...)`) within these getters is highly inefficient.
**Action:** Move expensive calculations (like counting offline devices) to a `_compute_device_cache` method that is called during coordinator data updates, and store the results in internal cache variables (e.g., `self._offline_devices_cache`) to provide O(1) access for properties.
