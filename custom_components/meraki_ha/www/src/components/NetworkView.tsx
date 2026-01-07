import React, { useState } from 'react';

// Define the types for our data
interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
}

interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
}

interface Device {
  entity_id: string;
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
}

interface NetworkViewProps {
  data: {
    networks: Network[];
    devices: Device[];
  };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data, setActiveView }) => {
  const { networks, devices } = data;

  // Filter to only show networks that are enabled in settings
  const enabledNetworks =
    networks?.filter((network) => network.is_enabled) || [];

  // If there's only one network, expand it by default
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(
    enabledNetworks.length === 1 ? enabledNetworks[0].id : null
  );

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  if (!enabledNetworks || enabledNetworks.length === 0) {
    return (
      <div className="empty-state">
        <ha-icon icon="mdi:network-off"></ha-icon>
        <p>No networks are enabled for this integration.</p>
        <p className="hint">
          Go to Settings → Devices & Services → Meraki → Configure to enable
          networks.
        </p>
      </div>
    );
  }

  return (
    <div className="network-list">
      {enabledNetworks.map((network) => {
        const isOpen = openNetworkId === network.id;
        const networkDevices = devices.filter(
          (d) => d.networkId === network.id
        );
        const enabledSsids = network.ssids
          ? network.ssids.filter((s) => s.enabled).length
          : 0;
        const totalSsids = network.ssids ? network.ssids.length : 0;

        return (
          <div key={network.id} className="network-card">
            <div
              className="network-header"
              onClick={() => handleNetworkClick(network.id)}
            >
              <ha-icon icon="mdi:lan" className="network-icon"></ha-icon>
              <span className="network-name">{network.name}</span>
              <span className="device-count">
                {networkDevices.length} device
                {networkDevices.length !== 1 ? 's' : ''}
              </span>
              <ha-icon
                icon={isOpen ? 'mdi:chevron-up' : 'mdi:chevron-down'}
                className="expand-icon"
              ></ha-icon>
            </div>

            {isOpen && (
              <div className="network-content">
                <DeviceTable
                  devices={networkDevices}
                  setActiveView={setActiveView}
                />

                {network.ssids && network.ssids.length > 0 && (
                  <>
                    <div className="ssid-header">
                      <ha-icon icon="mdi:wifi"></ha-icon>
                      <span>
                        {enabledSsids} of {totalSsids} SSIDs Enabled
                      </span>
                    </div>
                    <div className="ssid-grid">
                      {network.ssids.map((ssid) => (
                        <div key={ssid.number} className="ssid-card">
                          <span className="ssid-name">{ssid.name}</span>
                          <ha-icon
                            icon={ssid.enabled ? 'mdi:wifi' : 'mdi:wifi-off'}
                            className={`ssid-status-icon ${
                              ssid.enabled ? 'enabled' : 'disabled'
                            }`}
                          ></ha-icon>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

// Inline DeviceTable component for simplicity
interface DeviceTableProps {
  devices: Device[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const DeviceTable: React.FC<DeviceTableProps> = ({
  devices,
  setActiveView,
}) => {
  const [searchTerm, setSearchTerm] = useState('');

  const getDeviceIcon = (model: string) => {
    if (model?.startsWith('MR')) return 'mdi:access-point';
    if (model?.startsWith('MS')) return 'mdi:lan';
    if (model?.startsWith('MV')) return 'mdi:cctv';
    if (model?.startsWith('MX')) return 'mdi:router-network';
    if (model?.startsWith('MG')) return 'mdi:cellphone-wireless';
    if (model?.startsWith('MT')) return 'mdi:thermometer';
    return 'mdi:devices';
  };

  const getStatusClass = (status: string) => {
    const s = status?.toLowerCase();
    if (s === 'online') return 'online';
    if (s === 'offline' || s === 'dormant') return 'offline';
    if (s === 'alerting') return 'alerting';
    return '';
  };

  const filteredDevices = devices.filter(
    (device) =>
      device.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      device.serial?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      device.model?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleRowClick = (serial: string) => {
    setActiveView({ view: 'device', deviceId: serial });
  };

  const handleEntityClick = (e: React.MouseEvent, entityId: string) => {
    e.preventDefault();
    e.stopPropagation();

    // Dispatch Home Assistant's more-info event
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    document.body.dispatchEvent(event);
  };

  if (devices.length === 0) {
    return (
      <div
        style={{
          textAlign: 'center',
          padding: '24px',
          color: 'var(--text-secondary)',
        }}
      >
        No devices in this network.
      </div>
    );
  }

  return (
    <div className="device-table-container">
      {devices.length > 5 && (
        <input
          type="text"
          placeholder="Search devices..."
          className="device-search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      )}

      <table className="device-table">
        <thead>
          <tr>
            <th>Device</th>
            <th>Model</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {filteredDevices.map((device) => (
            <tr
              key={device.serial}
              className="device-row"
              onClick={() => handleRowClick(device.serial)}
            >
              <td>
                <div className="device-name-cell">
                  <ha-icon icon={getDeviceIcon(device.model)}></ha-icon>
                  {device.entity_id ? (
                    <a
                      href="#"
                      className="device-name-link"
                      onClick={(e) => handleEntityClick(e, device.entity_id)}
                    >
                      {device.name || device.serial}
                    </a>
                  ) : (
                    <span>{device.name || device.serial}</span>
                  )}
                </div>
              </td>
              <td>{device.model || '—'}</td>
              <td>
                <span
                  className={`device-status ${getStatusClass(device.status)}`}
                >
                  {device.status || 'Unknown'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NetworkView;
