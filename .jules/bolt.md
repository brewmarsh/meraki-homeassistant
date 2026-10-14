## 2024-05-18 - Single-Pass Iteration for Multiple Filters
**Learning:** Performing multiple list comprehensions sequentially to filter the same list based on independent criteria creates a hidden O(k*N) inefficiency and unnecessary intermediate memory allocations.
**Action:** Refactor multiple list comprehensions into a single comprehension with combined logical conditions (`if A or B`) to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
