import React, { useState, useEffect } from 'react';
import QRCode from 'react-qr-code';

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
  onClose: () => void;
}

const TimedAccess: React.FC<TimedAccessProps> = ({
  hass,
  configEntryId,
  data,
  onClose,
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
  }, []);

  // Fetch policies when network changes
  useEffect(() => {
    if (selectedNetwork) {
      fetchPolicies(selectedNetwork);
    }
  }, [selectedNetwork]);

  const fetchKeys = async () => {
    setLoading(true);
    try {
      const result = await hass.callWS({
        type: 'meraki_ha/timed_access/get_keys',
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
      const result = await hass.callWS({
        type: 'meraki_ha/timed_access/get_policies',
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
      await hass.callWS({
        type: 'meraki_ha/timed_access/create',
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
      await hass.callWS({
        type: 'meraki_ha/timed_access/delete',
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
    // Filter SSIDs by network ID
    // The main App.tsx passes `data` which has `ssids` as a flat list
    // e.g., ssids: [ { number: 0, name: 'Main WiFi', networkId: 'N_12345' } ]
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
    <div className="settings-overlay">
      <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
        <div className="settings-header">
          <h2>🔑 Timed Guest Access</h2>
          <button className="settings-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="settings-content">
          <div className="timed-access-grid">
            {/* Create Section */}
            <div className="timed-access-create">
              <h3 className="section-label">Create New Key</h3>

              <div className="settings-section">
                <label className="field-label">Network</label>
                <select
                  className="filter-select"
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
                <div className="settings-section">
                  <label className="field-label">SSID</label>
                  <select
                    className="filter-select"
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

              <div className="settings-section">
                <label className="field-label">Group Policy</label>
                <select
                  className="filter-select"
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

              <div className="settings-section">
                <label className="field-label">Duration</label>
                <select
                  className="filter-select"
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

              <div className="settings-section">
                <label className="field-label">Name (Optional)</label>
                <input
                  type="text"
                  className="search-input"
                  placeholder="e.g. Guest-John"
                  value={customName}
                  onChange={(e) => setCustomName(e.target.value)}
                />
              </div>

              <div className="settings-section">
                <label className="field-label">Passphrase (Optional)</label>
                <input
                  type="text"
                  className="search-input"
                  placeholder="Leave empty to auto-generate"
                  value={customPassphrase}
                  onChange={(e) => setCustomPassphrase(e.target.value)}
                />
              </div>

              <button
                className="btn-primary"
                onClick={handleCreate}
                disabled={creating || !selectedNetwork || !selectedSsid}
              >
                {creating ? 'Creating...' : '🔑 Generate Access Key'}
              </button>
            </div>

            {/* List Section */}
            <div className="timed-access-list">
              <h3 className="section-label">Active Guest Keys</h3>
              {loading ? (
                <p className="text-muted">Loading keys...</p>
              ) : keys.length === 0 ? (
                <p className="text-muted">No active keys found.</p>
              ) : (
                <div className="guest-keys-list">
                  {keys.map((key) => {
                    const ssidName =
                      getSsidsForNetwork(key.network_id).find(
                        (s: any) => s.number.toString() === key.ssid_number
                      )?.name || `SSID ${key.ssid_number}`;
                    const wifiString = `WIFI:T:WPA;S:${ssidName};P:${key.passphrase};;`;

                    return (
                      <div
                        key={key.identity_psk_id}
                        className="guest-key-card"
                      >
                        <div className="guest-key-header">
                          <div>
                            <div className="guest-key-name">{key.name}</div>
                            <div className="text-sm text-muted">
                              {ssidName}
                            </div>
                          </div>
                          <button
                            onClick={() => handleDelete(key)}
                            className="btn-revoke"
                          >
                            Revoke
                          </button>
                        </div>

                        <div className="guest-key-passphrase">
                          {key.passphrase}
                        </div>

                        <div className="guest-key-footer">
                          <div className="guest-key-expiry">
                            {formatExpiry(key.expires_at)}
                          </div>
                          <div className="guest-key-qr">
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
        </div>
      </div>
    </div>
  );
};

export default TimedAccess;
