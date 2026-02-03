# Agent Scorecard Report

**Target Agent Profile:** Standard Agent Readiness checks (ACL & Type Safety)
**Overall Score: 83.8/100** - PASS

✅ **Status: PASSED** - This codebase is Agent-Ready.

### ⚠️ Project Issues
- God Modules Detected (Inbound > 50): const.py, coordinator.py, types.py
- Circular Dependencies Detected: core/api/client.py->core/api/endpoints/appliance.py, core/api/client.py->core/api/endpoints/camera.py, core/api/client.py->core/api/endpoints/devices.py, core/api/client.py->core/api/endpoints/network.py, core/api/client.py->core/api/endpoints/organization.py, core/api/client.py->core/api/endpoints/sensor.py, core/api/client.py->core/api/endpoints/switch.py, core/api/client.py->core/api/endpoints/wireless.py, core/api/client.py->core/coordinator_helpers/client_fetcher.py

## 🎯 Top Refactoring Targets (Agent Cognitive Load (ACL))

ACL = Complexity + (Lines of Code / 20). Target: ACL <= 10.

| Function | File | ACL | Status |
|----------|------|-----|--------|
| `_process_detailed_data` | `core/api/client.py` | 51.1 | 🔴 Red |
| `parse_network_data` | `core/parsers/network.py` | 33.1 | 🔴 Red |
| `calculate_ssid_status` | `helpers/ssid_status_calculator.py` | 21.2 | 🔴 Red |
| `parse_sensor_data` | `core/parsers/sensors.py` | 21.1 | 🔴 Red |
| `discover_entities` | `discovery/service.py` | 19.2 | 🟡 Yellow |
| `handle_meraki_errors` | `core/utils/api_utils.py` | 18.3 | 🟡 Yellow |
| `discover_entities` | `discovery/handlers/mx.py` | 17.9 | 🟡 Yellow |
| `discover_entities` | `discovery/handlers/network.py` | 17.8 | 🟡 Yellow |
| `async_handle_webhook` | `webhook.py` | 17.1 | 🟡 Yellow |
| `_build_detail_tasks` | `core/api/client.py` | 16.0 | 🟡 Yellow |

## 🛡️ Type Safety Index

Target: >90% of functions must have explicit type signatures.

| File | Type Safety Index | Status |
| :--- | :---------------: | :----- |
| sensor/device/radio_settings.py | 0% | ❌ |
| sensor/network/ssid_details.py | 29% | ❌ |
| sensor/network/vlans_list.py | 67% | ❌ |
| switch/adult_content_filtering.py | 88% | ❌ |
| const.py | 100% | ✅ |
| reauth_flow.py | 100% | ✅ |
| diagnostics.py | 100% | ✅ |
| const_conf.py | 100% | ✅ |
| coordinator.py | 100% | ✅ |
| const_api.py | 100% | ✅ |
| __init__.py | 100% | ✅ |
| descriptions.py | 100% | ✅ |
| webhook.py | 100% | ✅ |
| entity_descriptions.py | 100% | ✅ |
| async_logging.py | 100% | ✅ |
| const_platform.py | 100% | ✅ |
| authentication.py | 100% | ✅ |
| select.py | 100% | ✅ |
| types.py | 100% | ✅ |
| config_flow.py | 100% | ✅ |
| entity.py | 100% | ✅ |
| frontend.py | 100% | ✅ |
| options_flow.py | 100% | ✅ |
| repairs.py | 100% | ✅ |
| const_device.py | 100% | ✅ |
| sensor_registry.py | 100% | ✅ |
| schemas.py | 100% | ✅ |
| const_sensor.py | 100% | ✅ |
| camera.py | 100% | ✅ |
| const_data.py | 100% | ✅ |
| text/__init__.py | 100% | ✅ |
| text/meraki_ssid_name.py | 100% | ✅ |
| sensor/client_tracker.py | 100% | ✅ |
| sensor/__init__.py | 100% | ✅ |
| sensor/org/__init__.py | 100% | ✅ |
| sensor/org/org_device_type_clients.py | 100% | ✅ |
| sensor/org/org_clients.py | 100% | ✅ |
| sensor/device/meraki_firmware_status.py | 100% | ✅ |
| sensor/device/appliance_uplink.py | 100% | ✅ |
| sensor/device/device_status.py | 100% | ✅ |
| sensor/device/meraki_wan1_connectivity.py | 100% | ✅ |
| sensor/device/__init__.py | 100% | ✅ |
| sensor/device/camera_analytics.py | 100% | ✅ |
| sensor/device/switch_port.py | 100% | ✅ |
| sensor/device/appliance_port.py | 100% | ✅ |
| sensor/device/meraki_mt_base.py | 100% | ✅ |
| sensor/device/data_usage.py | 100% | ✅ |
| sensor/device/poe_usage.py | 100% | ✅ |
| sensor/device/camera_audio_detection.py | 100% | ✅ |
| sensor/device/connected_clients.py | 100% | ✅ |
| sensor/device/meraki_wan2_connectivity.py | 100% | ✅ |
| sensor/device/camera_sense_status.py | 100% | ✅ |
| sensor/device/rtsp_url.py | 100% | ✅ |
| sensor/network/ssid_per_client_bandwidth_limit.py | 100% | ✅ |
| sensor/network/ssid_ip_assignment_mode.py | 100% | ✅ |
| sensor/network/ssid_availability.py | 100% | ✅ |
| sensor/network/ssid_wpa_encryption_mode.py | 100% | ✅ |
| sensor/network/ssid_psk.py | 100% | ✅ |
| sensor/network/base.py | 100% | ✅ |
| sensor/network/__init__.py | 100% | ✅ |
| sensor/network/traffic_shaping.py | 100% | ✅ |
| sensor/network/ssid_visible.py | 100% | ✅ |
| sensor/network/ssid_per_ssid_bandwidth_limit.py | 100% | ✅ |
| sensor/network/vlan.py | 100% | ✅ |
| sensor/network/ssid_auth_mode.py | 100% | ✅ |
| sensor/network/ssid_client_count.py | 100% | ✅ |
| sensor/network/ssid_encryption_mode.py | 100% | ✅ |
| sensor/network/network_clients.py | 100% | ✅ |
| sensor/network/ssid_band_selection.py | 100% | ✅ |
| sensor/network/ssid_splash_page.py | 100% | ✅ |
| sensor/ssid/__init__.py | 100% | ✅ |
| number/__init__.py | 100% | ✅ |
| number/uplink_bandwidth.py | 100% | ✅ |
| number/setup_helpers.py | 100% | ✅ |
| hubs/__init__.py | 100% | ✅ |
| hubs/network.py | 100% | ✅ |
| hubs/organization.py | 100% | ✅ |
| discovery/service.py | 100% | ✅ |
| discovery/__init__.py | 100% | ✅ |
| discovery/handlers/mt.py | 100% | ✅ |
| discovery/handlers/base.py | 100% | ✅ |
| discovery/handlers/__init__.py | 100% | ✅ |
| discovery/handlers/network.py | 100% | ✅ |
| discovery/handlers/ssid.py | 100% | ✅ |
| discovery/handlers/ms.py | 100% | ✅ |
| discovery/handlers/mr.py | 100% | ✅ |
| discovery/handlers/gx.py | 100% | ✅ |
| discovery/handlers/mv.py | 100% | ✅ |
| discovery/handlers/mx.py | 100% | ✅ |
| coordinators/__init__.py | 100% | ✅ |
| event/__init__.py | 100% | ✅ |
| event/device/mt_button.py | 100% | ✅ |
| event/device/camera_motion.py | 100% | ✅ |
| helpers/schema.py | 100% | ✅ |
| helpers/__init__.py | 100% | ✅ |
| helpers/serialization.py | 100% | ✅ |
| helpers/ssid_status_calculator.py | 100% | ✅ |
| helpers/device_info_helpers.py | 100% | ✅ |
| platforms/__init__.py | 100% | ✅ |
| platforms/sensor/__init__.py | 100% | ✅ |
| platforms/sensor/device/__init__.py | 100% | ✅ |
| platforms/sensor/device/uplink_status.py | 100% | ✅ |
| platforms/sensor/device/connected_clients.py | 100% | ✅ |
| platforms/sensor/network/__init__.py | 100% | ✅ |
| platforms/sensor/network/info.py | 100% | ✅ |
| binary_sensor/__init__.py | 100% | ✅ |
| binary_sensor/network.py | 100% | ✅ |
| binary_sensor/switch_port.py | 100% | ✅ |
| binary_sensor/device/__init__.py | 100% | ✅ |
| binary_sensor/device/meraki_mt_binary_base.py | 100% | ✅ |
| binary_sensor/device/camera_motion.py | 100% | ✅ |
| media/__init__.py | 100% | ✅ |
| meraki_select/__init__.py | 100% | ✅ |
| meraki_select/meraki_content_filtering.py | 100% | ✅ |
| meraki_select/vpn.py | 100% | ✅ |
| button/__init__.py | 100% | ✅ |
| button/reboot.py | 100% | ✅ |
| button/device/mt15_refresh_data.py | 100% | ✅ |
| button/device/__init__.py | 100% | ✅ |
| button/device/switch_port_cycle.py | 100% | ✅ |
| button/device/camera_snapshot.py | 100% | ✅ |
| switch/camera_profiles.py | 100% | ✅ |
| switch/firewall_rule.py | 100% | ✅ |
| switch/meraki_client_blocker.py | 100% | ✅ |
| switch/__init__.py | 100% | ✅ |
| switch/traffic_shaping.py | 100% | ✅ |
| switch/mt40_power_outlet.py | 100% | ✅ |
| switch/camera_settings.py | 100% | ✅ |
| switch/meraki_ssid_device_switch.py | 100% | ✅ |
| switch/setup_helpers.py | 100% | ✅ |
| switch/camera_controls.py | 100% | ✅ |
| switch/content_filtering.py | 100% | ✅ |
| switch/vlan_dhcp.py | 100% | ✅ |
| switch/vpn.py | 100% | ✅ |
| api/__init__.py | 100% | ✅ |
| api/websocket.py | 100% | ✅ |
| core/errors.py | 100% | ✅ |
| core/models.py | 100% | ✅ |
| core/__init__.py | 100% | ✅ |
| core/helpers.py | 100% | ✅ |
| core/managers.py | 100% | ✅ |
| core/timed_access_manager.py | 100% | ✅ |
| core/repository.py | 100% | ✅ |
| core/coordinator_helpers/data_fetcher.py | 100% | ✅ |
| core/coordinator_helpers/client_fetcher.py | 100% | ✅ |
| core/coordinator_helpers/__init__.py | 100% | ✅ |
| core/coordinator_helpers/device_fetcher.py | 100% | ✅ |
| core/coordinator_helpers/service_setup.py | 100% | ✅ |
| core/utils/_mappers.py | 100% | ✅ |
| core/utils/device_types.py | 100% | ✅ |
| core/utils/naming_utils.py | 100% | ✅ |
| core/utils/__init__.py | 100% | ✅ |
| core/utils/network_utils.py | 100% | ✅ |
| core/utils/icon_utils.py | 100% | ✅ |
| core/utils/api_utils.py | 100% | ✅ |
| core/utils/entity_id_utils.py | 100% | ✅ |
| core/utils/_data.py | 100% | ✅ |
| core/utils/_const.py | 100% | ✅ |
| core/utils/validation_utils.py | 100% | ✅ |
| core/parsers/__init__.py | 100% | ✅ |
| core/parsers/network.py | 100% | ✅ |
| core/parsers/switch.py | 100% | ✅ |
| core/parsers/wireless.py | 100% | ✅ |
| core/parsers/devices.py | 100% | ✅ |
| core/parsers/sensors.py | 100% | ✅ |
| core/parsers/appliance.py | 100% | ✅ |
| core/parsers/camera.py | 100% | ✅ |
| core/entities/meraki_firewall_rule_entity.py | 100% | ✅ |
| core/entities/__init__.py | 100% | ✅ |
| core/entities/meraki_vlan_entity.py | 100% | ✅ |
| core/entities/meraki_network_entity.py | 100% | ✅ |
| core/api/__init__.py | 100% | ✅ |
| core/api/client.py | 100% | ✅ |
| core/api/cache.py | 100% | ✅ |
| core/api/endpoints/__init__.py | 100% | ✅ |
| core/api/endpoints/network.py | 100% | ✅ |
| core/api/endpoints/sensor.py | 100% | ✅ |
| core/api/endpoints/switch.py | 100% | ✅ |
| core/api/endpoints/wireless.py | 100% | ✅ |
| core/api/endpoints/devices.py | 100% | ✅ |
| core/api/endpoints/organization.py | 100% | ✅ |
| core/api/endpoints/appliance.py | 100% | ✅ |
| core/api/endpoints/camera.py | 100% | ✅ |
| core/repositories/__init__.py | 100% | ✅ |
| core/repositories/camera_repository.py | 100% | ✅ |
| services/camera_service.py | 100% | ✅ |
| services/device_control_service.py | 100% | ✅ |
| services/network_control_service.py | 100% | ✅ |
| services/__init__.py | 100% | ✅ |
| services/switch_port_service.py | 100% | ✅ |

## 🤖 Agent Prompts for Remediation

### File: `sensor/device/radio_settings.py`
- **Type Safety**: Coverage is 0%. Prompt: 'Add explicit type signatures to all functions in `sensor/device/radio_settings.py` to meet the 90% Type Safety Index requirement.'

### File: `sensor/network/ssid_details.py`
- **Type Safety**: Coverage is 29%. Prompt: 'Add explicit type signatures to all functions in `sensor/network/ssid_details.py` to meet the 90% Type Safety Index requirement.'

### File: `sensor/network/vlans_list.py`
- **Type Safety**: Coverage is 67%. Prompt: 'Add explicit type signatures to all functions in `sensor/network/vlans_list.py` to meet the 90% Type Safety Index requirement.'

### File: `helpers/ssid_status_calculator.py`
- **Critical ACL**: Functions `calculate_ssid_status` have Red ACL (>20). Prompt: 'Refactor functions in `helpers/ssid_status_calculator.py` with high cognitive load to bring ACL below 10. Split complex logic and reduce function length.'

### File: `switch/adult_content_filtering.py`
- **Type Safety**: Coverage is 88%. Prompt: 'Add explicit type signatures to all functions in `switch/adult_content_filtering.py` to meet the 90% Type Safety Index requirement.'

### File: `core/parsers/network.py`
- **Critical ACL**: Functions `parse_network_data` have Red ACL (>20). Prompt: 'Refactor functions in `core/parsers/network.py` with high cognitive load to bring ACL below 10. Split complex logic and reduce function length.'

### File: `core/parsers/sensors.py`
- **Critical ACL**: Functions `parse_sensor_data` have Red ACL (>20). Prompt: 'Refactor functions in `core/parsers/sensors.py` with high cognitive load to bring ACL below 10. Split complex logic and reduce function length.'

### File: `core/api/client.py`
- **Critical ACL**: Functions `_process_detailed_data` have Red ACL (>20). Prompt: 'Refactor functions in `core/api/client.py` with high cognitive load to bring ACL below 10. Split complex logic and reduce function length.'


### 📂 Full File Analysis

| File | Score | Issues |
| :--- | :---: | :--- |
| const.py | 100 ✅ |  |
| reauth_flow.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| diagnostics.py | 100 ✅ |  |
| const_conf.py | 100 ✅ |  |
| coordinator.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| const_api.py | 100 ✅ |  |
| __init__.py | 100 ✅ |  |
| descriptions.py | 100 ✅ |  |
| webhook.py | 90 ✅ | 2 Yellow ACL functions (-10) |
| entity_descriptions.py | 100 ✅ |  |
| async_logging.py | 100 ✅ |  |
| const_platform.py | 100 ✅ |  |
| authentication.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| select.py | 100 ✅ |  |
| types.py | 100 ✅ |  |
| config_flow.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| entity.py | 100 ✅ |  |
| frontend.py | 100 ✅ |  |
| options_flow.py | 100 ✅ |  |
| repairs.py | 100 ✅ |  |
| const_device.py | 100 ✅ |  |
| sensor_registry.py | 100 ✅ |  |
| schemas.py | 100 ✅ |  |
| const_sensor.py | 100 ✅ |  |
| camera.py | 100 ✅ |  |
| const_data.py | 100 ✅ |  |
| text/__init__.py | 100 ✅ |  |
| text/meraki_ssid_name.py | 100 ✅ |  |
| sensor/client_tracker.py | 100 ✅ |  |
| sensor/__init__.py | 100 ✅ |  |
| sensor/org/__init__.py | 100 ✅ |  |
| sensor/org/org_device_type_clients.py | 100 ✅ |  |
| sensor/org/org_clients.py | 100 ✅ |  |
| sensor/device/radio_settings.py | 80 ✅ | Type Safety Index 0% < 90% (-20) |
| sensor/device/meraki_firmware_status.py | 100 ✅ |  |
| sensor/device/appliance_uplink.py | 100 ✅ |  |
| sensor/device/device_status.py | 100 ✅ |  |
| sensor/device/meraki_wan1_connectivity.py | 100 ✅ |  |
| sensor/device/__init__.py | 100 ✅ |  |
| sensor/device/camera_analytics.py | 100 ✅ |  |
| sensor/device/switch_port.py | 100 ✅ |  |
| sensor/device/appliance_port.py | 100 ✅ |  |
| sensor/device/meraki_mt_base.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| sensor/device/data_usage.py | 100 ✅ |  |
| sensor/device/poe_usage.py | 100 ✅ |  |
| sensor/device/camera_audio_detection.py | 100 ✅ |  |
| sensor/device/connected_clients.py | 100 ✅ |  |
| sensor/device/meraki_wan2_connectivity.py | 100 ✅ |  |
| sensor/device/camera_sense_status.py | 100 ✅ |  |
| sensor/device/rtsp_url.py | 100 ✅ |  |
| sensor/network/ssid_per_client_bandwidth_limit.py | 100 ✅ |  |
| sensor/network/ssid_details.py | 80 ✅ | Type Safety Index 29% < 90% (-20) |
| sensor/network/ssid_ip_assignment_mode.py | 100 ✅ |  |
| sensor/network/ssid_availability.py | 100 ✅ |  |
| sensor/network/ssid_wpa_encryption_mode.py | 100 ✅ |  |
| sensor/network/ssid_psk.py | 100 ✅ |  |
| sensor/network/base.py | 100 ✅ |  |
| sensor/network/__init__.py | 100 ✅ |  |
| sensor/network/traffic_shaping.py | 100 ✅ |  |
| sensor/network/ssid_visible.py | 100 ✅ |  |
| sensor/network/ssid_per_ssid_bandwidth_limit.py | 100 ✅ |  |
| sensor/network/vlans_list.py | 80 ✅ | Type Safety Index 67% < 90% (-20) |
| sensor/network/vlan.py | 100 ✅ |  |
| sensor/network/ssid_auth_mode.py | 100 ✅ |  |
| sensor/network/ssid_client_count.py | 100 ✅ |  |
| sensor/network/ssid_encryption_mode.py | 100 ✅ |  |
| sensor/network/network_clients.py | 100 ✅ |  |
| sensor/network/ssid_band_selection.py | 100 ✅ |  |
| sensor/network/ssid_splash_page.py | 100 ✅ |  |
| sensor/ssid/__init__.py | 100 ✅ |  |
| number/__init__.py | 100 ✅ |  |
| number/uplink_bandwidth.py | 100 ✅ |  |
| number/setup_helpers.py | 100 ✅ |  |
| hubs/__init__.py | 100 ✅ |  |
| hubs/network.py | 100 ✅ |  |
| hubs/organization.py | 100 ✅ |  |
| discovery/service.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| discovery/__init__.py | 100 ✅ |  |
| discovery/handlers/mt.py | 100 ✅ |  |
| discovery/handlers/base.py | 100 ✅ |  |
| discovery/handlers/__init__.py | 100 ✅ |  |
| discovery/handlers/network.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| discovery/handlers/ssid.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| discovery/handlers/ms.py | 100 ✅ |  |
| discovery/handlers/mr.py | 100 ✅ |  |
| discovery/handlers/gx.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| discovery/handlers/mv.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| discovery/handlers/mx.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| coordinators/__init__.py | 100 ✅ |  |
| event/__init__.py | 100 ✅ |  |
| event/device/mt_button.py | 100 ✅ |  |
| event/device/camera_motion.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| helpers/schema.py | 100 ✅ |  |
| helpers/__init__.py | 100 ✅ |  |
| helpers/serialization.py | 100 ✅ |  |
| helpers/ssid_status_calculator.py | 85 ✅ | 1 Red ACL functions (-15) |
| helpers/device_info_helpers.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| platforms/__init__.py | 100 ✅ |  |
| platforms/sensor/__init__.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| platforms/sensor/device/__init__.py | 100 ✅ |  |
| platforms/sensor/device/uplink_status.py | 100 ✅ |  |
| platforms/sensor/device/connected_clients.py | 100 ✅ |  |
| platforms/sensor/network/__init__.py | 100 ✅ |  |
| platforms/sensor/network/info.py | 100 ✅ |  |
| binary_sensor/__init__.py | 100 ✅ |  |
| binary_sensor/network.py | 100 ✅ |  |
| binary_sensor/switch_port.py | 100 ✅ |  |
| binary_sensor/device/__init__.py | 100 ✅ |  |
| binary_sensor/device/meraki_mt_binary_base.py | 100 ✅ |  |
| binary_sensor/device/camera_motion.py | 100 ✅ |  |
| media/__init__.py | 100 ✅ |  |
| meraki_select/__init__.py | 100 ✅ |  |
| meraki_select/meraki_content_filtering.py | 100 ✅ |  |
| meraki_select/vpn.py | 100 ✅ |  |
| button/__init__.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| button/reboot.py | 100 ✅ |  |
| button/device/mt15_refresh_data.py | 100 ✅ |  |
| button/device/__init__.py | 100 ✅ |  |
| button/device/switch_port_cycle.py | 100 ✅ |  |
| button/device/camera_snapshot.py | 100 ✅ |  |
| switch/camera_profiles.py | 100 ✅ |  |
| switch/firewall_rule.py | 100 ✅ |  |
| switch/meraki_client_blocker.py | 100 ✅ |  |
| switch/__init__.py | 100 ✅ |  |
| switch/traffic_shaping.py | 100 ✅ |  |
| switch/mt40_power_outlet.py | 100 ✅ |  |
| switch/camera_settings.py | 100 ✅ |  |
| switch/meraki_ssid_device_switch.py | 100 ✅ |  |
| switch/adult_content_filtering.py | 80 ✅ | Type Safety Index 88% < 90% (-20) |
| switch/setup_helpers.py | 100 ✅ |  |
| switch/camera_controls.py | 100 ✅ |  |
| switch/content_filtering.py | 100 ✅ |  |
| switch/vlan_dhcp.py | 100 ✅ |  |
| switch/vpn.py | 100 ✅ |  |
| api/__init__.py | 100 ✅ |  |
| api/websocket.py | 100 ✅ |  |
| core/errors.py | 100 ✅ |  |
| core/models.py | 100 ✅ |  |
| core/__init__.py | 100 ✅ |  |
| core/helpers.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| core/managers.py | 100 ✅ |  |
| core/timed_access_manager.py | 100 ✅ |  |
| core/repository.py | 100 ✅ |  |
| core/coordinator_helpers/data_fetcher.py | 90 ✅ | 2 Yellow ACL functions (-10) |
| core/coordinator_helpers/client_fetcher.py | 100 ✅ |  |
| core/coordinator_helpers/__init__.py | 100 ✅ |  |
| core/coordinator_helpers/device_fetcher.py | 100 ✅ |  |
| core/coordinator_helpers/service_setup.py | 100 ✅ |  |
| core/utils/_mappers.py | 100 ✅ |  |
| core/utils/device_types.py | 100 ✅ |  |
| core/utils/naming_utils.py | 100 ✅ |  |
| core/utils/__init__.py | 100 ✅ |  |
| core/utils/network_utils.py | 100 ✅ |  |
| core/utils/icon_utils.py | 100 ✅ |  |
| core/utils/api_utils.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| core/utils/entity_id_utils.py | 100 ✅ |  |
| core/utils/_data.py | 100 ✅ |  |
| core/utils/_const.py | 100 ✅ |  |
| core/utils/validation_utils.py | 100 ✅ |  |
| core/parsers/__init__.py | 100 ✅ |  |
| core/parsers/network.py | 85 ✅ | 1 Red ACL functions (-15) |
| core/parsers/switch.py | 100 ✅ |  |
| core/parsers/wireless.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| core/parsers/devices.py | 100 ✅ |  |
| core/parsers/sensors.py | 85 ✅ | 1 Red ACL functions (-15) |
| core/parsers/appliance.py | 100 ✅ |  |
| core/parsers/camera.py | 100 ✅ |  |
| core/entities/meraki_firewall_rule_entity.py | 100 ✅ |  |
| core/entities/__init__.py | 100 ✅ |  |
| core/entities/meraki_vlan_entity.py | 100 ✅ |  |
| core/entities/meraki_network_entity.py | 100 ✅ |  |
| core/api/__init__.py | 100 ✅ |  |
| core/api/client.py | 70 ✅ | 1 Red ACL functions (-15), 3 Yellow ACL functions (-15) |
| core/api/cache.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| core/api/endpoints/__init__.py | 100 ✅ |  |
| core/api/endpoints/network.py | 100 ✅ |  |
| core/api/endpoints/sensor.py | 100 ✅ |  |
| core/api/endpoints/switch.py | 100 ✅ |  |
| core/api/endpoints/wireless.py | 100 ✅ |  |
| core/api/endpoints/devices.py | 100 ✅ |  |
| core/api/endpoints/organization.py | 100 ✅ |  |
| core/api/endpoints/appliance.py | 100 ✅ |  |
| core/api/endpoints/camera.py | 100 ✅ |  |
| core/repositories/__init__.py | 100 ✅ |  |
| core/repositories/camera_repository.py | 95 ✅ | 1 Yellow ACL functions (-5) |
| services/camera_service.py | 100 ✅ |  |
| services/device_control_service.py | 100 ✅ |  |
| services/network_control_service.py | 100 ✅ |  |
| services/__init__.py | 100 ✅ |  |
| services/switch_port_service.py | 100 ✅ |  |

---
*Generated by Agent-Scorecard*