import React from 'react';

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
    </div>
  );
};

export default DeviceView;
