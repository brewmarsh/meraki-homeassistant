import React from 'react';

interface RelayDestination {
  name: string;
  status: 'connected' | 'connecting' | 'disconnected' | 'error';
  host: string;
  port: number;
  topic_filter: string;
  messages_relayed: number;
  last_relay_time: string | null;
  last_error: string | null;
  last_error_time: string | null;
}

interface MqttServiceStats {
  is_running: boolean;
  messages_received: number;
  messages_processed: number;
  last_message_time: string | null;
  start_time: string | null;
  sensors_mapped: number;
}

interface MqttStatusCardProps {
  mqttStats: MqttServiceStats | null;
  relayDestinations: Record<string, RelayDestination>;
}

const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  const getStatusStyle = (status: string) => {
    switch (status) {
      case 'connected':
        return { backgroundColor: '#22c55e', color: '#fff' };
      case 'connecting':
        return { backgroundColor: '#f59e0b', color: '#fff' };
      case 'disconnected':
        return { backgroundColor: '#6b7280', color: '#fff' };
      case 'error':
        return { backgroundColor: '#ef4444', color: '#fff' };
      default:
        return { backgroundColor: '#6b7280', color: '#fff' };
    }
  };

  return (
    <span
      style={{
        ...getStatusStyle(status),
        padding: '2px 8px',
        borderRadius: '12px',
        fontSize: '11px',
        fontWeight: 600,
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
      }}
    >
      {status}
    </span>
  );
};

const formatTime = (isoTime: string | null): string => {
  if (!isoTime) return 'Never';
  const date = new Date(isoTime);
  const now = new Date();
  const diff = now.getTime() - date.getTime();

  if (diff < 60000) {
    return 'Just now';
  } else if (diff < 3600000) {
    const mins = Math.floor(diff / 60000);
    return `${mins}m ago`;
  } else if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000);
    return `${hours}h ago`;
  }
  return date.toLocaleDateString();
};

const StatItem: React.FC<{ label: string; value: string | number }> = ({
  label,
  value,
}) => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'space-between',
      padding: '4px 0',
    }}
  >
    <span style={{ color: 'var(--secondary-text-color, #888)' }}>{label}</span>
    <span style={{ fontWeight: 500 }}>{value}</span>
  </div>
);

export const MqttStatusCard: React.FC<MqttStatusCardProps> = ({
  mqttStats,
  relayDestinations,
}) => {
  if (!mqttStats && Object.keys(relayDestinations).length === 0) {
    return null;
  }

  const cardStyle: React.CSSProperties = {
    backgroundColor:
      'var(--ha-card-background, var(--card-background-color, #fff))',
    borderRadius: '12px',
    padding: '16px',
    marginBottom: '16px',
    boxShadow: 'var(--ha-card-box-shadow, 0 2px 4px rgba(0,0,0,0.1))',
  };

  const headerStyle: React.CSSProperties = {
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    marginBottom: '16px',
    paddingBottom: '12px',
    borderBottom: '1px solid var(--divider-color, #e0e0e0)',
  };

  const sectionStyle: React.CSSProperties = {
    marginBottom: '16px',
  };

  const relayCardStyle: React.CSSProperties = {
    backgroundColor: 'var(--primary-background-color, #f5f5f5)',
    borderRadius: '8px',
    padding: '12px',
    marginBottom: '8px',
  };

  return (
    <div style={cardStyle}>
      <div style={headerStyle}>
        <svg
          viewBox="0 0 24 24"
          width="24"
          height="24"
          fill={mqttStats?.is_running ? '#22c55e' : '#ef4444'}
        >
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" />
        </svg>
        <div style={{ flex: 1 }}>
          <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>
            MQTT Status
          </h3>
          <span
            style={{
              fontSize: '12px',
              color: 'var(--secondary-text-color, #888)',
            }}
          >
            Real-time sensor data
          </span>
        </div>
        <StatusBadge
          status={mqttStats?.is_running ? 'connected' : 'disconnected'}
        />
      </div>

      {mqttStats && (
        <div style={sectionStyle}>
          <h4
            style={{
              margin: '0 0 8px 0',
              fontSize: '13px',
              fontWeight: 600,
              color: 'var(--primary-text-color)',
            }}
          >
            Service Statistics
          </h4>
          <StatItem
            label="Messages Received"
            value={mqttStats.messages_received.toLocaleString()}
          />
          <StatItem
            label="Messages Processed"
            value={mqttStats.messages_processed.toLocaleString()}
          />
          <StatItem label="Sensors Mapped" value={mqttStats.sensors_mapped} />
          <StatItem
            label="Last Message"
            value={formatTime(mqttStats.last_message_time)}
          />
          <StatItem
            label="Uptime Since"
            value={formatTime(mqttStats.start_time)}
          />
        </div>
      )}

      {Object.keys(relayDestinations).length > 0 && (
        <div style={sectionStyle}>
          <h4
            style={{
              margin: '0 0 12px 0',
              fontSize: '13px',
              fontWeight: 600,
              color: 'var(--primary-text-color)',
            }}
          >
            Relay Destinations ({Object.keys(relayDestinations).length})
          </h4>
          {Object.entries(relayDestinations).map(([name, dest]) => (
            <div key={name} style={relayCardStyle}>
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: '8px',
                }}
              >
                <span style={{ fontWeight: 600 }}>{name}</span>
                <StatusBadge status={dest.status} />
              </div>
              <div
                style={{
                  fontSize: '12px',
                  color: 'var(--secondary-text-color, #888)',
                }}
              >
                <div>
                  {dest.host}:{dest.port}
                </div>
                <div style={{ fontFamily: 'monospace', marginTop: '4px' }}>
                  {dest.topic_filter}
                </div>
              </div>
              <div style={{ marginTop: '8px', fontSize: '12px' }}>
                <StatItem
                  label="Messages Relayed"
                  value={dest.messages_relayed.toLocaleString()}
                />
                <StatItem
                  label="Last Relay"
                  value={formatTime(dest.last_relay_time)}
                />
                {dest.last_error && (
                  <div
                    style={{
                      marginTop: '4px',
                      padding: '6px',
                      backgroundColor: 'rgba(239, 68, 68, 0.1)',
                      borderRadius: '4px',
                    }}
                  >
                    <div style={{ color: '#ef4444', fontWeight: 500 }}>
                      Last Error
                    </div>
                    <div style={{ fontSize: '11px', marginTop: '2px' }}>
                      {dest.last_error}
                    </div>
                    <div
                      style={{
                        fontSize: '10px',
                        color: 'var(--secondary-text-color)',
                      }}
                    >
                      {formatTime(dest.last_error_time)}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MqttStatusCard;
