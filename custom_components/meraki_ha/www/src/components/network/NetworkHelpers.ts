import { Device, Network, DeviceGroup } from '../../types/meraki';
import { HomeAssistant } from '../../types/ha';

export const isDeviceOnline = (
  device: Device,
  hass: HomeAssistant
): boolean => {
  if (device.model?.toUpperCase().startsWith('MV')) {
    return device.status === 'online';
  }

  const haState = device.entity_id && hass?.states?.[device.entity_id];
  let status = device.status;
  if (
    haState &&
    haState.state !== 'unavailable' &&
    haState.state !== 'unknown'
  ) {
    status = haState.state;
  }
  return ['online', 'active', 'home', 'on'].includes(status?.toLowerCase());
};

export const filterByPrefix = (
  devices: Device[],
  prefixes: string[]
): Device[] => {
  return devices.filter((d) =>
    prefixes.some((p) => d.model?.toUpperCase().startsWith(p))
  );
};

export const groupNetworkDevices = (
  networks: Network[],
  devices: Device[]
): Record<string, DeviceGroup[]> => {
  if (!networks || !devices) return {};
  const result: Record<string, DeviceGroup[]> = {};

  networks.forEach((network) => {
    const networkDevices = devices.filter((d) => d.networkId === network.id);

    result[network.id] = [
      {
        label: 'Appliances',
        devices: filterByPrefix(networkDevices, ['MX', 'Z', 'MG', 'GX']),
        icon: 'mdi:shield-check',
        type: 'appliance',
      },
      {
        label: 'Switches',
        devices: filterByPrefix(networkDevices, ['MS', 'GS']),
        icon: 'mdi:lan',
        type: 'switch',
      },
      {
        label: 'Cameras',
        devices: filterByPrefix(networkDevices, ['MV']),
        icon: 'mdi:cctv',
        type: 'camera',
      },
      {
        label: 'Sensors',
        devices: filterByPrefix(networkDevices, ['MT']),
        icon: 'mdi:thermometer',
        type: 'sensor',
      },
      {
        label: 'Wireless APs',
        devices: filterByPrefix(networkDevices, ['MR', 'GR']),
        icon: 'mdi:wifi',
        type: 'wireless',
      },
      {
        label: 'Other Devices',
        devices: networkDevices.filter(
          (d) =>
            !['MR', 'GR', 'MS', 'GS', 'MV', 'MT', 'MX', 'Z', 'MG', 'GX'].some(
              (p) => d.model?.toUpperCase().startsWith(p)
            )
        ),
        icon: 'mdi:devices',
        type: 'other',
      },
    ];
  });
  return result;
};
