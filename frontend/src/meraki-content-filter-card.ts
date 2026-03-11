import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, sharedStyles } from './shared-ui';

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

  // New Optimistic UI States to fight cloud caching
  @state() private _optimisticProfile: string | null = null;
  @state() private _isUpdating: boolean = false;

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
    if (!this.hass || !this._config) {
        return html`
          <ha-card .header="${this._config?.name || 'Meraki Content Filter'}">
            <div class="card-content">
              ${renderWarning("Integration Initializing", "Waiting for Home Assistant data...")}
            </div>
            <div class="version">v${__VERSION__}</div>
          </ha-card>
        `;
    }

    const entityId = this._config.entity || this._discoverEntity();
    const stateObj = entityId ? this.hass.states[entityId] : undefined;

    const titleStateObj = this._config.entity ? this.hass.states[this._config.entity] : undefined;
    const titleFriendlyName = titleStateObj?.attributes?.friendly_name || "Meraki";
    const title = this._config.name || (this._config.entity ? `${titleFriendlyName} Content Filter` : "Meraki Content Filter");

    if (!entityId || !stateObj) {
      return html`
        <ha-card .header="${title}">
          <div class="card-content">
             ${renderWarning("Entity Missing", "No content filter entity was found. Please check your configuration.")}
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const currentProfile = stateObj.state || 'Unknown';
    const profiles = stateObj.attributes?.options || ["None", "Security", "Family", "Strict"];

    // Use the optimistic profile if an update is actively processing
    const displayProfile = this._optimisticProfile || currentProfile;

    return html`
      <ha-card .header="${title}">
        <div class="card-content">
          <div class="button-grid">
            ${profiles.map((profile: string) => {
              const isActive = displayProfile.toLowerCase() === profile.toLowerCase();
              const isPendingThisButton = this._isUpdating && this._optimisticProfile === profile;
              
              return html`
                <button
                  class="filter-btn ${isActive ? 'active' : ''} ${this._isUpdating && !isPendingThisButton ? 'disabled' : ''}"
                  ?disabled=${this._isUpdating}
                  @click=${() => this._setFilterProfile(profile, entityId)}
                >
                  ${isPendingThisButton 
                    ? html`<ha-circular-progress active size="small"></ha-circular-progress> Saving...` 
                    : profile}
                </button>
              `;
            })}
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private async _setFilterProfile(profile: string, entityId: string): Promise<void> {
    // Block spam clicks if an update is already happening
    if (!this.hass || !entityId || !profile || this._isUpdating) return;

    this._isUpdating = true;
    this._optimisticProfile = profile;

    try {
      await this.hass.callService('select', 'select_option', {
        entity_id: entityId,
        option: profile,
      });

      // Hold the optimistic state for 8 seconds to let the Meraki cloud cache clear 
      // before allowing the real HA state to take over the UI again.
      setTimeout(() => {
        this._optimisticProfile = null;
        this._isUpdating = false;
      }, 8000);

    } catch (err: any) {
      console.error("Failed to call select_option service:", err);
      // Revert immediately if the API actually threw an error
      this._optimisticProfile = null; 
      this._isUpdating = false;
    }
  }

  static styles = [
    sharedStyles,
    css`
      :host { display: block; }
      ha-card {
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
      }
      .card-content { padding: 16px; }
      .button-grid {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }
      
      .filter-btn {
        width: 100%;
        padding: 12px;
        background: transparent;
        color: var(--primary-text-color, #ffffff);
        border: 1px solid var(--divider-color, #444444);
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s ease;
        font-family: inherit;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
      .filter-btn:hover:not(:disabled) {
        background: var(--secondary-background-color, rgba(255,255,255,0.05));
      }
      .filter-btn.active {
        background: var(--success-color, #4caf50);
        color: #ffffff;
        border-color: var(--success-color, #4caf50);
        font-weight: bold;
      }
      .filter-btn.disabled {
        opacity: 0.5;
        cursor: not-allowed;
      }
      
      /* Style the circular progress to match the text color */
      ha-circular-progress {
        --mdc-theme-primary: currentColor;
      }
    `
  ];
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

  private _computeLabel = (schema: any): string => {
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
    .editor-container { padding: 16px; }
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
