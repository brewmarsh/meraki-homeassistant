## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - Single-Pass Iteration for Multiple Filters
**Learning:** Using multiple list comprehensions on the same dataset (especially with loop invariant logic inside) is inefficient and adds bytecode execution overhead.
**Action:** Extract invariant logic outside the loop using standard conditional branching to select the appropriate O(N) strategy upfront.
