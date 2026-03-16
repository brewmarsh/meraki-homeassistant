import QRCode from 'qrcode';
import { HomeAssistant } from '../types/ha';
import { SSID } from '../types/meraki';

export class WifiHelpers {
  /**
   * Resolves a value that might be an entity ID or a raw string.
   */
  static getValue(hass: HomeAssistant, value?: string): string {
    if (!value || !hass) return value || '';
    if (hass.states[value]) {
      return hass.states[value].state;
    }
    return value;
  }

  /**
   * Discovers a Wi-Fi password using manual overrides, entity IDs, or smart attribute mapping.
   */
  static getPasswordForSsid(
    hass: HomeAssistant,
    ssids: SSID[],
    ssidNameOrNumber: string,
    networkId?: string,
    overridePassword?: string
  ): string {
    if (!hass) return '';

    // 1. Manual Override - Use provided password or resolve it if it's an entity ID
    if (overridePassword && overridePassword !== 'password123') {
      return this.getValue(hass, overridePassword);
    }

    if (!ssidNameOrNumber) return '';

    // 2. Resolve the SSID object from the cached data
    const ssidNum = parseInt(ssidNameOrNumber, 10);
    const ssidObj = ssids.find((s) => {
      const matchNetwork = !networkId || s.networkId === networkId;
      if (!isNaN(ssidNum)) {
        return s.number === ssidNum && matchNetwork;
      }
      return s.name === ssidNameOrNumber && matchNetwork;
    });

    // 3. Smart Auto-Discovery using attributes
    if (ssidObj) {
      for (const entityId in hass.states) {
        const stateObj = hass.states[entityId];
        const attrs = stateObj.attributes;

        if (
          attrs.network_id === ssidObj.networkId &&
          attrs.ssid_number === ssidObj.number
        ) {
          if (attrs.psk) return String(attrs.psk);
          if (attrs.password) return String(attrs.password);

          // Fallback to checking the state if the entity name looks like a password
          if (
            stateObj.state &&
            !['unknown', 'unavailable'].includes(stateObj.state)
          ) {
            if (entityId.includes('password') || entityId.includes('psk')) {
              return stateObj.state;
            }
          }
        }
      }
    }

    // 4. Fuzzy search fallback by name
    const ssidName = ssidObj ? ssidObj.name : ssidNameOrNumber;
    const normalizedSsid = ssidName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    for (const entityId in hass.states) {
      if (
        entityId.includes(normalizedSsid) &&
        (entityId.includes('password') || entityId.includes('psk'))
      ) {
        const stateObj = hass.states[entityId];
        if (
          stateObj.state &&
          !['unknown', 'unavailable'].includes(stateObj.state)
        ) {
          return stateObj.state;
        }
      }
    }

    return '';
  }

  /**
   * Escapes special characters for Wi-Fi QR strings.
   */
  static escapeWifiString(str: string): string {
    return str.replace(/([\\;,:"])/g, '\\$1');
  }

  /**
   * Generates a standard Wi-Fi QR string.
   */
  static generateWifiQrString(ssid: string, password?: string): string {
    const escapedSsid = this.escapeWifiString(ssid);
    const escapedPassword = password ? this.escapeWifiString(password) : '';
    return escapedPassword
      ? `WIFI:T:WPA;S:${escapedSsid};P:${escapedPassword};;`
      : `WIFI:T:nopass;S:${escapedSsid};P:;;`;
  }

  /**
   * Generates an SVG QR code from a string.
   */
  static async generateQrSvg(qrString: string, margin = 1): Promise<string> {
    try {
      return await QRCode.toString(qrString, {
        type: 'svg',
        margin: margin,
        color: {
          dark: '#000000',
          light: '#ffffff',
        },
      });
    } catch (err) {
      console.error('Failed to generate QR code SVG:', err);
      return '<div style="text-align:center; padding: 24px;">QR Code Unavailable</div>';
    }
  }

  /**
   * Generates a random, human-readable natural password.
   */
  static generateNaturalPassword(): string {
    const adjs = [
      'hot', 'cold', 'fast', 'slow', 'red', 'blue', 'green', 'tall', 'short',
      'loud', 'quiet', 'happy', 'brave', 'calm', 'cool', 'smart', 'bright',
      'clear', 'warm', 'wild', 'free', 'solid', 'swift', 'dark', 'light'
    ];
    const nouns = [
      'butter', 'potato', 'apple', 'tiger', 'lion', 'bear', 'hawk', 'tree',
      'river', 'mountain', 'ocean', 'breeze', 'cloud', 'star', 'moon', 'forest',
      'stone', 'water', 'fire', 'wood', 'metal', 'glass', 'sky', 'earth', 'sun'
    ];

    const pick = (arr: string[]) => arr[Math.floor(Math.random() * arr.length)];
    return `${pick(adjs)}-${pick(nouns)}-${Math.floor(Math.random() * 1000)}`;
  }
}
