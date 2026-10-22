## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-19 - Consolidating List Comprehensions for Multiple Filters
**Learning:** Sequential list comprehensions filtering the same source list (e.g., `keys = [k for k in keys if cond1]`, then `keys = [k for k in keys if cond2]`) create unnecessary intermediate lists in memory and result in multiple O(N) passes.
**Action:** Refactor sequential list filtering into a single list comprehension using logical `and`/`or` to perform filtering in a single O(N) pass while avoiding intermediate allocations. Remember to handle cases where filter parameters are empty to prevent returning a full copy when a reference would suffice.
