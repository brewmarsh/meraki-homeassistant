import { LitElement, html, css } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';

interface Config {
  type: string;
  name?: string;
  config_entry_id?: string;
}

export class MerakiGuestAccessCardEditor extends LitElement {
  @property({ attribute: false }) public hass?: HomeAssistant;
  @state() private _config?: Config;

  public setConfig(config: Config): void {
    this._config = config;
  }

  private _computeLabel = (schema: any): string => {
    if (schema.name === "name") return "Title (Optional)";
    if (schema.name === "config_entry_id") return "Config Entry ID (Optional override)";
    return schema.name;
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    const schema = [
      { name: "name", selector: { text: {} } },
      { name: "config_entry_id", selector: { text: {} } }
    ];

    return html`
      <div class="editor-container">
        <ha-form
          .hass=${this.hass}
          .data=${this._config}
          .schema=${schema}
          .computeLabel=${this._computeLabel}
          @value-changed=${this._valueChanged}
        ></ha-form>
      </div>
    `;
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

if (!customElements.get('meraki-guest-access-card-editor')) {
  customElements.define('meraki-guest-access-card-editor', MerakiGuestAccessCardEditor);
}
