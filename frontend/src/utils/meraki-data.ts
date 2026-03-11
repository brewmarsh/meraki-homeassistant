// src/utils/meraki-data.ts
import { HomeAssistant } from '../types/ha';
import { Network, SSID } from '../types/meraki';
import { WsCommand } from '../types/websocket';
import { safeCallWS } from './api';

export class MerakiDataProvider {
  /**
   * Fetches wireless networks and SSIDs directly from the integration's backend cache.
   */
  static async fetchConfig(hass: HomeAssistant) {
    try {
      const configEntries = await hass.callWS<any[]>({
        type: 'config_entries/get',
        domain: 'meraki_ha',
      });

      const entryId = configEntries.length > 0 ? configEntries[0].entry_id : null;
      if (!entryId) return { networks: [], ssids: [], entryId: null };

      const data = await safeCallWS<any>(hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: entryId,
      });

      const networks: Network[] = (Array.isArray(data.networks) ? data.networks : [])
        .filter((n: any) => n.productTypes?.includes('wireless'));
      const ssids: SSID[] = Array.isArray(data.ssids) ? data.ssids : [];

      return { networks, ssids, entryId };
    } catch (err) {
      console.error('Failed to fetch Meraki data via WS:', err);
      return { networks: [], ssids: [], entryId: null };
    }
  }

  /**
   * Formats networks for an ha-form dropdown.
   */
  static getNetworkOptions(networks: Network[], includeAllOption = false) {
    const options = networks.map(n => ({ value: n.id, label: n.name }));
    return includeAllOption ? [{ value: "", label: "All Networks" }, ...options] : options;
  }

  /**
   * Formats SSIDs for an ha-form dropdown. 
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(ssids: SSID[], networkId?: string, valueType: 'name' | 'number' = 'name') {
    const filtered = networkId ? ssids.filter(s => s.networkId === networkId) : ssids;
    return filtered.map(s => ({
      value: valueType === 'number' ? String(s.number) : s.name,
      label: `${s.name} (SSID ${s.number})`
    }));
  }
}
