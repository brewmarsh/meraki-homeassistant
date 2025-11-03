import React from 'react';

interface Device {
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
}

interface DeviceViewProps {
  devices: Device[];
}

const DeviceView: React.FC<DeviceViewProps> = ({ devices }) => {
  if (!devices || devices.length === 0) {
    return <p>No devices found in this network.</p>;
  }

  return (
    <div className="device-list">
      <h4>Devices</h4>
      {devices.map((device) => (
        <div key={device.serial} className="device-item">
          <p>
            <strong>{device.name || 'Unnamed Device'}</strong>
          </p>
          <p>
            Model: {device.model} | Status: {device.status}
          </p>
          <p>
            {device.lanIp && `IP: ${device.lanIp} | `}
            {device.mac && `MAC: ${device.mac}`}
          </p>
        </div>
      ))}
    </div>
  );
};

export default DeviceView;
