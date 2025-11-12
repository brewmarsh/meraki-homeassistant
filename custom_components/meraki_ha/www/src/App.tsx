import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import NetworkView from './components/NetworkView';
import EventLog from './components/EventLog';

// Define a more complete type for the Home Assistant object
interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
  };
  themes: {
    darkMode: boolean;
  };
}

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
}

interface Device {
  entity_id: string;
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
}

interface MerakiData {
  networks: Network[];
  devices: Device[];
  enabled_networks: string[];
  config_entry_id: string;
  version: string;
}

interface AppProps {
  hass: Hass;
  config_entry_id: string;
}

const App: React.FC<AppProps> = ({ hass, config_entry_id }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hass || !hass.connection) {
      setError('Home Assistant connection object not found.');
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const result = await hass.connection.sendMessagePromise({
          type: 'meraki_ha/get_config',
          config_entry_id: config_entry_id,
        });
        setData(result);
      } catch (err: any) {
        console.error('Error fetching Meraki data:', err);
        setError(`Failed to fetch Meraki data: ${err.message || 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [hass, config_entry_id]);

  const handleToggle = async (networkId: string, enabled: boolean) => {
    if (!data) return;

    const newEnabledNetworks = enabled
      ? [...data.enabled_networks, networkId]
      : data.enabled_networks.filter((id) => id !== networkId);

    // Optimistically update the UI
    const updatedNetworks = data.networks.map((n) =>
      n.id === networkId ? { ...n, is_enabled: enabled } : n
    );
    setData({
      ...data,
      networks: updatedNetworks,
      enabled_networks: newEnabledNetworks,
    });

    try {
      await hass.connection.sendMessagePromise({
        type: 'meraki_ha/update_enabled_networks',
        config_entry_id,
        enabled_networks: newEnabledNetworks,
      });
    } catch (err) {
      console.error('Error updating enabled networks:', err);
      // Revert the optimistic update on error
      setData(data);
    }
  };

  return (
    <div>
      <Header />
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && data && (
        <>
          <NetworkView data={data} onToggle={handleToggle} />
          <ha-card header="Event Log">
            <EventLog />
          </ha-card>
          <div style={{ textAlign: 'center', marginTop: '16px' }}>
            <p>Version: {data.version}</p>
          </div>
        </>
      )}
    </div>
  );
};

export default App;
