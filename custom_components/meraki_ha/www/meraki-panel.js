<<<<<<< HEAD
=======
/**
 * Meraki Home Assistant Panel
 * Implements a custom element for displaying Meraki data.
 */
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
class MerakiPanel extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this._hass = null;
    this._panel = null;
    this._subscription = null;
<<<<<<< HEAD
=======
    this._lastData = null;
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
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
<<<<<<< HEAD
=======

    if (this._lastData) {
      this._updateContent(this._lastData);
    }
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
  }

  disconnectedCallback() {
    if (this._subscription) {
      this._subscription.then((unsub) => unsub());
      this._subscription = null;
    }
  }

<<<<<<< HEAD
  _updateContent(data) {
    const content = this.shadowRoot.getElementById('content');
    content.innerHTML = '';

    if (!data) {
      const h1 = document.createElement('h1');
      h1.textContent = 'Meraki Dashboard';
      content.appendChild(h1);

      const errorCard = document.createElement('div');
      errorCard.className = 'card error';
      const h2 = document.createElement('h2');
      h2.textContent = 'Error';
      errorCard.appendChild(h2);
      const p = document.createElement('p');
      p.textContent = 'Received no data from the Meraki integration.';
      errorCard.appendChild(p);
      content.appendChild(errorCard);
      return;
    }

    const orgName = data.org_name || 'Unknown Organization';
=======
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
    if (!content) return;

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
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
    const networks = data.networks || [];
    const devices = data.devices || [];
    const clients = data.clients || [];

<<<<<<< HEAD
    const h1 = document.createElement('h1');
    h1.textContent = 'Meraki Dashboard';
    content.appendChild(h1);

    const orgCard = document.createElement('div');
    orgCard.className = 'card';
    const orgH2 = document.createElement('h2');
    orgH2.textContent = `Organization: ${orgName}`;
    orgCard.appendChild(orgH2);
    content.appendChild(orgCard);

    if (networks.length > 0) {
      const netCard = document.createElement('div');
      netCard.className = 'card';
      const netH2 = document.createElement('h2');
      netH2.textContent = 'Networks & Devices';
      netCard.appendChild(netH2);

      networks.forEach((network) => {
        const h3 = document.createElement('h3');
        h3.textContent = `${network.name} (ID: ${network.id})`;
        netCard.appendChild(h3);

=======
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
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
        const networkDevices = devices.filter(
          (d) => d.networkId === network.id
        );
        if (networkDevices.length > 0) {
<<<<<<< HEAD
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
=======
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
        const clientDesc = this._escapeHTML(client.description || 'Unknown Client');
        const clientIp = this._escapeHTML(client.ip);
        html += `<li>${clientDesc} (${clientIp})</li>`;
      });
      html += '</ul>';
      html += '</div>';
    }

    content.innerHTML = html;
>>>>>>> 44727ea (fix: ci workflow permissions, dependencies and services file)
  }
}

customElements.define('meraki-panel', MerakiPanel);
