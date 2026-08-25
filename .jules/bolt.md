## $(date +%Y-%m-%d) - [Optimize memory allocation for appliance connected clients]
**Learning:** Found a pattern where intermediate lists were created using list comprehensions solely to take their `len()` to count items in a hot update loop (running on every sensor update). This increases memory allocation and garbage collection overhead.
**Action:** Replace `len([x for x in list if condition])` with `sum(1 for x in list if condition)` to leverage O(1) space complexity via generator expressions for all counting logic.
