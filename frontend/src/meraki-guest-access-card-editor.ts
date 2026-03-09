import { LitElement, html, css } from 'lit';
import { property, state } from 'lit/decorators.js';
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

  protected render() {
    if (!this.hass || !this._config) {
      return html``;
    }

    return html`
      <div class="card-config">
        <ha-textfield
          label="Name (Optional)"
          .value=${this._config.name || ""}
          configValue="name"
          @input=${this._valueChanged}
          style="width: 100%; margin-bottom: 16px;"
        ></ha-textfield>
        <ha-textfield
          label="Config Entry ID (Optional)"
          .value=${this._config.config_entry_id || ""}
          configValue="config_entry_id"
          @input=${this._valueChanged}
          style="width: 100%;"
        ></ha-textfield>
      </div>
    `;
  }

  private _valueChanged(ev: any): void {
    if (!this._config || !this.hass) return;
    const target = ev.target;
    const configValue = target.value;
    const configKey = target.configValue;

    if (this._config[configKey as keyof Config] === configValue) return;

    const newConfig = {
      ...this._config,
      [configKey]: configValue,
    };

    if (newConfig[configKey as keyof Config] === "" || newConfig[configKey as keyof Config] === undefined) {
      delete newConfig[configKey as keyof Config];
    }

    const event = new CustomEvent("config-changed", {
      detail: { config: newConfig },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }

  static styles = css`
    .card-config {
      display: flex;
      flex-direction: column;
    }
  `;
}

if (!customElements.get('meraki-guest-access-card-editor')) {
  customElements.define('meraki-guest-access-card-editor', MerakiGuestAccessCardEditor);
}
