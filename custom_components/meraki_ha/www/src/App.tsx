<<<<<<< HEAD
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
interface Network {
  id: string;
  name: string;
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
      setError("Home Assistant connection object not found.");
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

  return (
    <div>
      <Header />
      {loading && <p>Loading...</p>}
      {error && <p>Error: {error}</p>}
      {!loading && !error && data && (
        <>
          <NetworkView data={data} />
          <ha-card header="Event Log">
            <EventLog />
          </ha-card>
        </>
=======
import React, { useState, useEffect, useRef } from 'react';
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState({
    view: 'dashboard',
    deviceId: undefined,
  });
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (window.location.hostname === 'localhost') {
        setData({
          "networks": [
            { "id": "N_12345", "name": "Main Office", "is_enabled": true, "ssids": [] }
          ],
          devices: [
            { name: 'Living Room AP', model: 'MR33', serial: 'Q2JD-XXXX-XXXX', status: 'online', entity_id: 'switch.living_room_ap', networkId: 'N_12345' },
            { name: 'Office Switch', model: 'MS220-8P', serial: 'Q2HD-XXXX-XXXX', status: 'online', entity_id: 'switch.office_switch', networkId: 'N_12345' },
            { name: 'Front Door Camera', model: 'MV12', serial: 'Q2FD-XXXX-XXXX', status: 'online', entity_id: 'camera.front_door_camera', networkId: 'N_12345' },
          ],
          ssids: [],
        });
        setLoading(false);
        return;
    }
    let accessToken = localStorage.getItem('meraki_ha_llat');
    if (!accessToken) {
      accessToken = prompt(
        'Please enter your Home Assistant Long-Lived Access Token:'
      );
      if (accessToken) {
        localStorage.setItem('meraki_ha_llat', accessToken);
      } else {
        setError('No access token provided.');
        setLoading(false);
        return;
      }
    }

    const haUrl = (window as any).HA_URL.replace(/^http/, 'ws');
    const wsUrl = `${haUrl}/api/websocket`;
    socketRef.current = new WebSocket(wsUrl);
    const socket = socketRef.current;
    let messageId = 1;

    socket.onopen = () => {
      console.log('WebSocket connection established');
      socket.send(
        JSON.stringify({
          type: 'auth',
          access_token: accessToken,
        })
      );
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === 'auth_ok') {
        console.log('Authenticated successfully');
        socket.send(
          JSON.stringify({
            id: messageId,
            type: 'meraki_ha/get_config',
            config_entry_id: (window as any).CONFIG_ENTRY_ID,
          })
        );
      } else if (message.type === 'auth_invalid') {
        console.error('Authentication failed:', message.message);
        setError('Authentication failed. Please check your token.');
        setLoading(false);
        localStorage.removeItem('meraki_ha_llat');
      } else if (message.id === messageId) {
        if (message.type === 'result') {
          if (message.success) {
            const resultData = message.result;
            const { networks, enabled_networks } = resultData;

            if (networks && enabled_networks) {
              const processedNetworks = networks.map((network: any) => ({
                ...network,
                is_enabled: enabled_networks.includes(network.id),
              }));
              resultData.networks = processedNetworks;
            }
            setData(resultData);
          } else {
            console.error('Failed to fetch Meraki data:', message.error);
            setError(`Failed to fetch Meraki data: ${message.error.message}`);
          }
          setLoading(false);
        }
      }
    };

    socket.onerror = (err) => {
      console.error('WebSocket error:', err);
      setError('WebSocket connection error. See console for details.');
      setLoading(false);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      if (socket && socket.readyState === 1) {
        socket.close();
      }
    };
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  const handleToggle = (networkId: string, enabled: boolean) => {
    if (!data) return;

    const updatedNetworks = data.networks.map((network: any) =>
      network.id === networkId ? { ...network, is_enabled: enabled } : network
    );

    const updatedData = { ...data, networks: updatedNetworks };
    setData(updatedData);

    const enabledNetworkIds = updatedNetworks
      .filter((network: any) => network.is_enabled)
      .map((network: any) => network.id);

    const socket = socketRef.current;
    if (socket && socket.readyState === 1) {
      socket.send(
        JSON.stringify({
          id: Date.now(),
          type: 'meraki_ha/update_enabled_networks',
          config_entry_id: (window as any).CONFIG_ENTRY_ID,
          enabled_networks: enabledNetworkIds,
        })
      );
    } else {
      console.error('WebSocket is not connected.');
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Meraki HA Web UI</h1>
      {activeView.view === 'dashboard' ? (
        <NetworkView data={data} onToggle={handleToggle} setActiveView={setActiveView} />
      ) : (
        <DeviceView
          activeView={activeView}
          setActiveView={setActiveView}
          data={data}
        />
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
      )}
    </div>
  );
};

export default App;
