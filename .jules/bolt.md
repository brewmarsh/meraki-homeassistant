## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-10-02 - Refactoring Multiple Sequential List Comprehensions
**Learning:** Multiple sequential list comprehensions that operate on the same source data (e.g. `[k for k in keys if ...]`) introduce an O(k*N) iteration overhead and create intermediate list allocations in memory.
**Action:** Refactor sequential list comprehensions into a single explicit `for` loop to execute all filters in a single O(N) pass, reducing time complexity and memory usage.
