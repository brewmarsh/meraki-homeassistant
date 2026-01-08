import React, { useState, useEffect, useRef } from 'react';
// Frontend version: 2.2.0-beta.28
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';
import Settings from './components/Settings';
import TimedAccess from './components/TimedAccess';

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
  const [showTimedAccess, setShowTimedAccess] = useState(false);

  const configEntryId = panel?.config?.config_entry_id;

  useEffect(() => {
    if (window.location.hostname === 'localhost') {
      setData({
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
            ports_statuses: [
              { status: 'Connected' },
              { status: 'Connected' },
              { status: 'Disconnected' },
              { status: 'Disconnected' },
            ], // 2/4 in use
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
          {
            name: 'Server Room Sensor',
            model: 'MT10',
            serial: 'Q2MT-XXXX-XXXX',
            status: 'online',
            networkId: 'N_12345',
          },
          {
            name: 'Main Gateway',
            model: 'MX68',
            serial: 'Q2MX-XXXX-XXXX',
            status: 'online',
            networkId: 'N_12345',
            wan1Ip: '203.0.113.1',
            wan2Ip: '198.51.100.1',
          },
        ],
        ssids: [
          {
            number: 0,
            name: 'Main WiFi',
            enabled: true,
            networkId: 'N_12345',
            entity_id: 'switch.main_wifi',
          },
        ],
        vlans: {
          N_12345: [
            {
              id: '1',
              name: 'Management',
              subnet: '192.168.1.0/24',
              applianceIp: '192.168.1.1',
            },
            {
              id: '10',
              name: 'IoT',
              subnet: '192.168.10.0/24',
              applianceIp: '192.168.10.1',
            },
          ],
        },
        networks: [
          {
            id: 'N_12345',
            name: 'Main Office',
            is_enabled: true,
            ssids: [
              {
                number: 0,
                name: 'Main WiFi',
                enabled: true,
                networkId: 'N_12345',
                entity_id: 'switch.main_wifi',
              },
            ],
            productTypes: [
              'wireless',
              'switch',
              'camera',
              'sensor',
              'appliance',
            ],
          },
        ],
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

    fetchData();
  }, [configEntryId]); // Rerun if configEntryId changes

  const fetchData = async () => {
    if (!hass || !configEntryId) return;

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


  if (loading || !data) {
    return (
      <div className="flex justify-center items-center h-screen bg-light-background dark:bg-dark-background text-light-text dark:text-dark-text">
        Loading...
      </div>
    );
  }

  return (
    <div className="p-4 relative bg-light-background dark:bg-dark-background text-light-text dark:text-dark-text">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Cisco Meraki Integration</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setShowTimedAccess(true)}
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            title="Timed Guest Access"
          >
            <ha-icon icon="mdi:clock-outline"></ha-icon>
          </button>
          <button
            onClick={fetchData}
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            title="Refresh Data"
          >
            <ha-icon icon="mdi:refresh"></ha-icon>
          </button>
          <button
            onClick={() => setShowSettings(true)}
            className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
            title="Settings"
          >
            <ha-icon icon="mdi:cog"></ha-icon>
          </button>
        </div>
      </div>

      {activeView.view === 'dashboard' ? (
        <NetworkView
          hass={hass}
          data={data}
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
      {showTimedAccess && data && (
        <TimedAccess
          hass={hass}
          configEntryId={configEntryId}
          data={data}
          onClose={() => setShowTimedAccess(false)}
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
