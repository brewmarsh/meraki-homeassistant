import React, { useState, useEffect, useRef } from 'react';
import QRCode from 'react-qr-code';
import { safeCallWS } from '../utils/api';
import { WsCommand, WsIpskKey } from '../types/websocket';

interface GroupPolicy {
  groupPolicyId: string;
  name: string;
}

interface TimedAccessProps {
  hass: any;
  configEntryId: string;
  data: any;
}

const TimedAccess: React.FC<TimedAccessProps> = ({
  hass,
  configEntryId,
  data,
}) => {
  const [keys, setKeys] = useState<WsIpskKey[]>([]);
  const [policies, setPolicies] = useState<GroupPolicy[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Form state
  const [selectedNetwork, setSelectedNetwork] = useState<string>('');
  const [selectedSsid, setSelectedSsid] = useState<string>('');
  const [selectedPolicy, setSelectedPolicy] = useState<string>('');
  const [duration, setDuration] = useState<string>('60'); // Minutes
  const [customName, setCustomName] = useState<string>('');
  const [customPassphrase, setCustomPassphrase] = useState<string>('');

  // Refs for custom elements
  const networkSelectRef = useRef<any>(null);
  const ssidSelectRef = useRef<any>(null);
  const policySelectRef = useRef<any>(null);
  const durationSelectRef = useRef<any>(null);

  // Initial load
  useEffect(() => {
    fetchKeys();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

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
    const handleNetworkChange = (e: any) => {
      setSelectedNetwork(e.target.value);
      setSelectedSsid('');
    };
    const handleSsidChange = (e: any) => setSelectedSsid(e.target.value);
    const handlePolicyChange = (e: any) => setSelectedPolicy(e.target.value);
    const handleDurationChange = (e: any) => setDuration(e.target.value);

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

  const fetchKeys = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const result = await safeCallWS<WsIpskKey[]>(hass, {
        type: WsCommand.GET_GUEST_KEYS,
        configEntryId: configEntryId,
      });
      setKeys(result);
    } catch (err: any) {
      console.error(err);
      setErrorMessage(err.message || err.toString() || "Failed to fetch guest keys.");
    } finally {
      setLoading(false);
    }
  };

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
        durationMinutes: parseInt(duration),
        name: customName || undefined,
        passphrase: customPassphrase || undefined,
        groupPolicyId: selectedPolicy || undefined,
      });
      await fetchKeys();
      // Reset form
      setCustomName('');
      setCustomPassphrase('');
    } catch (err: any) {
      setErrorMessage(err.message || err.toString() || "An unknown error occurred during creation.");
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (key: WsIpskKey) => {
    if (!confirm('Are you sure you want to revoke this key?')) return;
    setErrorMessage(null);
    try {
      await safeCallWS(hass, {
        type: WsCommand.REVOKE_GUEST_KEY,
        identityPskId: key.identity_psk_id,
      });
      fetchKeys();
    } catch (err: any) {
      setErrorMessage(err.message || err.toString() || "Failed to revoke key.");
    }
  };

  // Helper to find SSIDs for selected network
  const getSsidsForNetwork = (networkId: string) => {
    return data?.ssids?.filter((s: any) => s.networkId === networkId) || [];
  };

  // Format expiry
  const formatExpiry = (iso: string) => {
    const date = new Date(iso);
    const now = new Date();
    const diff = date.getTime() - now.getTime();
    if (diff <= 0) return 'Expired';
    const minutes = Math.floor(diff / 60000);
    return `${minutes} mins left (${date.toLocaleTimeString()})`;
  };

  const networks = data?.networks?.filter((n: any) => n.productTypes?.includes('wireless')) || [];
  const ssids = selectedNetwork ? getSsidsForNetwork(selectedNetwork) : [];

  return (
    <div className="max-w-6xl mx-auto p-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Timed guest access</h1>
      </div>

      {errorMessage && (
        <ha-alert
          alert-type="error"
          className="mb-6 block"
          dismissable
          onClose={() => setErrorMessage(null)}
        >
          {errorMessage}
        </ha-alert>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Create Section */}
        <div>
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
                {networks.map((n: any) => (
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
                {ssids.map((s: any) => (
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
                onInput={(e: any) => setCustomName(e.target.value)}
                className="w-full"
              />

              <ha-textfield
                label="Passphrase (Optional)"
                placeholder="Leave empty to auto-generate"
                value={customPassphrase}
                onInput={(e: any) => setCustomPassphrase(e.target.value)}
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
        </div>

        {/* List Section */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Active guest keys</h2>
          {loading ? (
            <div className="flex justify-center p-8">
              <ha-circular-progress active></ha-circular-progress>
            </div>
          ) : keys.length === 0 ? (
            <ha-card className="p-6 text-center text-[var(--secondary-text-color)] italic">
              No active keys found.
            </ha-card>
          ) : (
            <div className="space-y-4">
              {keys.map((key) => {
                const ssidName =
                  getSsidsForNetwork(key.network_id).find(
                    (s: any) => s.number.toString() === key.ssid_number
                  )?.name || `SSID ${key.ssid_number}`;
                const wifiString = `WIFI:T:WPA;S:${ssidName};P:${key.passphrase};;`;

                return (
                  <ha-card key={key.identity_psk_id} className="p-4">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <div className="text-lg font-bold">{key.name}</div>
                        <div className="text-sm text-[var(--secondary-text-color)]">
                          {ssidName}
                        </div>
                      </div>
                      <ha-button
                        onClick={() => handleDelete(key)}
                        className="text-[var(--error-color)]"
                      >
                        Revoke
                      </ha-button>
                    </div>

                    <div className="bg-[var(--secondary-background-color)] p-3 rounded font-mono text-center text-xl select-all mb-4 border border-[var(--divider-color)]">
                      {key.passphrase}
                    </div>

                    <div className="flex justify-between items-end">
                      <div className="text-sm text-[var(--primary-color)] font-medium">
                        {formatExpiry(key.expires_at)}
                      </div>
                      <div className="bg-white p-2 rounded shadow-sm">
                        <QRCode value={wifiString} size={80} />
                      </div>
                    </div>
                  </ha-card>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TimedAccess;
