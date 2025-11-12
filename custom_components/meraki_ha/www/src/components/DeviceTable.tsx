import React, { useState } from 'react';

interface DeviceTableProps {
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const DeviceTable: React.FC<DeviceTableProps> = ({ devices, setActiveView }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredDevices = devices.filter(device =>
    device.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    device.serial?.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
                className="border-b border-light-border dark:border-dark-border cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors duration-200"
                onClick={() => setActiveView({ view: 'device', deviceId: device.serial })}
              >
                <td className="p-4">{device.name || 'N/A'}</td>
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
