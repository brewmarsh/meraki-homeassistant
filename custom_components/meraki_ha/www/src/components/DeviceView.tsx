import React from 'react';

<<<<<<< HEAD
interface Device {
  entity_id: string;
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

const getDeviceType = (model: string): string => {
  if (model.startsWith('GS')) return 'Switches';
  if (model.startsWith('GR')) return 'Access Points';
  if (model.startsWith('MT')) return 'Sensors';
  if (model.startsWith('MS')) return 'Switches';
  if (model.startsWith('MV')) return 'Cameras';
  if (model.startsWith('MX')) return 'Routers';
  if (model.startsWith('MR')) return 'Access Points';
  return 'Other';
};

const HeroIndicator: React.FC<{
  deviceType: string;
  devices: Device[];
}> = ({ deviceType, devices }) => {
  const heroStyle: React.CSSProperties = {
    padding: '12px',
    marginBottom: '12px',
    borderRadius: 'var(--ha-card-border-radius, 4px)',
    backgroundColor: 'var(--secondary-background-color)',
    textAlign: 'center',
  };

  const onlineCount = devices.filter((d) => d.status === 'online').length;

  switch (deviceType) {
    case 'Cameras':
    case 'Switches':
    case 'Access Points':
    case 'Sensors':
      return (
        <div style={heroStyle}>
          <strong>
            {onlineCount} / {devices.length}
          </strong>{' '}
          {deviceType} Online
        </div>
      );
    case 'Routers':
      const isRouterOnline = devices.some((d) => d.status === 'online');
      return <div style={heroStyle}>Gateway Status: <strong>{isRouterOnline ? 'Online' : 'Offline'}</strong></div>;
    default:
      return null;
  }
};

const DeviceView: React.FC<DeviceViewProps> = ({ devices }) => {
  if (!devices || devices.length === 0) {
    return <p>No devices found in this network.</p>;
  }

  const groupedDevices = devices.reduce((acc, device) => {
    const deviceType = getDeviceType(device.model);
    if (!acc[deviceType]) {
      acc[deviceType] = [];
    }
    acc[deviceType].push(device);
    return acc;
  }, {} as Record<string, Device[]>);

  return (
    <div className="device-list" style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      {Object.entries(groupedDevices).map(([type, deviceList]) => (
        <div key={type} className="device-group">
          <HeroIndicator deviceType={type} devices={deviceList} />
          {deviceList.map((device) => (
            <div key={device.serial} className="device-item" style={{ marginBottom: '8px' }}>
              <p style={{ margin: 0 }}>
                <strong
                  onClick={() =>
                    device.entity_id &&
                    window.dispatchEvent(
                      new CustomEvent('hass-more-info', {
                        bubbles: true,
                        composed: true,
                        detail: { entityId: device.entity_id },
                      }),
                    )
                  }
                  style={{
                    cursor: device.entity_id ? 'pointer' : 'default',
                    color: device.entity_id ? 'var(--primary-color)' : undefined,
                  }}
                  title={device.entity_id || ''}
                >
                  {device.name || 'Unnamed Device'}
                </strong>
              </p>
              <p style={{ margin: 0, fontSize: 'var(--secondary-text-size)' }}>
                Model: {device.model} | Status: {device.status}
              </p>
              <p style={{ margin: 0, fontSize: 'var(--secondary-text-size)' }}>
                {device.lanIp && `IP: ${device.lanIp} | `}
                {device.mac && `MAC: ${device.mac}`}
              </p>
            </div>
          ))}
        </div>
      ))}
=======
interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
}) => {
  const device = data.devices.find(
    (d: any) => d.serial === activeView.deviceId
  );

  if (!device) {
    return (
      <div>
        <button
          onClick={() => setActiveView({ view: 'dashboard' })}
          className="text-blue-500 mb-4"
        >
          &larr; Back to Dashboard
        </button>
        <p>Device not found.</p>
      </div>
    );
  }

  const {
    name,
    model,
    serial,
    firmware,
    status,
    status_messages = [],
    entities = [],
  } = device;

  return (
    <div>
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="text-blue-500 mb-4 hover:underline"
      >
        &larr; Back to Dashboard
      </button>

      <div className="bg-light-card dark:bg-dark-card p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-bold mb-2">{name}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <strong>Model:</strong> {model}
          </div>
          <div>
            <strong>Serial:</strong> {serial}
          </div>
          <div>
            <strong>Firmware:</strong> {firmware}
          </div>
          <div>
            <strong>Status:</strong>{' '}
            <span className="capitalize">{status}</span>
          </div>
        </div>
      </div>

      {status_messages.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-2">Status Messages</h3>
          <div className="bg-yellow-100 dark:bg-yellow-900 border-l-4 border-yellow-500 text-yellow-700 dark:text-yellow-200 p-4 rounded-lg">
            <ul>
              {status_messages.map((msg: string, index: number) => (
                <li key={index} className="mb-1">
                  {msg}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div>
        <h3 className="text-xl font-semibold mb-4">Entities</h3>
        <div className="overflow-x-auto bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-light-border dark:border-dark-border">
                <th className="text-left p-4 font-semibold">Name</th>
                <th className="text-left p-4 font-semibold">Entity ID</th>
                <th className="text-left p-4 font-semibold">State</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity: any) => (
                <tr
                  key={entity.entity_id}
                  className="border-b border-light-border dark:border-dark-border last:border-b-0"
                >
                  <td className="p-4">{entity.name}</td>
                  <td className="p-4">{entity.entity_id}</td>
                  <td className="p-4">{entity.state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
    </div>
  );
};

export default DeviceView;
