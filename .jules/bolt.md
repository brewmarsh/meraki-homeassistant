## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-19 - Merging Dependent Iterations
**Learning:** Extracting an initial subset via a generator/comprehension and subsequently looping over that subset creates an unnecessary O(N) + O(K) sequence. When generating both subsets from the same root data, combining the filtering logic into a single `for` loop prevents the second pass.
**Action:** Replace cascaded sequence comprehensions that filter the same source dataset (like device lists) with a single `for` loop that evaluates conditions and populates multiple lists simultaneously to guarantee O(N) execution.
