import React, { useState, useEffect } from 'react';

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
  hass: any;
  config_entry_id: string;
}

const getDeviceType = (model: string): string => {
  if (model.startsWith('MS')) return 'Switches';
  if (model.startsWith('MV')) return 'Cameras';
  if (model.startsWith('MX')) return 'Routers';
  if (model.startsWith('MR')) return 'Access Points';
  return 'Other';
};

const HeroIndicator: React.FC<{
  deviceType: string;
  devices: Device[];
  hass: any;
  config_entry_id: string;
}> = ({ deviceType, devices, hass, config_entry_id }) => {
  const [snapshotUrl, setSnapshotUrl] = useState<string | null>(null);

  useEffect(() => {
    if (deviceType === 'Cameras' && devices.length > 0) {
      const fetchSnapshot = async () => {
        try {
          const result = await hass.connection.sendMessagePromise({
            type: 'meraki_ha/get_camera_snapshot',
            config_entry_id: config_entry_id,
            serial: devices[0].serial,
          });
          setSnapshotUrl(result.url);
        } catch (err) {
          console.error('Error fetching camera snapshot:', err);
        }
      };
      fetchSnapshot();
    }
  }, [deviceType, devices, hass, config_entry_id]);

  const heroStyle: React.CSSProperties = {
    padding: '12px',
    marginBottom: '12px',
    borderRadius: 'var(--ha-card-border-radius, 4px)',
    backgroundColor: 'var(--secondary-background-color)',
    textAlign: 'center',
  };

  switch (deviceType) {
    case 'Cameras':
      return (
        <div style={heroStyle}>
          {snapshotUrl ? <img src={snapshotUrl} style={{ maxWidth: '100%' }} /> : 'Loading camera preview...'}
        </div>
      );
    case 'Switches':
      const onlineSwitches = devices.filter((d) => d.status === 'online').length;
      return (
        <div style={heroStyle}>
          <strong>
            {onlineSwitches} / {devices.length}
          </strong>{' '}
          Switches Online
        </div>
      );
    case 'Routers':
      const isRouterOnline = devices.some((d) => d.status === 'online');
      return <div style={heroStyle}>Gateway Status: <strong>{isRouterOnline ? 'Online' : 'Offline'}</strong></div>;
    case 'Access Points':
      const onlineAPs = devices.filter((d) => d.status === 'online').length;
      return (
        <div style={heroStyle}>
          <strong>
            {onlineAPs} / {devices.length}
          </strong>{' '}
          Access Points Online
        </div>
      );
    default:
      return null;
  }
};

const DeviceView: React.FC<DeviceViewProps> = ({ devices, hass, config_entry_id }) => {
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
          <h4 style={{ marginTop: 0, marginBottom: '8px', borderBottom: '1px solid var(--divider-color)' }}>{type}</h4>
          <HeroIndicator deviceType={type} devices={deviceList} hass={hass} config_entry_id={config_entry_id} />
          {deviceList.map((device) => (
            <div key={device.serial} className="device-item" style={{ marginBottom: '8px' }}>
              <p style={{ margin: 0 }}>
                <strong>{device.name || 'Unnamed Device'}</strong>
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
