import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';

interface Config {
  type: string;
  name?: string;
  config_entry_id?: string;
}

@customElement('meraki-guest-access-card')
export class MerakiGuestAccessCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  @state() private _selectedNetwork: string = '';
  @state() private _selectedSsid: string = '';
  @state() private _selectedPolicy: string = '';
  @state() private _duration: string = '60';
  @state() private _customName: string = '';
  @state() private _customPassphrase: string = '';

  @state() private _creating: boolean = false;
  @state() private _error: string | null = null;
  @state() private _success: string | null = null;

  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];
  @state() private _policies: any[] = [];
  @state() private _loading: boolean = true;

  public setConfig(config: Config): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = config;
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      name: 'Meraki Guest Access',
    };
  }

  public static getConfigElement(): HTMLElement {
    return document.createElement('div');
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._fetchInitialData();
  }

  protected updated(changedProperties: PropertyValues) {
    super.updated(changedProperties);
    if (changedProperties.has('hass') && this.hass && !this._networks.length) {
      this._fetchInitialData();
    }
  }

  private async _fetchInitialData() {
    if (!this.hass) return;
    this._loading = true;
    try {
      const configEntries = await this.hass.callWS<any[]>({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });

      const entryId = this._config?.config_entry_id || (configEntries.length > 0 ? configEntries[0].entry_id : null);
      if (!entryId) {
        this._error = 'Meraki integration not found. Please configure it first.';
        this._loading = false;
        return;
      }

      const data = await safeCallWS<any>(this.hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: entryId,
      });

      this._networks = data.networks.filter((n: any) => n.productTypes?.includes('wireless')) || [];
      this._ssids = data.ssids || [];

      if (this._networks.length > 0 && !this._selectedNetwork) {
        this._selectedNetwork = this._networks[0].id;
        this._fetchPolicies(this._selectedNetwork, entryId);
      }
    } catch (err: any) {
      this._error = `Failed to fetch Meraki data: ${err.message || err}`;
    } finally {
      this._loading = false;
    }
  }

  private async _fetchPolicies(networkId: string, configEntryId?: string) {
    if (!this.hass) return;
    try {
      let entryId = configEntryId || this._config?.config_entry_id;
      if (!entryId) {
        const configEntries = await this.hass.callWS<any[]>({
          type: 'config_entries/get',
          domain: 'meraki_ha',
        });
        entryId = configEntries.length > 0 ? configEntries[0].entry_id : undefined;
      }

      if (!entryId) return;

      const policies = await safeCallWS<any[]>(this.hass, {
        type: WsCommand.TIMED_ACCESS_GET_POLICIES,
        config_entry_id: entryId,
        networkId: networkId,
      });
      this._policies = policies;
    } catch (err: any) {
      console.error('Failed to fetch policies:', err);
      this._policies = [];
    }
  }

  protected render() {
    if (this._loading && !this._networks.length) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content flex justify-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    }

    const filteredSsids = this._ssids.filter(s => s.networkId === this._selectedNetwork);

    return html`
      <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
        <div class="card-content">
          ${this._error
            ? html`
                <ha-alert alert-type="error" dismissable @alert-dismissed-clicked="${() => (this._error = null)}">
                  ${this._error}
                </ha-alert>
              `
            : ''}
          ${this._success
            ? html`
                <ha-alert alert-type="success" dismissable @alert-dismissed-clicked="${() => (this._success = null)}">
                  ${this._success}
                </ha-alert>
              `
            : ''}

          <div class="form-container">
            <ha-select
              label="Network"
              .value="${this._selectedNetwork}"
              @selected="${this._handleNetworkChanged}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${this._networks.map(
                (n) => html`<ha-list-item .value="${n.id}">${n.name}</ha-list-item>`
              )}
            </ha-select>

            <ha-select
              label="SSID"
              .value="${this._selectedSsid}"
              .disabled="${!this._selectedNetwork}"
              @selected="${this._handleSsidChanged}"
              fixedMenuPosition
              naturalMenuWidth
            >
              ${filteredSsids.map(
                (s) => html`<ha-list-item .value="${s.number.toString()}">${s.name} (SSID ${s.number})</ha-list-item>`
              )}
            </ha-select>

            <ha-select
              label="Group Policy"
              .value="${this._selectedPolicy}"
              .disabled="${!this._selectedNetwork}"
              @selected="${(e: any) => (this._selectedPolicy = e.target.value)}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <ha-list-item value="">None (Default)</ha-list-item>
              ${this._policies.map(
                (p) => html`<ha-list-item .value="${p.groupPolicyId}">${p.name}</ha-list-item>`
              )}
            </ha-select>

            <ha-select
              label="Duration"
              .value="${this._duration}"
              @selected="${(e: any) => (this._duration = e.target.value)}"
              fixedMenuPosition
              naturalMenuWidth
            >
              <ha-list-item value="30">30 Minutes</ha-list-item>
              <ha-list-item value="60">1 Hour</ha-list-item>
              <ha-list-item value="240">4 Hours</ha-list-item>
              <ha-list-item value="1440">24 Hours</ha-list-item>
              <ha-list-item value="10080">7 Days</ha-list-item>
            </ha-select>

            <ha-textfield
              label="Name (Optional)"
              placeholder="e.g. Guest-John"
              .value="${this._customName}"
              @input="${(e: any) => (this._customName = e.target.value)}"
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value="${this._customPassphrase}"
              @input="${(e: any) => (this._customPassphrase = e.target.value)}"
            ></ha-textfield>

            <ha-button
              raised
              .disabled="${this._creating || !this._selectedNetwork || !this._selectedSsid}"
              @click="${this._handleCreate}"
            >
              ${this._creating ? 'Creating...' : 'Generate access key'}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `;
  }

  private _handleNetworkChanged(e: any) {
    const newNetworkId = e.target.value;
    if (newNetworkId === this._selectedNetwork) return;
    this._selectedNetwork = newNetworkId;
    this._selectedSsid = '';
    this._selectedPolicy = '';
    this._fetchPolicies(newNetworkId);
  }

  private _handleSsidChanged(e: any) {
    this._selectedSsid = e.target.value;
  }

  private async _handleCreate() {
    if (!this._selectedNetwork || !this._selectedSsid) return;

    this._creating = true;
    this._error = null;
    this._success = null;

    try {
      await this.hass.callService('meraki_ha', 'create_guest_key', {
        network_id: this._selectedNetwork,
        ssid_number: parseInt(this._selectedSsid, 10),
        duration_minutes: parseInt(this._duration, 10),
        name: this._customName || undefined,
        passphrase: this._customPassphrase || undefined,
        group_policy_id: this._selectedPolicy || undefined,
      });

      this._success = 'Guest access key created successfully!';
      this._customName = '';
      this._customPassphrase = '';
    } catch (err: any) {
      this._error = `Failed to create guest key: ${err.message || err}`;
    } finally {
      this._creating = false;
    }
  }

  static styles = css`
    :host {
      display: block;
    }
    .card-content {
      padding: 16px;
    }
    .form-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    ha-select, ha-textfield, ha-button {
      width: 100%;
    }
    ha-alert {
      display: block;
      margin-bottom: 16px;
    }
    .flex {
      display: flex;
    }
    .justify-center {
      justify-content: center;
    }
    .p-8 {
      padding: 32px;
    }
  `;
}
// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: true,
});
