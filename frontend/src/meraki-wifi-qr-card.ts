import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';
import QRCode from 'qrcode';

interface Config {
  type: string;
  ssid: string;
  password?: string;
  name?: string;
}

@customElement('meraki-wifi-qr-card-editor')
export class MerakiWifiQrCardEditor extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];
  @state() private _selectedNetwork: string = '';
  @state() private _loading: boolean = false;

  public setConfig(config: Config): void {
    this._config = config;
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._fetchInitialData();
  }

  private async _fetchInitialData() {
    if (!this.hass) return;
    this._loading = true;
    try {
      const configEntries = await this.hass.callWS<any[]>({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });

      const entryId = configEntries.length > 0 ? configEntries[0].entry_id : null;
      if (!entryId) return;

      const data = await safeCallWS<any>(this.hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: entryId,
      });

      this._networks = (Array.isArray(data.networks) ? data.networks : []).filter((n: any) => n.productTypes?.includes('wireless'));
      this._ssids = Array.isArray(data.ssids) ? data.ssids : [];
    } catch (err: any) {
      console.error('Failed to fetch Meraki data:', err);
    } finally {
      this._loading = false;
    }
  }

  private _handleNetworkChange(ev: any) {
    ev.stopPropagation();
    const newNetworkId = ev.target.value;
    if (newNetworkId !== this._selectedNetwork) {
      this._selectedNetwork = newNetworkId;
      // Clear SSID on network change
      this._updateConfig('ssid', '');
    }
  }

  private _handleSSIDChange(ev: any) {
    ev.stopPropagation();
    const newSsidName = ev.target.value;
    if (newSsidName && newSsidName !== this._config?.ssid) {
      this._updateConfig('ssid', newSsidName);
    }
  }

  private _valueChanged(ev: any) {
    if (!this._config) return;
    const target = ev.target;
    const field = target.configValue;
    if (!field) return;
    if (this._config[field as keyof Config] === target.value) return;
    this._updateConfig(field as keyof Config, target.value);
  }

  private _updateConfig(field: keyof Config, value: string) {
    if (!this._config) return;
    const newConfig = {
      ...this._config,
      [field]: value,
    };
    this._config = newConfig;
    this._dispatchEvent(newConfig);
  }

  private _dispatchEvent(config: Config) {
    const event = new CustomEvent('config-changed', {
      detail: { config },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    const filteredSsids = (this._ssids || []).filter(s => s.networkId === this._selectedNetwork);

    return html`
      <div class="card-config">
        <ha-select
          label="Network (Optional - to populate SSID)"
          .value="${this._selectedNetwork}"
          @closed="${this._handleNetworkChange}"
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="">Select a network</ha-list-item>
          ${(this._networks || []).map(n => html`<ha-list-item .value="${n.id}">${n.name}</ha-list-item>`)}
        </ha-select>

        <ha-select
          label="SSID"
          .value="${this._config?.ssid || ''}"
          .disabled="${!this._selectedNetwork}"
          @closed="${this._handleSSIDChange}"
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="">Select an SSID</ha-list-item>
          ${filteredSsids.map(s => html`<ha-list-item .value="${s.name}">${s.name}</ha-list-item>`)}
        </ha-select>

        <ha-textfield
          label="Password or Entity ID"
          .value="${this._config.password || ''}"
          .configValue="${'password'}"
          @input="${this._valueChanged}"
        ></ha-textfield>

        <ha-textfield
          label="Card Title"
          .value="${this._config.name || ''}"
          .configValue="${'name'}"
          @input="${this._valueChanged}"
        ></ha-textfield>
      </div>
    `;
  }

  static styles = css`
    .card-config {
      display: flex;
      flex-direction: column;
      gap: 16px;
      padding: 16px;
    }
    ha-select, ha-textfield {
      width: 100%;
    }
  `;
}

@customElement('meraki-wifi-qr-card')
export class MerakiWifiQrCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _qrSvg: string = '';

  public static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config || !config.ssid) {
      throw new Error('Please define an SSID');
    }
    this._config = config;
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      ssid: 'Guest WiFi',
      password: 'password123',
      name: 'Wi-Fi Access',
    };
  }

  protected updated(changedProperties: PropertyValues) {
    if (changedProperties.has('hass') || changedProperties.has('_config')) {
      const oldSsid = changedProperties.has('hass') ? this._getValueFromHass(this._config?.ssid, changedProperties.get('hass')) : null;
      const newSsid = this._getValue(this._config?.ssid);
      const oldPass = changedProperties.has('hass') ? this._getValueFromHass(this._config?.password, changedProperties.get('hass')) : null;
      const newPass = this._getValue(this._config?.password);

      if (changedProperties.has('_config') || oldSsid !== newSsid || oldPass !== newPass) {
        this._generateQR();
      }
    }
  }

  private _getValueFromHass(value: string | undefined, hass: any): string {
    if (!value || !hass) return value || '';
    if (hass.states[value]) {
      return hass.states[value].state;
    }
    return value;
  }

  private _getValue(value?: string): string {
    if (!value || !this.hass) return value || '';
    if (this.hass.states[value]) {
      return this.hass.states[value].state;
    }
    return value;
  }

  private _generateWifiString(ssid: string, password?: string): string {
    const escapedSsid = ssid.replace(/([\\;,":])/g, '\\$1');
    const escapedPassword = password ? password.replace(/([\\;,":])/g, '\\$1') : '';
    if (escapedPassword) {
      return `WIFI:T:WPA;S:${escapedSsid};P:${escapedPassword};;`;
    }
    return `WIFI:T:nopass;S:${escapedSsid};P:;;`;
  }

  private async _generateQR() {
    if (!this._config) return;

    const ssid = this._getValue(this._config.ssid);
    const password = this._getValue(this._config.password);

    if (!ssid) {
      this._qrSvg = '';
      return;
    }

    const wifiString = this._generateWifiString(ssid, password);
    try {
      this._qrSvg = await QRCode.toString(wifiString, {
        type: 'svg',
        margin: 2,
        color: {
          dark: '#000000',
          light: '#ffffff',
        },
      });
    } catch (err) {
      console.error('Failed to generate QR code', err);
      this._qrSvg = '';
    }
  }

  protected render() {
    if (!this._config || !this.hass) {
      return html``;
    }

    const ssid = this._getValue(this._config.ssid);
    const password = this._getValue(this._config.password);

    return html`
      <ha-card .header="${this._config.name || 'Wi-Fi Access'}">
        <div class="card-content">
          <div class="ssid-display">${ssid}</div>
          <div class="qr-container" .innerHTML="${this._qrSvg}"></div>
          ${password ? html`<div class="password-display">Password: <code>${password}</code></div>` : ''}
        </div>
      </ha-card>
    `;
  }

  static styles = css`
    :host {
      display: block;
    }
    .card-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 16px;
      gap: 16px;
    }
    .ssid-display {
      font-size: 1.5em;
      font-weight: bold;
      color: var(--primary-text-color);
      text-align: center;
    }
    .qr-container {
      width: 200px;
      height: 200px;
      background: white;
      padding: 8px;
      border-radius: 8px;
    }
    .qr-container svg {
      width: 100%;
      height: 100%;
    }
    .password-display {
      color: var(--secondary-text-color);
      text-align: center;
    }
    code {
      background: var(--secondary-background-color);
      padding: 2px 4px;
      border-radius: 4px;
      font-family: monospace;
    }
  `;
}

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-wifi-qr-card')) {
  (window as any).customCards.push({
    type: "meraki-wifi-qr-card",
    name: "Meraki Wi-Fi QR Card",
    description: "Display a scannable Wi-Fi QR code for guests.",
    preview: true,
  });
}
