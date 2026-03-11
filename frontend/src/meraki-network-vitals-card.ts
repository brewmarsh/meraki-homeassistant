import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, sharedStyles } from './shared-ui';

declare const __VERSION__: string;

interface Config {
  type: string;
  gateway_entity?: string;
  switch_entity?: string;
  ap_entity?: string;
  throughput_entity?: string;
  name?: string;
  gateway_tap_action?: any;
  switch_tap_action?: any;
  ap_tap_action?: any;
}

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
    this._config = {
      ...config,
      gateway_tap_action: config.gateway_tap_action || { action: "more-info" },
      switch_tap_action: config.switch_tap_action || { action: "more-info" },
      ap_tap_action: config.ap_tap_action || { action: "more-info" },
    };
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      gateway_entity: '',
      switch_entity: '',
      ap_entity: '',
      throughput_entity: '',
      name: 'Meraki Network Vitals',
      gateway_tap_action: { action: 'more-info' },
      switch_tap_action: { action: 'more-info' },
      ap_tap_action: { action: 'more-info' },
    };
  }

  private _getGatewayEntity(): string {
    if (this._config?.gateway_entity) return this._config.gateway_entity;
    if (this.hass?.states) {
      return Object.keys(this.hass.states).find(id => id.includes('aggregated_gateway') || id.includes('_mx_health')) || '';
    }
    return '';
  }

  private _getSwitchEntity(): string {
    if (this._config?.switch_entity) return this._config.switch_entity;
    if (this.hass?.states) {
      return Object.keys(this.hass.states).find(id => id.includes('aggregated_switch') || id.includes('_ms_health')) || '';
    }
    return '';
  }

  private _getApEntity(): string {
    if (this._config?.ap_entity) return this._config.ap_entity;
    if (this.hass?.states) {
      return Object.keys(this.hass.states).find(id => id.includes('aggregated_ap') || id.includes('_mr_health')) || '';
    }
    return '';
  }

  private _getThroughputEntity(): string {
    if (this._config?.throughput_entity) return this._config.throughput_entity;
    if (this.hass?.states) {
      return Object.keys(this.hass.states).find(id => 
        id.startsWith('sensor.') && (id.includes('throughput') || id.includes('uplink_speed') || id.includes('uplink'))
      ) || '';
    }
    return '';
  }

  private _handleEntityClick(entityId: string | undefined, actionConfig: any) {
    if (!entityId || !actionConfig) return;

    if (actionConfig.action === 'navigate' && actionConfig.navigation_path) {
      const event = new CustomEvent('navigate', {
        detail: { path: actionConfig.navigation_path },
        bubbles: true,
        composed: true,
      });
      this.dispatchEvent(event);
    } else {
      const event = new CustomEvent('hass-more-info', {
        detail: { entityId: entityId },
        bubbles: true,
        composed: true,
      });
      this.dispatchEvent(event);
    }
  }

  private _renderStatusDot(entityId: string | undefined, label: string, actionConfig?: any) {
    const isClickable = !!entityId && !!this.hass.states[entityId];

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
    console.log(`MERAKI CARD DIAGNOSTIC - Status Dot (${label}) Raw Entity State:`, stateObj);
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
      <div
        class="status-item ${isClickable ? 'clickable' : ''}"
        @click=${() => isClickable ? this._handleEntityClick(entityId, actionConfig) : null}
        role="${isClickable ? 'button' : 'presentation'}"
        tabindex="${isClickable ? '0' : '-1'}"
      >
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
      return html`
        <ha-card>
          <div class="card-content">
            ${renderWarning("Initializing", "Waiting for Home Assistant data...")}
          </div>
        </ha-card>
      `;
    }

    const gatewayEntity = this._getGatewayEntity();
    const switchEntity = this._getSwitchEntity();
    const apEntity = this._getApEntity();
    const throughputEntity = this._getThroughputEntity();

    const gatewayStateObj = gatewayEntity ? this.hass.states[gatewayEntity] : undefined;
    const throughputStateObj = throughputEntity ? this.hass.states[throughputEntity] : undefined;

    console.log("MERAKI CARD DIAGNOSTIC - Gateway State:", gatewayStateObj);
    console.log("MERAKI CARD DIAGNOSTIC - Throughput Entity State:", throughputStateObj);

    const throughputState = gatewayStateObj?.attributes?.uplink_performance?.throughput
      ? `${gatewayStateObj.attributes.uplink_performance.throughput} Mbps`
      : (throughputStateObj
          ? `${throughputStateObj.state} ${throughputStateObj.attributes?.unit_of_measurement || ""}`.trim()
          : "0 Mbps");

    console.log("MERAKI CARD DIAGNOSTIC - Extracted Throughput:", throughputState);

    return html`
      <ha-card>
        <div class="card-content">
          <div class="vitals-container">
            <div class="status-dots">
              ${this._renderStatusDot(gatewayEntity, 'Gateway', this._config.gateway_tap_action)}
              ${this._renderStatusDot(switchEntity, 'Switches', this._config.switch_tap_action)}
              ${this._renderStatusDot(apEntity, 'APs', this._config.ap_tap_action)}
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

  static styles = [
    sharedStyles,
    css`
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
      .status-item.clickable { cursor: pointer; }
      .status-icon { --mdc-icon-size: 16px; color: var(--secondary-text-color); }
      .status-label { font-size: 14px; font-weight: 500; color: var(--primary-text-color); white-space: nowrap; }
      .throughput-container { display: flex; align-items: center; gap: 4px; color: var(--secondary-text-color); }
      .throughput-value { font-size: 14px; font-weight: 600; white-space: nowrap; }
    `
  ];
}

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
        <ha-textfield
          label="Gateway Tap Action"
          .value=${this._config.gateway_tap_action?.action || "more-info"}
          .configValue=${"gateway_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="Switch Tap Action"
          .value=${this._config.switch_tap_action?.action || "more-info"}
          .configValue=${"switch_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
        <ha-textfield
          label="AP Tap Action"
          .value=${this._config.ap_tap_action?.action || "more-info"}
          .configValue=${"ap_tap_action"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config) return;
    const target = ev.target as any;
    const configValue = target.configValue;
    let newValue = ev.detail?.value ?? target.value;

    if (configValue && configValue.endsWith('_tap_action')) {
      if (newValue.startsWith('/')) {
        newValue = { action: 'navigate', navigation_path: newValue };
      } else {
        newValue = { action: newValue };
      }
    }

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
if (!customElements.get('meraki-network-vitals-card')) {
  customElements.define('meraki-network-vitals-card', MerakiNetworkVitalsCard);
}
if (!customElements.get('meraki-network-vitals-card-editor')) {
  customElements.define('meraki-network-vitals-card-editor', MerakiNetworkVitalsCardEditor);
}

(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-network-vitals-card')) {
  (window as any).customCards.push({
    type: "meraki-network-vitals-card",
    name: "Meraki Network Vitals",
    description: "Compact horizontal health header.",
    preview: true,
  });
}
