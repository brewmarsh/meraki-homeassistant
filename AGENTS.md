# Agent Guidelines

This document provides guidelines for agents working on this codebase.

## High-Level Recommendations

Based on a recent analysis of the codebase, the following high-level recommendations should be followed:

*   **Refactor to use `core` components:** The highest priority is to refactor the codebase to use the new `core` components and remove the old, redundant code. This will involve updating the platforms to use the new `core` entities and coordinators, and removing the old API client, coordinators, and entities.
*   **Improve Error Handling and Logging:** Enhance error catching, provide more user-friendly error messages, and ensure consistent logging across the integration.
*   **Optimize Data Retrieval:** Review API call patterns to optimize for performance and minimize API rate limit impact, especially for large organizations.

## 1. Code Style

- All Python code must adhere to the PEP 8 style guide.
- Use a linter like `flake8` or `pylint` to check for style issues before submitting code.
- Before submitting any changes, run `black` and `flake8` against the code to ensure it is formatted correctly and free of linting issues.

## 2. Documentation

- All public functions and classes must have comprehensive docstrings that explain their purpose, arguments, and return values.
- Use the Google Python Style Guide for docstring formatting.

## 6. Logging

- The integration uses the `logging` module to log messages.
- The logging level can be configured in the Home Assistant configuration.
- The logging messages should be informative and should include context, such as the function name and the arguments that were passed to the function.

## 7. Data Retrieval

- The integration uses a hybrid data retrieval strategy that combines polling with webhooks.
- The polling-based data retrieval strategy is implemented in the `core/coordinators` directory.
- The webhook-based data retrieval strategy is implemented in the `webhook.py` file.

## 3. Configuration

- All configuration data must be validated using `voluptuous` schemas.
- Provide clear error messages for invalid configuration.

## 4. Constants

- All constants must be defined in `custom_components/meraki_ha/const.py`.
- Do not use magic strings or numbers in the code.

## 5. Testing

- All new features must be accompanied by unit tests.
- Run the entire test suite before submitting code to ensure that no regressions have been introduced.
- Use chain-of-thought reasoning to ensure that you have solved the complete problem.

## 6. Dependencies

- Use `dependabot` or a similar tool to keep dependencies up-to-date.
- Regularly review and update dependencies as needed.

## 6. Dependencies

- Use `dependabot` to keep dependencies up-to-date.
- Regularly review and update dependencies as needed.
