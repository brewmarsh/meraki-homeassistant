import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';

declare const __VERSION__: string;

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
    // Priority: fix-content-filter-card-discovery branch
    this._config = { ...config };
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
        friendlyName.includes('content filter') ||
        entityId.includes('meraki')
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
    if (!this.hass) return html``;

    // Use configured entity or fallback to auto-discovery
    const entityId = this._config?.entity || this._discoverEntity();
    const stateObj = entityId ? this.hass.states[entityId] : undefined;

    if (!entityId || !stateObj) {
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
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const currentProfile = stateObj.state;
    const profiles = stateObj.attributes.options || ["None", "Security", "Family", "Strict"];
    const friendlyName = this._config?.name || stateObj.attributes.friendly_name || "Content Filter";

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
                @click="${() => this._handleProfileSelect(entityId, profile)}"
              >
                <span class="profile-name">${profile}</span>
              </div>
            `)}
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private async _handleProfileSelect(entityId: string, profile: string): Promise<void> {
    if (!this.hass || !entityId) return;

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
    :host { display: block; }
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
    }
    .warning-content strong { display: block; margin-bottom: 4px; }
    .warning-content p { margin: 0; font-size: 0.9em; opacity: 0.9; }
    .card-header { padding: 16px 16px 0; font-size: 24px; line-height: 1.2; }
    .card-content { padding: 16px; }
    .current-profile { color: var(--secondary-text-color); font-size: 0.9em; margin-bottom: 16px; }
    .profile-buttons { display: flex; flex-wrap: wrap; gap: 8px; }
    .profile-button {
      flex: 1 1 calc(50% - 4px);
      border: 1px solid var(--divider-color);
      border-radius: 8px;
      padding: 12px 8px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease-in-out;
      background-color: var(--card-background-color);
    }
    .profile-button:hover { background-color: var(--secondary-background-color); }
    .profile-button.active {
      background-color: var(--primary-color);
      color: var(--text-primary-color);
      border-color: var(--primary-color);
    }
    .profile-name { font-weight: bold; display: block; }
    .version {
      font-size: 9px;
      color: var(--secondary-text-color);
      text-align: right;
      padding: 4px 12px;
      opacity: 0.4;
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
    if (!this.hass || !this._config) return html``;

    return html`
      <div class="card-config">
        <ha-entity-picker
          .hass=${this.hass}
          .value=${this._config.entity}
          .configValue=${"entity"}
          .includeDomains=${["select"]}
          @value-changed=${this._valueChanged}
          allow-custom-entity
          label="Entity (Optional - Auto-discovery will attempt to find a Meraki content filter)"
        ></ha-entity-picker>
        <ha-textfield
          label="Display Name (Optional)"
          .value=${this._config.name || ""}
          .configValue=${"name"}
          @input=${this._valueChanged}
        ></ha-textfield>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config) return;
    const target = ev.target;
    const configValue = target.configValue;
    const newValue = ev.detail?.value ?? target.value;

    const newConfig = { ...this._config };
    if (!newValue) {
      delete newConfig[configValue];
    } else {
      newConfig[configValue] = newValue;
    }

    this.dispatchEvent(new CustomEvent("config-changed", {
      detail: { config: newConfig },
      bubbles: true,
      composed: true,
    }));
  }

  static styles = css`
    ha-entity-picker, ha-textfield { display: block; margin-bottom: 16px; width: 100%; }
  `;
}

// Global Registration
if (!customElements.get('meraki-content-filter-card')) {
  customElements.define('meraki-content-filter-card', MerakiContentFilterCard);
}
if (!customElements.get('meraki-content-filter-card-editor')) {
  customElements.define('meraki-content-filter-card-editor', MerakiContentFilterCardEditor);
}

(window as any).customCards = (window as any).customCards || [];
if (!(window as any).customCards.some((c: any) => c.type === 'meraki-content-filter-card')) {
  (window as any).customCards.push({
    type: "meraki-content-filter-card",
    name: "Meraki Content Filter",
    description: "Control Meraki Content Filtering profiles.",
    preview: true,
  });
}