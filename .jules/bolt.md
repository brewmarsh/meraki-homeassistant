## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - [MerakiPoeUsageSensor Performance Improvement]
**Learning:** Home Assistant's architecture reads sensor properties like `native_value` and `extra_state_attributes` frequently on the main event loop. If these getters contain O(N) operations like list comprehension or sums, it creates a bottleneck and wastes CPU.
**Action:** Move O(N) data aggregations into an `_update_state()` method that runs only when new data arrives from the coordinator, assigning results to simple `_attr_*` variables.
