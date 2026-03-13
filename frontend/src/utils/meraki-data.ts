// src/utils/meraki-data.ts
import { HomeAssistant } from '../types/ha';
import { Network, SSID } from '../types/meraki';
import { WsCommand } from '../types/websocket';
import { safeCallWS } from './api';

export interface GroupPolicy {
  networkId: string;
  groupPolicyId: string;
  name: string;
}

export class MerakiDataProvider {
  /**
   * Fetches wireless networks, SSIDs, and group policies directly from the integration's backend cache.
   */
  static async fetchConfig(hass: HomeAssistant) {
    try {
      const configEntries = await hass.callWS<any[]>({
        type: 'config/config_entries/get', // Fixed endpoint path
        domain: 'meraki_ha',
      });

      const entryId =
        configEntries.length > 0 ? configEntries[0].entry_id : null;
      if (!entryId)
        return { networks: [], ssids: [], groupPolicies: [], entryId: null };

      const data = await safeCallWS<any>(hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: entryId,
      });

      const networks: Network[] = (
        Array.isArray(data.networks) ? data.networks : []
      ).filter((n: any) => n.productTypes?.includes('wireless'));
      const ssids: SSID[] = Array.isArray(data.ssids) ? data.ssids : [];

      const groupPolicies: GroupPolicy[] = [];
      if (data.group_policies && typeof data.group_policies === 'object') {
        for (const [networkId, policies] of Object.entries(
          data.group_policies
        )) {
          if (Array.isArray(policies)) {
            policies.forEach((p: any) => {
              groupPolicies.push({
                networkId,
                groupPolicyId: String(p.groupPolicyId),
                name: p.name,
              });
            });
          }
        }
      }

      return { networks, ssids, groupPolicies, entryId };
    } catch (err) {
      console.error('Failed to fetch Meraki data via WS:', err);
      return { networks: [], ssids: [], groupPolicies: [], entryId: null };
    }
  }

  /**
   * Intelligently polls the backend until the API backoffs clear and data is populated.
   * @param hass The Home Assistant instance
   * @param onStatusUpdate Callback fired whenever the loading state or message changes
   * @param maxRetries Maximum number of polling attempts (default: 12 attempts / ~1 minute)
   * @param delayMs Delay between attempts in milliseconds (default: 5000ms)
   */
  static async pollConfig(
    hass: HomeAssistant,
    onStatusUpdate: (message: string, isLoading: boolean) => void,
    maxRetries: number = 12,
    delayMs: number = 5000
  ): Promise<{ networks: Network[], ssids: SSID[], groupPolicies: GroupPolicy[], entryId: string | null }> {
    
    for (let i = 0; i < maxRetries; i++) {
      try {
        const data = await this.fetchConfig(hass);
        
        // If networks are found, the integration is fully booted
        if (data.networks.length > 0) {
          onStatusUpdate("", false); 
          return data;
        }
        
        onStatusUpdate(`Waiting for integration to sync... (Attempt ${i + 1}/${maxRetries})`, true);
      } catch (err) {
        onStatusUpdate(`Error connecting to backend. Retrying... (Attempt ${i + 1}/${maxRetries})`, true);
      }

      // Wait before the next poll
      await new Promise(resolve => setTimeout(resolve, delayMs));
    }

    // Exhausted all retries
    onStatusUpdate("Integration failed to initialize after 1 minute. Please check backend logs.", false);
    return { networks: [], ssids: [], groupPolicies: [], entryId: null };
  }

  /**
   * Formats networks for an ha-form dropdown.
   */
  static getNetworkOptions(networks: Network[], includeAllOption = false) {
    const options = networks.map((n) => ({ value: n.id, label: n.name }));
    return includeAllOption
      ? [{ value: '', label: 'All Networks' }, ...options]
      : options;
  }

  /**
   * Formats SSIDs for an ha-form dropdown.
   * @param valueType Determines if the dropdown returns the SSID's string name (for QR codes) or integer number (for Guest API calls).
   */
  static getSsidOptions(
    ssids: SSID[],
    networkId?: string,
    valueType: 'name' | 'number' = 'name'
  ) {
    const filtered = networkId
      ? ssids.filter((s) => s.networkId === networkId)
      : ssids;
    return filtered.map((s) => ({
      value: valueType === 'number' ? String(s.number) : s.name,
      label: `${s.name} (SSID ${s.number})`,
    }));
  }

  /**
   * Formats Group Policies for an ha-form dropdown.
   */
  static getGroupPolicyOptions(
    groupPolicies: GroupPolicy[],
    networkId?: string
  ) {
    const filtered = networkId
      ? groupPolicies.filter((p) => p.networkId === networkId)
      : groupPolicies;
    const options = filtered.map((p) => ({
      value: p.groupPolicyId,
      label: p.name,
    }));
    return [
      { value: 'CREATE', label: "Create 'Home Assistant Guest' Policy" },
      { value: 'NONE', label: 'None (Network Default)' },
      ...options,
    ];
  }
}
