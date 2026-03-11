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
      // Broaden auto-discovery to catch the new God Module naming conventions
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
      // Default to more-info
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
    console.log(`MERAKI CARD DIAG
