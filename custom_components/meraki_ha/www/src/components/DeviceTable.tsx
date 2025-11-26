import React, { useState } from 'react';

interface DeviceTableProps {
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const DeviceTable: React.FC<DeviceTableProps> = ({
  devices,
  setActiveView,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const getDeviceIcon = (model: string) => {
    const m = model?.toUpperCase() || '';
    if (m.startsWith('MR')) return 'mdi:wifi';
    if (m.startsWith('MS')) return 'mdi:lan';
    if (m.startsWith('MV')) return 'mdi:cctv';
    if (m.startsWith('MX')) return 'mdi:shield-check';
    if (m.startsWith('MG')) return 'mdi:signal-cellular-outline';
    if (m.startsWith('MT')) return 'mdi:thermometer';
    if (m.startsWith('Z')) return 'mdi:router-wireless';
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
              <th className="text-left p-4 font-semibold">RTSP</th>
              <th className="text-center p-4 font-semibold w-16">Details</th>
            </tr>
          </thead>
          <tbody>
            {filteredDevices.map((device) => {
              const isCamera = device.model?.startsWith('MV');
              const rtspUrl =
                isCamera && device.lanIp
                  ? `rtsp://${device.lanIp}:9000/live`
                  : null;

              return (
                <tr
                  key={device.serial}
                  className="border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover cursor-pointer"
                  onClick={(e) => {
                    if (device.entity_id) {
                      handleDeviceClick(e, device.entity_id);
                    } else {
                      handleDetailsClick(e, device.serial);
                    }
                  }}
                >
                  <td className="p-4">
                    <div style={{ display: 'flex', alignItems: 'center' }}>
                      <ha-icon
                        icon={getDeviceIcon(device.model)}
                        style={{ marginRight: '8px' }}
                      ></ha-icon>
                      <span className="font-medium">{device.name || 'N/A'}</span>
                    </div>
                  </td>
                  <td className="p-4">{device.model || 'N/A'}</td>
                  <td className="p-4 capitalize">{device.status || 'N/A'}</td>
                  <td className="p-4">
                    {rtspUrl ? (
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
                    )}
                  </td>
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
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DeviceTable;
