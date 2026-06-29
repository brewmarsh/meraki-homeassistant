import { LitElement, html, css, PropertyValues } from 'lit';
import { property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, renderLoadingState, sharedStyles } from './shared-ui';
import { MerakiDataProvider } from './utils/meraki-data';
import { WifiHelpers } from './utils/wifi-helpers';
import './meraki-content-filter-card';
import './meraki-wifi-qr-card';
import './meraki-network-vitals-card';
import './meraki-vlan-card';
import './meraki-guest-access-card-editor';
import { Network, SSID, GroupPolicy } from './types/meraki';
import { CustomCard } from './types/custom-card';

declare const __VERSION__: string;

interface Config {
  type: string;
  name?: string;
  config_entry_id?: string;
}

export class MerakiGuestAccessCard extends LitElement {
  @property({ attribute: false }) public hass!: HomeAssistant;
  @state() private _config?: Config;

  @state() private _formData = {
    network: '',
    ssid: '',
    passphrase: '',
    policy: '',
    duration: '60',
    guestName: '',
  };

  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];
  @state() private _policies: GroupPolicy[] = [];

  @state() private _creating: boolean = false;
  @state() private _error: string | null = null;
  @state() private _success: string | null = null;
  @state() private _qrSvg: string = '';
  @state() private _isLoading: boolean = true;
  @state() private _loadingMessage: string = 'Connecting to Meraki...';
  @state() private _configEntryId: string | null = null;
  @state() private _provisioning: boolean = false;
  @state() private _countdown: number = 30;

  private _timerInterval?: number;

  public static async getConfigElement() {
    return document.createElement('meraki-guest-access-card-editor');
  }

  public setConfig(config: Config): void {
    if (!config) throw new Error('Invalid configuration');
    this._config = config;
  }

  protected firstUpdated(changedProperties: PropertyValues) {
    super.firstUpdated(changedProperties);
    this._loadCentralizedData();
  }

  public disconnectedCallback() {
    super.disconnectedCallback();
    this._stopProvisioningTimer();
  }

  protected updated(changedProperties: PropertyValues) {
    super.updated(changedProperties);
    if (
      changedProperties.has('hass') &&
      this.hass &&
      this.hass.user?.name &&
      !this._formData.guestName
    ) {
      this._formData = {
        ...this._formData,
        guestName: this._generateUniqueGuestName(),
      };
    }
  }

  private _generateUniqueGuestName(): string {
    const baseName = this.hass?.user?.name || 'Home Assistant';
    // Use Web Crypto API for secure random number generation
    const array = new Uint32Array(1);
    window.crypto.getRandomValues(array);
    const secureRandom = array[0] / (0xffffffff + 1);

    const randomSuffix = Math.floor(secureRandom * 10000)
      .toString()
      .padStart(4, '0');
    return `${baseName} - Guest ${randomSuffix}`;
  }

  private async _loadCentralizedData() {
    if (!this.hass) return;

    const { networks, ssids, groupPolicies, entryId } =
      await MerakiDataProvider.pollConfig(this.hass, (msg, isLoading) => {
        this._loadingMessage = msg;
        this._isLoading = isLoading;
      });

    if (networks.length === 0) {
      this._isLoading = false;
      return;
    }

    this._networks = networks;
    this._ssids = ssids;
    this._policies = groupPolicies || [];
    this._configEntryId = this._config?.config_entry_id || entryId;

    let initNetwork = this._formData.network;
    let initSsid = this._formData.ssid;
    let initPassphrase = this._formData.passphrase;
    let initPolicy = this._formData.policy;

    if (networks.length > 0 && !initNetwork) {
      initNetwork = networks[0].id;
    }

    if (initNetwork && !initSsid) {
      const availableSsids = ssids.filter((s) => s.networkId === initNetwork);
      if (availableSsids.length > 0) {
        initSsid = String(availableSsids[0].number);
      }
    }

    if (initNetwork && initSsid && !initPassphrase) {
      initPassphrase = WifiHelpers.getPasswordForSsid(
        this.hass,
        this._ssids,
        initSsid,
        initNetwork
      );
      if (!initPassphrase) {
        initPassphrase = WifiHelpers.generateNaturalPassword();
      }
    }

    if (initNetwork && !initPolicy) {
      const networkPolicies = this._policies.filter(
        (p) => p.networkId === initNetwork
      );
      if (networkPolicies.length > 0) {
        initPolicy = String(
          networkPolicies[0].groupPolicyId || networkPolicies[0].id
        );
      } else {
        initPolicy = 'NONE';
      }
    }

    this._formData = {
      ...this._formData,
      network: initNetwork,
      ssid: initSsid,
      passphrase: initPassphrase,
      policy: initPolicy,
    };

    this._isLoading = false;
  }

  private _formValueChanged(ev: CustomEvent) {
    const newValues = ev.detail.value;
    const oldNetwork = this._formData.network;

    const updatedData = { ...this._formData, ...newValues };

    if (updatedData.network !== oldNetwork) {
      updatedData.ssid = '';
      updatedData.passphrase = '';
      updatedData.policy = '';

      const availableSsids = this._ssids.filter(
        (s) => s.networkId === updatedData.network
      );
      if (availableSsids.length > 0) {
        updatedData.ssid = String(availableSsids[0].number);
      }

      const networkPolicies = this._policies.filter(
        (p) => p.networkId === updatedData.network
      );
      if (networkPolicies.length > 0) {
        updatedData.policy = String(
          networkPolicies[0].groupPolicyId || networkPolicies[0].id
        );
      } else {
        updatedData.policy = 'NONE';
      }
    }

    // Force secure password generation if it gets cleared out by ha-form initialization
    if (!updatedData.passphrase && updatedData.network && updatedData.ssid) {
      updatedData.passphrase =
        WifiHelpers.getPasswordForSsid(
          this.hass,
          this._ssids,
          updatedData.ssid,
          updatedData.network
        ) || WifiHelpers.generateNaturalPassword();
    }

    this._formData = updatedData;
  }

  private _startProvisioningTimer() {
    this._stopProvisioningTimer();
    this._provisioning = true;
    this._countdown = 30;

    this._timerInterval = window.setInterval(() => {
      this._countdown -= 1;
      if (this._countdown <= 0) {
        this._stopProvisioningTimer();
      }
    }, 1000);
  }

  private _stopProvisioningTimer() {
    if (this._timerInterval) {
      clearInterval(this._timerInterval);
      this._timerInterval = undefined;
    }
    this._provisioning = false;
  }

  private _computeLabel = (schema: { name: string }): string => {
    if (schema.name === 'network') return 'Network';
    if (schema.name === 'ssid') return 'SSID';
    if (schema.name === 'policy') return 'Group Policy (Required)';
    if (schema.name === 'passphrase')
      return 'Passphrase / PSK (Auto-discovered)';
    if (schema.name === 'duration') return 'Duration';
    if (schema.name === 'guestName') return 'Guest Name';
    return schema.name;
  };

  protected render() {
    if (this._isLoading) {
      return renderLoadingState(
        this._config?.name || 'Cisco Meraki Guest Access',
        this._loadingMessage,
        __VERSION__
      );
    }

    if (this._networks.length === 0) {
      return renderWarning(
        'No Wireless Networks',
        'No Cisco Meraki wireless networks found. Ensure the integration is configured.',
        __VERSION__
      );
    }

    const networkOptions = MerakiDataProvider.getNetworkOptions(
      this._networks
    );
    const ssidOptions = MerakiDataProvider.getSsidOptions(
      this._ssids,
      this._formData.network,
      'number'
    );
    const networkPolicies = this._policies.filter(
      (p) => p.networkId === this._formData.network
    );
    const policyOptions = networkPolicies.map((p) => ({
      value: String(p.groupPolicyId || p.id),
      label: p.name,
    }));

    if (policyOptions.length === 0) {
      policyOptions.push({ value: 'NONE', label: 'Network Default' });
    }

    const schema = [
      {
        name: 'network',
        selector: { select: { options: networkOptions, mode: 'dropdown' } },
      },
      {
        name: 'ssid',
        selector: { select: { options: ssidOptions, mode: 'dropdown' } },
      },
      {
        name: 'policy',
        selector: {
          select: { options: policyOptions, mode: 'dropdown' },
        },
      },
      { name: 'passphrase', selector: { text: {} } },
      {
        name: 'duration',
        selector: {
          select: {
            options: [
              { value: '15', label: '15 Minutes' },
              { value: '30', label: '30 Minutes' },
              { value: '60', label: '1 Hour' },
              { value: '120', label: '2 Hours' },
              { value: '240', label: '4 Hours' },
              { value: '480', label: '8 Hours' },
              { value: '720', label: '12 Hours' },
              { value: '1440', label: '24 Hours' },
              { value: '2880', label: '48 Hours' },
              { value: '10080', label: '7 Days' },
            ],
            mode: 'dropdown',
          },
        },
      },
      { name: 'guestName', selector: { text: {} } },
    ];

    const isFormValid =
      this._formData.network && this._formData.ssid && this._formData.policy;

    const ssidNum = parseInt(this._formData.ssid, 10);
    const selectedSsidData = this._ssids.find(
      (s) => s.networkId === this._formData.network && s.number === ssidNum
    );
    const isIpskEnabled = selectedSsidData?.authMode === 'ipsk-without-radius';
    const showIpskWarning = selectedSsidData && !isIpskEnabled;

    if (this._success && this._qrSvg) {
      const selectedNetwork = this._networks.find(
        (n) => n.id === this._formData.network
      );
      const ssidNum = parseInt(this._formData.ssid, 10);
      const selectedSsid = this._ssids.find(
        (s) => s.networkId === this._formData.network && s.number === ssidNum
      );

      return html`
        <ha-card .header="${this._config?.name || 'Share Access'}">
          <div class="card-content success-ui">
            <ha-alert alert-type="success">${this._success}</ha-alert>

            ${this._provisioning
              ? html`
                  <div class="provisioning-ui">
                    <ha-circular-progress
                      active
                      size="large"
                    ></ha-circular-progress>
                    <p>Syncing to Meraki Access Points...</p>
                    <p class="timer">
                      Please wait ${this._countdown}s for the password to
                      activate.
                    </p>
                  </div>
                `
              : html`
                  <div
                    class="qr-container"
                    style="width: 200px; height: 200px;"
                    .innerHTML="${this._qrSvg}"
                  ></div>

                  <div class="credentials-block">
                    <div class="credential-item">
                      <span class="label">Network:</span>
                      <span class="value"
                        >${selectedNetwork?.name || 'Unknown'}</span
                      >
                    </div>
                    <div class="credential-item">
                      <span class="label">SSID:</span>
                      <span class="value"
                        >${selectedSsid?.name || 'Unknown'}</span
                      >
                    </div>
                    <div class="credential-item">
                      <span class="label">Password:</span>
                      <code class="copyable-code"
                        >${this._formData.passphrase}</code
                      >
                    </div>
                  </div>
                `}

            <ha-button raised @click=${this._resetForm}>
              Create Another
            </ha-button>
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    return html`
      <ha-card .header="${this._config?.name || 'Cisco Meraki Guest Access'}">
        <div class="card-content">
          ${this._error
            ? html`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => (this._error = null)}"
                >${this._error}</ha-alert
              >`
            : ''}

          <div class="form-container">
            ${showIpskWarning
              ? html`
                  <ha-alert
                    alert-type="warning"
                    title="SSID Configuration Required"
                  >
                    The selected SSID "${selectedSsidData.name}" is not
                    configured for Identity PSK. Please change the security
                    mode to "Identity PSK without RADIUS" in your Meraki
                    Dashboard. See the integration README to learn how to do
                    this safely without dropping existing devices.
                  </ha-alert>
                `
              : ''}

            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${schema}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !isFormValid || showIpskWarning}
              @click=${this._generateAccessKey}
            >
              ${this._creating
                ? html`<ha-circular-progress
                    active
                    size="small"
                  ></ha-circular-progress>`
                : 'Generate Access Key'}
            </ha-button>
          </div>
        </div>
        <div class="version">v${__VERSION__}</div>
      </ha-card>
    `;
  }

  private _resetForm() {
    this._stopProvisioningTimer();
    this._success = null;
    this._error = null;
    this._qrSvg = '';
    // Proactively generate a fresh name and clear the password so a new one is forced
    this._formData = {
      ...this._formData,
      guestName: this._generateUniqueGuestName(),
      passphrase: '',
    };
    this._loadCentralizedData();
  }

  private async _generateAccessKey() {
    if (
      !this._formData.network ||
      !this._formData.ssid ||
      !this._formData.policy
    )
      return;
    this._creating = true;
    this._error = null;
    this._success = null;
    this._qrSvg = '';

    try {
      const payload: Record<string, unknown> = {
        network_id: this._formData.network,
        ssid: parseInt(this._formData.ssid, 10),
        duration: parseInt(this._formData.duration, 10),
      };

      if (
        this._formData.policy &&
        this._formData.policy !== 'NONE' &&
        this._formData.policy !== 'CREATE'
      ) {
        payload.group_policy = this._formData.policy;
      }

      if (this._formData.guestName) {
        payload.guest_name = this._formData.guestName;
      }

      if (this._formData.passphrase) {
        payload.passphrase = this._formData.passphrase;
      }

      await this.hass.callService(
        'meraki_ha',
        'generate_guest_access',
        payload
      );

      const ssidNum = parseInt(this._formData.ssid, 10);
      const ssidObj = this._ssids.find(
        (s) => s.networkId === this._formData.network && s.number === ssidNum
      );
      const ssidName = ssidObj ? ssidObj.name : 'Guest WiFi';
      const password = this._formData.passphrase;

      const qrString = WifiHelpers.generateWifiQrString(ssidName, password);
      this._qrSvg = await WifiHelpers.generateQrSvg(qrString);

      this._success = 'Guest access key created successfully!';
      this._startProvisioningTimer();
    } catch (err: unknown) {
      this._error = `Failed to create guest key: ${err instanceof Error ? err.message : err}`;
    } finally {
      this._creating = false;
    }
  }

  static styles = [
    sharedStyles,
    css`
      .form-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      ha-button {
        width: 100%;
        margin-top: 8px;
      }
      .success-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 16px;
        padding-bottom: 16px;
      }
      .credentials-block {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 8px;
        background: var(--secondary-background-color);
        padding: 16px;
        border-radius: 8px;
      }
      .credential-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .credential-item .label {
        font-weight: bold;
        color: var(--secondary-text-color);
      }
      ha-alert {
        width: 100%;
      }
      .provisioning-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 24px;
        text-align: center;
        gap: 8px;
      }
      .timer {
        font-weight: bold;
        color: var(--primary-color);
      }
    `,
  ];
}

declare global {
  interface HTMLElementTagNameMap {
    'meraki-guest-access-card': MerakiGuestAccessCard;
  }
}
if (!customElements.get('meraki-guest-access-card')) {
  customElements.define('meraki-guest-access-card', MerakiGuestAccessCard);
}
window.customCards = window.customCards || [];
if (
  !window.customCards.some(
    (c: CustomCard) => c.type === 'meraki-guest-access-card'
  )
) {
  window.customCards.push({
    type: 'meraki-guest-access-card',
    name: 'Cisco Meraki Guest Access',
    description: `Manage temporary guest WiFi access. Version: ${__VERSION__}`,
    preview: true,
    version: __VERSION__,
  });
}
