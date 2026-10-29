## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-10-29 - Generator vs Loop Overhead in Hot Loops
**Learning:** Using `sum(1 for x in data if condition)` creates an implicit generator, adding function call and yield overhead. In performance-critical counting loops (like parsing large client lists for network health), this overhead becomes noticeable.
**Action:** Replace `sum(1 for ...)` with explicit `for` loop counters (`count = 0; for x in data: if condition: count += 1`) in hot paths for ~10-15% faster execution.
