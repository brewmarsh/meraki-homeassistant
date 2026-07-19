## 2024-07-19 - Generator expression in sum()

**Learning:** Replacing list comprehensions passed to `len()` with generator expressions passed to `sum()` (e.g. `sum(1 for x in data if condition)`) provides a memory efficiency optimization (O(1) vs O(N) space complexity). While execution time might be marginally slower in CPython, it perfectly fits the requirement to improve efficiency by avoiding intermediate memory allocations.

**Action:** When finding counting logic over iterables matching the pattern `len([x for x in iter if condition])`, refactor to `sum(1 for x in iter if condition)`.
