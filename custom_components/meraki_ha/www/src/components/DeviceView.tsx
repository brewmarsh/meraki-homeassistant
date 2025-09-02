import React from 'react';

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const DeviceView: React.FC<DeviceViewProps> = ({ activeView, setActiveView, data }) => {
  const device = data.devices.find((d: any) => d.serial === activeView.deviceId);

  if (!device) {
    return <div>Device not found</div>;
  }

  return (
    <div>
      <button onClick={() => setActiveView({ view: 'dashboard' })} className="mb-4">
        &larr; Back to Dashboard
      </button>
      <h2 className="text-xl font-semibold mb-4">Device Details</h2>
      <p>Name: {device.name || device.mac}</p>
      <p>Status: {device.status}</p>
      <p>Model: {device.model}</p>
      <p>MAC Address: {device.mac}</p>
      <p>Serial: {device.serial}</p>
    </div>
  );
};

export default DeviceView;
