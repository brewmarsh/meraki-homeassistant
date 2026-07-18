## 2025-05-14 - Prevent List Allocation For Counting
**Learning:** Found instances where `len([x for x in list if condition])` was used. This creates a full list in memory just to get the length.
**Action:** Use a generator expression instead with `sum(1 for x in list if condition)` to save memory and avoid an intermediate list allocation. This improves performance inside `network_control_service.py` where client dictionaries are counted.
