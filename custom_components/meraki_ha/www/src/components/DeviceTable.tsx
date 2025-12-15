import React, { useState } from 'react';

interface DeviceTableProps {
  hass: any;
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  deviceType?: string; // 'wireless', 'switch', 'camera', 'sensor', 'appliance', 'other'
}

const DeviceTable: React.FC<DeviceTableProps> = ({
  hass,
  devices,
  setActiveView,
  deviceType = 'other',
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const getDeviceIcon = (model: string) => {
    const m = model?.toUpperCase() || '';
    if (m.startsWith('MR')) return 'mdi:wifi';
    if (m.startsWith('MS')) return 'mdi:lan';
    if (m.startsWith('MV')) return 'mdi:cctv';
    if (m.startsWith('MX')) return 'mdi:shield-check';
    if (m.startsWith('MG')) return 'mdi:signal-cellular-outline';

    // MT Series Specifics
    if (m.startsWith('MT40')) return 'mdi:power-plug';
    if (m.startsWith('MT12')) return 'mdi:water';
    if (m.startsWith('MT20')) return 'mdi:door';
    if (m.startsWith('MT30')) return 'mdi:gesture-tap-button';
    if (m.startsWith('MT')) return 'mdi:thermometer';

    if (m.startsWith('Z')) return 'mdi:router-wireless';
    if (m.startsWith('GS')) return 'mdi:lan';
    if (m.startsWith('GR')) return 'mdi:wifi';
    if (m.startsWith('GX')) return 'mdi:shield-check';
    return 'mdi:help-circle';
  };

  const filteredDevices = devices.filter(
    (device) =>
      device.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      device.serial?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeviceClick = (e: React.MouseEvent, entityId: string) => {
    e.preventDefault();
    e.stopPropagation();
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    e.currentTarget.dispatchEvent(event);
  };

  const handleDetailsClick = (e: React.MouseEvent, serial: string) => {
    e.preventDefault();
    e.stopPropagation();
    setActiveView({ view: 'device', deviceId: serial });
  };

  const capitalizeFirst = (s: string) => {
    if (!s) return '';
    return s.charAt(0).toUpperCase() + s.slice(1);
  };

  const getSensorHeroMetric = (device: any) => {
    // If device is not online, fallback to device.status (which is handled in renderStatus)
    if (device.status !== 'online') return null;

    const model = device.model || '';
    const readings = device.readings || [];

    // MT40: Power status (on / off)
    if (model.startsWith('MT40')) {
      const switchEntity = device.entities?.find((e: any) =>
        e.entity_id.startsWith('switch.')
      );
      if (switchEntity) {
        return switchEntity.state === 'on' ? 'On' : 'Off';
      }
      return 'Online';
    }

    // MT10, MT11: Temperature
    if (model.startsWith('MT10') || model.startsWith('MT11')) {
      const r = readings.find((r: any) => r.metric === 'temperature');
      if (r?.temperature?.celsius !== undefined) {
        return `${r.temperature.celsius.toFixed(1)} °C`;
      }
    }

    // MT12: Status (wet / dry)
    if (model.startsWith('MT12')) {
      const r = readings.find((r: any) => r.metric === 'water');
      if (r?.water?.present !== undefined) {
        return r.water.present ? 'Wet' : 'Dry';
      }
    }

    // MT14, MT15: TVOC
    if (model.startsWith('MT14') || model.startsWith('MT15')) {
      const r = readings.find((r: any) => r.metric === 'tvoc');
      if (r?.tvoc?.concentration !== undefined) {
        return `${r.tvoc.concentration} μg/m³`;
      }
    }

    // MT20: Door status (open / closed)
    if (model.startsWith('MT20')) {
      const r = readings.find((r: any) => r.metric === 'door');
      if (r?.door?.open !== undefined) {
        return r.door.open ? 'Open' : 'Closed';
      }
    }

    return null;
  };

  const renderStatus = (device: any) => {
    // Prioritize API status for Cameras
    if (deviceType === 'camera') {
      return device.status ? capitalizeFirst(device.status) : 'N/A';
    }

    // MT Sensors Logic
    if (device.model?.startsWith('MT')) {
      const status = device.status || 'N/A';
      if (status !== 'online') {
        return capitalizeFirst(status);
      }
      // Device is online
      const hero = getSensorHeroMetric(device);
      if (hero) return hero;

      return 'Online';
    }

    // Default logic: Prioritize HA entity state
    const haState = device.entity_id && hass?.states?.[device.entity_id];
    if (
      haState &&
      haState.state !== 'unavailable' &&
      haState.state !== 'unknown'
    ) {
      return capitalizeFirst(haState.state);
    }
    const status = device.status || 'N/A';
    return capitalizeFirst(status);
  };

  const renderExtraColumnHeader = () => {
    if (deviceType === 'switch') return 'Ports';
    if (deviceType === 'appliance') return 'External IP';
    if (deviceType === 'camera') return 'RTSP';
    return null;
  };

  const renderExtraColumnCell = (device: any) => {
    if (deviceType === 'switch') {
      // Calculate ports in use
      if (device.ports_statuses && Array.isArray(device.ports_statuses)) {
        const total = device.ports_statuses.length;
        const inUse = device.ports_statuses.filter(
          (p: any) => p.status === 'Connected'
        ).length;
        return `${inUse} / ${total}`;
      }
      return '-';
    }
    if (deviceType === 'appliance') {
      const wan1 = device.wan1Ip;
      const wan2 = device.wan2Ip;
      if (wan1 && wan2) return `${wan1}, ${wan2}`;
      return wan1 || wan2 || '-';
    }
    if (deviceType === 'camera') {
      const rtspUrl = device.lanIp
        ? `rtsp://${device.lanIp}:9000/live`
        : null;
      return rtspUrl ? (
        <a
          href={rtspUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-500 hover:text-blue-700 underline"
          onClick={(e) => e.stopPropagation()}
        >
          Stream Link
        </a>
      ) : (
        <span className="text-gray-400">-</span>
      );
    }
    return null;
  };

  const hasExtraColumn = ['switch', 'appliance', 'camera'].includes(deviceType);

  return (
    <div className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md">
      <input
        type="text"
        placeholder="Search by name or serial..."
        className="w-full p-2 mb-4 border rounded-lg bg-light-background dark:bg-dark-background dark:border-gray-600"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-light-border dark:border-dark-border">
              <th className="text-left p-4 font-semibold">Name</th>
              <th className="text-left p-4 font-semibold">Model</th>
              <th className="text-left p-4 font-semibold">Status</th>
              {hasExtraColumn && (
                <th className="text-left p-4 font-semibold">
                  {renderExtraColumnHeader()}
                </th>
              )}
              <th className="text-center p-4 font-semibold w-16">Details</th>
            </tr>
          </thead>
          <tbody>
            {filteredDevices.map((device) => (
              <tr
                key={device.serial}
                className="border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover cursor-pointer"
                onClick={(e) => handleDetailsClick(e, device.serial)}
              >
                <td className="p-4">
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <ha-icon
                      icon={getDeviceIcon(device.model)}
                      style={{ marginRight: '8px' }}
                    ></ha-icon>
                    <span
                      className="font-medium text-blue-500 hover:underline"
                      onClick={(e) => {
                        if (device.entity_id) {
                          handleDeviceClick(e, device.entity_id);
                        }
                      }}
                    >
                      {device.name || 'N/A'}
                    </span>
                  </div>
                </td>
                <td className="p-4">{device.model || 'N/A'}</td>
                <td className="p-4">{renderStatus(device)}</td>
                {hasExtraColumn && (
                  <td className="p-4">{renderExtraColumnCell(device)}</td>
                )}
                <td className="p-4 text-center">
                  <button
                    onClick={(e) => handleDetailsClick(e, device.serial)}
                    className="p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 transition-colors"
                    title="View Details"
                  >
                    <ha-icon icon="mdi:information-outline"></ha-icon>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DeviceTable;
