import React from 'react';

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: {
    devices: Array<{
      name: string;
      model: string;
      serial: string;
      firmware?: string;
      status: string;
      lanIp?: string;
      mac?: string;
      status_messages?: string[];
      entities?: Array<{ entity_id: string; name: string; state: string }>;
    }>;
  };
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
}) => {
  const device = data.devices.find(
    (d) => d.serial === activeView.deviceId
  );

  if (!device) {
    return (
      <div>
        <button
          onClick={() => setActiveView({ view: 'dashboard' })}
          className="back-button"
        >
          ← Back to Dashboard
        </button>
        <div className="empty-state">
          <ha-icon icon="mdi:help-circle"></ha-icon>
          <p>Device not found.</p>
        </div>
      </div>
    );
  }

  const {
    name,
    model,
    serial,
    firmware,
    status,
    lanIp,
    mac,
    status_messages = [],
    entities = [],
  } = device;

  const getStatusClass = (s: string) => {
    const status = s?.toLowerCase();
    if (status === 'online') return 'online';
    if (status === 'offline' || status === 'dormant') return 'offline';
    if (status === 'alerting') return 'alerting';
    return '';
  };

  const handleEntityClick = (entityId: string) => {
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    document.body.dispatchEvent(event);
  };

  return (
    <div>
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="back-button"
      >
        ← Back to Dashboard
      </button>

      <div className="device-detail-card">
        <h2>{name || serial}</h2>
        <div className="device-info-grid">
          <div className="device-info-item">
            <strong>Model</strong>
            {model || '—'}
          </div>
          <div className="device-info-item">
            <strong>Serial</strong>
            {serial}
          </div>
          <div className="device-info-item">
            <strong>Status</strong>
            <span className={`device-status ${getStatusClass(status)}`}>
              {status || 'Unknown'}
            </span>
          </div>
          {firmware && (
            <div className="device-info-item">
              <strong>Firmware</strong>
              {firmware}
            </div>
          )}
          {lanIp && (
            <div className="device-info-item">
              <strong>LAN IP</strong>
              {lanIp}
            </div>
          )}
          {mac && (
            <div className="device-info-item">
              <strong>MAC Address</strong>
              {mac}
            </div>
          )}
        </div>
      </div>

      {status_messages.length > 0 && (
        <div className="device-detail-card" style={{ borderLeft: '4px solid #ff9800' }}>
          <h3 style={{ margin: '0 0 12px 0', fontSize: '16px' }}>Status Messages</h3>
          <ul style={{ margin: 0, paddingLeft: '20px' }}>
            {status_messages.map((msg: string, index: number) => (
              <li key={index} style={{ marginBottom: '8px' }}>
                {msg}
              </li>
            ))}
          </ul>
        </div>
      )}

      {entities.length > 0 && (
        <div className="device-detail-card">
          <h3 style={{ margin: '0 0 16px 0', fontSize: '16px' }}>Entities</h3>
          <table className="device-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Entity ID</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity) => (
                <tr
                  key={entity.entity_id}
                  className="device-row"
                  onClick={() => handleEntityClick(entity.entity_id)}
                >
                  <td>{entity.name}</td>
                  <td style={{ fontFamily: 'monospace', fontSize: '13px' }}>
                    {entity.entity_id}
                  </td>
                  <td>{entity.state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default DeviceView;
