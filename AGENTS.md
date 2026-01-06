# `AGENTS.md`: AI Agent Guidelines

**This document is for AI agents working on this codebase.** Human developers should refer to the `DEVELOPMENT.md` file for instructions.

## 1. Core Mission

Your primary goal is to assist human developers by performing well-defined tasks, such as fixing bugs, adding features, and refactoring code. You must do so in a way that is consistent with the project's standards and conventions.

## 2. Onboarding & Project-Specifics

Before starting any task, you **must** familiarize yourself with the project by reviewing the following files:

- **`README.md`**: To understand the project's purpose and high-level structure.
- **`DEVELOPMENT.md`**: To understand the development environment, coding standards, and architectural principles.
- **`pyproject.toml`** or **`package.json`**: To understand the project's dependencies and available scripts.

## 3. Tool Usage

- **Be precise with your tool calls.** Do not use vague or ambiguous parameters.
- **Use the `read_file` tool** to get the exact content of a file before modifying it.
- **Use the `replace` tool** for making targeted changes to files. Be sure to provide enough context in the `old_string` to avoid ambiguity.
- **Use the `run_shell_command` tool** for running commands. Be mindful of the user's operating system and use the correct syntax.
- **When in doubt, ask.** If you are unsure about how to proceed, or if a user's request is ambiguous, ask for clarification.

## 4. Code Contributions

- **Follow all coding standards and best practices** outlined in the `DEVELOPMENT.md` file.
- **Run all quality checks** before submitting your changes.
- **Write clear and concise commit messages** that follow the Conventional Commits format.

## 5. Self-Correction and Learning

- If you make a mistake, acknowledge it and correct it.
- If you discover a new technique or a better way of doing something, incorporate it into your future work.
- If you encounter a new tool or a new version of a tool, read its documentation to understand how to use it correctly.
