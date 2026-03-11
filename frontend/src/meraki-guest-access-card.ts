import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, renderLoading, sharedStyles } from './shared-ui';
import './meraki-content-filter-card';
import './meraki-wifi-qr-card';
import './meraki-network-vitals-card';
import './meraki-guest-access-card-editor';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';

declare const __VERSION__: string;

interface Config {
  type: string;
  name?: string;
  config_entry_id?: string;
}

export class MerakiGuestAccessCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  // Consolidate UI state into a single object for ha-form
  @state() private _formData = {
    network: '',
    ssid: '',
    duration: '60',
    guestName: ''
  };

  @state() private _creating: boolean = false;
  @state() private _error: string | null = null;
  @state() private _success: string | null = null;

  @state() private _policies: any[] = [];
  @state() private _isLoading: boolean = true;
  @state() private _initDone: boolean = false;
  @state() private _configEntryId: string = '';

  public static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = config;
  }

  protected updated(changedProperties: PropertyValues) {
    super.updated(changedProperties);
    if (changedProperties.has('hass') && this.hass) {
      if (!this._initDone) {
        this._initDone = true;
        this._fetchConfigEntry();
      }

      this._autoSelectAndLoad();

      // Pre-fill the guest name with the current HA user if blank
      if (this.hass.user?.name && !this._formData.guestName) {
        this._formData = { ...this._formData, guestName: this.hass.user.name };
      }
    }
  }

  private async _fetchConfigEntry() {
    if (!this.hass) return;
    try {
      const configEntries = await this.hass.callWS<any[]>({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });
      this._configEntryId = this._config?.config_entry_id || (configEntries.length > 0 ? configEntries[0].entry_id : '');
      if (this._formData.network) {
        this._fetchPolicies(this._formData.network);
      }
    } catch (err) {
      console.error("Failed to fetch Meraki config entries", err);
    }
  }

  private _autoSelectAndLoad() {
    const networks = this._getNetworks();
    if (networks.length > 0) {
      if (!this._formData.network) {
        this._formData = { ...this._formData, network: networks[0].id };
        this._fetchPolicies(this._formData.network);
      }
      this._isLoading = false;
    } else {
        if (this._isLoading && this._initDone) {
            setTimeout(() => {
                if (this._getNetworks().length === 0) {
                    this._isLoading = false;
                    this.requestUpdate();
                }
            }, 2000);
        }
    }
  }

  private _getNetworks(): Network[] {
    if (!this.hass) return [];
    const networks: Record<string, Network> = {};

    Object.values(this.hass.states).forEach(state => {
      const attrs = state.attributes;
      if (attrs.network_id && attrs.network_name) {
        const productTypes = attrs.product_types || [];
        if (productTypes.includes('wireless')) {
          networks[attrs.network_id] = {
            id: attrs.network_id,
            name: attrs.network_name,
            productTypes: productTypes
          };
        }
      }
    });

    return Object.values(networks);
  }

  private _getSsids(networkId: string): SSID[] {
    if (!this.hass || !networkId) return [];
    const ssids: Record<string, SSID> = {};

    Object.values(this.hass.states).forEach(state => {
      const attrs = state.attributes;
      if (attrs.network_id === networkId && attrs.ssid_number !== undefined && attrs.ssid_name) {
        ssids[attrs.ssid_number] = {
          name: attrs.ssid_name,
          number: attrs.ssid_number,
          networkId: attrs.network_id,
          enabled: attrs.enabled !== false,
          authMode: attrs.auth_mode
        };
      }
    });

    return Object.values(ssids).sort((a, b) => a.number - b.number);
  }

  private async _fetchPolicies(networkId: string) {
    if (!this.hass) return;
    const entryId = this._configEntryId || this._config?.config_entry_id;
    if (!entryId) return;

    try {
      const policies = await safeCallWS<any[]>(this.hass, {
        type: WsCommand.TIMED_ACCESS_GET_POLICIES,
        config_entry_id: entryId,
        network_id: networkId,
      });
      this._policies = Array.isArray(policies) ? policies : (policies as any)?.policies || [];
    } catch (err) {
      this._policies = [];
    }
  }

  private _formValueChanged(ev: CustomEvent) {
    const newValues = ev.detail.value;
    const oldNetwork = this._formData.network;
    
    this._formData = { ...this._formData, ...newValues };

    // If the user changed the network dropdown, aggressively clear the SSID
    if (this._formData.network !== oldNetwork) {
      this._formData = { ...this._formData, ssid: '' };
      if (this._formData.network) {
        this._fetchPolicies(this._formData.network);
      }
    }
  }

  private _computeLabel = (schema: any): string => {
    if (schema.name === "network") return "Network";
    if (schema.name === "ssid") return "SSID";
    if (schema.name === "duration") return "Duration";
    if (schema.name === "guestName") return "Guest Name";
    return schema.name;
  }

  protected render() {
    if (this._isLoading) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content flex justify-center p-8">
            ${renderLoading("Loading...")}
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const networks = this._getNetworks();
    
    if (networks.length === 0) {
        return html`
          <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
            <div class="card-content">
              ${renderWarning("No Wireless Networks", "No Meraki wireless networks found. Ensure the integration is configured and entities are enabled.")}
            </div>
            <div class="version">v${__VERSION__}</div>
          </ha-card>
        `;
    }

    // Dynamically build the dropdown options
    const networkOptions = networks.map(n => ({ value: n.id, label: n.name }));
    const filteredSsids = this._getSsids(this._formData.network);
    const ssidOptions = filteredSsids.map(s => ({ value: String(s.number), label: `${s.name} (SSID ${s.number})` }));

    // Define the schema for ha-form
    const schema = [
      {
        name: "network",
        selector: { select: { options: networkOptions, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: ssidOptions, mode: "dropdown" } }
      },
      {
        name: "duration",
        selector: { 
          select: { 
            options: [
              { value: "60", label: "1 Hour" },
              { value: "1440", label: "24 Hours" }
            ], 
            mode: "dropdown" 
          } 
        }
      },
      {
        name: "guestName",
        selector: { text: {} }
      }
    ];

    const isFormValid = this._formData.network && this._formData.ssid;

    return html`
      <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
        <div class="card-content">
          ${this._error ? html`<ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => (this._error = null)}">${this._error}</ha-alert>` : ''}
          ${this._success ? html`<ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => (this._success = null)}">${this._success}</ha-alert>` : ''}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${schema}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button 
              raised 
              .disabled=${this._creating || !isFormValid} 
              @click=${this._generateAccessKey}
            >
              ${this._creating ? html`<ha-circular-progress active size="small"></ha-circular-progress>` : 'Generate Access Key'}
            </ha-button>
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private async _generateAccessKey() {
    if (!this._formData.network || !this._formData.ssid) return;
    this._creating = true;
    this._error = null;
    this._success = null;

    try {
      await this.hass.callService('meraki_ha', 'generate_guest_access', {
        network_id: this._formData.network,
        ssid_number: parseInt(this._formData.ssid, 10),
        duration_minutes: parseInt(this._formData.duration, 10),
        name: this._formData.guestName || undefined,
        // Optional parameters not currently in UI but supported by the backend API
        passphrase: undefined,
        group_policy_id: undefined, 
      });

      this._success = 'Guest access key created successfully!';
    } catch (err: any) {
      this._error = `Failed to create guest key: ${err.message || err}`;
    } finally {
      this._creating = false;
    }
  }

  static styles = [
    sharedStyles,
    css`
      .form-container { display: flex; flex-direction: column; gap: 16px; }
      ha-button { width: 100%; margin-top: 8px; }
      .flex { display: flex; }
      .justify-center { justify-content: center; }
      .p-8 { padding: 32px; }
    `
  ];
}

declare global {
  interface HTMLElementTagNameMap {
    'meraki-guest-access-card': MerakiGuestAccessCard;
  }
}

// Register components
if (!customElements.get('meraki-guest-access-card')) {
  customElements.define('meraki-guest-access-card', MerakiGuestAccessCard);
}

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-guest-access-card')) {
  (window as any).customCards.push({
    type: "meraki-guest-access-card",
    name: "Meraki Guest Access",
    description: `Manage temporary guest WiFi access. Version: ${__VERSION__}`,
    preview: true,
    version: __VERSION__,
  });
}
