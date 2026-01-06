# Meraki Home Assistant Panel - Development Notes

**Status:** ✅ Resolved  
**Last Updated:** 2025-01-05

---

## Overview

This document describes the architecture of the Meraki Home Assistant custom panel and how to develop it further.

## Architecture

The Meraki panel is a React-based custom panel for Home Assistant. It follows the official HA custom panel pattern:

```
Home Assistant                     Meraki Panel
     │                                 │
     ├──── Creates <meraki-panel> ────►│
     │                                 │
     ├──── Sets hass property ────────►│
     │     (authenticated connection)  │
     │                                 │
     │◄─── hass.callWS() ─────────────┤
     │     {type: 'meraki_ha/get_config'}
     │                                 │
     ├──── Returns data ──────────────►│
```

### Key Components

| Component | Location | Purpose |
|-----------|----------|---------|
| Web Component Wrapper | `www/src/main.tsx` | Bridges HA panel system with React |
| React App | `www/src/App.tsx` | Main UI logic |
| TypeScript Types | `www/src/types/hass.ts` | HA object type definitions |
| Vite Config | `www/vite.config.js` | Builds IIFE bundle for HA |
| WebSocket API | `api/websocket.py` | Subscription handler for real-time updates |
| REST-style API | `web_api.py` | Request/response handlers |
| Panel Registration | `frontend.py` | Registers panel with HA |

### How the Panel Works

1. **Registration**: `frontend.py` registers the panel with Home Assistant, pointing to `meraki-panel.js`

2. **Loading**: When user navigates to the panel, HA loads the JavaScript and creates a `<meraki-panel>` element

3. **Property Injection**: HA sets these properties on the element:
   - `hass` - The Home Assistant object with states and connection
   - `panel` - Panel configuration including `config_entry_id`
   - `narrow` - Boolean for mobile/narrow mode
   - `route` - Current route information

4. **React Mounting**: The Web Component wrapper (`main.tsx`) passes these properties to the React app

5. **Data Fetching**: React uses `hass.callWS()` to call WebSocket commands like `meraki_ha/get_config`

## Development

### Frontend Development

```bash
cd custom_components/meraki_ha/www

# Install dependencies
npm install

# Development server (limited functionality without HA)
npm run dev

# Build for production
npm run build
```

The build process:
1. Compiles TypeScript/React with Vite
2. Outputs to `build/` directory
3. Copies `meraki-panel.js` and `style.css` to `www/` root

### Adding New WebSocket Commands

1. Add handler in `web_api.py`:

```python
@websocket_api.async_response
async def handle_my_command(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: dict[str, Any],
) -> None:
    # Handle the command
    connection.send_result(msg["id"], {"data": "result"})
```

2. Register in `async_setup_api()`:

```python
websocket_api.async_register_command(
    hass,
    "meraki_ha/my_command",
    handle_my_command,
    Schema({...}),
)
```

3. Call from frontend:

```typescript
const result = await hass.callWS({
  type: 'meraki_ha/my_command',
  config_entry_id: configEntryId,
});
```

### Available WebSocket Commands

| Command | Description |
|---------|-------------|
| `meraki_ha/get_config` | Get full Meraki data (networks, devices, SSIDs) |
| `meraki_ha/update_enabled_networks` | Enable/disable network tracking |
| `meraki_ha/get_camera_stream_url` | Get camera stream URL |
| `meraki_ha/get_camera_snapshot` | Get camera snapshot URL |
| `meraki_ha/create_timed_access_key` | Create temporary WiFi access |
| `meraki_ha/subscribe_meraki_data` | Subscribe to real-time updates |

## Previous Issues (Resolved)

The panel previously had these issues that have been fixed:

1. **Manual WebSocket Connection** - The old code created its own WebSocket and prompted for an access token. Now uses `hass.callWS()` which leverages HA's authenticated connection.

2. **Not a Web Component** - The old code mounted React to `document.getElementById('root')`. Now properly registers as a custom element that HA can instantiate.

3. **Unregistered Subscription Handler** - The `api/websocket.py` handler existed but wasn't registered in `__init__.py`. Now properly registered.

4. **Build Configuration** - Vite wasn't configured to output an IIFE bundle. Now builds a single `meraki-panel.js` file.

## Testing

After making changes:

1. Run `npm run build` in the `www/` directory
2. Restart Home Assistant
3. Clear browser cache (Ctrl+Shift+R)
4. Navigate to the Meraki panel

## File Structure

```
custom_components/meraki_ha/
├── __init__.py              # Integration setup, registers WebSocket APIs
├── frontend.py              # Panel registration
├── web_api.py               # WebSocket command handlers
├── api/
│   └── websocket.py         # Subscription handler
└── www/
    ├── src/
    │   ├── main.tsx         # Web Component wrapper
    │   ├── App.tsx          # Main React app
    │   ├── types/
    │   │   └── hass.ts      # HA TypeScript types
    │   └── components/      # React components
    ├── vite.config.js       # Build configuration
    ├── package.json         # Dependencies
    ├── meraki-panel.js      # Built bundle (served to HA)
    └── style.css            # Built styles
```
