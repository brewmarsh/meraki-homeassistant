## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-19 - Conditional List Comprehensions
**Learning:** Sequential list comprehensions that filter the same source list for different conditions result in unnecessary list allocations. However, including loop-invariant conditions (e.g., `not param` or `item.id == param`) within a single comprehension is also an anti-pattern as the invariant is evaluated on every iteration.
**Action:** Use early return conditional branches (e.g., `if not param: return original`) to avoid allocations when possible, and use outer conditional statements (e.g., `if param and param2: return [...]`) to select the appropriate optimized single-pass comprehension.
