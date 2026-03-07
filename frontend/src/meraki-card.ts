import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import './meraki-content-filter-card';
import './meraki-wifi-qr-card';
import './meraki-network-vitals-card';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';

interface Config {
  type: string;
  name?: string;
  config_entry_id?: string;
}

export class MerakiGuestAccessCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  @state() private _selectedNetwork: string = '';
  @state() private _selectedSSID: string = '';
  @state() private _selectedPolicy: string = '';
  @state() private _selectedDuration: string = '60';
  @state() private _customName: string = '';
  @state() private _customPassphrase: string = '';

  @state() private _creating: boolean = false;
  @state() private _error: string | null = null;
  @state() private _success: string | null = null;

  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];
  @state() private _policies: any[] = [];
  @state() private _isLoading: boolean = true;
  @state() private _initDone: boolean = false;

  public static async getConfigElement() {
    return document.createElement("meraki-guest-access-card-editor");
  }

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

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._fetchInitialData();
  }

  protected updated(changedProperties: PropertyValues) {
    super.updated(changedProperties);
    if (changedProperties.has('hass') && this.hass) {
      if (!this._initDone && this.hass) {
        this._fetchInitialData();
      }
      if (this.hass.user?.name && !this._customName) {
        this._customName = this.hass.user.name;
      }
    }
  }

  private async _fetchInitialData() {
    this._initDone = true;
    if (!this.hass) return;
    this._isLoading = true;
    try {
      const configEntries = await this.hass.callWS<any[]>({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });

      const entryId = this._config?.config_entry_id || (configEntries.length > 0 ? configEntries[0].entry_id : null);
      if (!entryId) {
        this._error = 'Meraki integration not found. Please configure it first.';
        this._isLoading = false;
        return;
      }

      const data = await safeCallWS<any>(this.hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: entryId,
      });

      this._networks = (Array.isArray(data.networks) ? data.networks : []).filter((n: any) => n.productTypes?.includes('wireless'));
      this._ssids = Array.isArray(data.ssids) ? data.ssids : [];

      if (this._networks.length > 0 && !this._selectedNetwork) {
        this._selectedNetwork = this._networks[0].id;
        await this._fetchPolicies(this._selectedNetwork, entryId);
      }
    } catch (err: any) {
      this._error = `Failed to fetch Meraki data: ${err.message || err}`;
    } finally {
      this._isLoading = false;
    }
  }

  private async _fetchSSIDs() {
    // Placeholder as SSIDs are currently fetched in _fetchInitialData
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
        network_id: networkId,
      });
      this._policies = Array.isArray(policies) ? policies : (policies as any)?.policies || [];
    } catch (err: any) {
      console.error('Failed to fetch policies:', err);
      this._policies = [];
    }
  }

  protected render() {
    if (this._isLoading) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content flex justify-center items-center p-8">
            <ha-circular-progress active></ha-circular-progress>
          </div>
        </ha-card>
      `;
    }

    const filteredSsids = (this._ssids || []).filter(s => s.networkId === this._selectedNetwork);

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
              .value=${this._selectedNetwork}
              @closed=${this._handleNetworkChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(this._networks || []).map(
                (n) => html`
                  <ha-list-item .value=${n.id}>
                    ${n.name}
                  </ha-list-item>
                `
              )}
            </ha-select>

            <ha-select
              label="SSID"
              .value=${this._selectedSSID}
              .disabled=${!this._selectedNetwork}
              @closed=${this._handleSSIDChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              ${(filteredSsids || []).map(
                (s) => html`
                  <ha-list-item .value=${String(s.number)}>
                    ${s.name} (SSID ${s.number})
                  </ha-list-item>
                `
              )}
            </ha-select>

            <ha-select
              label="Group Policy"
              .value=${this._selectedPolicy}
              .disabled=${!this._selectedNetwork}
              @closed=${this._handlePolicyChange}
              fixedMenuPosition
              naturalMenuWidth
            >
              <ha-list-item value="">None (Default)</ha-list-item>
              ${(this._policies || []).map(
                (p) => html`
                  <ha-list-item .value=${String(p.groupPolicyId)}>
                    ${p.name}
                  </ha-list-item>
                `
              )}
            </ha-select>

            <ha-select
              label="Duration"
              .value=${this._selectedDuration}
              @closed=${this._handleDurationChange}
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
              .value=${this._customName}
              @input=${(e: any) => (this._customName = e.target.value)}
            ></ha-textfield>

            <ha-textfield
              label="Passphrase (Optional)"
              placeholder="Leave empty to auto-generate"
              .value=${this._customPassphrase}
              @input=${(e: any) => (this._customPassphrase = e.target.value)}
            ></ha-textfield>

            <ha-button
              raised
              .disabled=${this._creating || !this._selectedNetwork || !this._selectedSSID}
              @click=${this._handleCreate}
            >
              ${this._creating ? 'Creating...' : 'Generate access key'}
            </ha-button>
          </div>
        </div>
      </ha-card>
    `;
  }

  private _handleNetworkChange(e: Event) {
    e.stopPropagation();
    const target = e.target as any;
    const newNetworkId = target.value;
    if (!newNetworkId || newNetworkId === this._selectedNetwork) return;
    this._selectedNetwork = newNetworkId;
    this._selectedSSID = '';
    this._selectedPolicy = '';
    this._fetchSSIDs();
    this._fetchPolicies(newNetworkId);
  }

  private _handleSSIDChange(e: Event) {
    e.stopPropagation();
    const target = e.target as any;
    this._selectedSSID = target.value;
  }

  private _handlePolicyChange(e: Event) {
    e.stopPropagation();
    const target = e.target as any;
    this._selectedPolicy = target.value;
  }

  private _handleDurationChange(e: Event) {
    e.stopPropagation();
    const target = e.target as any;
    this._selectedDuration = target.value;
  }

  private async _handleCreate() {
    if (!this._selectedNetwork || !this._selectedSSID) return;

    this._creating = true;
    this._error = null;
    this._success = null;

    try {
      await this.hass.callService('meraki_ha', 'create_guest_key', {
        network_id: this._selectedNetwork,
        ssid_number: parseInt(this._selectedSSID, 10),
        duration_minutes: parseInt(this._selectedDuration, 10),
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
    .items-center {
      align-items: center;
    }
    .p-8 {
      padding: 32px;
    }
  `;
}

@customElement('meraki-guest-access-card-editor')
export class MerakiGuestAccessCardEditor extends LitElement {
  @property({ attribute: false }) public hass?: HomeAssistant;
  @state() private _config?: Config;

  public setConfig(config: Config): void {
    this._config = config;
  }

  protected render() {
    if (!this.hass || !this._config) {
      return html``;
    }

    return html`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
          style="width: 100%;"
        ></ha-textfield>
        <ha-textfield
          label="Config Entry ID (Optional)"
          .value=${this._config.config_entry_id || ""}
          .configValue=${"config_entry_id"}
          @input=${this._valueChanged}
          style="width: 100%;"
        ></ha-textfield>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config || !this.hass) return;
    const target = ev.target;
    const configKey = target.configValue;

    if (!configKey) return;

    let newValue = target.value;
    if (this._config[configKey as keyof Config] === newValue) return;

    const newConfig = { ...this._config };
    if (newValue === "" || newValue === undefined) {
      delete newConfig[configKey as keyof Config];
    } else {
      (newConfig as any)[configKey] = newValue;
    }

    this._config = newConfig;

    const event = new CustomEvent("config-changed", {
      detail: { config: this._config },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }

  static styles = css`
    .card-config {
      display: flex;
      flex-direction: column;
      padding: 8px 0;
      gap: 16px;
    }
  `;
}

if (!customElements.get("meraki-guest-access-card")) {
  customElements.define("meraki-guest-access-card", MerakiGuestAccessCard);
}

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: "meraki-guest-access-card",
  name: "Meraki Guest Access",
  description: "Create and manage Meraki IPSK guest access keys.",
  preview: true,
});