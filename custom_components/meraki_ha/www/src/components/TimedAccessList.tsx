import React from 'react';
import QRCode from 'react-qr-code';
import { safeCallWS } from '../utils/api';
import { WsCommand, WsIpskKey } from '../types/websocket';
import { SSID } from './TimedAccessCreate';

interface TimedAccessListProps {
  hass: any;
  keys: WsIpskKey[];
  loading: boolean;
  getSsidsForNetwork: (networkId: string) => SSID[];
  onKeysChanged: () => void;
  setErrorMessage: (msg: string | null) => void;
}

const TimedAccessList: React.FC<TimedAccessListProps> = ({
  hass,
  keys,
  loading,
  getSsidsForNetwork,
  onKeysChanged,
  setErrorMessage,
}) => {
  const handleDelete = async (key: WsIpskKey) => {
    if (!confirm('Are you sure you want to revoke this key?')) return;
    setErrorMessage(null);
    try {
      await safeCallWS(hass, {
        type: WsCommand.REVOKE_GUEST_KEY,
        identityPskId: key.identity_psk_id,
      });
      onKeysChanged();
    } catch (err: any) {
      setErrorMessage(
        err.message || err.toString() || 'Failed to revoke key.'
      );
    }
  };

  const formatExpiry = (iso: string) => {
    const date = new Date(iso);
    const now = new Date();
    const diff = date.getTime() - now.getTime();
    if (diff <= 0) return 'Expired';
    const minutes = Math.floor(diff / 60000);
    return `${minutes} mins left (${date.toLocaleTimeString()})`;
  };

  if (loading) {
    return (
      <div className="flex justify-center p-8">
        <ha-circular-progress active></ha-circular-progress>
      </div>
    );
  }

  if (keys.length === 0) {
    return (
      <ha-card className="p-6 text-center text-[var(--secondary-text-color)] italic">
        No active keys found.
      </ha-card>
    );
  }

  return (
    <div className="space-y-4">
      {keys.map((key) => {
        const ssidName =
          getSsidsForNetwork(key.network_id).find(
            (s) => s.number.toString() === key.ssid_number
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
  );
};

export default TimedAccessList;
