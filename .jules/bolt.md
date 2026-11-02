## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-19 - Conditional List Comprehension vs Single Loop

**Learning:** Using multiple list comprehensions to filter by dynamic parameters inside a method (e.g., filtering `keys` by `network_id` and/or `config_entry_id`) creates unnecessary O(n) passes when both filters are applied. Returning early using standard conditional logic is faster than relying on a combined condition in a single loop when you can statically determine which specific list comprehension (filtering strategy) to use.
**Action:** When filtering a list by optional dynamic conditions, branch the code (using standard `if` statements) to evaluate the condition *outside* the loop, returning early or executing a single, minimal list comprehension rather than cramming condition checks inside the comprehension itself or iterating sequentially.
