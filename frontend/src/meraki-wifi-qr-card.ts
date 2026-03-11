import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { Network, SSID } from './types/meraki';
import { renderWarning, sharedStyles } from './shared-ui';
import { MerakiDataProvider } from './utils/meraki-data';
import QRCode from 'qrcode';

declare const __VERSION__: string;

interface Config {
  type: string;
  ssid: string;
  networkId?: string;
  password?: string; 
  name?: string;
}

export class MerakiWifiQrCardEditor extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];

  public setConfig(config: Config): void {
    this._config = config;
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._loadCentralizedData();
  }

  private async _loadCentralizedData() {
    if (!this.hass) return;
    const { networks, ssids } = await MerakiDataProvider.fetchConfig(this.hass);
    this._networks = networks;
    this._ssids = ssids;
  }

  private _valueChanged(ev: CustomEvent): void {
    if (!this._config) return;
    const formValues = ev.detail.value;
    const newConfig = { ...this._config, ...formValues };

    // Automatically clear the SSID if the Network selection was changed
    if (this._config.networkId !== formValues.networkId) {
      newConfig.ssid = "";
    }

    // Clean up empty strings
    Object.keys(newConfig).forEach(key => {
      if (newConfig[key as keyof Config] === "") {
        delete newConfig[key as keyof Config];
      }
    });

    this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: newConfig }, bubbles: true, composed: true }));
  }

  private _computeLabel = (schema: any): string => {
    if (schema.name === "networkId") return "Network (Optional filter)";
    if (schema.name === "ssid") return "SSID (Required)";
    if (schema.name === "password") return "Password (Optional override or Entity ID)";
    if (schema.name === "name") return "Card Title (Optional)";
    return schema.name;
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    const networkOptions = MerakiDataProvider.getNetworkOptions(this._networks, true);
    const ssidOptions = MerakiDataProvider.getSsidOptions(this._ssids, this._config.networkId, 'name');

    const schema = [
      { name: "networkId", selector: { select: { options: networkOptions, mode: "dropdown" } } },
      { name: "ssid", selector: { select: { options: ssidOptions, custom_value: true, mode: "dropdown" } } },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
    ];

    return html`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }

  static styles = css`.editor-container { padding: 16px; }`;
}

export class MerakiWifiQrCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _qrSvg: string = '';

  public static async getConfigElement() {
    return document.createElement("meraki-wifi-qr-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config || !config.ssid) {
      throw new Error('Please select an SSID');
    }
    this._config = config;
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      ssid: '', 
      name: 'Wi-Fi Access',
    };
  }

  protected updated(changedProperties: PropertyValues) {
    if (changedProperties.has('hass') || changedProperties.has('_config')) {
      this._generateQR();
    }
  }

  private _getValue(value?: string): string {
    if (!value || !this.hass) return value || '';
    if (this.hass.states[value]) {
      return this.hass.states[value].state;
    }
    return value;
  }

  private _getPasswordForSsid(ssidName: string): string {
    if (!this.hass) return '';

    // Pass 1: Manual Override - User typed a password or entity ID directly into the editor
    if (this._config?.password && this._config.password !== 'password123') {
        return this._getValue(this._config.password);
    }

    if (!ssidName) return '';

    // Pass 2: Strict match by attribute
    for (const entityId in this.hass.states) {
      const stateObj = this.hass.states[entityId];
      const attrs = stateObj.attributes;

      if (attrs.ssid_name === ssidName || attrs.ssid === ssidName) {
        if (attrs.psk) return String(attrs.psk);
        if (attrs.password) return String(attrs.password);

        if ((entityId.includes('password') || entityId.includes('psk')) &&
            stateObj.state && !['unknown', 'unavailable'].includes(stateObj.state)) {
          return stateObj.state;
        }
      }
    }

    // Pass 3: Fuzzy search for a dedicated password sensor matching the SSID name
    const normalizedSsid = ssidName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    for (const entityId in this.hass.states) {
      if (entityId.includes(normalizedSsid) && (entityId.includes('password') || entityId.includes('psk'))) {
        const stateObj = this.hass.states[entityId];
        if (stateObj.state && !['unknown', 'unavailable'].includes(stateObj.state)) {
          return stateObj.state;
        }
      }
    }

    return '';
  }

  private _generateWifiString(ssid: string, password?: string): string {
    const escapedSsid = ssid.replace(/([\\;,":])/g, '\\$1');
    const escapedPassword = password ? password.replace(/([\\;,":])/g, '\\$1') : '';
    return escapedPassword 
      ? `WIFI:T:WPA;S:${escapedSsid};P:${escapedPassword};;`
      : `WIFI:T:nopass;S:${escapedSsid};P:;;`;
  }

  private async _generateQR() {
    if (!this._config) return;
    const ssid = this._getValue(this._config.ssid);
    const password = this._getPasswordForSsid(ssid);

    if (!ssid) {
      this._qrSvg = '';
      return;
    }

    try {
      const wifiString = this._generateWifiString(ssid, password);
      this._qrSvg = await QRCode.toString(wifiString, {
        type: 'svg',
        margin: 2,
        color: { dark: '#000000', light: '#ffffff' },
      });
    } catch (err) {
      console.error('Failed to generate QR code', err);
      this._qrSvg = '';
    }
  }

  protected render() {
    if (!this._config || !this.hass) {
      return html`
        <ha-card .header=${this._config?.name || 'Wi-Fi Access'}>
          <div class="card-content">
            ${renderWarning("Integration Initializing", "Waiting for Home Assistant data...")}
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const ssid = this._getValue(this._config.ssid);
    const password = this._getPasswordForSsid(ssid);

    return html`
      <ha-card .header=${this._config.name || 'Wi-Fi Access'}>
        <div class="card-content">
          <div class="ssid-display">${ssid}</div>
          <div class="qr-container" .innerHTML=${this._qrSvg}></div>
          ${password ? html`<div class="password-display">Password: <code>${password}</code></div>` : ''}
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  static styles = [
    sharedStyles,
    css`
      :host { display: block; }
      .card-content { display: flex; flex-direction: column; align-items: center; padding: 16px; gap: 16px; }
      .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
      .qr-container { width: 200px; height: 200px; background: white; padding: 8px; border-radius: 8px; }
      .qr-container svg { width: 100%; height: 100%; }
      .password-display { color: var(--secondary-text-color); text-align: center; }
      code { background: var(--secondary-background-color); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
    `
  ];
}

// Register components
if (!customElements.get('meraki-wifi-qr-card')) {
  customElements.define('meraki-wifi-qr-card', MerakiWifiQrCard);
}
if (!customElements.get('meraki-wifi-qr-card-editor')) {
  customElements.define('meraki-wifi-qr-card-editor', MerakiWifiQrCardEditor);
}

// Register the card
(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-wifi-qr-card')) {
  (window as any).customCards.push({
    type: "meraki-wifi-qr-card",
    name: "Meraki Wi-Fi QR Card",
    description: "Display a scannable Wi-Fi QR code for guests.",
    preview: true,
  });
}