class MerakiPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._panel = null;
    this._subscription = null;
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
  }

  disconnectedCallback() {
    if (this._subscription) {
      this._subscription.then((unsub) => unsub());
      this._subscription = null;
    }
  }

  _updateContent(data) {
    const content = this.shadowRoot.getElementById('content');
    content.innerHTML = ''; // Clear existing content

    const header = document.createElement('h1');
    header.textContent = 'Meraki Dashboard';
    content.appendChild(header);

    if (!data) {
      const card = document.createElement('div');
      card.className = 'card error';

      const h2 = document.createElement('h2');
      h2.textContent = 'Error';
      card.appendChild(h2);

      const p = document.createElement('p');
      p.textContent = 'Received no data from the Meraki integration.';
      card.appendChild(p);

      content.appendChild(card);
      return;
    }

    const orgName = data.org_name || 'Unknown Organization';
    const networks = data.networks || [];
    const devices = data.devices || [];
    const clients = data.clients || [];

    // Organization Card
    const orgCard = document.createElement('div');
    orgCard.className = 'card';
    const orgH2 = document.createElement('h2');
    orgH2.textContent = `Organization: ${orgName}`;
    orgCard.appendChild(orgH2);
    content.appendChild(orgCard);

    // Networks & Devices
    if (networks.length > 0) {
      const netCard = document.createElement('div');
      netCard.className = 'card';

      const netH2 = document.createElement('h2');
      netH2.textContent = 'Networks & Devices';
      netCard.appendChild(netH2);

      networks.forEach((network) => {
        const netH3 = document.createElement('h3');
        netH3.textContent = `${network.name} (ID: ${network.id})`;
        netCard.appendChild(netH3);

        const networkDevices = devices.filter(
          (d) => d.networkId === network.id
        );

        if (networkDevices.length > 0) {
          const ul = document.createElement('ul');
          networkDevices.forEach((device) => {
            const li = document.createElement('li');
            li.textContent = `${device.name || 'Unnamed Device'} (${device.productType} - ${device.serial})`;
            ul.appendChild(li);
          });
          netCard.appendChild(ul);
        } else {
          const p = document.createElement('p');
          p.textContent = 'No devices in this network.';
          netCard.appendChild(p);
        }
      });
      content.appendChild(netCard);
    }

    // Clients
    if (clients.length > 0) {
      const clientCard = document.createElement('div');
      clientCard.className = 'card';

      const clientH2 = document.createElement('h2');
      clientH2.textContent = 'Clients';
      clientCard.appendChild(clientH2);

      const ul = document.createElement('ul');
      clients.forEach((client) => {
        const li = document.createElement('li');
        li.textContent = `${client.description || 'Unknown Client'} (${client.ip})`;
        ul.appendChild(li);
      });
      clientCard.appendChild(ul);

      content.appendChild(clientCard);
    }
  }
}

customElements.define('meraki-panel', MerakiPanel);
