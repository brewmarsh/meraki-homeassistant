# Integration Quality Scale Checklist

When changing the quality scale of an integration, make sure you have completed the rules before opening the PR to change the quality scale. In the PR description, please deliver a copy of this checklist and mark the rules that have been completed. Make sure you add links to the relevant code to help a speedy grading process.

## Bronze
- [x] `action-setup` - Service actions are registered in async_setup (N/A)
- [x] `appropriate-polling` - If it's a polling integration, set an appropriate polling interval
- [x] `brands` - Has branding assets available for the integration
- [x] `common-modules` - Place common patterns in common modules
- [x] `config-flow-test-coverage` - Full test coverage for the config flow
- [x] `config-flow` - Integration needs to be able to be set up via the UI
- [x] `data_description` - Uses `data_description` to give context to fields
- [x] `uses-config-entry-data-and-options-correctly` - Uses `ConfigEntry.data` and `ConfigEntry.options` correctly
- [x] `dependency-transparency` - Dependency transparency
- [x] `docs-actions` - The documentation describes the provided service actions that can be used (N/A)
- [x] `docs-high-level-description` - The documentation includes a high-level description of the integration brand, product, or service
- [x] `docs-installation-instructions` - The documentation provides step-by-step installation instructions for the integration, including, if needed, prerequisites
- [x] `docs-removal-instructions` - The documentation provides removal instructions
- [x] `entity-event-setup` - Entity events are subscribed in the correct lifecycle methods
- [x] `entity-unique-id` - Entities have a unique ID
- [x] `has-entity-name` - Entities use has_entity_name = True
- [x] `runtime-data` - Use ConfigEntry.runtime_data to store runtime data
- [x] `test-before-configure` - Test a connection in the config flow
- [x] `test-before-setup` - Check during integration initialization if we are able to set it up correctly
- [x] `unique-config-entry` - Don't allow the same device or service to be able to be set up twice

## Silver
- [x] `action-exceptions` - Service actions raise exceptions when encountering failures
- [x] `config-entry-unloading` - Support config entry unloading
- [x] `docs-configuration-parameters` - The documentation describes all integration configuration options
- [x] `docs-installation-parameters` - The documentation describes all integration installation parameters
- [x] `entity-unavailable` - Mark entity unavailable if appropriate
- [x] `integration-owner` - Has an integration owner
- [x] `log-when-unavailable` - If internet/device/service is unavailable, log once when unavailable and once when back connected
- [x] `parallel-updates` - Number of parallel updates is specified (N/A)
- [x] `reauthentication-flow` - Reauthentication needs to be available via the UI
- [x] `test-coverage` - Above 95% test coverage for all integration modules

## Gold
- [x] `devices` - The integration creates devices
- [x] `diagnostics` - Implements diagnostics
- [x] `discovery-update-info` - Integration uses discovery info to update network information (N/A)
- [x] `discovery` - Devices can be discovered (N/A)
- [x] `docs-data-update` - The documentation describes how data is updated
- [x] `docs-examples` - The documentation provides automation examples the user can use.
- [x] `docs-known-limitations` - The documentation describes known limitations of the integration (not to be confused with bugs)
- [x] `docs-supported-devices` - The documentation describes known supported / unsupported devices
- [x] `docs-supported-functions` - The documentation describes the supported functionality, including entities, and platforms
- [x] `docs-troubleshooting` - The documentation provides troubleshooting information
- [x] `docs-use-cases` - The documentation describes use cases to illustrate how this integration can be used
- [x] `dynamic-devices` - Devices added after integration setup
- [x] `entity-category` - Entities are assigned an appropriate EntityCategory
- [x] `entity-device-class` - Entities use device classes where possible
- [x] `entity-disabled-by-default` - Integration disables less popular (or noisy) entities
- [x] `entity-translations` - Entities have translated names
- [x] `exception-translations` - Exception messages are translatable
- [x] `icon-translations` - Entities implement icon translations
- [x] `reconfiguration-flow` - Integrations should have a reconfigure flow
- [x] `repair-issues` - Repair issues and repair flows are used when user intervention is needed
- [x] `stale-devices` - Stale devices are removed

## Platinum
- [x] `async-dependency` - Dependency is async
- [x] `inject-websession` - The integration dependency supports passing in a websession
- [x] `strict-typing` - Strict typing
