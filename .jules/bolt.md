## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2025-02-15 - [Optimize Connected Clients Counting]
**Learning:** Found a performance issue in `MerakiDeviceConnectedClientsSensor._update_state` where an intermediate list of matching network clients was created just to be immediately passed to `len()`, which introduces unnecessary memory allocation overhead in a hot loop when evaluating Home Assistant state on every event cycle.
**Action:** Replaced `len([x for x in list if cond])` with a generator expression `sum(1 for x in list if cond)`. This evaluates the condition and sums the length iteratively without allocating additional memory for an intermediate list, transitioning the operation's space complexity from O(N) to O(1).
