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
          className="flex items-center text-blue-500 hover:underline mb-4"
        >
          <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
          Back to Dashboard
        </button>
        <ha-card className="p-6 text-center">
          <ha-icon icon="mdi:alert-circle-outline" style={{ '--mdc-icon-size': '48px', color: 'red' } as any}></ha-icon>
          <p className="mt-2 text-lg font-semibold">Device Not Found</p>
          <p className="text-gray-500">The device with serial {activeView.deviceId} could not be located.</p>
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

  const getStatusColorClass = (status: string) => {
    const s = status?.toLowerCase();
    if (s === 'online' || s === 'active' || s === 'home') return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300';
    if (s === 'alerting') return 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300';
    return 'bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300';
  };

  return (
    <div className="space-y-6">
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="flex items-center text-blue-500 hover:underline"
      >
        <ha-icon icon="mdi:arrow-left" style={{ marginRight: '4px' }}></ha-icon>
        Back to Dashboard
      </button>

      <ha-card>
        <div className="p-6">
          <div className="flex flex-col md:flex-row md:items-center gap-4 mb-8">
            <div className="p-4 bg-blue-100 dark:bg-blue-900 rounded-full text-blue-600 dark:text-blue-300 w-fit">
              <ha-icon icon={getDeviceIcon(device.model)} style={{ '--mdc-icon-size': '40px' } as any}></ha-icon>
            </div>
            <div className="flex-grow">
              <h2 className="text-3xl font-bold">{device.name || 'Unnamed Device'}</h2>
              <p className="text-gray-500 dark:text-gray-400 text-lg">
                {device.model} <span className="mx-2">•</span> {device.serial}
              </p>
            </div>
            <div className={`px-4 py-2 rounded-full text-sm font-bold uppercase tracking-wider ${getStatusColorClass(device.status)}`}>
              {device.status || 'Unknown'}
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
            <div className="space-y-6">
              <h3 className="text-xl font-semibold border-b border-gray-200 dark:border-gray-700 pb-2">Technical Details</h3>
              <div className="grid grid-cols-1 gap-4">
                <div className="flex justify-between items-center py-2 border-b border-gray-50 dark:border-gray-800">
                  <span className="text-gray-500 dark:text-gray-400">MAC Address</span>
                  <span className="font-mono bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded text-sm">{device.mac || 'N/A'}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-50 dark:border-gray-800">
                  <span className="text-gray-500 dark:text-gray-400">LAN IP</span>
                  <span className="font-semibold">{device.lanIp || 'N/A'}</span>
                </div>
                <div className="flex justify-between items-center py-2 border-b border-gray-50 dark:border-gray-800">
                  <span className="text-gray-500 dark:text-gray-400">Network ID</span>
                  <span>{device.networkId || 'N/A'}</span>
                </div>
                {device.wan1Ip && (
                  <div className="flex justify-between items-center py-2 border-b border-gray-50 dark:border-gray-800">
                    <span className="text-gray-500 dark:text-gray-400">WAN 1 IP</span>
                    <span className="font-semibold">{device.wan1Ip}</span>
                  </div>
                )}
                {device.wan2Ip && (
                  <div className="flex justify-between items-center py-2 border-b border-gray-50 dark:border-gray-800">
                    <span className="text-gray-500 dark:text-gray-400">WAN 2 IP</span>
                    <span className="font-semibold">{device.wan2Ip}</span>
                  </div>
                )}
                {device.tags && device.tags.length > 0 && (
                  <div className="flex justify-between items-start py-2">
                    <span className="text-gray-500 dark:text-gray-400">Tags</span>
                    <div className="flex flex-wrap gap-1 justify-end max-w-[200px]">
                      {device.tags.map((tag: string) => (
                        <span key={tag} className="bg-gray-200 dark:bg-gray-700 text-xs px-2 py-1 rounded">{tag}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-6">
              {device.ports_statuses ? (
                <>
                  <h3 className="text-xl font-semibold border-b border-gray-200 dark:border-gray-700 pb-2">Port Status</h3>
                  <div className="grid grid-cols-4 sm:grid-cols-6 xl:grid-cols-8 gap-3">
                    {device.ports_statuses.map((port: any, index: number) => (
                      <div
                        key={index}
                        className={`aspect-square flex flex-col items-center justify-center rounded-lg border-2 transition-all ${
                          port.status === 'Connected'
                            ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800 text-green-600'
                            : 'bg-gray-50 border-gray-200 dark:bg-gray-800/40 dark:border-gray-700 text-gray-400'
                        }`}
                        title={`Port ${index + 1}: ${port.status}`}
                      >
                        <span className="text-[10px] font-bold mb-1">{index + 1}</span>
                        <ha-icon icon="mdi:lan-connect" style={{ '--mdc-icon-size': '24px' } as any}></ha-icon>
                      </div>
                    ))}
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-500 mt-4">
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span>{device.ports_statuses.filter((p: any) => p.status === 'Connected').length} Connected</span>
                    <div className="w-3 h-3 rounded-full bg-gray-300 dark:bg-gray-600 ml-4"></div>
                    <span>{device.ports_statuses.filter((p: any) => p.status !== 'Connected').length} Disconnected</span>
                  </div>
                </>
              ) : (
                <div className="h-full flex flex-col items-center justify-center text-gray-400 opacity-50 italic">
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
            <h3 className="text-xl font-semibold mb-6">Live Sensor Readings</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {device.readings.map((reading: any, idx: number) => (
                <div key={idx} className="p-4 bg-gray-50 dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 flex items-center gap-4">
                  <div className="p-2 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
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
                    <div className="text-xs font-bold uppercase tracking-wider text-gray-500">{reading.metric}</div>
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
