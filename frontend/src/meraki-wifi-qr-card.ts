import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import QRCode from 'qrcode';

interface Config {
  type: string;
  ssid: string;
  password?: string;
  name?: string;
}

@customElement('meraki-wifi-qr-card')
export class MerakiWifiQrCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _qrSvg: string = '';

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

if (!customElements.get("meraki-wifi-qr-card")) {
  customElements.define("meraki-wifi-qr-card", MerakiWifiQrCard);
}

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: "meraki-wifi-qr-card",
  name: "Meraki Wi-Fi QR Card",
  description: "Display a scannable Wi-Fi QR code for guests.",
  preview: true,
});
