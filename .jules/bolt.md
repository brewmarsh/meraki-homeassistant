## 2024-05-18 - List Comprehensions vs Generator Expressions in length checks
**Learning:** `len([x for x in data if condition])` builds an entire intermediate list in memory just to count elements.
**Action:** Replace with `sum(1 for x in data if condition)` to save memory and CPU cycles when only the count is needed. This codebase has instances of this in `custom_components/meraki_ha/services/network_control_service.py`.
