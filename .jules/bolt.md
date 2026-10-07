## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - Refactoring Multiple Sequential List Comprehensions
**Learning:** Using multiple list comprehensions sequentially to filter the same source data (like filtering `self.active_keys` twice) creates unnecessary intermediate list allocations and O(k*N) time complexity.
**Action:** Combine conditions using boolean operators (`and` / `or`) inside a single list comprehension or generator to achieve the filtering in one O(N) pass, preventing intermediate allocations.
