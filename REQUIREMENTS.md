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
| Device names should be formattable, with options for prefixes, suffixes, or omission of device type labels. | Not Included |
| Devices should include the model name, serial number, MAC address(es) and firmware version. | Partially Included |

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
| The integration should have option flow, to set scan interval and device name format. | Partially Included |
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
| Meraki appliances should have sensors that track data usage. | Not Included |
| Meraki appliances should have a sensor that tracks the number of connected clients. | Included |
| Meraki appliances have VLANs; these VLANs should appear as Home Assistant devices. | Not Included |
| Meraki appliances have an external hostname; this should appear as details of the Home Assistant device. | Not Included |
| Meraki appliances should have a sensor that tracks the number of ports in use. | Not Included |
| Meraki appliances should have a sensor that tracks the number of ports available. | Not Included |

### Meraki Wireless
| Requirement | Status |
| :--- | :--- |
| Meraki wireless devices should have a sensor that tracks the number of connected clients. | Included |

### Meraki Switches
| Requirement | Status |
| :--- | :--- |
| If the Meraki switch supports PoE, the switch should have sensors that aggregated PoE usage. | Not Included |
| Meraki switches should have a sensor that tracks the number of ports in use. | Not Included |
| Meraki switches should have a sensor that tracks the number of ports available. | Not Included |

### Meraki Cameras
| Requirement | Status |
| :--- | :--- |
| Meraki cameras should have a data element that reflects the URL of the camera stream. | Partially Included |
| Meraki cameras should have a Home Assistant switch that enables RTSP streaming. | Included |

### Meraki Sensors
| Requirement | Status |
| :--- | :--- |
| Meraki sensors should have appropriate sensor and switch values based on their model. | Not Included |

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
