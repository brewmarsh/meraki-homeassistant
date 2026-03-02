import React, { useState, useEffect } from 'react';
import QRCode from 'react-qr-code';
import { safeCallWS } from '../utils/api';
import { WsCommand } from '../types/websocket';

interface TimedAccessKey {
  identity_psk_id: string;
  network_id: string;
  ssid_number: string;
  name: string;
  passphrase: string;
  expires_at: string;
}

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
  const [keys, setKeys] = useState<TimedAccessKey[]>([]);
  const [policies, setPolicies] = useState<GroupPolicy[]>([]);
  const [loading, setLoading] = useState(false);
  const [creating, setCreating] = useState(false);

  // Form state
  const [selectedNetwork, setSelectedNetwork] = useState<string>('');
  const [selectedSsid, setSelectedSsid] = useState<string>('');
  const [selectedPolicy, setSelectedPolicy] = useState<string>('');
  const [duration, setDuration] = useState<string>('60'); // Minutes
  const [customName, setCustomName] = useState<string>('');
  const [customPassphrase, setCustomPassphrase] = useState<string>('');

  // Initial load
  useEffect(() => {
    fetchKeys();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Fetch policies when network changes
  useEffect(() => {
    if (selectedNetwork) {
      fetchPolicies(selectedNetwork);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedNetwork]);

  const fetchKeys = async () => {
    setLoading(true);
    try {
      const result = await safeCallWS<TimedAccessKey[]>(hass, {
        type: WsCommand.TIMED_ACCESS_GET_KEYS,
        config_entry_id: configEntryId,
      });
      setKeys(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchPolicies = async (networkId: string) => {
    try {
      const result = await safeCallWS<GroupPolicy[]>(hass, {
        type: WsCommand.TIMED_ACCESS_GET_POLICIES,
        config_entry_id: configEntryId,
        network_id: networkId,
      });
      setPolicies(result);
    } catch (err) {
      console.error(err);
      setPolicies([]);
    }
  };

  const handleCreate = async () => {
    if (!selectedNetwork || !selectedSsid || !duration) return;
    setCreating(true);
    try {
      await safeCallWS(hass, {
        type: WsCommand.TIMED_ACCESS_CREATE,
        config_entry_id: configEntryId,
        network_id: selectedNetwork,
        ssid_number: selectedSsid,
        duration: parseInt(duration),
        name: customName || undefined,
        passphrase: customPassphrase || undefined,
        group_policy_id: selectedPolicy || undefined,
      });
      await fetchKeys();
      // Reset form
      setCustomName('');
      setCustomPassphrase('');
    } catch (err) {
      alert(`Error creating key: ${err}`);
    } finally {
      setCreating(false);
    }
  };

  const handleDelete = async (key: TimedAccessKey) => {
    if (!confirm('Are you sure you want to revoke this key?')) return;
    try {
      await safeCallWS(hass, {
        type: WsCommand.TIMED_ACCESS_DELETE,
        config_entry_id: configEntryId,
        identity_psk_id: key.identity_psk_id,
        network_id: key.network_id,
        ssid_number: key.ssid_number,
      });
      fetchKeys();
    } catch (err) {
      alert(`Error deleting key: ${err}`);
    }
  };

  // Helper to find SSIDs for selected network
  const getSsidsForNetwork = (networkId: string) => {
    // Ideally filter for IPSK without Radius.
    // We assume data.ssids or data.networks contains SSIDs details.
    // The main App.tsx passes `data` which has `ssids`. But those are flat list of ALL SSIDs?
    // In App.tsx:
    // ssids: [ { number: 0, name: 'Main WiFi', networkId: 'N_12345' } ]
    // Let's use that.
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

  return (
    <div className="max-w-6xl mx-auto">
      <ha-card className="bg-[var(--card-background-color)] text-[var(--primary-text-color)] shadow-lg rounded-lg overflow-hidden p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">Timed Guest Access</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Create Section */}
          <div className="space-y-4 border-r pr-6 border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold">Create New Key</h3>

            <div>
              <label className="block text-sm font-medium mb-1">Network</label>
              <select
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                value={selectedNetwork}
                onChange={(e) => {
                  setSelectedNetwork(e.target.value);
                  setSelectedSsid('');
                }}
              >
                <option value="">Select Network</option>
                {data?.networks
                  ?.filter((n: any) => n.productTypes?.includes('wireless'))
                  .map((n: any) => (
                    <option key={n.id} value={n.id}>
                      {n.name}
                    </option>
                  ))}
              </select>
            </div>

            {selectedNetwork && (
              <div>
                <label className="block text-sm font-medium mb-1">SSID</label>
                <select
                  className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                  value={selectedSsid}
                  onChange={(e) => setSelectedSsid(e.target.value)}
                >
                  <option value="">Select SSID</option>
                  {getSsidsForNetwork(selectedNetwork).map((s: any) => (
                    <option key={s.number} value={s.number}>
                      {s.name} (SSID {s.number})
                    </option>
                  ))}
                </select>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium mb-1">
                Group Policy
              </label>
              <select
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                value={selectedPolicy}
                onChange={(e) => setSelectedPolicy(e.target.value)}
                disabled={!selectedNetwork}
              >
                <option value="">None (Default)</option>
                {policies.map((p) => (
                  <option key={p.groupPolicyId} value={p.groupPolicyId}>
                    {p.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Duration (Minutes)
              </label>
              <select
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
              >
                <option value="30">30 Minutes</option>
                <option value="60">1 Hour</option>
                <option value="240">4 Hours</option>
                <option value="1440">24 Hours</option>
                <option value="10080">7 Days</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Name (Optional)
              </label>
              <input
                type="text"
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                placeholder="e.g. Guest-John"
                value={customName}
                onChange={(e) => setCustomName(e.target.value)}
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Passphrase (Optional)
              </label>
              <input
                type="text"
                className="w-full p-2 border rounded dark:bg-gray-700 dark:border-gray-600"
                placeholder="Leave empty to auto-generate"
                value={customPassphrase}
                onChange={(e) => setCustomPassphrase(e.target.value)}
              />
            </div>

            <button
              className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700 disabled:opacity-50"
              onClick={handleCreate}
              disabled={creating || !selectedNetwork || !selectedSsid}
            >
              {creating ? 'Creating...' : 'Generate Access Key'}
            </button>
          </div>

          {/* List Section */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Active Guest Keys</h3>
            {loading ? (
              <div>Loading keys...</div>
            ) : keys.length === 0 ? (
              <div className="text-gray-500 italic">No active keys found.</div>
            ) : (
              <div className="space-y-4">
                {keys.map((key) => {
                  const ssidName =
                    getSsidsForNetwork(key.network_id).find(
                      (s: any) => s.number.toString() === key.ssid_number
                    )?.name || `SSID ${key.ssid_number}`;
                  const wifiString = `WIFI:T:WPA;S:${ssidName};P:${key.passphrase};;`;

                  return (
                    <div
                      key={key.identity_psk_id}
                      className="border rounded p-4 dark:border-gray-700 flex flex-col gap-2"
                    >
                      <div className="flex justify-between items-start">
                        <div>
                          <div className="font-bold">{key.name}</div>
                          <div className="text-sm text-gray-500">
                            {ssidName}
                          </div>
                        </div>
                        <button
                          onClick={() => handleDelete(key)}
                          className="text-red-500 hover:text-red-700 text-sm border border-red-500 rounded px-2 py-1"
                        >
                          Revoke
                        </button>
                      </div>

                      <div className="bg-gray-100 dark:bg-gray-900 p-2 rounded font-mono text-center text-lg select-all">
                        {key.passphrase}
                      </div>

                      <div className="flex justify-between items-end">
                        <div className="text-sm text-blue-600 dark:text-blue-400">
                          {formatExpiry(key.expires_at)}
                        </div>
                        <div className="bg-white p-1 rounded">
                          <QRCode value={wifiString} size={64} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </ha-card>
    </div>
  );
};

export default TimedAccess;
