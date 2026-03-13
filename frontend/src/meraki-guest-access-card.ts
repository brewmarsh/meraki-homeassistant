import { LitElement, html, css, PropertyValues } from 'lit';
import { customElement, property, state } from 'lit/decorators.js';
import { HomeAssistant } from './types/ha';
import { renderWarning, renderLoading, sharedStyles } from './shared-ui';
import { MerakiDataProvider } from './utils/meraki-data';
import './meraki-content-filter-card';
import './meraki-wifi-qr-card';
import './meraki-network-vitals-card';
import './meraki-guest-access-card-editor';
import { Network, SSID } from './types/meraki';
import { WsCommand } from './types/websocket';
import { safeCallWS } from './utils/api';

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
    policy: '', // Added Policy field
    duration: '60',
    guestName: '',
  };

  @state() private _networks: Network[] = [];
  @state() private _ssids: SSID[] = [];
  @state() private _policies: any[] = []; // Restored Policies array

  @state() private _creating: boolean = false;
  @state() private _error: string | null = null;
  @state() private _success: string | null = null;
  @state() private _isLoading: boolean = true;
  @state() private _loadingMessage: string = "Connecting to Meraki...";
  @state() private _configEntryId: string | null = null;

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

  protected updated(changedProperties: PropertyValues) {
    super.updated(changedProperties);
    if (
      changedProperties.has('hass') &&
      this.hass &&
      this.hass.user?.name &&
      !this._formData.guestName
    ) {
      this._formData = { ...this._formData, guestName: this.hass.user.name };
    }
  }

  private async _loadCentralizedData() {
    if (!this.hass) return;

    const { networks, ssids, groupPolicies, entryId } = await MerakiDataProvider.pollConfig(
      this.hass,
      (msg, isLoading) => {
        this._loadingMessage = msg;
        this._isLoading = isLoading;
      }
    );

    if (networks.length === 0) {
      this._isLoading = false;
      return; // Polling failed after max retries
    }

    this._networks = networks;
    this._ssids = ssids;
    this._policies = groupPolicies;
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
      initPassphrase = this._getPasswordForSelectedSsid(initNetwork, initSsid);
    }

    // Auto-select the first available policy if none is selected
    if (initNetwork && !initPolicy) {
      const networkPolicies = this._policies.filter(p => p.networkId === initNetwork);
      if (networkPolicies.length > 0) {
        initPolicy = String(networkPolicies[0].groupPolicyId || networkPolicies[0].id);
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

  private _getPasswordForSelectedSsid(
    networkId: string,
    ssidNumberStr: string
  ): string {
    if (!this.hass || !networkId || !ssidNumberStr) return '';
    const ssidNum = parseInt(ssidNumberStr, 10);
    let ssidName = '';

    const ssidObj = this._ssids.find(
      (s) => s.networkId === networkId && s.number === ssidNum
    );
    if (ssidObj) {
      ssidName = ssidObj.name;
    }

    for (const entityId in this.hass.states) {
      const stateObj = this.hass.states[entityId];
      const attrs = stateObj.attributes;

      if (attrs.network_id === networkId && attrs.ssid_number === ssidNum) {
        if (!ssidName) ssidName = attrs.ssid_name || attrs.ssid || '';
        if (attrs.psk) return String(attrs.psk);
        if (attrs.password) return String(attrs.password);
      }
    }

    if (ssidName) {
      const normalizedSsid = ssidName.toLowerCase().replace(/[^a-z0-9]/g, '_');
      for (const entityId in this.hass.states) {
        if (
          entityId.includes(normalizedSsid) &&
          (entityId.includes('password') || entityId.includes('psk'))
        ) {
          const stateObj = this.hass.states[entityId];
          if (
            stateObj.state &&
            !['unknown', 'unavailable'].includes(stateObj.state)
          ) {
            return stateObj.state;
          }
        }
      }
    }

    return '';
  }

  private _formValueChanged(ev: CustomEvent) {
    const newValues = ev.detail.value;
    const oldNetwork = this._formData.network;
    const oldSsid = this._formData.ssid;

    let updatedData = { ...this._formData, ...newValues };

    if (updatedData.network !== oldNetwork) {
      updatedData.ssid = '';
      updatedData.passphrase = '';
      updatedData.policy = ''; // Clear the policy since the network changed

      const availableSsids = this._ssids.filter(
        (s) => s.networkId === updatedData.network
      );
      if (availableSsids.length > 0) {
        updatedData.ssid = String(availableSsids[0].number);
      }

      // Auto-select the first available policy for the new network
      const networkPolicies = this._policies.filter(p => p.networkId === updatedData.network);
      if (networkPolicies.length > 0) {
        updatedData.policy = String(networkPolicies[0].groupPolicyId || networkPolicies[0].id);
      }
    }

    if (updatedData.ssid && updatedData.ssid !== oldSsid) {
      updatedData.passphrase = this._getPasswordForSelectedSsid(
        updatedData.network,
        updatedData.ssid
      );
    }

    this._formData = updatedData;
  }

  private _computeLabel = (schema: any): string => {
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
    // [MERAKI CARD DIAGNOSTIC]
    console.debug('Meraki Guest Access Card Render State:', {
      isLoading: this._isLoading,
      networks: this._networks.length,
      ssids: this._ssids.length,
      policies: this._policies.length,
      formData: this._formData
    });

    if (this._isLoading) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content" style="display: flex; flex-direction: column; align-items: center; padding: 32px;">
            <ha-circular-progress active></ha-circular-progress>
            <div style="margin-top: 16px; color: var(--secondary-text-color); text-align: center;">
              ${this._loadingMessage}
            </div>
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    if (this._networks.length === 0) {
      return html`
        <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
          <div class="card-content">
            ${renderWarning(
              'No Wireless Networks',
              'No Meraki wireless networks found. Ensure the integration is configured.'
            )}
          </div>
          <div class="version">v${__VERSION__}</div>
        </ha-card>
      `;
    }

    const networkOptions = MerakiDataProvider.getNetworkOptions(
      this._networks
    );
    const ssidOptions = MerakiDataProvider.getSsidOptions(
      this._ssids,
      this._formData.network,
      'number'
    );
    const policyOptions = this._policies
      .filter((p) => p.networkId === this._formData.network)
      .map((p) => ({
        value: String(p.groupPolicyId || p.id),
        label: p.name,
      }));

    const schema = [
      {
        name: 'network',
        selector: { select: { options: networkOptions, mode: 'dropdown' } },
      },
      {
        name: 'ssid',
        selector: { select: { options: ssidOptions, mode: 'dropdown' } },
      },
      // Only show the policy dropdown if policies successfully loaded for this network
      ...(policyOptions.length > 0
        ? [
            {
              name: 'policy',
              selector: {
                select: { options: policyOptions, mode: 'dropdown' },
              },
            },
          ]
        : []),
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

    return html`
      <ha-card .header="${this._config?.name || 'Meraki Guest Access'}">
        <div class="card-content">
          ${this._error
            ? html`<ha-alert
                alert-type="error"
                dismissable
                @alert-dismissed-clicked="${() => (this._error = null)}"
                >${this._error}</ha-alert
              >`
            : ''}
          ${this._success
            ? html`<ha-alert
                alert-type="success"
                dismissable
                @alert-dismissed-clicked="${() => (this._success = null)}"
                >${this._success}</ha-alert
              >`
            : ''}

          <div class="form-container">
            <ha-form
              .hass=${this.hass}
              .data=${this._formData}
              .schema=${schema}
              .computeLabel=${this._computeLabel}
              @value-changed=${this._formValueChanged}
            ></ha-form>

            <ha-button
              raised
              .disabled=${this._creating || !isFormValid}
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

    try {
      const payload: any = {
        network_id: this._formData.network,
        ssid: parseInt(this._formData.ssid, 10),
        duration: parseInt(this._formData.duration, 10),
        group_policy_id: this._formData.policy, // Injects the required Meraki API parameter
      };

      if (this._formData.guestName) {
        payload.name = this._formData.guestName;
      }

      if (this._formData.passphrase) {
        payload.passphrase = this._formData.passphrase;
      }

      await this.hass.callService(
        'meraki_ha',
        'generate_guest_access',
        payload
      );
      this._success = 'Guest access key created successfully!';
    } catch (err: any) {
      this._error = `Failed to create guest key: ${err.message || err}`;
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
      .flex {
        display: flex;
      }
      .justify-center {
        justify-content: center;
      }
      .p-8 {
        padding: 32px;
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
(window as any).customCards = (window as any).customCards || [];
if (
  !(window as any).customCards.some(
    (c: any) => c.type === 'meraki-guest-access-card'
  )
) {
  (window as any).customCards.push({
    type: 'meraki-guest-access-card',
    name: 'Meraki Guest Access',
    description: `Manage temporary guest WiFi access. Version: ${__VERSION__}`,
    preview: true,
    version: __VERSION__,
  });
}
