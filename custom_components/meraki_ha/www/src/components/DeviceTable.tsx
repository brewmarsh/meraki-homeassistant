import React, { useState } from 'react';

interface DeviceTableProps {
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const DeviceTable: React.FC<DeviceTableProps> = ({ devices, setActiveView }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const getDeviceIcon = (model: string) => {
    if (model?.startsWith('MR')) return 'mdi:access-point';
    if (model?.startsWith('MS')) return 'mdi:lan';
    if (model?.startsWith('MV')) return 'mdi:cctv';
    return 'mdi:help-circle';
  };

  const filteredDevices = devices.filter(device =>
    device.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.serial?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeviceClick = (e: React.MouseEvent<HTMLAnchorElement>, entityId: string) => {
    e.preventDefault();
    e.stopPropagation(); // Prevent the row's onClick from firing
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    e.currentTarget.dispatchEvent(event);
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
            </tr>
          </thead>
          <tbody>
            {filteredDevices.map(device => (
              <tr
                key={device.serial}
                className="border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover cursor-pointer"
                onClick={() => setActiveView({ view: 'device', deviceId: device.serial })}
              >
                <td className="p-4">
                  <div style={{ display: 'flex', alignItems: 'center' }}>
                    <ha-icon icon={getDeviceIcon(device.model)} style={{ marginRight: '8px' }}></ha-icon>
                    <a
                      href="#"
                      onClick={(e) => {
                        if (device.entity_id) {
                          handleDeviceClick(e, device.entity_id);
                        }
                      }}
                      className="text-blue-500 hover:underline"
                    >
                      {device.name || 'N/A'}
                    </a>
                  </div>
                </td>
                <td className="p-4">{device.model || 'N/A'}</td>
                <td className="p-4 capitalize">{device.status || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DeviceTable;
