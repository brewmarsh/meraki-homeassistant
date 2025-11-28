import React, { useState, useEffect } from 'react';
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';
import Settings from './components/Settings';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

// Update props to accept hass and panel
interface AppProps {
  hass: any;
  panel: any;
}

const App: React.FC<AppProps> = ({ hass, panel }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState({
    view: 'dashboard',
    deviceId: undefined,
  });
  const [showSettings, setShowSettings] = useState(false);

  const configEntryId = panel?.config?.config_entry_id;

  useEffect(() => {
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

    if (!hass || !configEntryId) {
      setError('Hass or Config Entry ID not available.');
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        setLoading(true);
        const result: MerakiData = await hass.callWS({
          type: 'meraki_ha/get_config',
          config_entry_id: configEntryId,
        });
        setData(result);
        setError(null);
      } catch (err: any) {
        console.error('Error fetching Meraki data:', err);
        setError(err.message || 'An unknown error occurred.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Optional: Subscribe to updates if the backend supports it
    // const unsubscribe = hass.connection.subscribeMessage(
    //   (message) => {
    //     console.log('Received update:', message);
    //     // Update state based on the message
    //   },
    //   {
    //     type: 'meraki_ha/subscribe_updates',
    //     config_entry_id: configEntryId,
    //   }
    // );

    // return () => unsubscribe();
  }, [configEntryId]); // Rerun if configEntryId changes

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  const handleToggle = (networkId: string, enabled: boolean) => {
    // This functionality is not fully implemented in this refactor
    console.log(`Toggled network ${networkId} to ${enabled}`);
  };

  return (
    <div className="p-4 relative bg-light-background dark:bg-dark-background text-light-text dark:text-dark-text">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Cisco Meraki Integration</h1>
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
          hass={hass}
          data={data}
          onToggle={handleToggle}
          setActiveView={setActiveView}
          configEntryId={configEntryId}
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
          hass={hass} // Pass hass to settings
          options={data.options || {}}
          configEntryId={configEntryId}
          onClose={() => setShowSettings(false)}
        />
      )}
      {data?.version && (
        <div className="absolute bottom-0 right-0 p-2 text-xs text-gray-500">
          Version: {data.version}
        </div>
      )}
    </div>
  );
};

export default App;
