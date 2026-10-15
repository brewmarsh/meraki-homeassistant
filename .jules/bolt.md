## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-10-15 - Single Pass List Comprehension Filtering
**Learning:** Sequential list comprehensions that filter the same source data create unnecessary intermediate list allocations in memory.
**Action:** Refactor multiple sequential list comprehensions into a single list comprehension using logical operators (`and`/`or`) to achieve the same filtering in a single O(N) pass, eliminating intermediate memory allocations.
