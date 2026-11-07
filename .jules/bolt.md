## 2024-05-18 - Single-Pass Iteration for Multiple Counts
**Learning:** Performing multiple `sum(1 for ...)` operations on the same list to extract different counts (like "critical" and "warning" alerts) creates a hidden O(k*N) inefficiency.
**Action:** Refactor multiple generator counts into a single `for` loop to perform an O(N) pass, reducing loop overhead and redundant dictionary lookups.

## 2024-05-19 - Conditional List Comprehensions
**Learning:** Sequential list comprehensions that filter the same source list for different conditions result in unnecessary list allocations. However, including loop-invariant conditions (e.g., `not param` or `item.id == param`) within a single comprehension is also an anti-pattern as the invariant is evaluated on every iteration.
**Action:** Use early return conditional branches (e.g., `if not param: return original`) to avoid allocations when possible, and use outer conditional statements (e.g., `if param and param2: return [...]`) to select the appropriate optimized single-pass comprehension.

## 2024-05-19 - CI Pipeline libturbojpeg Dependency
**Learning:** Ubuntu 26.04 no longer offers `libturbojpeg` as a package name, throwing a 'no installation candidate' error in GitHub Actions `ubuntu-latest` (which has migrated to Ubuntu 26). The new package name is `libturbojpeg0`.
**Action:** Always use `libturbojpeg0` for apt installations in CI pipelines to ensure cross-compatibility with Ubuntu 26.04+ runners.

## 2024-05-19 - Pytest Compatibility with Python 3.12+
**Learning:** `pytest<8.0.0` has compatibility issues with Python 3.12+ AST compilation, resulting in `TypeError: required field "lineno" missing from alias` when rewriting assertions.
**Action:** Ensure `pytest>=8.0.0` is used in Python 3.12+ environments.

## 2024-05-19 - Mypy Dependency Inclusion
**Learning:** `mypy` requires explicit dependency inclusion inline with `uv run` to resolve types for installed libraries without py.typed markers like `meraki` or `pytest-homeassistant-custom-component`. Alternatively, they can be ignored via `ignore_missing_imports = true` in `pyproject.toml`.
**Action:** Ignore missing imports for these testing/external libraries in `pyproject.toml` instead of cluttering CI commands with specific test deps just for linting.
