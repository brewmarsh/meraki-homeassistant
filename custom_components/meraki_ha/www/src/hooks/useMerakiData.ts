import { useState, useEffect, useCallback } from 'react';
import { MerakiData, MerakiNetwork } from '../types/data';
import { safeCallWS } from '../utils/api';
import { WsCommand } from '../types/websocket';

export const useMerakiData = (hass: any, configEntryId?: string) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [configNotFound, setConfigNotFound] = useState<boolean>(false);

  const fetchData = useCallback(async () => {
    if (window.location.hostname === 'localhost') {
      setData({
        devices: [
          { name: 'Living Room AP', model: 'MR33', serial: 'Q2JD-XXXX-XXXX', status: 'online', entity_id: 'switch.living_room_ap', networkId: 'N_12345' },
          { name: 'Office Switch', model: 'MS220-8P', serial: 'Q2HD-XXXX-XXXX', status: 'online', entity_id: 'switch.office_switch', networkId: 'N_12345', ports_statuses: [{ status: 'Connected' }, { status: 'Connected' }, { status: 'Disconnected' }, { status: 'Disconnected' }] },
          { name: 'Front Door Camera', model: 'MV12', serial: 'Q2FD-XXXX-XXXX', status: 'online', lanIp: '192.168.1.100', entity_id: 'camera.front_door_camera', networkId: 'N_12345' },
          { name: 'Server Room Sensor', model: 'MT10', serial: 'Q2MT-XXXX-XXXX', status: 'online', networkId: 'N_12345' },
          { name: 'Main Gateway', model: 'MX68', serial: 'Q2MX-XXXX-XXXX', status: 'online', networkId: 'N_12345', wan1Ip: '203.0.113.1', wan2Ip: '198.51.100.1' },
        ],
        ssids: [{ number: 0, name: 'Main WiFi', enabled: true, networkId: 'N_12345', entity_id: 'switch.main_wifi' }],
        vlans: {
          N_12345: [
            { id: '1', name: 'Management', subnet: '192.168.1.0/24', applianceIp: '192.168.1.1' },
            { id: '10', name: 'IoT', subnet: '192.168.10.0/24', applianceIp: '192.168.10.1' },
          ],
        },
        networks: [
          {
            id: 'N_12345',
            name: 'Main Office',
            is_enabled: true,
            ssids: [{ number: 0, name: 'Main WiFi', enabled: true, networkId: 'N_12345', entity_id: 'switch.main_wifi' }],
            productTypes: ['wireless', 'switch', 'camera', 'sensor', 'appliance'],
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
        version: "2.3.0-beta.120"
      });
      setLoading(false);
      return;
    }

    if (!hass || !configEntryId) {
      setError('Hass or Config Entry ID not available.');
      setLoading(false);
      return;
    }

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
  }, [hass, configEntryId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleToggleNetwork = async (networkId: string, enabled: boolean) => {
    if (!data || !data.networks) return;
    const updatedNetworks = data.networks.map((network: MerakiNetwork) =>
      network.id === networkId ? { ...network, is_enabled: enabled } : network
    );
    const updatedData = { ...data, networks: updatedNetworks };
    setData(updatedData);

    const enabledNetworkIds = updatedNetworks
      .filter((network: MerakiNetwork) => network.is_enabled)
      .map((network: MerakiNetwork) => network.id);

    try {
      await safeCallWS(hass, {
        type: WsCommand.UPDATE_ENABLED_NETWORKS,
        config_entry_id: configEntryId,
        enabled_networks: enabledNetworkIds,
      });
    } catch (err: any) {
      console.error('Error updating enabled networks:', err);
      setError(err.message || 'An unknown error occurred while updating networks.');
      setData(data); // Revert to old data on error
    }
  };

  return { data, loading, error, configNotFound, fetchData, handleToggleNetwork };
};
