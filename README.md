# Meraki Home Assistant Integration 🏠☁️

Welcome to the **Meraki Home Assistant Integration**! This project bridges the gap between your Cisco Meraki cloud-managed network and your local Home Assistant instance. Whether you're managing a home lab, a small business, or just love having total control over your network gear, this integration has you covered.

**Note:** This is currently in **Beta**. We're moving fast and improving stability, so feedback is always welcome!

## ✨ Features

We support a wide range of Meraki devices and features, bringing cloud management down to earth:

### 📹 Cameras (MV Series)

Keep an eye on things with robust camera integration.

- Live Status: See if your cameras are online or offline instantly.
- Streaming: View RTSP streams directly in your dashboard (requires local access).
- Motion Detection: (Where supported) trigger automations based on camera activity.

### 🔌 Switches (MS)

Manage your wired network like a pro.

- Port Control: Cycle power to PoE ports to reboot sticky devices remotely.
- Monitoring: Track power usage (PoE) and connectivity status per port.
- VLANs: View VLAN configurations and status.

### 🌡️ Sensors (MT Series)

Environmental monitoring made easy.

- Complete Range: Support for MT10 (Temp/Humidity), MT11 (Temp/Probe), MT12 (Water Leak), MT14 (Air Quality), and MT20 (Door Open/Close).
- MT40: Full support for the MT40 Smart Power Controller (new!).

### 📶 Wireless (MR)

Control your Wi-Fi experience.

- SSID Management: Toggle SSIDs on or off dynamically.
- Client Counts: See how many devices are connected to each network in real-time.

### 🛡️ Gateways (MX)

- Uplink Status: Monitor your internet connection health and failover status.

## 🖥️ The Dashboard

We've built a custom **Meraki Panel** right into Home Assistant. It gives you a bird's-eye view of your organization without needing to clutter your standard Lovelace dashboard with hundreds of entities.

![Network View](docs/images/network_view.png)
_The Network View provides a quick summary of all your sites._

![Device Detail](docs/images/device_detail_view.png)
_Drill down into specific devices for detailed controls and metrics._

## 🚀 Getting Started

1. **Install:** Use HACS (recommended) to install "Meraki Home Assistant". Alternatively, copy the `custom_components/meraki_ha` folder to your HA `custom_components` directory.
2. **Configure:** Go to **Settings > Devices & Services > Add Integration** and search for "Meraki".
3. **API Key:** Enter your Meraki Dashboard API Key. The integration will discover your organizations.
4. **Enjoy:** Check out the new "Meraki" panel in your sidebar!

## 🤝 Contributing

We love contributions! Please read our [CONTRIBUTING.md](CONTRIBUTING.md) and [DEVELOPMENT.md](DEVELOPMENT.md) guides to get started.

## 🤖 Development & AI Collaboration

This project uses **Jules AI** as an asynchronous coding partner to accelerate development and maintain 2026.1 architectural standards.

### 🛠 How We Build
- **Branches:** All active development happens on the `beta` branch. The `main` branch is protected and reserved for stable production releases.
- **Task Delegation:** We use the `[Jules]` issue template to assign specific refactors or features to the AI.
- **Human Oversight:** Every AI-generated Pull Request undergoes a human code review. We verify 2026.1 compliance (Sentence case, Diagnostic categories, and `has_entity_name`) before merging.

### 🤝 Contributing Alongside AI
Humans are welcome! If you'd like to contribute:
1. Check the `ROADMAP.md` to see what Jules is currently working on to avoid merge conflicts.
2. Use our Issue Templates so both the maintainers and Jules can understand your bug reports or feature requests.
3. If you're a developer, refer to `AGENTS.md` for our specific AI coding conventions.

---

_Built with ❤️ by the Open Source Community._
