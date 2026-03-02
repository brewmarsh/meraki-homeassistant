import React, { useState, useEffect } from 'react';
// Frontend version: 2.3.0-beta.120
import NetworkView from './components/NetworkView';
import DeviceView from './components/DeviceView';
import Settings from './components/Settings';
import TimedAccess from './components/TimedAccess';
import { safeCallWS } from './utils/api';
import { WsCommand } from './types/websocket';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

// Update props to accept hass, panel, and config_entry_id
interface AppProps {
  hass: any;
  panel?: any;
  config_entry_id?: string;
}

const App: React.FC<AppProps> = ({ hass, panel, config_entry_id }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [configNotFound, setConfigNotFound] = useState<boolean>(false);
  const [activeView, setActiveView] = useState<{ view: string; deviceId?: string }>({
    view: 'dashboard',
    deviceId: undefined,
  });
  const [showSettings, setShowSettings] = useState(false);
  const [showTimedAccess, setShowTimedAccess] = useState(false);

  const configEntryId = config_entry_id || panel?.config?.config_entry_id;

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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [configEntryId]); // Rerun if configEntryId changes

  const fetchData = async () => {
    if (!hass || !configEntryId) return;

    try {
      setLoading(true);
      const result = await safeCallWS<MerakiData>(hass, {
        type: WsCommand.GET_CONFIG,
        config_entry_id: configEntryId,
      });
      setData(result);
      setError(null);
      setConfigNotFound(false);
    } catch (err: any) {
      console.error('Error fetching Meraki data:', err);
      if (err.code === 'not_found') {
        setConfigNotFound(true);
        setError('Meraki integration is not yet configured or config entry was not found.');
      } else {
        setError(err.message || 'An unknown error occurred.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (networkId: string, enabled: boolean) => {
    if (!data) return;

    const updatedNetworks = data.networks.map((network: any) =>
      network.id === networkId ? { ...network, is_enabled: enabled } : network
    );

    const updatedData = { ...data, networks: updatedNetworks };
    setData(updatedData);

    const enabledNetworkIds = updatedNetworks
      .filter((network: any) => network.is_enabled)
      .map((network: any) => network.id);

    try {
      await safeCallWS(hass, {
        type: WsCommand.UPDATE_ENABLED_NETWORKS,
        config_entry_id: configEntryId,
        enabled_networks: enabledNetworkIds,
      });
    } catch (err: any) {
      console.error('Error updating enabled networks:', err);
      setError(
        err.message || 'An unknown error occurred while updating networks.'
      );
      // Revert UI if API call fails
      setData(data);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen bg-light-background dark:bg-dark-background text-[var(--primary-text-color)]">
        Loading...
      </div>
    );
  }

  if (configNotFound) {
    return (
      <div className="flex flex-col justify-center items-center h-screen bg-light-background dark:bg-dark-background text-[var(--primary-text-color)] p-4 text-center">
        <ha-icon icon="mdi:alert-circle-outline" style={{'--mdc-icon-size': '64px', color: 'var(--error-color)'} as any} className="mb-4"></ha-icon>
        <h2 className="text-xl font-bold mb-2">Integration Not Configured</h2>
        <p className="mb-6 max-w-md text-[var(--secondary-text-color)]">
          The Meraki integration has not been configured yet, or the configuration entry could not be found.
          Please ensure the integration is added and configured in Home Assistant.
        </p>
        <a
          href="/config/integrations"
          className="bg-[var(--primary-color)] text-[var(--text-primary-color, white)] px-6 py-2 rounded-lg hover:opacity-90 transition-colors"
        >
          Go to Integrations
        </a>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="flex flex-col justify-center items-center h-screen bg-light-background dark:bg-dark-background text-[var(--primary-text-color)] p-4 text-center">
        <ha-icon icon="mdi:error-outline" style={{'--mdc-icon-size': '64px', color: 'var(--error-color)'} as any} className="mb-4"></ha-icon>
        <h2 className="text-xl font-bold mb-2">Error</h2>
        <p className="mb-6 text-[var(--secondary-text-color)]">{error}</p>
        <button
          onClick={fetchData}
          className="bg-[var(--primary-color)] text-[var(--text-primary-color, white)] px-6 py-2 rounded-lg hover:opacity-90 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="flex justify-center items-center h-screen bg-light-background dark:bg-dark-background text-[var(--primary-text-color)]">
        No data found.
      </div>
    );
  }

  return (
    <div className="p-4 relative bg-light-background dark:bg-dark-background text-[var(--primary-text-color)]">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Cisco Meraki Integration</h1>
        <div className="flex gap-2">
          <button
            onClick={() => setShowTimedAccess(true)}
            className="p-2 rounded-full hover:bg-light-hover dark:hover:bg-dark-hover text-[var(--secondary-text-color)]"
            title="Timed Guest Access"
          >
            <ha-icon icon="mdi:clock-outline"></ha-icon>
          </button>
          <button
            onClick={fetchData}
            className="p-2 rounded-full hover:bg-light-hover dark:hover:bg-dark-hover text-[var(--secondary-text-color)]"
            title="Refresh Data"
          >
            <ha-icon icon="mdi:refresh"></ha-icon>
          </button>
          <button
            onClick={() => setShowSettings(true)}
            className="p-2 rounded-full hover:bg-light-hover dark:hover:bg-dark-hover text-[var(--secondary-text-color)]"
            title="Settings"
          >
            <ha-icon icon="mdi:cog"></ha-icon>
          </button>
        </div>
      </div>

      {activeView.view === 'dashboard' ? (
        <NetworkView
          hass={hass}
          data={data as any}
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
      {showTimedAccess && data && (
        <TimedAccess
          hass={hass}
          configEntryId={configEntryId}
          data={data}
          onClose={() => setShowTimedAccess(false)}
        />
      )}
      {data?.version && (
        <div className="absolute bottom-0 right-0 p-2 text-xs text-[var(--secondary-text-color)]">
          Version: {data.version}
        </div>
      )}
    </div>
  );
};

export default App;
