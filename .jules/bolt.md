## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2026-10-19 - Single-Pass List Filtering
**Learning:** Sequential list comprehensions acting as chained filters (e.g., `[x for x in data if cond1]` followed by `[x for x in data if cond2]`) create unnecessary intermediate list allocations in memory and execute multiple O(N) passes.
**Action:** Combine multiple filtering conditions into a single list comprehension using logical operators (`and`/`or`) to achieve O(N) filtering in a single pass without intermediate memory allocation.
