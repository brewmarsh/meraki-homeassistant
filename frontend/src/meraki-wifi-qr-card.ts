import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';
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
    this._fetchInitialData();
  }

  private async _fetchInitialData() {
    if (!this.hass) return;
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
    }
  }

  private _valueChanged(ev: CustomEvent): void {
    if (!this._config) return;
    
    // ha-form passes the entire updated config object inside ev.detail.value
    const newConfig = { ...this._config, ...ev.detail.value };

    // Clean up empty strings so they don't clutter your raw YAML
    Object.keys(newConfig).forEach(key => {
      if (newConfig[key as keyof Config] === "") {
        delete newConfig[key as keyof Config];
      }
    });

    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: newConfig },
      bubbles: true,
      composed: true,
    }));
  }

  // Arrow function ensures 'this' context is preserved when called by ha-form
  private _computeLabel = (schema: any): string => {
    if (schema.name === "networkId") return "Network (Optional filter)";
    if (schema.name === "ssid") return "SSID (Required)";
    if (schema.name === "password") return "Password or Entity ID (e.g. sensor.guest_pw)";
    if (schema.name === "name") return "Card Title (Optional)";
    return schema.name;
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    // Build dynamic options for the dropdowns
    const networkOptions = [
      { value: "", label: "All Networks" },
      ...this._networks.map(n => ({ value: n.id, label: n.name }))
    ];
    
    const filteredSsids = this._config.networkId 
        ? this._ssids.filter(s => s.networkId === this._config!.networkId) 
        : this._ssids;
        
    const ssidOptions = filteredSsids.map(s => ({ value: s.name, label: `${s.name} (SSID ${s.number})` }));

    // Define the schema for Home Assistant to automatically build the form
    const schema = [
      {
        name: "networkId",
        selector: { select: { options: networkOptions, mode: "dropdown" } }
      },
      {
        name: "ssid",
        selector: { select: { options: ssidOptions, custom_value: true, mode: "dropdown" } }
      },
      {
        name: "password",
        selector: { text: {} }
      },
      {
        name: "name",
        selector: { text: {} }
      }
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

  static styles = css`
    .editor-container { padding: 16px; }
  `;
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
    const password = this._getValue(this._config.password);

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
    if (!this._config || !this.hass) return html``;
    const ssid = this._getValue(this._config.ssid);

    return html`
      <ha-card .header=${this._config.name || 'Wi-Fi Access'}>
        <div class="card-content">
          <div class="ssid-display">${ssid}</div>
          <div class="qr-container" .innerHTML=${this._qrSvg}></div>
          ${this._getValue(this._config.password) ? html`<div class="password-display">Password: <code>${this._getValue(this._config.password)}</code></div>` : ''}
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  static styles = css`
    :host { display: block; }
    .card-content { display: flex; flex-direction: column; align-items: center; padding: 16px; gap: 16px; }
    .ssid-display { font-size: 1.5em; font-weight: bold; color: var(--primary-text-color); text-align: center; }
    .qr-container { width: 200px; height: 200px; background: white; padding: 8px; border-radius: 8px; }
    .qr-container svg { width: 100%; height: 100%; }
    .password-display { color: var(--secondary-text-color); text-align: center; }
    code { background: var(--secondary-background-color); padding: 2px 4px; border-radius: 4px; font-family: monospace; }
    .version { font-size: 9px; color: var(--secondary-text-color); text-align: right; padding: 0 16px 8px; opacity: 0.4; }
  `;
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
