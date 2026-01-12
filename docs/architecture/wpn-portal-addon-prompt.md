WPN Portal Add-on Development Prompt

Copy and paste this entire prompt into a new AI agent session for the add-on repository.

---

## PROMPT START

You are building a **Cisco Meraki Wireless Personal Network (WPN) Registration Portal** as a Home Assistant Add-on. This is a Docker-based add-on that provides a beautiful, publicly-accessible portal for residents/guests to register for WiFi access, and an admin dashboard for managing Identity PSKs (IPSKs).

## Project Overview

### Purpose

Create a self-service WiFi registration portal for multi-dwelling units (apartments, dormitories, senior living, hotels) that:

1. Allows residents to self-register and receive their personal WiFi credentials
2. Provides an admin dashboard for IPSK management
3. Integrates deeply with Home Assistant via WebSocket API
4. Associates IPSKs with Home Assistant devices, areas, and users

### Technology Stack

| Layer          | Technology                                  |
| -------------- | ------------------------------------------- |
| Container      | Docker                                      |
| Backend        | Python 3.12+, FastAPI, uvicorn              |
| Frontend       | React 18+, TypeScript, Vite                 |
| Database       | SQLite (dev), PostgreSQL (optional prod)    |
| HA Integration | Home Assistant WebSocket API                |
| Styling        | CSS with Cisco Meraki branding (blue theme) |

### Architecture

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Meraki WPN Portal Add-on (Docker)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         FastAPI Backend                                │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │  │
│  │  │ Auth API    │  │ IPSK API    │  │ Devices API │  │ Admin API   │   │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │  │
│  │                              │                                         │  │
│  │  ┌───────────────────────────┴───────────────────────────────────┐    │  │
│  │  │                    HA WebSocket Client                         │    │  │
│  │  │  • Calls meraki_ha/ipsk/* commands                            │    │  │
│  │  │  • Fetches devices, areas, entities                           │    │  │
│  │  │  • Subscribes to state changes                                │    │  │
│  │  └───────────────────────────────────────────────────────────────┘    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      React Frontend                                    │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐     │  │
│  │  │ Public Portal    │  │ Admin Dashboard  │  │ IPSK Manager     │     │  │
│  │  │ (Registration)   │  │ (HA Auth)        │  │ (Device Assoc)   │     │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘     │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         Configuration                                  │  │
│  │  • HA URL & Long-Lived Access Token                                   │  │
│  │  • Auth Methods: Self-Reg, Invite Codes, Email Verification           │  │
│  │  • Branding: Logo URL, Property Name, Colors                          │  │
│  │  • Default SSID, Network, Group Policy                                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ WebSocket API
                                    ▼
                    ┌───────────────────────────┐
                    │      Home Assistant       │
                    │    meraki_ha integration  │
                    │  (IPSK Manager backend)   │
                    └───────────────────────────┘
```

## Repository Structure

```text
meraki-wpn-portal/
├── .github/
│   └── workflows/
│       └── build.yaml              # Build and publish Docker image
├── Dockerfile                       # Multi-stage build
├── config.yaml                      # HA Add-on configuration
├── run.sh                           # Startup script
├── DOCS.md                          # Add-on documentation
├── README.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app entry
│   │   ├── config.py                # Settings from environment
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py              # Dependencies (auth, db)
│   │   │   ├── auth.py              # Authentication endpoints
│   │   │   ├── registration.py      # Public registration endpoints
│   │   │   ├── ipsk.py              # IPSK management endpoints
│   │   │   ├── devices.py           # HA device endpoints
│   │   │   └── admin.py             # Admin endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── ha_client.py         # Home Assistant WebSocket client
│   │   │   ├── security.py          # Password hashing, JWT
│   │   │   └── invite_codes.py      # Invite code management
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py              # User/Resident model
│   │   │   ├── registration.py      # Registration request model
│   │   │   └── invite_code.py       # Invite code model
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py          # SQLAlchemy setup
│   │   │   └── models.py            # DB models
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── auth.py              # Auth request/response schemas
│   │       ├── registration.py      # Registration schemas
│   │       ├── ipsk.py              # IPSK schemas
│   │       └── device.py            # Device schemas
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_registration.py
│       ├── test_ipsk.py
│       └── test_ha_client.py
├── frontend/
│   ├── public/
│   │   └── meraki-logo.svg
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── index.css                # Meraki theme
│   │   ├── api/
│   │   │   └── client.ts            # API client
│   │   ├── components/
│   │   │   ├── Layout.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── QRCode.tsx
│   │   │   ├── IPSKCard.tsx
│   │   │   ├── DeviceSelector.tsx
│   │   │   └── AreaSelector.tsx     # HA areas dropdown
│   │   ├── pages/
│   │   │   ├── public/
│   │   │   │   ├── Registration.tsx
│   │   │   │   ├── MyNetwork.tsx
│   │   │   │   └── Success.tsx
│   │   │   └── admin/
│   │   │       ├── Dashboard.tsx
│   │   │       ├── IPSKManager.tsx
│   │   │       ├── DeviceAssociation.tsx
│   │   │       ├── InviteCodes.tsx
│   │   │       └── Settings.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useIPSK.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   └── types/
│   │       ├── ipsk.ts
│   │       ├── device.ts
│   │       └── user.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
└── translations/
    └── en.yaml                      # Add-on translations
```

## Cisco Meraki Branding

### Color Palette

```css
:root {
  /* Primary Meraki Blue */
  --meraki-blue: #00a4e4;
  --meraki-blue-dark: #0078a8;
  --meraki-blue-light: #e6f7fd;

  /* Secondary Colors */
  --meraki-navy: #003b5c;
  --meraki-teal: #00b5ad;
  --meraki-green: #78be20;

  /* Cisco Brand Colors */
  --cisco-blue: #049fd9;
  --cisco-dark: #1e4471;

  /* Neutral Colors */
  --gray-900: #1a202c;
  --gray-700: #4a5568;
  --gray-500: #a0aec0;
  --gray-300: #e2e8f0;
  --gray-100: #f7fafc;
  --white: #ffffff;

  /* Status Colors */
  --success: #48bb78;
  --warning: #ecc94b;
  --error: #f56565;

  /* Typography */
  --font-family: 'CiscoSans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Spacing */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

### Design Guidelines

1. **Header**: Meraki blue gradient background with white text
2. **Cards**: White background with subtle shadow, rounded corners
3. **Buttons**:
   - Primary: Meraki blue with white text
   - Secondary: White with blue border
   - Danger: Red for destructive actions
4. **Forms**: Clean, spacious inputs with blue focus states
5. **Icons**: Use material design icons or similar clean iconography
6. **Logo**: Cisco Meraki logo in header, customizable property logo below

## Configuration Options (config.yaml)

```yaml
name: 'Meraki WPN Portal'
description: 'Self-service WiFi registration portal for Meraki networks'
version: '1.0.0'
slug: 'meraki-wpn-portal'
arch:
  - aarch64
  - amd64
  - armv7
url: 'https://github.com/yourusername/meraki-wpn-portal'
ingress: true
ingress_port: 8099
panel_icon: 'mdi:wifi-plus'
panel_title: 'WPN Portal'
ports:
  8080/tcp: 8080
ports_description:
  8080/tcp: 'Public registration portal'
options:
  # Home Assistant Connection
  ha_url: 'http://homeassistant.local:8123'
  ha_token: ''

  # Branding
  property_name: 'My Property'
  logo_url: ''
  primary_color: '#00A4E4'

  # Default Network Settings
  default_network_id: ''
  default_ssid_number: 0
  default_group_policy_id: ''

  # Authentication Methods (admin can toggle)
  auth_self_registration: true
  auth_invite_codes: true
  auth_email_verification: false
  auth_sms_verification: false

  # Registration Options
  require_unit_number: true
  unit_source: 'ha_areas' # "ha_areas" | "manual_list" | "free_text"
  manual_units: []

  # IPSK Settings
  default_ipsk_duration_hours: 0 # 0 = permanent
  passphrase_length: 12

  # Admin Settings
  admin_notification_email: ''

schema:
  ha_url: str
  ha_token: password
  property_name: str
  logo_url: url?
  primary_color: str?
  default_network_id: str
  default_ssid_number: int(0,14)
  default_group_policy_id: str?
  auth_self_registration: bool
  auth_invite_codes: bool
  auth_email_verification: bool
  auth_sms_verification: bool
  require_unit_number: bool
  unit_source: list(ha_areas|manual_list|free_text)
  manual_units:
    - str
  default_ipsk_duration_hours: int(0,8760)
  passphrase_length: int(8,32)
  admin_notification_email: email?
```

## API Endpoints

### Public Endpoints (No Auth Required)

```text
POST /api/register
  Request:
    {
      "name": "John Smith",
      "email": "john@example.com",
      "unit": "201",  // or area_id if using HA areas
      "invite_code": "WELCOME2026"  // optional
    }
  Response:
    {
      "success": true,
      "ipsk_name": "Unit-201-John",
      "ssid_name": "Resident-WiFi",
      "passphrase": "SecurePass123",
      "qr_code": "data:image/png;base64,...",
      "wifi_config_string": "WIFI:T:WPA;S:Resident-WiFi;P:SecurePass123;;"
    }

GET /api/my-network?email={email}&code={verification_code}
  Response:
    {
      "ipsk_name": "Unit-201-John",
      "ssid_name": "Resident-WiFi",
      "passphrase": "SecurePass123",
      "status": "active",
      "connected_devices": 2
    }

GET /api/options
  Response:
    {
      "property_name": "Sunset Apartments",
      "logo_url": "https://...",
      "units": ["101", "102", "201", "202"],  // or HA areas
      "auth_methods": {
        "self_registration": true,
        "invite_codes": true,
        "email_verification": false
      }
    }
```

### Admin Endpoints (Requires HA Auth)

```text
# IPSK Management (proxies to HA meraki_ha/ipsk/* WebSocket)
GET    /api/admin/ipsks
POST   /api/admin/ipsks
GET    /api/admin/ipsks/{ipsk_id}
PUT    /api/admin/ipsks/{ipsk_id}
DELETE /api/admin/ipsks/{ipsk_id}
POST   /api/admin/ipsks/{ipsk_id}/revoke
POST   /api/admin/ipsks/{ipsk_id}/reveal-passphrase

# Device Association
GET    /api/admin/ha/devices          # List HA devices
GET    /api/admin/ha/areas            # List HA areas
POST   /api/admin/ipsks/{ipsk_id}/associate
  Request:
    {
      "device_id": "device_123",  // or
      "area_id": "living_room"
    }

# Invite Codes
GET    /api/admin/invite-codes
POST   /api/admin/invite-codes
DELETE /api/admin/invite-codes/{code}

# Settings
GET    /api/admin/settings
PUT    /api/admin/settings

# Dashboard Stats
GET    /api/admin/stats
  Response:
    {
      "total_ipsks": 47,
      "active_ipsks": 42,
      "expired_ipsks": 5,
      "online_devices": 12,
      "registrations_today": 3
    }
```

## Home Assistant WebSocket Integration

The add-on communicates with Home Assistant via WebSocket to manage IPSKs:

```python
# backend/app/core/ha_client.py

import aiohttp
from typing import Any

class HomeAssistantClient:
    """Client for Home Assistant WebSocket API."""

    def __init__(self, url: str, token: str):
        self.url = url.rstrip("/")
        self.ws_url = f"{self.url.replace('http', 'ws')}/api/websocket"
        self.token = token
        self._ws = None
        self._msg_id = 0

    async def connect(self) -> None:
        """Connect to Home Assistant WebSocket."""
        ...

    async def _send_command(self, command: dict[str, Any]) -> dict[str, Any]:
        """Send a command and wait for response."""
        ...

    # IPSK Management (calls meraki_ha integration)
    async def list_ipsks(
        self,
        network_id: str | None = None,
        ssid_number: int | None = None,
        status: str | None = None,
    ) -> list[dict]:
        """List all IPSKs."""
        return await self._send_command({
            "type": "meraki_ha/ipsk/list",
            "network_id": network_id,
            "ssid_number": ssid_number,
            "status": status,
        })

    async def create_ipsk(
        self,
        name: str,
        network_id: str,
        ssid_number: int,
        passphrase: str | None = None,
        duration_hours: int | None = None,
        group_policy_id: str | None = None,
        associated_device_id: str | None = None,
        associated_area_id: str | None = None,
        associated_user: str | None = None,
        associated_unit: str | None = None,
    ) -> dict:
        """Create a new IPSK."""
        return await self._send_command({
            "type": "meraki_ha/ipsk/create",
            "name": name,
            "network_id": network_id,
            "ssid_number": ssid_number,
            "passphrase": passphrase,
            "duration_hours": duration_hours,
            "group_policy_id": group_policy_id,
            "associated_device_id": associated_device_id,
            "associated_area_id": associated_area_id,
            "associated_user": associated_user,
            "associated_unit": associated_unit,
        })

    async def revoke_ipsk(self, ipsk_id: str) -> None:
        """Revoke an IPSK."""
        await self._send_command({
            "type": "meraki_ha/ipsk/revoke",
            "ipsk_id": ipsk_id,
        })

    async def get_ipsk(
        self,
        ipsk_id: str,
        include_passphrase: bool = False,
    ) -> dict:
        """Get IPSK details."""
        return await self._send_command({
            "type": "meraki_ha/ipsk/get",
            "ipsk_id": ipsk_id,
            "include_passphrase": include_passphrase,
        })

    async def get_ipsk_options(self) -> dict:
        """Get available networks, SSIDs, group policies, areas."""
        return await self._send_command({
            "type": "meraki_ha/ipsk/options",
        })

    # Home Assistant Data
    async def get_devices(self) -> list[dict]:
        """Get all HA devices."""
        return await self._send_command({
            "type": "config/device_registry/list",
        })

    async def get_areas(self) -> list[dict]:
        """Get all HA areas."""
        return await self._send_command({
            "type": "config/area_registry/list",
        })

    async def get_entities(self) -> list[dict]:
        """Get all HA entities."""
        return await self._send_command({
            "type": "config/entity_registry/list",
        })
```

## Frontend Pages

### 1. Public Registration Page (`/register`)

```text
┌─────────────────────────────────────────────────────────────────┐
│  ████████  CISCO  MERAKI                                        │
│  ═══════════════════════════════════════════════════════════════│
│                                                                  │
│              ┌────────────────────────────────────┐             │
│              │      🏢 Sunset Apartments          │             │
│              │      [Property Logo]               │             │
│              └────────────────────────────────────┘             │
│                                                                  │
│                  Welcome to Your WiFi Portal                     │
│                                                                  │
│     ┌─────────────────────────────────────────────────────┐     │
│     │                                                      │     │
│     │  👤 Full Name                                        │     │
│     │  ┌──────────────────────────────────────────────┐   │     │
│     │  │ John Smith                                   │   │     │
│     │  └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │  📧 Email Address                                    │     │
│     │  ┌──────────────────────────────────────────────┐   │     │
│     │  │ john@example.com                             │   │     │
│     │  └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │  🏠 Unit / Room                                      │     │
│     │  ┌──────────────────────────────────────────────┐   │     │
│     │  │ Select your unit...                       ▼  │   │     │
│     │  └──────────────────────────────────────────────┘   │     │
│     │  (Dropdown populated from HA areas or config)       │     │
│     │                                                      │     │
│     │  🎟️ Invitation Code (if provided)                   │     │
│     │  ┌──────────────────────────────────────────────┐   │     │
│     │  │ WELCOME2026                                  │   │     │
│     │  └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │  ┌──────────────────────────────────────────────┐   │     │
│     │  │         🌐  Get My WiFi Access               │   │     │
│     │  └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│           Already have access? [View My Network]                 │
│                                                                  │
│  ─────────────────────────────────────────────────────────────  │
│  Powered by Cisco Meraki | Privacy Policy | Help                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Success Page (`/success`)

```text
┌─────────────────────────────────────────────────────────────────┐
│  ████████  CISCO  MERAKI          Sunset Apartments             │
│  ═══════════════════════════════════════════════════════════════│
│                                                                  │
│                      ✅ You're All Set!                          │
│                                                                  │
│     ┌─────────────────────────────────────────────────────┐     │
│     │                                                      │     │
│     │   Your Personal WiFi Credentials                     │     │
│     │                                                      │     │
│     │   Network Name (SSID)                                │     │
│     │   ┌──────────────────────────────────────────────┐   │     │
│     │   │  Resident-WiFi                          📋   │   │     │
│     │   └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │   Password                                           │     │
│     │   ┌──────────────────────────────────────────────┐   │     │
│     │   │  SecurePass123                          📋   │   │     │
│     │   └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │   ┌──────────────────────────────────────────────┐   │     │
│     │   │                                              │   │     │
│     │   │         ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                     │   │     │
│     │   │         █ QR CODE FOR  █                     │   │     │
│     │   │         █ EASY CONNECT █                     │   │     │
│     │   │         █              █                     │   │     │
│     │   │         ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                     │   │     │
│     │   │                                              │   │     │
│     │   │   Scan with your phone's camera              │   │     │
│     │   └──────────────────────────────────────────────┘   │     │
│     │                                                      │     │
│     │   ┌────────────────┐  ┌────────────────────────┐    │     │
│     │   │  📧 Email Me   │  │  📱 Download Config    │    │     │
│     │   └────────────────┘  └────────────────────────┘    │     │
│     │                                                      │     │
│     └─────────────────────────────────────────────────────┘     │
│                                                                  │
│             Need help? Contact your property manager             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Admin Dashboard (`/admin`)

```text
┌─────────────────────────────────────────────────────────────────┐
│  ████████  MERAKI WPN ADMIN                    👤 Admin ▼       │
│  ═══════════════════════════════════════════════════════════════│
│  [Dashboard] [IPSKs] [Devices] [Invite Codes] [Settings]        │
│  ───────────────────────────────────────────────────────────────│
│                                                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │
│  │   47    │ │   42    │ │    5    │ │    3    │ │   12    │   │
│  │ Total   │ │ Active  │ │ Expired │ │ Revoked │ │ Online  │   │
│  │ IPSKs   │ │         │ │         │ │         │ │ Now     │   │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘   │
│                                                                  │
│  Recent Activity                          Registrations (7 days)│
│  ┌────────────────────────────────┐      ┌─────────────────────┐│
│  │ ✅ Unit 201 - John registered  │      │     ▄               ││
│  │ ⚠️  Guest-Jane expired         │      │   ▄ █ ▄             ││
│  │ 🔗 SmartTV linked to LG TV     │      │ ▄ █ █ █   ▄ ▄       ││
│  │ ✅ Unit 305 - Mary registered  │      │ █ █ █ █ ▄ █ █       ││
│  └────────────────────────────────┘      └─────────────────────┘│
│                                                                  │
│  Quick Actions                                                   │
│  ┌─────────────────────┐ ┌─────────────────────┐                │
│  │  ➕ Create IPSK     │ │  🎟️ Generate Codes  │                │
│  └─────────────────────┘ └─────────────────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4. IPSK Manager (`/admin/ipsks`)

```text
┌─────────────────────────────────────────────────────────────────┐
│  ████████  MERAKI WPN ADMIN                    👤 Admin ▼       │
│  ═══════════════════════════════════════════════════════════════│
│  [Dashboard] [IPSKs] [Devices] [Invite Codes] [Settings]        │
│  ───────────────────────────────────────────────────────────────│
│                                                                  │
│  IPSK Management                                                 │
│                                                                  │
│  ┌─────────────────┐ ┌───────────────┐ ┌───────────────┐        │
│  │ ➕ Create IPSK  │ │ 🔍 Search...  │ │ Filter: All ▼ │        │
│  └─────────────────┘ └───────────────┘ └───────────────┘        │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Name            │ Unit/Device    │ Status   │ Actions     │  │
│  ├───────────────────────────────────────────────────────────┤  │
│  │ Unit-201-John   │ 🏠 Unit 201    │ 🟢 Active │ ✏️ 👁️ 🗑️   │  │
│  │ SmartTV-Living  │ 📺 LG TV       │ 🟢 Active │ ✏️ 👁️ 🗑️   │  │
│  │ Guest-Jane      │ 👤 Jane Doe    │ 🟡 24h    │ ✏️ 👁️ 🗑️   │  │
│  │ IoT-Thermostat  │ 🌡️ Ecobee      │ 🟢 Active │ ✏️ 👁️ 🗑️   │  │
│  │ Apt-305-Mary    │ 🏠 Unit 305    │ 🟢 Active │ ✏️ 👁️ 🗑️   │  │
│  │ Old-Guest       │ 👤 Visitor     │ 🔴 Expired│ 🗑️          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ◀ Previous  Page 1 of 3  Next ▶                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Docker Build

```dockerfile
# Dockerfile
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS backend
WORKDIR /app

# Install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/app ./app

# Copy frontend build
COPY --from=frontend-builder /app/frontend/dist ./static

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Key Implementation Notes

1. **Authentication**:

   - Public endpoints: No auth required
   - Admin endpoints: Validate HA Long-Lived Access Token
   - Consider adding rate limiting for public registration

2. **Unit/Room Selection**:

   - Option A: Pull from Home Assistant areas via WebSocket
   - Option B: Manual list in add-on config
   - Option C: Free text input

3. **QR Code Generation**:

   - Use `qrcode` Python library
   - Format: `WIFI:T:WPA;S:{ssid};P:{password};;`

4. **Error Handling**:

   - Graceful fallback if HA WebSocket disconnects
   - Retry logic for transient failures
   - User-friendly error messages

5. **Security**:

   - Never log passphrases
   - Encrypt stored data
   - HTTPS required for production
   - CSRF protection on forms

6. **Testing**:
   - Unit tests for API endpoints
   - Integration tests with mock HA WebSocket
   - E2E tests for registration flow

## Getting Started

1. Create a new repository: `meraki-wpn-portal`
2. Initialize with the structure above
3. Start with the backend FastAPI skeleton
4. Implement HA WebSocket client
5. Build frontend registration page
6. Add admin dashboard
7. Create Dockerfile and config.yaml
8. Test as HA add-on

## Dependencies

### Backend (requirements.txt)

```text
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
aiohttp>=3.9.0
websockets>=12.0
sqlalchemy>=2.0.0
alembic>=1.13.0
pydantic>=2.5.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
qrcode[pil]>=7.4.0
python-multipart>=0.0.6
httpx>=0.26.0
```

### Frontend (package.json dependencies)

```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "axios": "^1.6.0",
    "qrcode.react": "^3.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

---

## PROMPT END

---

**Notes for the agent:**

- This add-on depends on the meraki_ha integration having the IPSK Manager feature (Option A issue) implemented
- The add-on acts as a frontend/API layer that proxies to Home Assistant
- Focus on the Cisco Meraki blue branding throughout
- The unit/room dropdown should support HA areas as a data source
