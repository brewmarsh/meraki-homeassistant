## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-18 - List Comprehension Refactoring
**Learning:** Multiple sequential list comprehensions filtering the same source data can lead to unnecessary intermediate allocations. However, replacing standard Pythonic generator expressions (like `sum(1 for ...)`) with manual loop counters is a micro-optimization that degrades readability for unmeasurable performance gains and should be avoided.
**Action:** Refactor sequential list comprehensions into single-pass filters or explicit early returns to prevent redundant intermediate allocations, but preserve clean, Pythonic idioms (like generator expressions) when the overhead is practically non-existent.
