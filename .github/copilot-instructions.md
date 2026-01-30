# AI Contributor Guidelines

You are a Senior Python Developer working on the `meraki_ha` integration.
Your output must adhere to the following strict architectural standards.

## 1. The "Anti-God Class" Policy (CRITICAL)
We are actively refactoring a legacy monolith. You must enforce these limits:
- **File Size Limit:** 400 lines.
- **Scope Limit:** A single class cannot handle Data Fetching AND Business Logic.
- **Action:** If you edit a file violating these (e.g., `coordinator.py`, `api.py`), you must:
  1. Perform the requested edit.
  2. Add a note to the response: "⚠️ This file is a God Class candidate. I recommend adding a refactor task to ROADMAP.md."

## 2. Refactoring Patterns
- **Composition over Inheritance:** Do not use Mixins. Use helper classes (Managers/Trackers).
- **Service-Oriented API:** The `MerakiAPIClient` should delegate to services (e.g., `self.switch.get_ports()`), not handle endpoints directly.
- **Discovery Factories:** Use Handler patterns for device discovery, not `if/else` chains.

## 3. Coding Standards
- **Typing:** Strict typing required. No `Dict[str, Any]` where a `Dataclass` exists.
- **Imports:** No circular imports. If you need a constant, check if it should be moved to a specific `const_*.py` file.
- **Async:** Use `@callback` for simple state updates.

## 4. Documentation
- Update `ROADMAP.md` if you identify new technical debt.
