import React from 'react';

export interface MerakiPortStatus {
  status: string;
}

export interface MerakiSensorReading {
  metric: string;
  temperature?: { celsius: number };
  humidity?: { relativePercentage: number };
  water?: { present: boolean };
  door?: { open: boolean };
  tvoc?: { concentration: number };
  pm25?: { concentration: number };
}

export interface MerakiDevice {
  name?: string;
  model: string;
  serial: string;
  status: string;
  mac?: string;
  lanIp?: string;
  networkId?: string;
  wan1Ip?: string;
  wan2Ip?: string;
  tags?: string[];
  ports_statuses?: MerakiPortStatus[];
  readings?: MerakiSensorReading[];
}

export interface DeviceViewData {
  devices?: MerakiDevice[];
}

export interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: DeviceViewData;
}

const ICON_PREFIXES = [
  { prefix: 'MT40', icon: 'mdi:power-plug' },
  { prefix: 'MT12', icon: 'mdi:water' },
  { prefix: 'MT20', icon: 'mdi:door' },
  { prefix: 'MT30', icon: 'mdi:gesture-tap-button' },
  { prefix: 'MT', icon: 'mdi:thermometer' },
  { prefix: 'MR', icon: 'mdi:wifi' },
  { prefix: 'MS', icon: 'mdi:lan' },
  { prefix: 'MV', icon: 'mdi:cctv' },
  { prefix: 'MX', icon: 'mdi:shield-check' },
  { prefix: 'MG', icon: 'mdi:signal-cellular-outline' },
  { prefix: 'Z', icon: 'mdi:router-wireless' },
  { prefix: 'GS', icon: 'mdi:lan' },
  { prefix: 'GR', icon: 'mdi:wifi' },
  { prefix: 'GX', icon: 'mdi:shield-check' },
];

const getDeviceIcon = (model: string | undefined): string => {
  const m = model?.toUpperCase() || '';
  const match = ICON_PREFIXES.find((item) => m.startsWith(item.prefix));
  return match?.icon || 'mdi:help-circle';
};

const getStatusColor = (status: string | undefined): string => {
  const s = status?.toLowerCase() || '';
  if (['online', 'active', 'home'].includes(s)) return 'var(--success-color)';
  if (s === 'alerting') return 'var(--warning-color)';
  return 'var(--error-color)';
};

const DeviceNotFound: React.FC<{ deviceId?: string; onBack: () => void }> = ({ deviceId, onBack }) => (
  <div className="p-4">
    <button
      onClick={onBack}
      className="flex items-center text-[var(--primary-color)] hover:underline mb-4"
    >
      <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
      Back to dashboard
    </button>
    <ha-card className="p-6 text-center text-[var(--primary-text-color)]">
      <ha-icon icon="mdi:alert-circle-outline" style={{ '--mdc-icon-size': '48px', color: 'var(--error-color)' } as any}></ha-icon>
      <p className="mt-2 text-lg font-semibold">Device not found</p>
      <p className="text-[var(--secondary-text-color)]">The device with serial {deviceId} could not be located.</p>
    </ha-card>
  </div>
);

const DeviceHeader: React.FC<{ device: MerakiDevice }> = ({ device }) => (
  <div className="flex flex-col md:flex-row md:items-center gap-4 mb-8">
    <div
      className="p-4 rounded-full w-fit flex items-center justify-center"
      style={{ backgroundColor: 'var(--secondary-background-color)', color: 'var(--primary-color)' }}
    >
      <ha-icon icon={getDeviceIcon(device.model)} style={{ '--mdc-icon-size': '40px' } as any}></ha-icon>
    </div>
    <div className="flex-grow">
      <h2 className="text-3xl font-bold">{device.name || 'Unnamed device'}</h2>
      <p className="text-[var(--secondary-text-color)] text-lg">
        {device.model} <span className="mx-2">•</span> {device.serial}
      </p>
    </div>
    <div
      className="px-4 py-2 rounded-full text-sm font-bold uppercase tracking-wider"
      style={{ border: `1px solid ${getStatusColor(device.status)}`, color: getStatusColor(device.status) }}
    >
      {device.status || 'Unknown'}
    </div>
  </div>
);

const TechnicalDetails: React.FC<{ device: MerakiDevice }> = ({ device }) => (
  <div className="space-y-2">
    <h3 className="text-xl font-semibold border-b border-[var(--divider-color)] pb-2 mb-4">Technical details</h3>

    <ha-settings-row>
      <span slot="heading">MAC address</span>
      <span className="font-mono bg-[var(--secondary-background-color)] px-2 py-1 rounded text-sm">{device.mac || 'N/A'}</span>
    </ha-settings-row>

    <ha-settings-row>
      <span slot="heading">LAN IP</span>
      <span className="font-semibold">{device.lanIp || 'N/A'}</span>
    </ha-settings-row>

    <ha-settings-row>
      <span slot="heading">Network ID</span>
      <span className="text-sm truncate max-w-[200px]" title={device.networkId}>{device.networkId || 'N/A'}</span>
    </ha-settings-row>

    {device.wan1Ip && (
      <ha-settings-row>
        <span slot="heading">WAN 1 IP</span>
        <span className="font-semibold">{device.wan1Ip}</span>
      </ha-settings-row>
    )}
    {device.wan2Ip && (
      <ha-settings-row>
        <span slot="heading">WAN 2 IP</span>
        <span className="font-semibold">{device.wan2Ip}</span>
      </ha-settings-row>
    )}
    {device.tags && device.tags.length > 0 && (
      <ha-settings-row>
        <span slot="heading">Tags</span>
        <div className="flex flex-wrap gap-1 justify-end max-w-[200px]">
          {device.tags.map((tag: string) => (
            <span key={tag} className="bg-[var(--secondary-background-color)] text-xs px-2 py-1 rounded">{tag}</span>
          ))}
        </div>
      </ha-settings-row>
    )}
  </div>
);

const PortStatusGrid: React.FC<{ ports?: MerakiPortStatus[] }> = ({ ports }) => {
  if (!ports) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-[var(--secondary-text-color)] opacity-50 italic">
        <ha-icon icon="mdi:information-outline" style={{ '--mdc-icon-size': '48px' } as any} className="mb-2"></ha-icon>
        <p>No port data available for this device type.</p>
      </div>
    );
  }

  const connectedCount = ports.filter((p) => p.status === 'Connected').length;
  const disconnectedCount = ports.length - connectedCount;

  return (
    <>
      <h3 className="text-xl font-semibold border-b border-[var(--divider-color)] pb-2">Port status</h3>
      <div className="grid grid-cols-4 sm:grid-cols-6 xl:grid-cols-8 gap-3">
        {ports.map((port, index) => (
          <div
            key={index}
            className="aspect-square flex flex-col items-center justify-center rounded-lg border-2 transition-all"
            style={{
              backgroundColor: port.status === 'Connected' ? 'rgba(var(--rgb-success-color), 0.1)' : 'var(--secondary-background-color)',
              borderColor: port.status === 'Connected' ? 'var(--success-color)' : 'var(--divider-color)',
              color: port.status === 'Connected' ? 'var(--success-color)' : 'var(--secondary-text-color)'
            }}
            title={`Port ${index + 1}: ${port.status}`}
          >
            <span className="text-[10px] font-bold mb-1">{index + 1}</span>
            <ha-icon icon="mdi:lan-connect" style={{ '--mdc-icon-size': '24px' } as any}></ha-icon>
          </div>
        ))}
      </div>
      <div className="flex items-center gap-2 text-sm text-[var(--secondary-text-color)] mt-4">
        <div className="w-3 h-3 rounded-full bg-[var(--success-color)]"></div>
        <span>{connectedCount} Connected</span>
        <div className="w-3 h-3 rounded-full bg-[var(--divider-color)] ml-4"></div>
        <span>{disconnectedCount} Disconnected</span>
      </div>
    </>
  );
};

const getReadingIcon = (metric: string): string => {
  const icons: Record<string, string> = {
    temperature: 'mdi:thermometer',
    humidity: 'mdi:water-percent',
    water: 'mdi:water',
    door: 'mdi:door',
    tvoc: 'mdi:air-filter',
  };
  return icons[metric] || 'mdi:chart-bell-curve';
};

const getReadingValue = (reading: MerakiSensorReading): string => {
  if (reading.temperature) return `${reading.temperature.celsius.toFixed(1)}°C`;
  if (reading.humidity) return `${reading.humidity.relativePercentage}%`;
  if (reading.water) return reading.water.present ? 'Wet' : 'Dry';
  if (reading.door) return reading.door.open ? 'Open' : 'Closed';
  if (reading.tvoc) return `${reading.tvoc.concentration} μg/m³`;
  if (reading.pm25) return `${reading.pm25.concentration} μg/m³`;
  return 'N/A';
};

const SensorReadingsGrid: React.FC<{ readings?: MerakiSensorReading[] }> = ({ readings }) => {
  if (!readings || readings.length === 0) return null;

  return (
    <ha-card>
      <div className="p-6">
        <h3 className="text-xl font-semibold mb-6">Live sensor readings</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {readings.map((reading, idx) => (
            <div key={idx} className="p-4 bg-[var(--secondary-background-color)] rounded-xl border border-[var(--divider-color)] flex items-center gap-4">
              <div className="p-2 bg-[var(--card-background-color)] rounded-lg shadow-sm">
                <ha-icon
                  icon={getReadingIcon(reading.metric)}
                  style={{ color: 'var(--primary-color)' }}
                ></ha-icon>
              </div>
              <div>
                <div className="text-xs font-bold uppercase tracking-wider text-[var(--secondary-text-color)]">{reading.metric}</div>
                <div className="text-xl font-black">{getReadingValue(reading)}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </ha-card>
  );
};

const DeviceView: React.FC<DeviceViewProps> = ({ activeView, setActiveView, data }) => {
  const onBack = () => setActiveView({ view: 'dashboard' });
  const device = data?.devices?.find((d) => d.serial === activeView.deviceId);

  if (!device) {
    return <DeviceNotFound deviceId={activeView.deviceId} onBack={onBack} />;
  }

  return (
    <div className="space-y-6 text-[var(--primary-text-color)]">
      <button
        onClick={onBack}
        className="flex items-center text-[var(--primary-color)] hover:underline"
      >
        <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
        Back to dashboard
      </button>

      <ha-card>
        <div className="p-6">
          <DeviceHeader device={device} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <TechnicalDetails device={device} />
            <div className="space-y-6">
              <PortStatusGrid ports={device.ports_statuses} />
            </div>
          </div>
        </div>
      </ha-card>

      <SensorReadingsGrid readings={device.readings} />
    </div>
  );
};

export default DeviceView;
