import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { safeCallWS } from './utils/api';

interface HassObject {
  connection: {
    sendMessagePromise(message: any): Promise<any>;
  };
  callWS(message: any): Promise<any>;
  [key: string]: any;
}

interface PanelInfo {
  config: {
    config_entry_id: string;
  };
}

interface Network {
  id: string;
  name: string;
  is_enabled: boolean;
}

interface Device {
  name: string;
  model: string;
  serial: string;
  status: string;
  entity_id: string;
  networkId: string;
  lanIp?: string;
  mac?: string;
}

interface MerakiData {
  version: string;
  networks: Network[];
  devices: Device[];
  enabled_networks: string[];
}

@customElement('meraki-panel')
export class MerakiPanel extends LitElement {
  @property({ attribute: false }) hass!: HassObject;
  @property({ attribute: false }) panel!: PanelInfo;

  @state() private _data: MerakiData | null = null;
  @state() private _loading = true;
  @state() private _error: string | null = null;
  @state() private entryId: string | null = null;

  static styles = css`
    :host {
      display: block;
      padding: 16px;
    }
    ha-card {
      margin-bottom: 16px;
    }
    .card-header {
      display: flex;
      align-items: center;
      padding: 16px;
    }
    .card-content {
      padding: 16px;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    this._fetchData();
  }

  private async _fetchData() {
    if (!this.hass) {
      this._error = 'Home Assistant objects not available.';
      this._loading = false;
      return;
    }

    try {
      const entries = await this.hass.callWS({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });

      if (entries && (entries as any[]).length > 0) {
        this.entryId = (entries as any[])[0].entry_id;
      } else {
        this._error = 'No configuration found';
        this._loading = false;
        return;
      }

      const data = await safeCallWS<MerakiData>(this.hass, {
        type: 'meraki_ha/get_config',
        config_entry_id: this.entryId,
      });
      this._data = data;
    } catch (err: any) {
      if (err.code === 'not_found') {
        this._error = 'Meraki integration not configured. Please add and configure the integration in Home Assistant.';
      } else {
        this._error = `Failed to fetch Meraki data: ${err.message || 'Unknown error'}`;
      }
    } finally {
      this._loading = false;
    }
  }

  private async _handleToggle(networkId: string, enabled: boolean) {
    if (!this._data || !this.entryId) return;

    const enabled_networks = enabled
      ? [...this._data.enabled_networks, networkId]
      : this._data.enabled_networks.filter((id) => id !== networkId);

    const originalData = this._data;
    this._data = { ...this._data, enabled_networks };

    try {
      await this.hass.connection.sendMessagePromise({
        type: 'meraki_ha/update_enabled_networks',
        config_entry_id: this.entryId,
        enabled_networks,
      });
    } catch (err) {
      console.error('Error updating enabled networks:', err);
      this._data = originalData;
    }
  }

  private _moreInfo(entityId: string) {
    const event = new Event('hass-more-info', {
      bubbles: true,
      composed: true,
    });
    (event as any).detail = { entityId };
    this.dispatchEvent(event);
  }

  render() {
    if (this._loading) {
      return html`<p>Loading...</p>`;
    }

    if (this._error) {
      return html`<p>Error: ${this._error}</p>`;
    }

    if (!this._data) {
      return html`<p>No data found.</p>`;
    }

    const { networks, devices, version, enabled_networks } = this._data;

    return html`
      <ha-card header="Meraki Dashboard">
        <div class="card-content">
          ${networks.map(
            (network) => html`
              <ha-card .header="${network.name}">
                <div class="card-content">
                  <p>This is where the devices would go</p>
                </div>
                <div class="card-actions">
                  <ha-switch
                    .checked=${enabled_networks.includes(network.id)}
                    @change=${(e: any) =>
                      this._handleToggle(network.id, e.target.checked)}
                  >
                  </ha-switch>
                </div>
              </ha-card>
            `
          )}
        </div>
        <div style="text-align: center; margin-top: 16px;">
          <p>Version: ${version}</p>
        </div>
      </ha-card>
    `;
  }
}
