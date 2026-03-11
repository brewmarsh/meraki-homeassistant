import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
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

  @state() private _selectedNetwork: string = '';
  @state() private _selectedSsid: string = '';
  @state() private _selectedPolicy: string = '';
  @state() private _duration: string = '60';
  @state() private _guestName: string = '';
  @state() private _passphrase: string = '';

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

      if (this.hass.user?.name && !this._guestName) {
        this._guestName = this.hass.user.name;
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
      if (this._selectedNetwork) {
        this._fetchPolicies(this._selectedNetwork);
      }
    } catch (err) {
      console.error("Failed to fetch Meraki config entries", err);
    }
  }

  private _autoSelectAndLoad() {
    const networks = this._getNetworks();
    if (networks.length > 0) {
      if (!this._selectedNetwork) {
        this._selectedNetwork = networks[0].id;
        this._fetchPolicies(this._selectedNetwork);
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

  protected render() {
    if (this._isLoading) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const networks = this._getNetworks();
    const filteredSsids = this._getSsids(this._selectedNetwork);

    if (networks.length === 0) {
        return html`
          <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
            <div class="card-content">
              <ha-alert alert-type="warning">No Meraki wireless networks found. Ensure the integration is configured and entities are enabled.</ha-alert>
            </div>
            <div class="version">v${__VERSION__}</div>
          </ha-card>
        `;
    }

    return html`
      <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
        <div class="card-content">
          ${this._error ? html`<ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => (this._error = null)}">${this._error}</ha-alert>` : ''}
          ${this._success ? html`<ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => (this._success = null)}">${this._success}</ha-alert>` : ''}

          <div class="form-container">
            <ha-select
              label="Network"
              .value=${this._selectedNetwork}
              @closed=${(e: Event) => this._handleDropdownChange(e, "Network")}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${networks.map(n => html`<mwc-list-item value="${n.id}">${n.name}</mwc-list-item>`)}
            </ha-select>

            <ha-select
              label="SSID"
              .value=${this._selectedSsid}
              .disabled=${!this._selectedNetwork}
              @closed=${(e: Event) => this._handleDropdownChange(e, "SSID")}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${filteredSsids.map(s => html`<mwc-list-item value="${String(s.number)}">${s.name} (SSID ${s.number})</mwc-list-item>`)}
            </ha-select>

            <ha-select
              label="Duration"
              .value=${this._duration}
              @closed=${(e: Event) => this._handleDropdownChange(e, "Duration")}
              fixedMenuPosition
              naturalMenuWidth
            >
              <mwc-list-item value="60">1 Hour</mwc-list-item>
              <mwc-list-item value="1440">24 Hours</mwc-list-item>
            </ha-select>

            <ha-textfield label="Guest Name" .value=${this._guestName} @input=${this._handleGuestNameChange}></ha-textfield>

            <ha-button raised .disabled=${this._creating || !this._selectedNetwork || !this._selectedSsid} @click=${this._generateAccessKey}>
              ${this._creating ? html`<ha-circular-progress active size="small"></ha-circular-progress>` : 'Generate Access Key'}
            </ha-button>
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private _handleDropdownChange(ev: Event, label: string) {
    ev.stopPropagation();
    const target = ev.target as any;
    const value = target.value;

    if (!value) return; // Ignore blank selections

    console.log(`MERAKI CARD DIAGNOSTIC - Dropdown changed: ${label} = ${value}`);

    if (label === "Network") {
      if (this._selectedNetwork === value) return;
      this._selectedNetwork = value;
      this._fetchPolicies(value);
      // Reset SSID when network changes to prevent invalid selections
      this._selectedSsid = ""; 
    } else if (label === "SSID") {
      this._selectedSsid = value;
    } else if (label === "Duration") {
      this._duration = value;
    }
  }

  private _handleGuestNameChange(e: Event) { this._guestName = (e.target as any).value; }

  private async _generateAccessKey() {
    if (!this._selectedNetwork || !this._selectedSsid) return;
    this._creating = true;
    this._error = null;
    this._success = null;

    try {
      await this.hass.callService('meraki_ha', 'generate_guest_access', {
        network_id: this._selectedNetwork,
        ssid_number: parseInt(this._selectedSsid, 10),
        duration_minutes: parseInt(this._duration, 10),
        name: this._guestName || undefined,
        passphrase: this._passphrase || undefined,
        group_policy_id: this._selectedPolicy || undefined,
      });

      this._success = 'Guest access key created successfully!';
    } catch (err: any) {
      this._error = `Failed to create guest key: ${err.message || err}`;
    } finally {
      this._creating = false;
    }
  }

  static styles = css`
    .form-container { display: flex; flex-direction: column; gap: 16px; }
    ha-select, ha-textfield, ha-button { width: 100%; }
    .flex { display: flex; }
    .justify-center { justify-content: center; }
    .version {
      font-size: 10px;
      color: var(--secondary-text-color);
      text-align: right;
      padding: 0 16px 8px;
      opacity: 0.5;
    }
  `;
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
