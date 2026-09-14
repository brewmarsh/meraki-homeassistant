## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.
## 2024-05-18 - [MerakiPoeUsageSensor Performance Improvement]
**Learning:** Home Assistant's architecture reads sensor properties like `native_value` and `extra_state_attributes` frequently on the main event loop. If these getters contain O(N) operations like list comprehension or sums, it creates a bottleneck and wastes CPU.
**Action:** Move O(N) data aggregations into an `_update_state()` method that runs only when new data arrives from the coordinator, assigning results to simple `_attr_*` variables.

## 2024-05-18 - [MerakiPoeUsageSensor Mypy Fix]
**Learning:** Home Assistant's `_attr_native_value` can technically hold a variety of generic types (like `date`, `str`, or `Decimal`) according to its base class (`SensorEntity` or `Entity`). So if a subclass defines `def native_value(self) -> float | None:`, returning `self._attr_native_value` directly will trigger mypy errors (`str | int | float | date | Decimal | None` incompatible with `float | None`).
**Action:** When overriding generic property getters to return `self._attr_native_value` using a specific union type, use `isinstance()` checks and explicit casts (e.g., `if isinstance(val, (int, float)): return float(val)`) to satisfy the type checker before returning the cached value.
