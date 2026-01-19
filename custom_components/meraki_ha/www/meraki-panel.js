class MerakiPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._panel = null;
    this._subscription = null;
    this._lastData = null;
  }

  set hass(hass) {
    this._hass = hass;
    if (this._hass && this._panel && !this._subscription) {
      this._subscribeToMerakiData();
    }
  }

  set panel(panel) {
    this._panel = panel;
    if (this._hass && this._panel && !this._subscription) {
      this._subscribeToMerakiData();
    }
  }

  _subscribeToMerakiData() {
    if (!this._hass || !this._panel) return;

    this._subscription = this._hass.connection.subscribeMessage(
      (data) => this._updateContent(data),
      {
        type: 'meraki_ha/subscribe_meraki_data',
        config_entry_id: this._panel.config.config_entry_id,
      }
    );
  }

  connectedCallback() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          font-family: Arial, sans-serif;
          padding: 16px;
          display: block;
        }
        .card {
          background-color: #fff;
          border: 1px solid #ddd;
          border-radius: 4px;
          padding: 16px;
          margin-bottom: 16px;
        }
        h1, h2, h3 {
          margin-top: 0;
        }
        ul {
          padding-left: 20px;
        }
        li {
          margin-bottom: 8px;
        }
        .error {
          color: red;
          font-weight: bold;
        }
      </style>
      <div id="content">
        <h1>Meraki Dashboard</h1>
        <div class="card">
          <h2>Loading data...</h2>
        </div>
      </div>
    `;

    if (this._lastData) {
      this._updateContent(this._lastData);
    }
  }

  disconnectedCallback() {
    if (this._subscription) {
      this._subscription.then((unsub) => unsub());
      this._subscription = null;
    }
  }

  _escapeHTML(str) {
    if (typeof str !== 'string') return str;
    return str.replace(
      /[&<>'"]/g,
      (tag) =>
        ({
          '&': '&amp;',
          '<': '&lt;',
          '>': '&gt;',
          "'": '&#39;',
          '"': '&quot;',
        })[tag]
    );
  }

  _updateContent(data) {
    this._lastData = data;
    const content = this.shadowRoot.getElementById('content');
    if (!content) return; // connectedCallback will handle it

    if (!data) {
      content.innerHTML = `
        <h1>Meraki Dashboard</h1>
        <div class="card error">
          <h2>Error</h2>
          <p>Received no data from the Meraki integration.</p>
        </div>
      `;
      return;
    }

    const orgName = this._escapeHTML(data.org_name || 'Unknown Organization');
    const networks = data.networks || [];
    const devices = data.devices || [];
    const clients = data.clients || [];

    let html = `
      <h1>Meraki Dashboard</h1>
      <div class="card">
        <h2>Organization: ${orgName}</h2>
      </div>
    `;

    if (networks.length > 0) {
      html += '<div class="card">';
      html += '<h2>Networks & Devices</h2>';
      networks.forEach((network) => {
        const netName = this._escapeHTML(network.name);
        const netId = this._escapeHTML(network.id);
        html += `<h3>${netName} (ID: ${netId})</h3>`;
        const networkDevices = devices.filter(
          (d) => d.networkId === network.id
        );
        if (networkDevices.length > 0) {
          html += '<ul>';
          networkDevices.forEach((device) => {
            const devName = this._escapeHTML(device.name || 'Unnamed Device');
            const devType = this._escapeHTML(device.productType);
            const devSerial = this._escapeHTML(device.serial);
            html += `<li>${devName} (${devType} - ${devSerial})</li>`;
          });
          html += '</ul>';
        } else {
          html += '<p>No devices in this network.</p>';
        }
      });
      html += '</div>';
    }

    if (clients.length > 0) {
      html += '<div class="card">';
      html += '<h2>Clients</h2>';
      html += '<ul>';
      clients.forEach((client) => {
        const clientDesc = this._escapeHTML(
          client.description || 'Unknown Client'
        );
        const clientIp = this._escapeHTML(client.ip);
        html += `<li>${clientDesc} (${clientIp})</li>`;
      });
      html += '</ul>';
      html += '</div>';
    }

    content.innerHTML = html;
  }
}

customElements.define('meraki-panel', MerakiPanel);
