import React, { useState, useEffect, useRef } from 'react';
import { safeCallWS } from '../utils/api';
import { WsCommand } from '../types/websocket';

export interface GroupPolicy {
  groupPolicyId: string;
  name: string;
}

export interface Network {
  id: string;
  name: string;
  productTypes?: string[];
}

export interface SSID {
  networkId: string;
  number: number;
  name: string;
}

interface TimedAccessCreateProps {
  hass: any;
  configEntryId: string;
  networks: Network[];
  getSsidsForNetwork: (networkId: string) => SSID[];
  onCreated: () => void;
  setErrorMessage: (msg: string | null) => void;
}

const TimedAccessCreate: React.FC<TimedAccessCreateProps> = ({
  hass,
  configEntryId,
  networks,
  getSsidsForNetwork,
  onCreated,
  setErrorMessage,
}) => {
  const [policies, setPolicies] = useState<GroupPolicy[]>([]);
  const [creating, setCreating] = useState(false);

  // Form state
  const [selectedNetwork, setSelectedNetwork] = useState<string>('');
  const [selectedSsid, setSelectedSsid] = useState<string>('');
  const [selectedPolicy, setSelectedPolicy] = useState<string>('');
  const [duration, setDuration] = useState<string>('60'); // Minutes
  const [customName, setCustomName] = useState<string>('');
  const [customPassphrase, setCustomPassphrase] = useState<string>('');

  // Refs for custom elements
  const networkSelectRef = useRef<HTMLElement>(null);
  const ssidSelectRef = useRef<HTMLElement>(null);
  const policySelectRef = useRef<HTMLElement>(null);
  const durationSelectRef = useRef<HTMLElement>(null);

  // Fetch policies when network changes
  useEffect(() => {
    if (selectedNetwork) {
      fetchPolicies(selectedNetwork);
    } else {
      setPolicies([]);
      setSelectedPolicy('');
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedNetwork]);

  // Handle ha-select events
  useEffect(() => {
    const handleNetworkChange = (e: Event) => {
      setSelectedNetwork((e.target as HTMLInputElement).value);
      setSelectedSsid('');
    };
    const handleSsidChange = (e: Event) =>
      setSelectedSsid((e.target as HTMLInputElement).value);
    const handlePolicyChange = (e: Event) =>
      setSelectedPolicy((e.target as HTMLInputElement).value);
    const handleDurationChange = (e: Event) =>
      setDuration((e.target as HTMLInputElement).value);

    const networkEl = networkSelectRef.current;
    const ssidEl = ssidSelectRef.current;
    const policyEl = policySelectRef.current;
    const durationEl = durationSelectRef.current;

    networkEl?.addEventListener('change', handleNetworkChange);
    ssidEl?.addEventListener('change', handleSsidChange);
    policyEl?.addEventListener('change', handlePolicyChange);
    durationEl?.addEventListener('change', handleDurationChange);

    return () => {
      networkEl?.removeEventListener('change', handleNetworkChange);
      ssidEl?.removeEventListener('change', handleSsidChange);
      policyEl?.removeEventListener('change', handlePolicyChange);
      durationEl?.removeEventListener('change', handleDurationChange);
    };
  }, []);

  const fetchPolicies = async (networkId: string) => {
    try {
      const result = await safeCallWS<GroupPolicy[]>(hass, {
        type: WsCommand.TIMED_ACCESS_GET_POLICIES,
        configEntryId: configEntryId,
        networkId: networkId,
      });
      setPolicies(result);
    } catch (err: any) {
      console.error(err);
      setPolicies([]);
    }
  };

  const handleCreate = async () => {
    if (!selectedNetwork || !selectedSsid || !duration) return;
    setCreating(true);
    setErrorMessage(null);
    try {
      await safeCallWS(hass, {
        type: WsCommand.CREATE_GUEST_KEY,
        configEntryId: configEntryId,
        networkId: selectedNetwork,
        ssidNumber: selectedSsid,
        durationMinutes: parseInt(duration, 10),
        name: customName || undefined,
        passphrase: customPassphrase || undefined,
        groupPolicyId: selectedPolicy || undefined,
      });
      onCreated();
      // Reset form
      setCustomName('');
      setCustomPassphrase('');
    } catch (err: any) {
      setErrorMessage(
        err.message ||
          err.toString() ||
          'An unknown error occurred during creation.'
      );
    } finally {
      setCreating(false);
    }
  };

  const ssids = selectedNetwork ? getSsidsForNetwork(selectedNetwork) : [];

  return (
    <ha-card header="Create new key" className="p-4">
      <div className="space-y-4 flex flex-col">
        <ha-select
          ref={networkSelectRef}
          label="Network"
          value={selectedNetwork}
          className="w-full"
          fixedMenuPosition
          naturalMenuWidth
        >
          {networks.map((n) => (
            <ha-list-item key={n.id} value={n.id}>
              {n.name}
            </ha-list-item>
          ))}
        </ha-select>

        <ha-select
          ref={ssidSelectRef}
          label="SSID"
          value={selectedSsid}
          disabled={!selectedNetwork}
          className="w-full"
          fixedMenuPosition
          naturalMenuWidth
        >
          {ssids.map((s) => (
            <ha-list-item key={s.number} value={s.number.toString()}>
              {s.name} (SSID {s.number})
            </ha-list-item>
          ))}
        </ha-select>

        <ha-select
          ref={policySelectRef}
          label="Group policy"
          value={selectedPolicy}
          disabled={!selectedNetwork}
          className="w-full"
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="">None (Default)</ha-list-item>
          {policies.map((p) => (
            <ha-list-item key={p.groupPolicyId} value={p.groupPolicyId}>
              {p.name}
            </ha-list-item>
          ))}
        </ha-select>

        <ha-select
          ref={durationSelectRef}
          label="Duration"
          value={duration}
          className="w-full"
          fixedMenuPosition
          naturalMenuWidth
        >
          <ha-list-item value="30">30 Minutes</ha-list-item>
          <ha-list-item value="60">1 Hour</ha-list-item>
          <ha-list-item value="240">4 Hours</ha-list-item>
          <ha-list-item value="1440">24 Hours</ha-list-item>
          <ha-list-item value="10080">7 Days</ha-list-item>
        </ha-select>

        <ha-textfield
          label="Name (Optional)"
          placeholder="e.g. Guest-John"
          value={customName}
          onInput={(e: React.FormEvent<HTMLElement>) =>
            setCustomName((e.target as HTMLInputElement).value)
          }
          className="w-full"
        />

        <ha-textfield
          label="Passphrase (Optional)"
          placeholder="Leave empty to auto-generate"
          value={customPassphrase}
          onInput={(e: React.FormEvent<HTMLElement>) =>
            setCustomPassphrase((e.target as HTMLInputElement).value)
          }
          className="w-full"
        />

        <ha-button
          raised
          onClick={handleCreate}
          disabled={creating || !selectedNetwork || !selectedSsid}
          className="w-full"
        >
          {creating ? 'Creating...' : 'Generate access key'}
        </ha-button>
      </div>
    </ha-card>
  );
};

export default TimedAccessCreate;
