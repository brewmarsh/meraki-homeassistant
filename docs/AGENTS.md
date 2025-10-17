# Agent Guidelines for Documentation

Hello, fellow agent! This document provides guidelines for maintaining the documentation within this `docs` directory. Following these guidelines will ensure the documentation remains organized, consistent, and useful for everyone.

## 1. Documentation Structure

The documentation is organized into the following subdirectories. Before creating a new document, please check if a suitable location already exists.

- **`/requirements`**: For functional and non-functional requirements of the integration.
- **`/design`**: For high-level design specifications of new features.
- **`/architecture`**: For in-depth architectural discussions, refactoring plans, and developer setup guides.
- **`/testing`**: For test plans and quality assurance strategies.

The main entry point for the documentation is the `README.md` file in this directory.

## 2. Creating New Documents

**ALWAYS use the template.**

Before creating any new document, you **must** start by copying the contents of `template.md`. This ensures all documents have a consistent structure.

- **File Naming:** Use lowercase letters and underscores (`_`) instead of spaces (e.g., `new_feature_design.md`).
- **Location:** Place the new document in the most relevant subdirectory.

## 3. When to Create vs. When to Update

- **Update an existing document** if your changes are an incremental improvement or a minor correction to the information already present.
- **Create a new document** if you are documenting a completely new feature, a major architectural change, or a new set of requirements that don't fit well within an existing document.

## 4. Updating the Table of Contents

If you add a new major document that should be easily discoverable (e.g., a new top-level design document), you **must** also add a link to it in the main `README.md` file located in this `docs` directory.

---

Thank you for helping to keep our documentation clean and organized!
