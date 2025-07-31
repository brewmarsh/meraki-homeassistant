# Meraki Home Assistant Integration Requirements

## Core Functionality

### Meraki API Integration
| Requirement | Status |
| :--- | :--- |
| The integration needs to communicate with the Cisco Meraki API to fetch data. | Included |
| It requires an API key and organization ID for authentication. | Included |
| The API key must be stored securely. | Included |

### Meraki Device Discovery and Setup
| Requirement | Status |
| :--- | :--- |
| The integration must discover Meraki hardware devices within the specified organization and networks. | Included |
| It should create or update device entities in Home Assistant based on these hardware devices. | Included |
| Device types (Wireless, Switch, Appliance, Camera, Sensor) should be correctly identified. | Included |
| Device names should be formattable, with options for prefixes, suffixes, or omission of device type labels. | Included |
| Devices should include the model name, serial number, MAC address(es) and firmware version. | Included |

### Data Retrieval
| Requirement | Status |
| :--- | :--- |
| The integration should retrieve device data, including connected clients for wireless devices (MR/GR) and network switches (MX, MS). | Included |
| Data should be updated at a configurable scan interval. | Included |

### Home Assistant Integration
| Requirement | Status |
| :--- | :--- |
| The integration should create sensor, device tracker, and switch entities in Home Assistant. | Included |
| The integration must properly handle config entries, including setup, unloading, and reloading. | Included |
| The integration needs to have a configuration flow to take the API key and org id. | Included |
| The integration should have option flow, to set scan interval and device name format. | Included |
| The integration should handle re-authentication of the API key. | Included |
| The integration should have a relaxed tag matching option for matching SSIDs to wireless devices. | Not Included |

### Mapping Meraki objects to Home Assistant objects
| Requirement | Status |
| :--- | :--- |
| Physical Meraki devices (Wireless, Switch, Appliance, Camera, Sensor) will have corresponding Home Assistant devices. | Included |
| Meraki networks will also be shown as Home Assistant devices. | Included |
| Meraki SSIDs (wireless networks) will also be shown as Home Assistant devices. | Included |
| Meraki VLANs will also be shown as Home Assistant devices. | Not Included |

### Meraki Appliances
| Requirement | Status |
| :--- | :--- |
| Meraki appliances should have sensors that track data usage. | Included |
| Meraki appliances should have a sensor that tracks the number of connected clients. | Included |
| Meraki appliances have VLANs; these VLANs should appear as Home Assistant devices. | Not Included |
| Meraki appliances have an external hostname; this should appear as details of the Home Assistant device. | Not Included |
| Meraki appliances should have a sensor that tracks the number of ports in use. | Included |
| Meraki appliances should have a sensor that tracks the number of ports available. | Included |
| The MX uplink status is not correct | Fixed |
| The MX port statuses are not correct | Fixed |
| Appliance `TypeError` | Fixed |

### Meraki Wireless
| Requirement | Status |
| :--- | :--- |
| Meraki wireless devices should have a sensor that tracks the number of connected clients. | Included |
| SSID names appear to be missing | Fixed |
| Disabled SSIDs should not be shown in the list | Fixed |
| SSID names should be updateable | Fixed |
| SSIDs should be able to have the "Broadcast SSID" feature enabled / disabled | Fixed |
| SSIDs do not have a prefix / suffix | Fixed |
| SSID renaming feature is not working | Fixed |

### Meraki Switches
| Requirement | Status |
| :--- | :--- |
| If the Meraki switch supports PoE, the switch should have sensors that aggregated PoE usage. | Included |
| Meraki switches should have a sensor that tracks the number of ports in use. | Included |
| Meraki switches should have a sensor that tracks the number of ports available. | Included |
| Some switches have two prefixes / suffixes; please ensure that they only have one | Fixed |
| Meraki switch status does not seem to be correct | Fixed |

### Meraki Cameras
| Requirement | Status |
| :--- | :--- |
| Meraki cameras should have a data element that reflects the URL of the camera stream. | Included |
| Meraki cameras should have a Home Assistant switch that enables RTSP streaming. | Included |
| Meraki camera RTSP URLs are not correct | Fixed |
| camera RTSP enabling does not work | Fixed |

### Meraki Sensors
| Requirement | Status |
| :--- | :--- |
| Meraki sensors should have appropriate sensor and switch values based on their model. | Included |

## Technical Requirements

### Asynchronous Operations
| Requirement | Status |
| :--- | :--- |
| All API calls and Home Assistant interactions must be asynchronous. | Included |

### Error Handling
| Requirement | Status |
| :--- | :--- |
| The integration should handle API errors, network issues, and other exceptions gracefully. | Included |
| Logging should be used for debugging and error reporting. | Included |

### Data Coordination
| Requirement | Status |
| :--- | :--- |
| A DataUpdateCoordinator should be used to manage data updates and prevent excessive API calls. | Included |
| A separate coordinator should be created to manage the device creations. | Included |

### Configuration Flow
| Requirement | Status |
| :--- | :--- |
| The integration must provide a configuration flow for users to enter their Meraki API credentials. | Included |

### Home Assistant API
| Requirement | Status |
| :--- | :--- |
| The integration must adhere to the Home Assistant API guidelines and conventions. | Included |

### Use of AIOHTTP
| Requirement | Status |
| :--- | :--- |
| The Integration uses AIOHTTP for the API calls. | Included |

### Use of Voluptuous
| Requirement | Status |
| :--- | :--- |
| The Integration uses Voluptuous for schema validation. | Included |

## Key Learnings from Debugging
| Requirement | Status |
| :--- | :--- |
| Import statements must be accurate and reflect the actual file structure and module names. | Included |
| Caching can cause significant issues, requiring aggressive cache clearing. | Partially Included |
| Thorough logging is essential for debugging. | Included |
| The removal of a base class requires the functionality to be moved to the child class. | N/A |
| The __init__.py file is the central location for the integration's logic. | Included |
| The use of the correct coordinator class is very important. | Included |

## Future Work

### High Priority / Core Functionality
- [ ] **Refactor to use `core` components:** The highest priority is to refactor the codebase to use the new `core` components and remove the old, redundant code. This will involve updating the platforms to use the new `core` entities and coordinators, and removing the old API client, coordinators, and entities.
- [ ] **Improve Error Handling and Logging:** Enhance error catching, provide more user-friendly error messages, and ensure consistent logging across the integration.
- [ ] **Optimize Data Retrieval:** Review API call patterns to optimize for performance and minimize API rate limit impact, especially for large organizations.

### New Features / Entities
- [ ] **Implement Switches for Internet Ports:** Allow control over WAN/Internet ports on MX appliances if API supports.
- [ ] **Signal Strength and Data Usage Sensors for Connected Clients:** Create sensors to monitor signal strength (RSSI, SNR) and data usage (upload/download) for individual clients connected to Meraki APs.
- [ ] **More Sensor Types for SSIDs:** Add sensors for additional SSID properties, e.g., security settings (WPA type), traffic statistics (data usage per SSID), active bands.
- [ ] **Support for Additional Meraki Product Types/Features:**
  - [ ] More detailed MV camera features (e.g., motion events, specific stream controls beyond snapshot URLs if available).
  - [ ] SM (Systems Manager) endpoint monitoring/management if relevant for HA.
  - [ ] Deeper sensor data for MT series (e.g., historical data, more specific readings if available).
  - [ ] More detailed switch port statistics (e.g., per-port traffic, PoE details beyond basic count).
- [ ] **Firmware Update Sensors/Notifications:** Entities to indicate available firmware updates for devices or networks.
- [ ] **Network Health/Event Sensors:** Monitor overall network health or specific Meraki events/alerts.

### Enhancements / Bug Fixes
- [ ] **Configuration Option for SSID Sensor Selection:** Allow users to choose which specific sensors (availability, channel, client count, etc.) they want to enable per SSID to reduce entity clutter.
- [ ] **Customize Device and Entity Names:** Provide more advanced configuration options for customizing how Meraki device and entity names are generated in Home Assistant.
- [ ] **Full Home Assistant Branding Support:** Ensure the integration meets all requirements for Home Assistant branding, including logos and documentation links.
- [ ] **Address Specific Bugs:**
  - [ ] Review "Radio profiles are not returned for all MR devices" (from README known issues) and investigate if it's an API limitation or an integration issue.
- [ ] **Fix SSID entity `device_info`:** Correctly link to parent AP via `via_device` attribute in `MerakiEntity` for SSID-specific entities.
- [ ] **Tag-based SSID Control Review:** The current `MerakiSSIDSwitch` uses device tags to control SSID state. Evaluate if a more direct API method for enabling/disabling SSIDs per AP (if available and appropriate) would be better, or if the tag strategy is the most robust.
- [ ] **VLAN Entity Clarification:** Determine if "Meraki VLANs" should be actual HA entities/devices or if VLAN information is purely contextual data for other entities. Adjust documentation and entity creation accordingly.

### Documentation
- [ ] **Troubleshooting Section:** Add a comprehensive troubleshooting section to `README.md` covering common issues (API key errors, rate limits, device discovery problems).
- [ ] **Configuration Guide:** Create a more detailed guide on configuring the integration, including explanations of all options in the config flow and options flow.
- [ ] **Update Documentation for SSID Device Creation:** Ensure documentation clearly explains how SSIDs are represented as devices and how their entities are structured.
- [ ] **MkDocs for Documentation Generation:** Set up MkDocs (or similar like Sphinx) for generating more structured and navigable documentation, potentially hosted on GitHub Pages.
- [ ] **Developer Documentation:** Add notes or a separate document for developers looking to contribute, explaining the coordinator structure, API client usage, and entity creation patterns.

### Code Quality & Refactoring
- [ ] **Unit and Integration Tests:** Expand test coverage significantly.
