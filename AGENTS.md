# AI Agent Instructions

This file contains instructions for AI agents working with this codebase.

## Best Practices

- When writing tests, ensure that all mocks are as accurate as possible to the real APIs they are replacing. This will help to prevent bugs from being introduced into the codebase.
- Remove all debugging code, such as `_LOGGER.debug` statements, once feature development is complete.
- Follow the coding style of the project. This will help to ensure that the codebase is consistent and easy to read.
- Write clear and concise commit messages. This will help other developers to understand the changes that have been made.
- Update the documentation when making changes. This will help to ensure that the documentation is accurate and up-to-date.
- Run all tests before submitting changes. This will help to ensure that the changes have not introduced any new bugs.
- When using the Meraki API, please double-check against the Meraki API documentation at <https://developer.cisco.com/meraki/api-v1/>
- When using the Home Assistant API, double-check against the Home Assistant API documentation at <https://developers.home-assistant.io/docs/api/rest/>
- Prioritize local control, use established libraries, manage dependencies, and be mindful of performance impacts. Specifically, always prefer interacting with devices through established Python libraries rather than directly within the integration.
