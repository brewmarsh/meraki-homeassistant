import React, { useState, useEffect } from 'react';
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';
import Settings from './components/Settings';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {}

const App: React.FC<AppProps> = () => {
  console.log('DEBUG (App.tsx): App component started.'); // New very early log
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState({
    view: 'dashboard',
    deviceId: undefined,
  });
  const [showSettings, setShowSettings] = useState(false);

  const fetchData = () => {
    if (window.location.hostname === 'localhost') {
      setData({
        networks: [
          { id: 'N_12345', name: 'Main Office', is_enabled: true, ssids: [] },
        ],
        devices: [
          {
            name: 'Living Room AP',
            model: 'MR33',
            serial: 'Q2JD-XXXX-XXXX',
            status: 'online',
            entity_id: 'switch.living_room_ap',
            networkId: 'N_12345',
          },
          {
            name: 'Office Switch',
            model: 'MS220-8P',
            serial: 'Q2HD-XXXX-XXXX',
            status: 'online',
            entity_id: 'switch.office_switch',
            networkId: 'N_12345',
          },
          {
            name: 'Front Door Camera',
            model: 'MV12',
            serial: 'Q2FD-XXXX-XXXX',
            status: 'online',
            lanIp: '192.168.1.100',
            entity_id: 'camera.front_door_camera',
            networkId: 'N_12345',
          },
        ],
        ssids: [],
        options: {
          enable_device_status: true,
          enable_org_sensors: true,
          enable_camera_entities: true,
          enable_device_sensors: true,
          enable_network_sensors: true,
          enable_vlan_sensors: true,
          enable_port_sensors: true,
          enable_ssid_sensors: true,
        },
      });
      setLoading(false);
      return;
    }

    let accessToken = localStorage.getItem('meraki_ha_llat');
    if (!accessToken) {
      // Try to get token from hass object if available (usually not in iframe)
      const hass = (window as any).hass;
      if (hass && hass.auth && hass.auth.accessToken) {
        accessToken = hass.auth.accessToken;
      }
    }

    // If still no token and not in dev, we rely on the existing connection flow
    // But typically the panel is served within HA which has auth.
    // The previous code used a standalone websocket connection pattern.
    // We will keep it but update to handle "options" in response.

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

    const haUrl = (window as any).HA_URL
      ? (window as any).HA_URL.replace(/^http/, 'ws')
      : window.location.protocol === 'https:'
      ? 'wss://' + window.location.host
      : 'ws://' + window.location.host;
    const wsUrl = `${haUrl}/api/websocket`;
    const socket = new WebSocket(wsUrl);
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
      console.log('DEBUG (App.tsx): WebSocket message received.');
      const message = JSON.parse(event.data);

      if (message.type === 'auth_ok') {
        console.log('Authenticated successfully');
        console.log(
          'DEBUG (App.tsx): Attempting to send meraki_ha/get_config'
        );
        const haConfigEntryId = (window as any).hass?.panel?.config
          ?.config_entry_id;
        console.log(
          'DEBUG (App.tsx): hass.panel.config.config_entry_id:',
          haConfigEntryId
        );
        socket.send(
          JSON.stringify({
            id: messageId,
            type: 'meraki_ha/get_config',
            config_entry_id: haConfigEntryId,
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
            // Check if result is wrapped in 'result' or is the result itself
            // Based on web_api.py: connection.send_result(msg["id"], { ... })
            // The HA websocket client returns { id, type: result, success: true, result: { ... } }
            // So message.result is the data.
            setData(message.result);
          } else {
            // This branch might not be reached if success is false, HA sends error type?
            // Usually HA sends type: "result", success: false, error: { ... }
            console.error('Failed to fetch Meraki data:', message.error);
            setError(`Failed to fetch Meraki data: ${message.error?.message}`);
          }
          setLoading(false);
        } else if (message.type === 'result' && message.success === false) {
          console.error('Failed to fetch Meraki data:', message.error);
          setError(`Failed to fetch Meraki data: ${message.error?.message}`);
          setLoading(false);
        }
      }
    };

    socket.onerror = (err) => {
      console.error('WebSocket error:', err);
      // setError('WebSocket connection error. See console for details.');
      // Don't block UI on socket error if we can fallback or retry, but here we rely on it.
    };

    return () => {
      if (socket.readyState === 1) {
        socket.close();
      }
    };
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  const handleToggle = (networkId: string, enabled: boolean) => {
    console.log(`Toggled network ${networkId} to ${enabled}`);
  };

  return (
    <div className="p-4 relative">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Meraki HA Web UI</h1>
        <button
          onClick={() => setShowSettings(true)}
          className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
          title="Settings"
        >
          <ha-icon icon="mdi:cog"></ha-icon>
        </button>
      </div>

      {activeView.view === 'dashboard' ? (
        <NetworkView
          data={data}
          onToggle={handleToggle}
          setActiveView={setActiveView}
        />
      ) : (
        <DeviceView
          activeView={activeView}
          setActiveView={setActiveView}
          data={data}
        />
      )}

      {showSettings && data && (
        <Settings
          options={data.options || {}}
          configEntryId={(function () {
            const haConfigEntryId = (window as any).hass?.panel?.config
              ?.config_entry_id;
            console.log(
              'DEBUG (App.tsx): Settings configEntryId from hass.panel.config.config_entry_id:',
              haConfigEntryId
            );
            return haConfigEntryId || (data as any).config_entry_id;
          })()}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  );
};

export default App;
