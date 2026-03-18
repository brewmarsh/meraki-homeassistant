import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, renderLoadingState, sharedStyles } from './shared-ui';
import { MerakiDataProvider } from './utils/meraki-data';

declare const __VERSION__: string;

interface Config {
  type: string;
  name?: string;
  [key: string]: any;
}

export class MerakiVlanCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _isLoading: boolean = true;
  @state() private _loadingMessage: string = "Connecting...";

  public static async getConfigElement() {
    return document.createElement("meraki-vlan-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = { ...config };
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._loadCentralizedData();
  }

  private async _loadCentralizedData() {
    if (!this.hass) return;

    await MerakiDataProvider.pollConfig(
      this.hass,
      (msg, isLoading) => {
        this._loadingMessage = msg;
        this._isLoading = isLoading;
      }
    );
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      name: 'Meraki VLANs',
    };
  }

  private _getVlanEntities() {
    if (!this.hass) return [];

    return Object.keys(this.hass.states)
      .filter((entityId) => {
        if (!entityId.startsWith('switch.')) return false;
        const stateObj = this.hass.states[entityId];
        return stateObj.attributes.vlan_id !== undefined && stateObj.attributes.subnet !== undefined;
      })
      .map((entityId) => {
        const stateObj = this.hass.states[entityId];
        return {
          entity_id: entityId,
          name: stateObj.attributes.vlan_name || stateObj.attributes.friendly_name?.replace(' DHCP', '') || 'Unknown VLAN',
          subnet: stateObj.attributes.subnet,
          gateway: stateObj.attributes.gateway,
          state: stateObj.state,
        };
      })
      .sort((a, b) => a.name.localeCompare(b.name));
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    if (this._isLoading) {
      return renderLoadingState(
        this._config?.name || 'Cisco Meraki VLANs',
        this._loadingMessage,
        __VERSION__
      );
    }

    const vlanEntities = this._getVlanEntities();

    if (vlanEntities.length === 0) {
      return renderWarning(
        "No VLANs Found",
        "No Meraki VLAN DHCP switches were found. Ensure VLAN management is enabled in the integration options.",
        __VERSION__
      );
    }

    return html`
      <ha-card .header="${this._config.name || 'Cisco Meraki VLANs'}">
        <div class="card-content">
          <div class="vlan-table">
            <div class="table-header">
              <div class="col-vlan">VLAN</div>
              <div class="col-network">Subnet / Gateway</div>
              <div class="col-dhcp">DHCP</div>
            </div>
            ${vlanEntities.map((vlan) => html`
              <div class="table-row">
                <div class="col-vlan">
                  <span class="vlan-name">${vlan.name}</span>
                </div>
                <div class="col-network">
                  <div class="subnet">${vlan.subnet}</div>
                  <div class="gateway">${vlan.gateway}</div>
                </div>
                <div class="col-dhcp">
                  <ha-switch
                    .checked=${vlan.state === 'on'}
                    @change=${() => this._toggleDhcp(vlan.entity_id)}
                  ></ha-switch>
                </div>
              </div>
            `)}
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private async _toggleDhcp(entityId: string): Promise<void> {
    if (!this.hass) return;
    try {
      await this.hass.callService('switch', 'toggle', {
        entity_id: entityId,
      });
    } catch (err) {
      console.error("Failed to toggle DHCP switch:", err);
    }
  }

  static styles = [
    sharedStyles,
    css`
      :host { display: block; }
      .card-content { padding: 0 16px 16px 16px; }

      .vlan-table {
        display: flex;
        flex-direction: column;
        width: 100%;
      }

      .table-header {
        display: flex;
        padding: 8px 0;
        border-bottom: 1px solid var(--divider-color);
        font-weight: bold;
        color: var(--secondary-text-color);
        font-size: 12px;
        text-transform: uppercase;
      }

      .table-row {
        display: flex;
        align-items: center;
        padding: 12px 0;
        border-bottom: 1px solid var(--divider-color);
      }

      .table-row:last-child {
        border-bottom: none;
      }

      .col-vlan { flex: 2; display: flex; align-items: center; }
      .col-network { flex: 3; }
      .col-dhcp { flex: 1; display: flex; justify-content: flex-end; }

      .vlan-name {
        font-weight: 500;
        color: var(--primary-text-color);
      }

      .subnet {
        font-size: 14px;
        color: var(--primary-text-color);
      }

      .gateway {
        font-size: 12px;
        color: var(--secondary-text-color);
      }

      ha-switch {
        --switch-checked-button-color: var(--success-color, #4caf50);
        --switch-checked-track-color: var(--success-color, #4caf50);
      }
    `
  ];
}

export class MerakiVlanCardEditor extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  public setConfig(config: Config): void {
    this._config = config;
  }

  private _schema = [
    {
      name: "name",
      selector: { text: {} },
    },
  ];

  protected render() {
    if (!this.hass || !this._config) return html``;

    return html`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${this._schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
  }

  private _computeLabel = (schema: any): string => {
    if (schema.name === "name") return "Display Name (Optional)";
    return schema.name;
  }

  private _valueChanged(ev: CustomEvent): void {
    if (!this._config) return;
    const config = { ...this._config, ...ev.detail.value };
    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config },
      bubbles: true,
      composed: true,
    }));
  }

  static styles = css`
    .editor-container { padding: 16px; }
  `;
}

// Global Registration
if (!customElements.get('meraki-vlan-card')) {
  customElements.define('meraki-vlan-card', MerakiVlanCard);
}
if (!customElements.get('meraki-vlan-card-editor')) {
  customElements.define('meraki-vlan-card-editor', MerakiVlanCardEditor);
}

(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-vlan-card')) {
  (window as any).customCards.push({
    type: "meraki-vlan-card",
    name: "Cisco Meraki VLAN Card",
    description: "Overview and management of configured VLANs.",
    preview: true,
  });
}
