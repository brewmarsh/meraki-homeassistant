import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { safeCallWS } from './utils/api';
import { WsCommand } from './types/websocket';

interface HassObject {
  connection: {
    sendMessagePromise<T = unknown>(message: Record<string, unknown>): Promise<T>;
  };
  callWS<T = unknown>(message: Record<string, unknown>): Promise<T>;
  [key: string]: unknown;
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

interface ConfigEntry {
  entry_id: string;
  domain: string;
}

const getConfigEntryId = async (hass: HassObject): Promise<string> => {
  const entries = await hass.callWS<ConfigEntry[]>({
    type: 'config_entries/get',
    domain: 'meraki_ha',
  });

  if (entries && entries.length > 0) {
    return entries[0].entry_id;
  }
  throw new Error('No configuration found');
};

const getMerakiData = async (hass: HassObject, entryId: string): Promise<MerakiData> => {
  return await safeCallWS<MerakiData>(hass, {
    type: WsCommand.GET_CONFIG,
    config_entry_id: entryId,
  });
};

const getErrorMessage = (err: unknown): string => {
  if (err && typeof err === 'object') {
    const errorObj = err as Record<string, unknown>;
    if (errorObj.code === 'not_found') {
      return 'Meraki integration not configured. Please add and configure the integration in Home Assistant.';
    }
    if (typeof errorObj.message === 'string') {
      return `Failed to fetch Meraki data: ${errorObj.message}`;
    }
  }
  if (err instanceof Error) {
    return `Failed to fetch Meraki data: ${err.message}`;
  }
  return `Failed to fetch Meraki data: Unknown error`;
};

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
      this.entryId = await getConfigEntryId(this.hass);
      this._data = await getMerakiData(this.hass, this.entryId);
    } catch (err: unknown) {
      this._error = getErrorMessage(err);
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
      await safeCallWS(this.hass, {
        type: WsCommand.UPDATE_ENABLED_NETWORKS,
        config_entry_id: this.entryId,
        enabled_networks,
      });
    } catch (err) {
      console.error('Error updating enabled networks:', err);
      this._data = originalData;
    }
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

    const { networks, version, enabled_networks } = this._data;

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
                    @change=${(e: Event) =>
                      this._handleToggle(network.id, (e.target as HTMLInputElement).checked)}
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
