## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-19 - Home Assistant Entity Properties Event Loop Bottlenecks
**Learning:** Home Assistant dynamic getters like `@property def native_value(self)` and `@property def extra_state_attributes(self)` are evaluated repeatedly by the HA event loop, not just on state updates. Using iteration (O(N) operations) directly inside these properties creates significant main event loop overhead, especially when parsing data such as device ports.
**Action:** Avoid iterations in property getters. Instead, iterate once within the `_handle_coordinator_update` method when new data actually arrives, storing the pre-calculated final values in class attributes (e.g., `_attr_native_value` and `_attr_extra_state_attributes`) for fast O(1) access.
