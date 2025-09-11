### Instructions for the next Jules agent

**Objective:** Fix the Meraki Home Assistant integration's web UI.

**Blocker:** The execution environment is extremely unstable. The `custom_components/meraki_ha/www/` directory is repeatedly deleted, preventing the frontend build from completing.

**Solution (The Plan to Execute):** The next agent must implement the following refactoring plan. The solution has been fully worked out.

**!! CRITICAL INSTRUCTION !!**
Due to the environment instability, **all file modifications should be performed in a single, rapid sequence** to minimize the window of time in which the files can be deleted. Do not perform exploratory actions. Execute this plan directly.

---

### The Plan

**1. Apply Backend Refactor**
*   **Action:** Delete the file `custom_components/meraki_ha/web_server.py`.
*   **Action:** Overwrite `custom_components/meraki_ha/__init__.py` with the content provided below in "Code Block 1".

**2. Refactor the Frontend**
*   **Action:** Overwrite `custom_components/meraki_ha/www/vite.config.js` with the content provided below in "Code Block 2".
*   **Action:** Overwrite `custom_components/meraki_ha/www/src/main.tsx` with the content provided below in "Code Block 3".
*   **Note:** The original `www/index.html` file is not present in the base repository and is no longer needed; do not create it.

**3. Build and Submit**
*   **Action:** Run the following command in the shell:
    ```bash
    cd custom_components/meraki_ha/www/ && npm install && npm run build
    ```
*   **Action:** Verify that the file `custom_components/meraki_ha/www/dist/meraki-panel.js` exists.
*   **Action:** Submit the changes with a descriptive commit message.

---

### Code Blocks

**Code Block 1: `custom_components/meraki_ha/__init__.py`**
```python
"""The Meraki Home Assistant integration."""

import logging
import secrets

from yarl import URL
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.network import get_url
from homeassistant.components.frontend import (
    async_register_built_in_panel,
    async_remove_panel,
)

from .api.websocket import async_setup_websocket_api
from .const import (
    CONF_MERAKI_API_KEY,
    CONF_MERAKI_ORG_ID,
    CONF_SCAN_INTERVAL,
    CONF_ENABLE_WEB_UI,
    DATA_CLIENT,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_ENABLE_WEB_UI,
    DOMAIN,
    PLATFORMS,
)
from .core.api.client import MerakiAPIClient
from .core.coordinators.meraki_data_coordinator import MerakiDataCoordinator
from .core.coordinators.switch_port_status_coordinator import (
    SwitchPortStatusCoordinator,
)
from .core.coordinators.ssid_firewall_coordinator import SsidFirewallCoordinator
from .core.repository import MerakiRepository
from .webhook import async_register_webhook, async_unregister_webhook
from .core.repositories.camera_repository import CameraRepository
from .services.device_control_service import DeviceControlService
from .services.camera_service import CameraService
from .services.network_control_service import NetworkControlService


_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Meraki integration."""
    hass.data.setdefault(DOMAIN, {})
    async_setup_websocket_api(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Meraki from a config entry."""
    _LOGGER.debug("Setting up Meraki entry: %s", entry.entry_id)
    try:
        api_client = MerakiAPIClient(
            hass=hass,
            api_key=entry.data[CONF_MERAKI_API_KEY],
            org_id=entry.data[CONF_MERAKI_ORG_ID],
        )
    except KeyError as err:
        _LOGGER.error("Missing required configuration: %s", err)
        return False

    try:
        scan_interval = int(
            entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
        )
        if scan_interval <= 0:
            scan_interval = DEFAULT_SCAN_INTERVAL
    except (ValueError, TypeError):
        scan_interval = DEFAULT_SCAN_INTERVAL

    coordinator = MerakiDataCoordinator(
        hass=hass,
        api_client=api_client,
        scan_interval=scan_interval,
        config_entry=entry,
    )

    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        DATA_CLIENT: api_client,
    }

    repository = MerakiRepository(api_client)
    switch_port_coordinator = SwitchPortStatusCoordinator(
        hass=hass,
        repository=repository,
        main_coordinator=coordinator,
        config_entry=entry,
    )
    await switch_port_coordinator.async_refresh()
    hass.data[DOMAIN][entry.entry_id]["switch_port_coordinator"] = (
        switch_port_coordinator
    )

    hass.data[DOMAIN][entry.entry_id]["ssid_firewall_coordinators"] = {}
    if coordinator.data:
        for ssid in coordinator.data.get("ssids", []):
            if "networkId" in ssid and "number" in ssid:
                ssid_fw_coordinator = SsidFirewallCoordinator(
                    hass=hass,
                    api_client=api_client,
                    scan_interval=scan_interval,
                    network_id=ssid["networkId"],
                    ssid_number=ssid["number"],
                )
                await ssid_fw_coordinator.async_refresh()
                hass.data[DOMAIN][entry.entry_id]["ssid_firewall_coordinators"][
                    f"{ssid['networkId']}_{ssid['number']}"
                ] = ssid_fw_coordinator

    if entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI):
        panel_url_path = f"meraki_{entry.entry_id}"
        async_register_built_in_panel(
            hass,
            component_name="meraki",
            sidebar_title="Meraki",
            sidebar_icon="mdi:cisco-webex",
            frontend_url_path=panel_url_path,
            config={"config_entry_id": entry.entry_id},
            require_admin=True,
        )

    control_service = DeviceControlService(meraki_repository)
    camera_repository = CameraRepository(api_client, api_client.organization_id)
    camera_service = CameraService(camera_repository)
    network_control_service = NetworkControlService(api_client, coordinator)

    from .discovery.service import DeviceDiscoveryService

    discovery_service = DeviceDiscoveryService(
        coordinator=coordinator,
        config_entry=entry,
        meraki_client=api_client,
        switch_port_coordinator=switch_port_coordinator,
        camera_service=camera_service,
        control_service=control_service,
        network_control_service=network_control_service,
    )
    discovered_entities = await discovery_service.discover_entities()
    hass.data[DOMAIN][entry.entry_id]["entities"] = discovered_entities

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if "webhook_http_server_id" not in entry.data:
        webhook_id = entry.entry_id
        secret = secrets.token_hex(16)
        webhook = await async_register_webhook(
            hass, webhook_id, secret, api_client, entry
        )
        if webhook and "id" in webhook:
            hass.config_entries.async_update_entry(
                entry,
                data={
                    **entry.data,
                    "webhook_http_server_id": webhook["id"],
                    "secret": secret,
                },
            )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Meraki config entry."""
    if hass.data.get(DOMAIN) and entry.entry_id in hass.data[DOMAIN]:
        if "webhook_http_server_id" in entry.data:
            api_client = hass.data[DOMAIN][entry.entry_id][DATA_CLIENT]
            await async_unregister_webhook(
                hass, entry.data["webhook_http_server_id"], api_client
            )

        if entry.options.get(CONF_ENABLE_WEB_UI, DEFAULT_ENABLE_WEB_UI):
            panel_url_path = f"meraki_{entry.entry_id}"
            async_remove_panel(hass, panel_url_path)

    try:
        unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    except ValueError:
        _LOGGER.debug("Ignoring 'Config entry was never loaded!' error during unload.")
        unload_ok = True

    if unload_ok:
        if DOMAIN in hass.data:
            hass.data[DOMAIN].pop(entry.entry_id, None)
            if not hass.data[DOMAIN]:
                hass.data.pop(DOMAIN)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload Meraki config entry."""
    unload_ok = await async_unload_entry(hass, entry)
    if unload_ok:
        await async_setup_entry(hass, entry)
```

**Code Block 2: `custom_components/meraki_ha/www/vite.config.js`**
```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: 'src/main.tsx',
      name: 'MerakiPanel',
      fileName: (format) => `meraki-panel.js`,
      formats: ['es'],
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM',
        },
      },
    },
    outDir: 'dist',
    sourcemap: false,
    minify: true,
  },
});
```

**Code Block 3: `custom_components/meraki_ha/www/src/main.tsx`**
```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

interface PanelInfo {
  config: {
    config_entry_id: string;
  };
}

interface HassObject {
  connection: any;
  connected: boolean;
}

class MerakiPanel extends HTMLElement {
  private _root?: ReactDOM.Root;
  private _hass?: HassObject;
  private _panel?: PanelInfo;

  connectedCallback() {
    this._root = ReactDOM.createRoot(this);
    this._render();
  }

  disconnectedCallback() {
    if (this._root) {
      this._root.unmount();
      this._root = undefined;
    }
  }

  set hass(hass: HassObject) {
    this._hass = hass;
    this._render();
  }

  set panel(panel: PanelInfo) {
    this._panel = panel;
    this._render();
  }

  private _render() {
    if (!this._root || !this._hass || !this._panel) {
      return;
    }

    this._root.render(
      <React.StrictMode>
        <App hass={this._hass} config_entry_id={this._panel.config.config_entry_id} />
      </React.StrictMode>
    );
  }
}

customElements.define('meraki-panel', MerakiPanel);
```
