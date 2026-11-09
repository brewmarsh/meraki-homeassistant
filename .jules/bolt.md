## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - Single-Pass Iteration for Multiple Filters
**Learning:** Performing sequential list comprehensions to build intermediate lists and then iterate over them again (e.g., filtering on `config_entry_id` then filtering the result on `network_id`) creates an O(k*N) inefficiency and unnecessary allocations.
**Action:** Refactor multiple filter loops into single optimized list comprehensions using standard conditional checks to select the right comprehension, avoiding intermediate lists and keeping iteration O(N).
