import { MerakiDataProvider } from './utils/meraki-data';

export class MerakiWifiQrCardEditor extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;
  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];

  public setConfig(config: Config): void {
    this._config = config;
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._loadCentralizedData();
  }

  private async _loadCentralizedData() {
    if (!this.hass) return;
    const { networks, ssids } = await MerakiDataProvider.fetchConfig(this.hass);
    this._networks = networks;
    this._ssids = ssids;
  }

  private _valueChanged(ev: CustomEvent): void {
    if (!this._config) return;
    const formValues = ev.detail.value;
    const newConfig = { ...this._config, ...formValues };

    if (this._config.networkId !== formValues.networkId) {
      newConfig.ssid = "";
    }

    Object.keys(newConfig).forEach(key => {
      if (newConfig[key as keyof Config] === "") {
        delete newConfig[key as keyof Config];
      }
    });

    this.dispatchEvent(new CustomEvent("config-changed", { detail: { config: newConfig }, bubbles: true, composed: true }));
  }

  private _computeLabel = (schema: any): string => {
    if (schema.name === "networkId") return "Network (Optional filter)";
    if (schema.name === "ssid") return "SSID (Required)";
    if (schema.name === "password") return "Password (Optional override or Entity ID)";
    if (schema.name === "name") return "Card Title (Optional)";
    return schema.name;
  }

  protected render() {
    if (!this.hass || !this._config) return html``;

    // Use our new utility to build the arrays! We pass 'name' to get the SSID string.
    const networkOptions = MerakiDataProvider.getNetworkOptions(this._networks, true);
    const ssidOptions = MerakiDataProvider.getSsidOptions(this._ssids, this._config.networkId, 'name');

    const schema = [
      { name: "networkId", selector: { select: { options: networkOptions, mode: "dropdown" } } },
      { name: "ssid", selector: { select: { options: ssidOptions, custom_value: true, mode: "dropdown" } } },
      { name: "password", selector: { text: {} } },
      { name: "name", selector: { text: {} } }
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

  static styles = css`.editor-container { padding: 16px; }`;
}
