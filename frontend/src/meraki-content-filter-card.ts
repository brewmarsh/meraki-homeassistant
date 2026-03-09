import { LitElement, html, css, PropertyValues } from 'lit';
import { property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';

interface Config {
  type: string;
  entity: string;
  name?: string;
  [key: string]: any;
}

export class MerakiContentFilterCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  public static async getConfigElement() {
    return document.createElement("meraki-content-filter-card-editor");
  }

  public setConfig(config: Config): void {
    if (!config) {
      throw new Error('Invalid configuration');
    }
    this._config = config;
  }

  private _discoverEntity(): string | undefined {
    if (!this.hass) return undefined;

    // Search for a select entity with 'content_filter' in unique_id or name
    return Object.keys(this.hass.states).find((entityId) => {
      if (!entityId.startsWith('select.')) return false;
      const stateObj = this.hass.states[entityId];
      const friendlyName = stateObj.attributes.friendly_name?.toLowerCase() || '';
      return (
        entityId.includes('content_filter') ||
        friendlyName.includes('content filter')
      );
    });
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      entity: '',
      name: 'Meraki Content Filter',
    };
  }

  protected render() {
    if (!this._config || !this.hass) {
      return html``;
    }

    const entityId = this._config.entity || this._discoverEntity();

    if (!entityId || !this.hass.states[entityId]) {
      return html`
        <ha-card>
          <div class="card-content">
            <div class="meraki-warning">
              <ha-icon icon="mdi:information"></ha-icon>
              <div class="warning-content">
                <strong>Integration Initializing</strong>
                <p>The Meraki integration is still fetching data or no content filter entity was found. Please wait or check your configuration.</p>
              </div>
            </div>
          </div>
        </ha-card>
      `;
    }

    const stateObj = this.hass.states[entityId];

    const currentProfile = stateObj.state;
    const profiles = stateObj.attributes.options || ["None", "Security", "Family", "Strict"];
    const friendlyName = this._config.name || stateObj.attributes.friendly_name || "Content Filter";

    return html`
      <ha-card>
        <div class="card-header">${friendlyName}</div>
        <div class="card-content">
          <div class="current-profile">
            Current Profile: <strong>${currentProfile}</strong>
          </div>
          <div class="profile-buttons">
            ${profiles.map((profile: string) => html`
              <div
                class="profile-button ${currentProfile === profile ? 'active' : ''}"
                @click="${() => this._handleProfileSelect(profile)}"
              >
                <span class="profile-name">${profile}</span>
              </div>
            `)}
          </div>
        </div>
      </ha-card>
    `;
  }

  private async _handleProfileSelect(profile: string): Promise<void> {
    if (!this.hass || !this._config) return;

    const entityId = this._config.entity || this._discoverEntity();
    if (!entityId) return;

    try {
      await this.hass.callService('select', 'select_option', {
        entity_id: entityId,
        option: profile,
      });
    } catch (err: any) {
      console.error("Failed to call select_option service:", err);
    }
  }

  static styles = css`
    :host {
      display: block;
    }
    ha-card {
      height: 100%;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .meraki-warning {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 12px;
      background-color: var(--warning-color);
      color: var(--primary-text-color);
      border-radius: 8px;
      border-left: 4px solid var(--warning-color);
    }
    .meraki-warning ha-icon {
      color: var(--primary-text-color);
    }
    .warning-content strong {
      display: block;
      margin-bottom: 4px;
    }
    .warning-content p {
      margin: 0;
      font-size: 0.9em;
      opacity: 0.8;
    }
    .card-header {
      padding: 16px 16px 0;
      font-size: 24px;
      line-height: 1.2;
    }
    .card-content {
      padding: 16px;
    }
    .current-profile {
      color: var(--secondary-text-color);
      font-size: 0.9em;
      margin-bottom: 16px;
    }
    .profile-buttons {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .profile-button {
      flex: 1 1 calc(50% - 4px);
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      padding: 8px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      background-color: var(--card-background-color);
    }
    .profile-button:hover {
      background-color: var(--secondary-background-color);
    }
    .profile-button.active {
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      border-color: var(--primary-color);
    }
    .profile-button.active .profile-name {
       color: var(--text-primary-color);
    }
    .profile-name {
      font-weight: bold;
      display: block;
    }
  `;
}

export class MerakiContentFilterCardEditor extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
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
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this._config.entity}
          configValue="entity"
          .includeDomains=${["select"]}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          label="Entity (Optional - Auto-discovery will try to find a content filter)"
        ></ha-entity-picker>
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          configValue="name"
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config || !this.hass) {
      return;
    }
    const target = ev.target;
    const configValue = target.configValue;

    if (!configValue) {
      return;
    }

    let newValue = target.value;
    if (ev.detail && ev.detail.value !== undefined) {
      newValue = ev.detail.value;
    }

    if (this._config[configValue] === newValue) {
      return;
    }

    const newConfig = { ...this._config };
    if (newValue === "" || newValue === undefined) {
      delete newConfig[configValue];
    } else {
      newConfig[configValue] = newValue;
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
    .card-config ha-entity-picker,
    .card-config ha-textfield {
      display: block;
      margin-bottom: 16px;
      width: 100%;
    }
  `;
}

if (!customElements.get('meraki-content-filter-card')) {
  customElements.define('meraki-content-filter-card', MerakiContentFilterCard);
}

if (!customElements.get('meraki-content-filter-card-editor')) {
  customElements.define('meraki-content-filter-card-editor', MerakiContentFilterCardEditor);
}

declare global {
  const __VERSION__: string;
}

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-content-filter-card')) {
  (window as any).customCards.push({
    type: "meraki-content-filter-card",
    name: "Meraki Content Filter",
    description: "Control Meraki Content Filtering profiles.",
    preview: true,
    version: __VERSION__,
  });
}
