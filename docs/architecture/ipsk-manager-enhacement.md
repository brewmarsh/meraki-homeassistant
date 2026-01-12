# Feature: IPSK Manager with Device Association

## Summary

Enhance the meraki_ha integration with a comprehensive Identity PSK (IPSK) management system that creates Home Assistant entities for each IPSK and allows association with HA devices, areas, and users.

## Background

Identity PSKs allow unique Wi-Fi passwords per device/user on Meraki networks. This feature will:

- Provide full IPSK lifecycle management (create, read, update, delete)
- Create HA entities for each IPSK (sensors, switches, binary sensors)
- Associate IPSKs with Home Assistant devices, areas, or users
- Enable automations based on IPSK status and connectivity
- Serve as the backend for the separate WPN Registration Portal add-on

## Requirements

### 1. IPSK Data Model

```python
@dataclass
class ManagedIPSK:
    """Represents a managed IPSK."""
    id: str                          # Meraki IPSK ID
    name: str                        # Human-readable name
    network_id: str                  # Meraki network ID
    ssid_number: int                 # SSID number (0-14)
    ssid_name: str                   # SSID name for display
    group_policy_id: str | None      # Optional group policy
    passphrase: str                  # The PSK (stored encrypted)
    expires_at: datetime | None      # Optional expiration
    created_at: datetime             # Creation timestamp
    created_by: str                  # Who created it (user/system)

    # Association fields
    associated_ha_device_id: str | None   # HA device registry ID
    associated_ha_area_id: str | None     # HA area ID
    associated_user_name: str | None      # User name (for residents)
    associated_unit: str | None           # Unit/room number

    # Status tracking
    status: Literal["active", "expired", "revoked", "pending"]
    last_seen: datetime | None       # Last time a client connected
    connected_client_count: int      # Current connected clients
```

### 2. IPSK Registry/Coordinator

Create a new coordinator to manage IPSKs:

```python
class IPSKCoordinator(DataUpdateCoordinator):
    """Coordinator for IPSK management."""

    async def async_create_ipsk(
        self,
        name: str,
        network_id: str,
        ssid_number: int,
        passphrase: str | None = None,  # Auto-generate if None
        expires_at: datetime | None = None,
        group_policy_id: str | None = None,
        associated_device_id: str | None = None,
        associated_area_id: str | None = None,
        associated_user: str | None = None,
        associated_unit: str | None = None,
    ) -> ManagedIPSK: ...

    async def async_revoke_ipsk(self, ipsk_id: str) -> None: ...

    async def async_update_ipsk(self, ipsk_id: str, **kwargs) -> ManagedIPSK: ...

    async def async_delete_ipsk(self, ipsk_id: str) -> None: ...

    async def async_get_ipsk(self, ipsk_id: str) -> ManagedIPSK | None: ...

    async def async_list_ipsks(
        self,
        network_id: str | None = None,
        ssid_number: int | None = None,
        status: str | None = None,
    ) -> list[ManagedIPSK]: ...
```

### 3. Home Assistant Entities per IPSK

For each managed IPSK, create these entities:

#### Sensor: IPSK Status

```yaml
sensor.meraki_ipsk_{name}:
  state: 'active' # active | expired | revoked | pending
  attributes:
    ipsk_id: 'abc123'
    name: 'SmartTV-LivingRoom'
    network_name: 'Home Network'
    ssid_name: 'IoT-Devices'
    ssid_number: 2
    group_policy: 'IoT Policy'
    passphrase_masked: 'Smar****'
    expires_at: '2026-02-01T00:00:00Z'
    created_at: '2026-01-12T10:00:00Z'
    associated_device: 'media_player.living_room_tv'
    associated_area: 'Living Room'
    associated_user: null
    associated_unit: null
    last_seen: '2026-01-12T15:30:00Z'
    connected_clients: 1
  device_class: null
  icon: mdi:key-wireless
```

#### Switch: IPSK Enable/Revoke

```yaml
switch.meraki_ipsk_{name}_enabled:
  state: 'on' # on = active, off = revoked
  # Turn off to revoke, turn on to re-enable
```

#### Binary Sensor: IPSK Connected

```yaml
binary_sensor.meraki_ipsk_{name}_connected:
  state: 'on' # on = device(s) currently connected
  attributes:
    connected_clients: 1
  device_class: connectivity
```

#### Button: Reveal Passphrase

```yaml
button.meraki_ipsk_{name}_reveal:
  # When pressed, fires event with passphrase
  # Or shows in persistent notification (configurable)
```

### 4. HA Services

```yaml
# Create a new IPSK
meraki_ha.create_ipsk:
  fields:
    name:
      required: true
      selector:
        text:
    network_id:
      required: true
      selector:
        select:
          options: '{{ networks }}'
    ssid_number:
      required: true
      selector:
        number:
          min: 0
          max: 14
    passphrase:
      required: false
      selector:
        text:
    duration_hours:
      required: false
      selector:
        number:
          min: 1
          max: 8760 # 1 year
    group_policy_id:
      required: false
      selector:
        select:
          options: '{{ group_policies }}'
    associated_device:
      required: false
      selector:
        device:
    associated_area:
      required: false
      selector:
        area:
    associated_user:
      required: false
      selector:
        text:
    associated_unit:
      required: false
      selector:
        select:
          options: '{{ areas }}' # HA areas as room options

# Revoke an IPSK
meraki_ha.revoke_ipsk:
  target:
    entity:
      integration: meraki_ha
      domain: sensor
  fields: {}

# Delete an IPSK permanently
meraki_ha.delete_ipsk:
  target:
    entity:
      integration: meraki_ha
      domain: sensor
  fields: {}

# Update IPSK association
meraki_ha.update_ipsk_association:
  target:
    entity:
      integration: meraki_ha
      domain: sensor
  fields:
    associated_device:
      selector:
        device:
    associated_area:
      selector:
        area:
    associated_user:
      selector:
        text:
    associated_unit:
      selector:
        select:
          options: '{{ areas }}'

# Bulk import IPSKs (for migration)
meraki_ha.import_ipsks:
  fields:
    network_id:
      required: true
    ssid_number:
      required: true
    # Imports existing IPSKs from Meraki and creates entities
```

### 5. Persistent Storage

Store IPSK metadata in Home Assistant's storage:

```python
# .storage/meraki_ha.ipsks
{
    "version": 1,
    "data": {
        "ipsks": {
            "abc123": {
                "id": "abc123",
                "name": "SmartTV-LivingRoom",
                "network_id": "L_123456",
                "ssid_number": 2,
                "passphrase_encrypted": "...",
                "associated_ha_device_id": "device_id_123",
                "associated_ha_area_id": "living_room",
                "associated_user_name": null,
                "associated_unit": null,
                "created_at": "2026-01-12T10:00:00Z",
                "created_by": "admin"
            }
        }
    }
}
```

### 6. WebSocket API for Add-on Communication

Expose WebSocket commands for the WPN Portal add-on:

```python
# Register WebSocket commands
@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/list",
    vol.Optional("network_id"): str,
    vol.Optional("ssid_number"): int,
    vol.Optional("status"): str,
})
async def ws_ipsk_list(hass, connection, msg): ...

@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/create",
    vol.Required("name"): str,
    vol.Required("network_id"): str,
    vol.Required("ssid_number"): int,
    vol.Optional("passphrase"): str,
    vol.Optional("duration_hours"): int,
    vol.Optional("group_policy_id"): str,
    vol.Optional("associated_device_id"): str,
    vol.Optional("associated_area_id"): str,
    vol.Optional("associated_user"): str,
    vol.Optional("associated_unit"): str,
})
async def ws_ipsk_create(hass, connection, msg): ...

@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/revoke",
    vol.Required("ipsk_id"): str,
})
async def ws_ipsk_revoke(hass, connection, msg): ...

@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/delete",
    vol.Required("ipsk_id"): str,
})
async def ws_ipsk_delete(hass, connection, msg): ...

@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/get",
    vol.Required("ipsk_id"): str,
    vol.Optional("include_passphrase"): bool,  # Requires admin
})
async def ws_ipsk_get(hass, connection, msg): ...

@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/update",
    vol.Required("ipsk_id"): str,
    vol.Optional("associated_device_id"): str,
    vol.Optional("associated_area_id"): str,
    vol.Optional("associated_user"): str,
    vol.Optional("associated_unit"): str,
})
async def ws_ipsk_update(hass, connection, msg): ...

# Get available options for dropdowns
@websocket_api.websocket_command({
    vol.Required("type"): "meraki_ha/ipsk/options",
})
async def ws_ipsk_options(hass, connection, msg):
    """Return available networks, SSIDs, group policies, areas."""
    ...
```

### 7. Configuration Options

Add to integration options flow:

```python
# In options_flow.py
IPSK_OPTIONS = {
    vol.Optional(CONF_IPSK_DEFAULT_DURATION, default=24): int,  # hours
    vol.Optional(CONF_IPSK_AUTO_EXPIRE_CLEANUP, default=True): bool,
    vol.Optional(CONF_IPSK_PASSPHRASE_LENGTH, default=12): int,
    vol.Optional(CONF_IPSK_NOTIFY_ON_EXPIRE, default=True): bool,
    vol.Optional(CONF_IPSK_NOTIFY_ON_CONNECT, default=False): bool,
}
```

### 8. Events

Fire events for automations:

```python
# When IPSK is created
hass.bus.async_fire("meraki_ipsk_created", {
    "ipsk_id": "abc123",
    "name": "Guest-John",
    "ssid_name": "Guest-WiFi",
    "expires_at": "2026-01-13T10:00:00Z",
})

# When IPSK expires
hass.bus.async_fire("meraki_ipsk_expired", {
    "ipsk_id": "abc123",
    "name": "Guest-John",
})

# When device connects using IPSK
hass.bus.async_fire("meraki_ipsk_device_connected", {
    "ipsk_id": "abc123",
    "name": "Guest-John",
    "client_mac": "aa:bb:cc:dd:ee:ff",
})

# When device disconnects
hass.bus.async_fire("meraki_ipsk_device_disconnected", {
    "ipsk_id": "abc123",
    "name": "Guest-John",
    "client_mac": "aa:bb:cc:dd:ee:ff",
})
```

## Implementation Tasks

- [ ] Create `ManagedIPSK` dataclass in `custom_components/meraki_ha/core/models/ipsk.py`
- [ ] Create `IPSKStore` for persistent storage in `custom_components/meraki_ha/core/ipsk_store.py`
- [ ] Create `IPSKCoordinator` in `custom_components/meraki_ha/coordinators/ipsk_coordinator.py`
- [ ] Add IPSK API methods to `WirelessEndpoints` (get_identity_psks, sync with Meraki)
- [ ] Create `IPSKSensor` entity in `custom_components/meraki_ha/sensor/ipsk_sensor.py`
- [ ] Create `IPSKSwitch` entity in `custom_components/meraki_ha/switch/ipsk_switch.py`
- [ ] Create `IPSKConnectedBinarySensor` in `custom_components/meraki_ha/binary_sensor/ipsk_connected.py`
- [ ] Create `IPSKRevealButton` in `custom_components/meraki_ha/button/ipsk_reveal.py`
- [ ] Register WebSocket API commands in `custom_components/meraki_ha/api/websocket.py`
- [ ] Add HA services in `custom_components/meraki_ha/services/ipsk_services.py`
- [ ] Update `services.yaml` with IPSK service definitions
- [ ] Add IPSK options to options flow
- [ ] Add translations for all new entities and services
- [ ] Write unit tests for IPSK coordinator
- [ ] Write unit tests for IPSK entities
- [ ] Write unit tests for WebSocket API
- [ ] Update documentation

## File Structure

```text
custom_components/meraki_ha/
├── core/
│   ├── models/
│   │   └── ipsk.py              # ManagedIPSK dataclass
│   └── ipsk_store.py            # Persistent storage
├── coordinators/
│   └── ipsk_coordinator.py      # IPSK data coordinator
├── sensor/
│   └── ipsk_sensor.py           # IPSK status sensor
├── switch/
│   └── ipsk_switch.py           # IPSK enable/revoke switch
├── binary_sensor/
│   └── ipsk_connected.py        # IPSK connection status
├── button/
│   └── ipsk_reveal.py           # Reveal passphrase button
├── api/
│   └── websocket.py             # WebSocket API (add IPSK commands)
├── services/
│   └── ipsk_services.py         # HA services for IPSK
└── services.yaml                # Service definitions
```

## Related

- Depends on: Existing Meraki API client, wireless endpoints
- Enables: WPN Registration Portal Add-on (separate repository)
- References: [Meraki IPSK API Documentation](https://developer.cisco.com/meraki/api-v1/#!create-network-wireless-ssid-identity-psk)

## Acceptance Criteria

1. [ ] Can create IPSKs via HA service call
2. [ ] IPSKs appear as sensor entities with full attribute data
3. [ ] Can revoke IPSKs via switch entity
4. [ ] Can associate IPSKs with HA devices/areas
5. [ ] WebSocket API accessible for external add-ons
6. [ ] Events fired for IPSK lifecycle changes
7. [ ] Passphrase stored encrypted in HA storage
8. [ ] Unit test coverage > 90%
9. [ ] All entities have proper translations

## Labels

`enhancement`, `feature`, `ipsk`, `wireless`
