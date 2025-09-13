class MerakiLovelaceCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._config = null;
    this._subscription = null;
  }

  setConfig(config) {
    if (!config.config_entry_id) {
      throw new Error("config_entry_id must be specified");
    }
    this._config = config;
    if (this._hass) {
      this._subscribeToMerakiData();
    }
  }

  set hass(hass) {
    this._hass = hass;
    if (this._config) {
      this._subscribeToMerakiData();
    }
  }

  _subscribeToMerakiData() {
    if (!this._hass || !this._config || this._subscription) return;

    this._subscription = this._hass.connection.subscribeMessage(
      (data) => this._updateContent(data),
      {
        type: 'meraki_ha/subscribe_meraki_data',
        config_entry_id: this._config.config_entry_id,
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
  }

  disconnectedCallback() {
    if (this._subscription) {
      this._subscription.then(unsub => unsub());
      this._subscription = null;
    }
  }

  _updateContent(data) {
    const content = this.shadowRoot.getElementById('content');
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

    const orgName = data.org_name || 'Unknown Organization';
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
        networks.forEach(network => {
            html += `<h3>${network.name} (ID: ${network.id})</h3>`;
            const networkDevices = devices.filter(d => d.networkId === network.id);
            if (networkDevices.length > 0) {
                html += '<ul>';
                networkDevices.forEach(device => {
                    html += `<li>${device.name || 'Unnamed Device'} (${device.productType} - ${device.serial})</li>`;
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
        clients.forEach(client => {
            html += `<li>${client.description || 'Unknown Client'} (${client.ip})</li>`;
        });
        html += '</ul>';
        html += '</div>';
    }

    content.innerHTML = html;
  }
}

customElements.define('meraki-lovelace-card', MerakiLovelaceCard);
