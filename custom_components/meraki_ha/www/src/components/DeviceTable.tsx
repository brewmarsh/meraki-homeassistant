import React, { useState } from 'react';

interface DeviceTableProps {
  hass: any;
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  deviceType?: string; // 'wireless', 'switch', 'camera', 'sensor', 'appliance', 'other'
}

const DeviceTable: React.FC<DeviceTableProps> = ({
  hass: _hass,
  devices,
  setActiveView,
  deviceType = 'other',
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  // Engineering Scaffolding: Centralized Icon Resolver
  const getDeviceIcon = (model: string) => {
    const m = model?.toUpperCase() || '';
    if (m.startsWith('MR')) return 'mdi:wifi';
    if (m.startsWith('MS')) return 'mdi:lan';
    if (m.startsWith('MV')) return 'mdi:cctv';
    if (m.startsWith('MX')) return 'mdi:shield-check';
    if (m.startsWith('MG')) return 'mdi:signal-cellular-outline';
    if (m.startsWith('MT40')) return 'mdi:power-plug';
    if (m.startsWith('MT12')) return 'mdi:water';
    if (m.startsWith('MT20')) return 'mdi:door';
    if (m.startsWith('MT30')) return 'mdi:gesture-tap-button';
    if (m.startsWith('MT')) return 'mdi:thermometer';
    if (m.startsWith('Z')) return 'mdi:router-wireless';
    if (m.startsWith('GS') || m.startsWith('GS')) return 'mdi:lan';
    return 'mdi:help-circle';
  };

  const filteredDevices = devices.filter(
    (device) =>
      device.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      device.serial?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleDeviceClick = (e: React.MouseEvent, entityId: string) => {
    e.preventDefault();
    e.stopPropagation();
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    e.currentTarget.dispatchEvent(event);
  };

  const getSensorHeroMetric = (device: any) => {
    if (device.status !== 'online') return null;
    const model = device.model || '';
    const readings = device.readings || [];

    const metricMap: { [key: string]: string } = {
      'MT10': 'temperature',
      'MT11': 'temperature',
      'MT12': 'water',
      'MT14': 'tvoc',
      'MT15': 'tvoc',
      'MT20': 'door'
    };

    const prefix = Object.keys(metricMap).find(p => model.startsWith(p));
    if (!prefix) return null;

    const r = readings.find((read: any) => read.metric === metricMap[prefix]);
    if (!r) return null;

    if (prefix === 'MT12') return r.water?.present ? 'Wet' : 'Dry';
    if (prefix === 'MT20') return r.door?.open ? 'Open' : 'Closed';
    if (r.temperature) return `${r.temperature.celsius.toFixed(1)} °C`;
    if (r.tvoc) return `${r.tvoc.concentration} μg/m³`;
    
    return null;
  };

  const renderStatus = (device: any) => {
    let statusText = device.status ? device.status.charAt(0).toUpperCase() + device.status.slice(1) : 'N/A';
    
    if (device.model?.startsWith('MT') && device.status === 'online') {
      const hero = getSensorHeroMetric(device);
      if (hero) statusText = hero;
    }

    const s = statusText.toLowerCase();
    const isActive = ['online', 'active', 'on', 'wet', 'connected', 'open'].includes(s);
    const isError = ['offline', 'unavailable', 'off', 'disconnected', 'alerting', 'closed'].includes(s);

    const color = isActive ? 'var(--success-color)' : isError ? 'var(--error-color)' : 'var(--primary-text-color)';

    return <span style={{ color }}>{statusText}</span>;
  };

  return (
    <ha-card className="mb-4">
      <div className="p-4">
        <input
          type="text"
          placeholder="Search by name or serial..."
          className="w-full p-2 mb-4 border border-[var(--divider-color)] rounded-lg bg-[var(--card-background-color)] text-[var(--primary-text-color)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-color)]"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        
        {/* Mobile-First Settings Row Layout */}
        <div className="flex flex-col">
          {filteredDevices.map((device) => (
            <div 
              key={device.serial}
              className="border-b border-[var(--divider-color)] last:border-0 hover:bg-[var(--secondary-background-color)] transition-colors cursor-pointer"
              onClick={() => setActiveView({ view: 'device', deviceId: device.serial })}
            >
              <ha-settings-row>
                <div slot="prefix" className="flex items-center justify-center w-10">
                  <ha-icon 
                    icon={getDeviceIcon(device.model)} 
                    style={{ color: 'var(--state-icon-color)' }}
                  ></ha-icon>
                </div>
                
                <div slot="heading" className="flex items-center gap-2">
                  <span 
                    className="font-medium text-[var(--primary-color)] hover:underline"
                    onClick={(e) => device.entity_id && handleDeviceClick(e, device.entity_id)}
                  >
                    {device.name || 'N/A'}
                  </span>
                </div>

                <div slot="description" className="text-[var(--secondary-text-color)] text-sm">
                  {device.model} • {device.serial}
                </div>

                <div className="flex flex-col items-end">
                  {renderStatus(device)}
                  {deviceType === 'switch' && device.ports_statuses && (
                     <div className="text-xs text-[var(--secondary-text-color)]">
                        {device.ports_statuses.filter((p: any) => p.status === 'Connected').length} / {device.ports_statuses.length} Ports
                     </div>
                  )}
                </div>
              </ha-settings-row>
            </div>
          ))}
        </div>
      </div>
    </ha-card>
  );
};

export default DeviceTable;