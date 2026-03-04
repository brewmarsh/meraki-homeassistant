import React, { useState, useEffect } from 'react';
import { safeCallWS } from '../utils/api';
import { WsCommand, WsIpskKey } from '../types/websocket';
import TimedAccessCreate, { Network, SSID } from './TimedAccessCreate';
import TimedAccessList from './TimedAccessList';

interface TimedAccessProps {
  hass: any;
  configEntryId: string;
  data: {
    networks?: Network[];
    ssids?: SSID[];
    [key: string]: any;
  };
}

const TimedAccess: React.FC<TimedAccessProps> = ({
  hass,
  configEntryId,
  data,
}) => {
  const [keys, setKeys] = useState<WsIpskKey[]>([]);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Initial load
  useEffect(() => {
    fetchKeys();
    // eslint-disable-next-line react-hooks/exhaustive-deps
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

  // Helper to find SSIDs for selected network
  const getSsidsForNetwork = (networkId: string): SSID[] => {
    return data?.ssids?.filter((s) => s.networkId === networkId) || [];
  };

  const networks = data?.networks?.filter((n) => n.productTypes?.includes('wireless')) || [];

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
          <TimedAccessCreate
            hass={hass}
            configEntryId={configEntryId}
            networks={networks}
            getSsidsForNetwork={getSsidsForNetwork}
            onCreated={fetchKeys}
            setErrorMessage={setErrorMessage}
          />
        </div>

        {/* List Section */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Active guest keys</h2>
          <TimedAccessList
            hass={hass}
            keys={keys}
            loading={loading}
            getSsidsForNetwork={getSsidsForNetwork}
            onKeysChanged={fetchKeys}
            setErrorMessage={setErrorMessage}
          />
        </div>
      </div>
    </div>
  );
};

export default TimedAccess;
