# Agent Guidelines

This document provides guidelines for agents working on this codebase.

## 1. Code Style

- All Python code must adhere to the PEP 8 style guide.
- Use a linter like `flake8` or `pylint` to check for style issues before submitting code.

## 2. Documentation

- All public functions and classes must have comprehensive docstrings that explain their purpose, arguments, and return values.
- Use the Google Python Style Guide for docstring formatting.

## 3. Configuration

- All configuration data must be validated using `voluptuous` schemas.
- Provide clear error messages for invalid configuration.

## 4. Constants

- All constants must be defined in `custom_components/meraki_ha/const.py`.
- Do not use magic strings or numbers in the code.

## 5. Testing

- All new features must be accompanied by unit tests.
- Run the entire test suite before submitting code to ensure that no regressions have been introduced.

## 6. Dependencies

- Use `dependabot` to keep dependencies up-to-date.
- Regularly review and update dependencies as needed.
