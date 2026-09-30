## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - Single Pass Iteration Optimization
**Learning:** Refactoring multiple sequential generator expressions or list comprehensions (which each execute an O(N) pass) into a single explicit O(N) `for` loop can reduce iteration overhead and redundant attribute lookups, especially when processing potentially large data lists like network devices or switch port statuses.
**Action:** Always inspect list/dict comprehensions that operate on the same source data for opportunities to combine them into a single-pass processing loop to maximize loop efficiency.
