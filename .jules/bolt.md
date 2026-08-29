## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-08-29 - [Optimize MerakiPoeUsageSensor Performance]
**Learning:** Home Assistant sensor getter properties (e.g., native_value, extra_state_attributes) are evaluated repeatedly. Doing O(N) list parsing inside these properties can be slow. Calculating values concurrently inside a single _update_state method on update events and caching them drastically speeds up evaluations and reduces overhead.
**Action:** Use an `_update_state()` method called during `_handle_coordinator_update` to process all O(N) loops exactly once per API sync. Pre-calculate values into cached `_attr_native_value` and `_attr_extra_state_attributes` properties.
