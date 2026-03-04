import React from 'react';

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
  const device = data?.devices?.find((d: any) => d.serial === activeView.deviceId);

  if (!device) {
    return (
      <div className="p-4">
        <button
          onClick={() => setActiveView({ view: 'dashboard' })}
          className="flex items-center text-[var(--primary-color)] hover:underline mb-4"
        >
          <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
          Back to dashboard
        </button>
        <ha-card className="p-6 text-center text-[var(--primary-text-color)]">
          <ha-icon icon="mdi:alert-circle-outline" style={{ '--mdc-icon-size': '48px', color: 'var(--error-color)' } as any}></ha-icon>
          <p className="mt-2 text-lg font-semibold">Device not found</p>
          <p className="text-[var(--secondary-text-color)]">The device with serial {activeView.deviceId} could not be located.</p>
        </ha-card>
      </div>
    );
  }

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

  const getStatusColor = (status: string) => {
    const s = status?.toLowerCase();
    if (s === 'online' || s === 'active' || s === 'home') return 'var(--success-color)';
    if (s === 'alerting') return 'var(--warning-color)';
    return 'var(--error-color)';
  };

  return (
    <div className="space-y-6 text-[var(--primary-text-color)]">
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="flex items-center text-[var(--primary-color)] hover:underline"
      >
        <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
        Back to dashboard
      </button>

      <ha-card>
        <div className="p-6">
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

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
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

            <div className="space-y-6">
              {device.ports_statuses ? (
                <>
                  <h3 className="text-xl font-semibold border-b border-[var(--divider-color)] pb-2">Port status</h3>
                  <div className="grid grid-cols-4 sm:grid-cols-6 xl:grid-cols-8 gap-3">
                    {device.ports_statuses.map((port: any, index: number) => (
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
                    <span>{device.ports_statuses.filter((p: any) => p.status === 'Connected').length} Connected</span>
                    <div className="w-3 h-3 rounded-full bg-[var(--divider-color)] ml-4"></div>
                    <span>{device.ports_statuses.filter((p: any) => p.status !== 'Connected').length} Disconnected</span>
                  </div>
                </>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-[var(--secondary-text-color)] opacity-50 italic">
                  <ha-icon icon="mdi:information-outline" style={{ '--mdc-icon-size': '48px' } as any} className="mb-2"></ha-icon>
                  <p>No port data available for this device type.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </ha-card>

      {device.readings && device.readings.length > 0 && (
        <ha-card>
          <div className="p-6">
            <h3 className="text-xl font-semibold mb-6">Live sensor readings</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {device.readings.map((reading: any, idx: number) => (
                <div key={idx} className="p-4 bg-[var(--secondary-background-color)] rounded-xl border border-[var(--divider-color)] flex items-center gap-4">
                  <div className="p-2 bg-[var(--card-background-color)] rounded-lg shadow-sm">
                    <ha-icon
                      icon={
                        reading.metric === 'temperature' ? 'mdi:thermometer' :
                        reading.metric === 'humidity' ? 'mdi:water-percent' :
                        reading.metric === 'water' ? 'mdi:water' :
                        reading.metric === 'door' ? 'mdi:door' :
                        reading.metric === 'tvoc' ? 'mdi:air-filter' :
                        'mdi:chart-bell-curve'
                      }
                      style={{ color: 'var(--primary-color)' }}
                    ></ha-icon>
                  </div>
                  <div>
                    <div className="text-xs font-bold uppercase tracking-wider text-[var(--secondary-text-color)]">{reading.metric}</div>
                    <div className="text-xl font-black">
                      {reading.temperature ? `${reading.temperature.celsius.toFixed(1)}°C` :
                       reading.humidity ? `${reading.humidity.relativePercentage}%` :
                       reading.water ? (reading.water.present ? 'Wet' : 'Dry') :
                       reading.door ? (reading.door.open ? 'Open' : 'Closed') :
                       reading.tvoc ? `${reading.tvoc.concentration} μg/m³` :
                       reading.pm25 ? `${reading.pm25.concentration} μg/m³` :
                       'N/A'}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </ha-card>
      )}
    </div>
  );
};

export default DeviceView;
