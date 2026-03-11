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
      name: '',
    };
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    // Use configured entity or fallback to auto-discovery
    const entityId = this._config.entity || this._discoverEntity();
    const stateObj = entityId ? this.hass.states[entityId] : undefined;

    if (stateObj) {
      console.log("MERAKI CARD DIAGNOSTIC - Content Filter Raw Entity State:", stateObj);
    }

    const titleStateObj = this._config.entity ? this.hass.states[this._config.entity] : undefined;
    const titleFriendlyName = titleStateObj?.attributes?.friendly_name || "Meraki";
    const title = this._config.name || (this._config.entity ? `${titleFriendlyName} Content Filter` : "Meraki Content Filter");

    if (!entityId || !stateObj) {
      return html`
        <ha-card .header="${title}">
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

    const currentProfile = stateObj.state || 'Unknown';
    const profiles = stateObj.attributes?.options || ["None", "Security", "Family", "Strict"];

    return html`
      <ha-card .header="${title}">
        <div class="card-content">
          <div class="button-grid">
            ${profiles.map((profile: string) => html`
              <ha-button
                ?raised=${currentProfile === profile}
                ?outlined=${currentProfile !== profile}
                class="${currentProfile === profile ? 'active' : ''}"
                @click=${() => this._setFilterProfile(profile, entityId)}
              >
                ${profile}
              </ha-button>
            `)}
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private async _setFilterProfile(profile: string, entityId: string): Promise<void> {
    console.log("Clicked:", profile);
    console.log("MERAKI CARD DIAGNOSTIC - Setting Filter Profile:", profile, "for entity:", entityId);

    if (!this.hass || !entityId || !profile) return;

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
    .card-content { padding: 16px; }
    .button-grid {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    ha-button {
      width: 100%;
      --mdc-theme-primary: var(--primary-text-color);
    }
    ha-button.active {
      --mdc-theme-primary: var(--success-color, #4caf50);
      --mdc-theme-on-primary: #ffffff;
      font-weight: bold;
    }
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

  private _schema = [
    {
      name: "entity",
      selector: { entity: { domain: "select" } },
    },
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

  private _computeLabel(schema: any): string {
    if (schema.name === "entity") return "Entity (Optional)";
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
    .editor-container {
      display: block;
      padding: 16px;
    }
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
