import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';

declare const __VERSION__: string;

interface Config {
  type: string;
  gateway_entity?: string;
  switch_entity?: string;
  ap_entity?: string;
  throughput_entity?: string;
  name?: string;
}

@customElement('meraki-network-vitals-card')
export class MerakiNetworkVitalsCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  public static async getConfigElement() {
    return document.createElement("meraki-network-vitals-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = config;
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      gateway_entity: '',
      switch_entity: '',
      ap_entity: '',
      throughput_entity: '',
      name: 'Meraki Network Vitals',
    };
  }

  private _renderStatusDot(entityId: string | undefined, label: string) {
    if (!entityId || !this.hass.states[entityId]) {
      return html`
        <div class="status-item">
          <svg height="12" width="12">
            <circle cx="6" cy="6" r="6" fill="var(--disabled-text-color)" />
          </svg>
          <span class="status-label">${label}</span>
        </div>
      `;
    }

    const stateObj = this.hass.states[entityId];
    const state = stateObj ? stateObj.state.toLowerCase() : 'unknown';
    let colorVar = 'var(--disabled-text-color)';

    if (state === 'ok' || state === 'online' || state === 'connected') {
      colorVar = 'var(--success-color)';
    } else if (state === 'warning') {
      colorVar = 'var(--warning-color)';
    } else if (state === 'error' || state === 'offline' || state === 'failed') {
      colorVar = 'var(--error-color)';
    }

    return html`
      <div class="status-item">
        <ha-state-icon .hass=${this.hass} .stateObj=${stateObj} class="status-icon"></ha-state-icon>
        <svg height="12" width="12">
          <circle cx="6" cy="6" r="6" fill="${colorVar}" />
        </svg>
        <span class="status-label">${label}</span>
      </div>
    `;
  }

  protected render() {
    if (!this._config || !this.hass) {
      return html``;
    }

    const throughputEntity = this._config.throughput_entity;
    const throughputState = throughputEntity && this.hass.states[throughputEntity]
      ? this.hass.states[throughputEntity].state + ' ' + (this.hass.states[throughputEntity].attributes.unit_of_measurement || '')
      : 'N/A';

    return html`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(this._config.gateway_entity, 'Gateway')}
              ${this._renderStatusDot(this._config.switch_entity, 'Switches')}
              ${this._renderStatusDot(this._config.ap_entity, 'APs')}
            </div>
            <div class="throughput-container">
              <ha-icon icon="mdi:swap-vertical"></ha-icon>
              <span class="throughput-value">${throughputState}</span>
            </div>
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  static styles = css`
    :host { display: block; }
    ha-card { height: 100%; display: flex; flex-direction: column; justify-content: center; }
    .card-content { padding: 12px 16px; }
    .vitals-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .status-dots { display: flex; align-items: center; flex-wrap: wrap; gap: 16px; }
    .status-item { display: flex; align-items: center; gap: 8px; }
    .status-icon { --mdc-icon-size: 16px; color: var(--secondary-text-color); }
    .status-label { font-size: 14px; font-weight: 500; color: var(--primary-text-color); white-space: nowrap; }
    .throughput-container { display: flex; align-items: center; gap: 4px; color: var(--secondary-text-color); }
    .throughput-value { font-size: 14px; font-weight: 600; white-space: nowrap; }
    .version {
      font-size: 9px;
      color: var(--secondary-text-color);
      text-align: right;
      padding: 0 12px 4px;
      opacity: 0.4;
    }
  `;
}

@customElement('meraki-network-vitals-card-editor')
export class MerakiNetworkVitalsCardEditor extends LitElement {
  @property({ attribute: false }) public hass?: HomeAssistant;
  @state() private _config?: Config;

  public setConfig(config: Config): void {
    this._config = config;
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    return html`
      <div class="card-config">
        <ha-textfield
          label="Custom Title"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-entity-picker
          label="Gateway Status"
          .hass=${this.hass}
          .value=${this._config.gateway_entity}
          .configValue=${"gateway_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Switch Aggregation"
          .hass=${this.hass}
          .value=${this._config.switch_entity}
          .configValue=${"switch_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="AP Aggregation"
          .hass=${this.hass}
          .value=${this._config.ap_entity}
          .configValue=${"ap_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
        <ha-entity-picker
          label="Throughput Sensor"
          .hass=${this.hass}
          .value=${this._config.throughput_entity}
          .configValue=${"throughput_entity"}
          @value-changed=${this._valueChanged}
        ></ha-entity-picker>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config) return;
    const target = ev.target;
    const configValue = target.configValue;
    const newValue = ev.detail?.value ?? target.value;

    const newConfig = { ...this._config, [configValue]: newValue };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: newConfig },
      bubbles: true,
      composed: true,
    }));
  }

  static styles = css`
    ha-textfield, ha-entity-picker { display: block; margin-bottom: 16px; width: 100%; }
  `;
}

// Global Registration
(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-network-vitals-card')) {
  (window as any).customCards.push({
    type: "meraki-network-vitals-card",
    name: "Meraki Network Vitals",
    description: "Compact horizontal health header.",
    preview: true,
  });
}