## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2026-10-10 - Consolidating Sequential List Comprehensions
**Learning:** Multiple sequential list comprehensions filtering the same source data (like filtering keys by config entry, then network ID) create O(k*N) time complexity and redundant intermediate list allocations in memory.
**Action:** Refactor sequential list comprehensions into a single O(N) pass using logical operators (`and`/`or`) within a single comprehension to improve execution time and memory efficiency.
## 2026-10-10 - Home Assistant Typing Issue in CI
**Learning:** The `event.UnsubscribeFunc` type was historically used in Home Assistant but may be undefined or removed in newer environments/typing stubs, causing mypy and CI failures when strict checking is applied.
**Action:** Use `CALLBACK_TYPE` from `homeassistant.core` as the correct, forward-compatible type hint for unsubscription callbacks.
