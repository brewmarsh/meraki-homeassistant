import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';

interface Config {
  type: string;
  entity: string;
  name?: string;
}

@customElement('meraki-content-filter-card')
export class MerakiContentFilterCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  public setConfig(config: Config): void {
    if (!config || !config.entity) {
      throw new Error('Please define a Meraki content filter entity');
    }
    this._config = config;
  }

  public static getStubConfig(): Record<string, unknown> {
    return {
      entity: 'select.meraki_network_content_filter',
      name: 'Meraki Content Filter',
    };
  }

  protected render() {
    if (!this._config || !this.hass) {
      return html``;
    }

    const entityId = this._config.entity;
    const stateObj = this.hass.states[entityId];

    if (!stateObj) {
      return html`
        <ha-card>
          <div class="card-content">
            <ha-alert alert-type="error">Entity not found: ${entityId}</ha-alert>
          </div>
        </ha-card>
      `;
    }

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

    try {
      await this.hass.callService('select', 'select_option', {
        entity_id: this._config.entity,
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
    .card-header {
      padding: 16px 16px 0;
      font-size: 24px;
      line-height: 1.2;
    }
    .card-content {
      padding: 16px;
    }
    .network-name {
      font-weight: 500;
      margin-bottom: 4px;
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
      --mdc-theme-primary: var(--primary-text-color);
      --mdc-theme-on-primary: var(--card-background-color);
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

// Register the card in the Home Assistant Lovelace UI picker
(window as any).customCards = (window as any).customCards || [];
(window as any).customCards.push({
  type: "meraki-content-filter-card",
  name: "Meraki Content Filter",
  description: "Control Meraki Content Filtering profiles.",
  preview: true,
});
