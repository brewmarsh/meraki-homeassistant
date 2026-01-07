import React, { useRef } from 'react';
import SwitchPortVisualization from './SwitchPortVisualization';
import SensorReading from './SensorReading';
import MetricCard from './MetricCard';

interface PortStatus {
  portId: string;
  status: string;
  enabled: boolean;
  isUplink?: boolean;
  speed?: string;
  duplex?: string;
  usageInKb?: { total?: number; sent?: number; recv?: number };
  trafficInKbps?: { total?: number; sent?: number; recv?: number };
  poe?: { isAllocated?: boolean; enabled?: boolean };
  powerUsageInWh?: number;
  clientName?: string;
  clientMac?: string;
  clientCount?: number;
  vlan?: number;
  errors?: string[];
  warnings?: string[];
  lldp?: {
    systemName?: string;
    systemDescription?: string;
    portId?: string;
    managementAddress?: string;
    portDescription?: string;
    systemCapabilities?: string;
    chassisId?: string;
  };
  cdp?: {
    deviceId?: string;
    systemName?: string;
    platform?: string;
    portId?: string;
    address?: string;
    nativeVlan?: number;
    managementAddress?: string;
    capabilities?: string;
  };
  securePort?: {
    enabled?: boolean;
    active?: boolean;
    authenticationStatus?: string;
  };
}

interface Client {
  id: string;
  mac: string;
  description?: string;
  ip?: string;
  manufacturer?: string;
  os?: string;
  status?: string;
  usage?: { sent: number; recv: number };
  recentDeviceSerial?: string;
  recentDeviceName?: string;
  ssid?: string;
  switchport?: string;
}

interface Device {
  name: string;
  model: string;
  serial: string;
  firmware?: string;
  status: string;
  lanIp?: string;
  mac?: string;
  productType?: string;
  status_messages?: string[];
  entities?: Array<{ entity_id: string; name: string; state: string }>;
  ports_statuses?: PortStatus[];
  readings?: {
    temperature?: number;
    humidity?: number;
    battery?: number;
    tvoc?: number;
    pm25?: number;
    co2?: number;
    noise?: number;
    indoorAirQuality?: number;
  };
  uptime?: number;
  lastReportedAt?: string;
  cloud_video_url?: string;
  rtsp_url?: string;
  basicServiceSets?: Array<{
    ssidName?: string;
    ssidNumber?: number;
    enabled?: boolean;
    band?: string;
    bssid?: string;
    channel?: number;
    channelWidth?: string;
    power?: string;
    visible?: boolean;
    broadcasting?: boolean;
  }>;
}

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string; clientId?: string };
  setActiveView: (view: {
    view: string;
    deviceId?: string;
    clientId?: string;
  }) => void;
  data: {
    devices: Device[];
    clients?: Client[];
  };
  hass?: {
    callWS: <T = unknown>(params: {
      type: string;
      [key: string]: unknown;
    }) => Promise<T>;
  };
  configEntryId?: string;
  cameraLinkIntegration?: string;
  configEntryOptions?: {
    temperature_unit?: 'celsius' | 'fahrenheit';
    [key: string]: unknown;
  };
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
  hass,
  configEntryId,
  cameraLinkIntegration,
  configEntryOptions,
}) => {
  const temperatureUnit = configEntryOptions?.temperature_unit || 'celsius';
  const device = data.devices.find((d) => d.serial === activeView.deviceId);

  // Get clients connected to this device
  const deviceClients = (data.clients || []).filter(
    (client) => client.recentDeviceSerial === device?.serial
  );
  const [snapshotUrl, setSnapshotUrl] = React.useState<string | null>(null);
  const [snapshotLoading, setSnapshotLoading] = React.useState(false);
  const [cloudVideoUrl, setCloudVideoUrl] = React.useState<string | null>(
    null
  );

  // Linked camera state
  const [availableCameras, setAvailableCameras] = React.useState<
    Array<{ entity_id: string; friendly_name: string }>
  >([]);
  const [linkedCameraId, setLinkedCameraId] = React.useState<string>('');
  const [showCameraConfig, setShowCameraConfig] = React.useState(false);
  const [viewLinkedCamera, setViewLinkedCamera] = React.useState(false);
  const [linkedCameraUrl, setLinkedCameraUrl] = React.useState<string | null>(
    null
  );
  const [linkedCameraLoading, setLinkedCameraLoading] = React.useState(false);

  // Use refs to avoid re-renders when hass object changes (happens on every HA state update)
  const hassRef = useRef(hass);
  hassRef.current = hass;
  const hasLoadedCameraDataRef = useRef<string | null>(null);

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
          <div className="icon">❓</div>
          <h3>Device Not Found</h3>
          <p>The requested device could not be found.</p>
        </div>
      </div>
    );
  }

  const {
    name,
    model = '',
    serial,
    firmware,
    status,
    lanIp,
    mac,
    productType,
    status_messages = [],
    entities = [],
    ports_statuses = [],
    readings,
    uptime,
    lastReportedAt,
  } = device;

  const getDeviceIcon = (): string => {
    const modelUpper = model.toUpperCase();
    const type = productType?.toLowerCase() || '';

    // Network switches
    if (modelUpper.startsWith('MS') || type === 'switch') return '🔀';
    // Cameras
    if (modelUpper.startsWith('MV') || type === 'camera') return '📹';
    // Wireless APs
    if (modelUpper.startsWith('MR') || type === 'wireless') return '📶';
    // Sensors - different icons based on model
    if (modelUpper.startsWith('MT') || type === 'sensor') {
      if (
        modelUpper.startsWith('MT10') ||
        modelUpper.startsWith('MT11') ||
        modelUpper.startsWith('MT15')
      ) {
        return '🌡️'; // Temperature sensor
      }
      if (modelUpper.startsWith('MT12')) {
        return '🚪'; // Door/open-close sensor
      }
      if (modelUpper.startsWith('MT14')) {
        return '💨'; // Air quality sensor
      }
      if (modelUpper.startsWith('MT20')) {
        return '🔘'; // Button sensor
      }
      if (modelUpper.startsWith('MT30')) {
        return '⚡'; // Power meter
      }
      return '📡'; // Default sensor
    }
    // Security appliances/firewalls
    if (
      modelUpper.startsWith('MX') ||
      modelUpper.startsWith('Z') ||
      type === 'appliance'
    )
      return '🛡️';
    return '📱';
  };

  const getDeviceTypeClass = (): string => {
    const modelUpper = model.toUpperCase();
    const type = productType?.toLowerCase() || '';

    if (modelUpper.startsWith('MS') || type === 'switch') return 'switch';
    if (modelUpper.startsWith('MV') || type === 'camera') return 'camera';
    if (modelUpper.startsWith('MR') || type === 'wireless') return 'wireless';
    if (modelUpper.startsWith('MT') || type === 'sensor') return 'sensor';
    if (
      modelUpper.startsWith('MX') ||
      modelUpper.startsWith('Z') ||
      type === 'appliance'
    )
      return 'appliance';
    return '';
  };

  const isSwitch =
    model.toUpperCase().startsWith('MS') || productType === 'switch';
  const isSensor =
    model.toUpperCase().startsWith('MT') || productType === 'sensor';
  const isCamera =
    model.toUpperCase().startsWith('MV') || productType === 'camera';
  const isWireless =
    model.toUpperCase().startsWith('MR') || productType === 'wireless';
  const isAppliance =
    model.toUpperCase().startsWith('MX') ||
    model.toUpperCase().startsWith('Z') ||
    productType === 'appliance';

  // Filter out entities that are already shown as hero sensor readings
  const heroEntityPatterns = [
    'temperature',
    'humidity',
    'battery',
    'tvoc',
    'pm25',
    'pm2_5',
    'co2',
    'noise',
    'indoor_air_quality',
    'air_quality',
    'voc',
  ];
  const filteredEntities = entities.filter((entity) => {
    const lowerName = entity.name.toLowerCase();
    const lowerEntityId = entity.entity_id.toLowerCase();
    return !heroEntityPatterns.some(
      (pattern) =>
        lowerName.includes(pattern) || lowerEntityId.includes(pattern)
    );
  });

  const formatUptime = (seconds?: number): string | null => {
    if (!seconds) return null;
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    if (days > 0) {
      return `${days}d ${hours}h`;
    }
    const minutes = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${minutes}m`;
  };

  // Format uptime for display in metric cards (returns days as number)
  const getUptimeDays = (seconds?: number): number => {
    if (!seconds) return 0;
    return Math.floor(seconds / 86400);
  };

  const formatLastSeen = (timestamp?: string): string => {
    if (!timestamp) return 'Just now';
    const date = new Date(timestamp);
    const now = new Date();
    const isToday = date.toDateString() === now.toDateString();

    if (isToday) {
      return date.toLocaleTimeString([], {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
    }
    return date.toLocaleString([], {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleEntityClick = (entityId: string) => {
    const event = new CustomEvent('hass-more-info', {
      bubbles: true,
      composed: true,
      detail: { entityId },
    });
    document.body.dispatchEvent(event);
  };

  // Fetch camera snapshot
  const fetchSnapshot = async () => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId || !device) return;
    setSnapshotLoading(true);
    try {
      const result = (await currentHass.callWS({
        type: 'meraki_ha/get_camera_snapshot',
        config_entry_id: configEntryId,
        serial: device.serial,
      })) as { url?: string };
      if (result?.url) {
        setSnapshotUrl(result.url);
      }
    } catch (err) {
      console.error('Failed to fetch snapshot:', err);
    } finally {
      setSnapshotLoading(false);
    }
  };

  // Fetch cloud video URL for "Open in Dashboard" button
  const fetchCloudVideoUrl = async () => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId || !device) return;
    try {
      const result = (await currentHass.callWS({
        type: 'meraki_ha/get_camera_stream_url',
        config_entry_id: configEntryId,
        serial: device.serial,
        stream_source: 'cloud',
      })) as { url?: string };
      if (result?.url) {
        setCloudVideoUrl(result.url);
      }
    } catch (err) {
      console.error('Failed to fetch cloud video URL:', err);
    }
  };

  // Open cloud video in new browser tab
  const openInDashboard = () => {
    if (cloudVideoUrl) {
      window.open(cloudVideoUrl, '_blank', 'noopener,noreferrer');
    }
  };

  // Fetch available cameras for linking (filtered by integration if configured)
  const fetchAvailableCameras = async () => {
    const currentHass = hassRef.current;
    if (!currentHass) return;
    try {
      const result = (await currentHass.callWS({
        type: 'meraki_ha/get_available_cameras',
        integration_filter: cameraLinkIntegration || '',
      })) as { cameras?: Array<{ entity_id: string; friendly_name: string }> };
      if (result?.cameras) {
        setAvailableCameras(result.cameras);
      }
    } catch (err) {
      console.error('Failed to fetch available cameras:', err);
    }
  };

  // Fetch current camera mapping
  const fetchCameraMapping = async () => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId || !device) return;
    try {
      const result = (await currentHass.callWS({
        type: 'meraki_ha/get_camera_mappings',
        config_entry_id: configEntryId,
      })) as { mappings?: Record<string, string> };
      if (result?.mappings && result.mappings[device.serial]) {
        setLinkedCameraId(result.mappings[device.serial]);
      }
    } catch (err) {
      console.error('Failed to fetch camera mappings:', err);
    }
  };

  // Save camera mapping
  const saveCameraMapping = async (entityId: string) => {
    const currentHass = hassRef.current;
    if (!currentHass || !configEntryId || !device) return;
    try {
      await currentHass.callWS({
        type: 'meraki_ha/set_camera_mapping',
        config_entry_id: configEntryId,
        serial: device.serial,
        linked_entity_id: entityId,
      });
      setLinkedCameraId(entityId);
      setShowCameraConfig(false);
      // If viewing linked camera, fetch the new signed URL
      if (viewLinkedCamera && entityId) {
        setLinkedCameraUrl(null);
        // Delay slightly to ensure state is updated
        setTimeout(() => fetchLinkedCameraUrl(), 100);
      }
    } catch (err) {
      console.error('Failed to save camera mapping:', err);
    }
  };

  // Fetch signed camera URL from Home Assistant
  const fetchLinkedCameraUrl = async () => {
    const currentHass = hassRef.current;
    if (!currentHass || !linkedCameraId) return;

    setLinkedCameraLoading(true);
    try {
      // Use Home Assistant's auth/sign_path to get a properly authenticated URL
      const result = (await currentHass.callWS({
        type: 'auth/sign_path',
        path: `/api/camera_proxy/${linkedCameraId}`,
        expires: 30, // URL valid for 30 seconds
      })) as { path?: string };

      if (result?.path) {
        setLinkedCameraUrl(result.path);
      }
    } catch (err) {
      console.error('Failed to get signed camera URL:', err);
      setLinkedCameraUrl(null);
    } finally {
      setLinkedCameraLoading(false);
    }
  };

  // Load camera data when viewing a camera device - only fetch once per device
  React.useEffect(() => {
    const isCameraDevice =
      device &&
      (device.model?.toUpperCase().startsWith('MV') ||
        device.productType === 'camera');
    const deviceSerial = device?.serial;

    // Only fetch if this is a new device we haven't loaded yet
    if (isCameraDevice && deviceSerial && configEntryId && hassRef.current) {
      if (hasLoadedCameraDataRef.current !== deviceSerial) {
        hasLoadedCameraDataRef.current = deviceSerial;
        fetchSnapshot();
        fetchCloudVideoUrl();
        fetchCameraMapping();
        fetchAvailableCameras();
      }
    }
  }, [device?.serial, configEntryId]);

  // Fetch signed URL when viewing linked camera
  React.useEffect(() => {
    if (viewLinkedCamera && linkedCameraId && hassRef.current) {
      fetchLinkedCameraUrl();
    }
  }, [viewLinkedCamera, linkedCameraId]);

  // Calculate PoE stats for switches
  const totalPoeEnergy = ports_statuses.reduce(
    (acc, p) => acc + (p.powerUsageInWh || 0),
    0
  );
  const totalConnectedClients = ports_statuses.reduce(
    (acc, p) => acc + (p.clientCount || 0),
    0
  );

  return (
    <div>
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="back-button"
      >
        ← Back to Dashboard
      </button>

      {/* Device Header */}
      <div className="device-header">
        <div className={`device-icon ${getDeviceTypeClass()}`}>
          {getDeviceIcon()}
        </div>
        <div className="device-info">
          <h1>{name || serial}</h1>
          <div className="meta">
            <span>
              <strong>Model:</strong> {model}
            </span>
            <span>
              <strong>Serial:</strong> {serial}
            </span>
            {firmware && (
              <span>
                <strong>Firmware:</strong> {firmware}
              </span>
            )}
            {lanIp && (
              <span>
                <strong>IP:</strong> {lanIp}
              </span>
            )}
            {mac && (
              <span>
                <strong>MAC:</strong>{' '}
                <span style={{ fontFamily: 'monospace' }}>{mac}</span>
              </span>
            )}
            {/* Sensor-specific: Battery in header */}
            {isSensor && readings?.battery != null && (
              <span>
                <strong>Battery:</strong>{' '}
                <span
                  style={{
                    color:
                      readings.battery > 20
                        ? 'var(--success)'
                        : 'var(--warning)',
                  }}
                >
                  {readings.battery}%
                </span>
              </span>
            )}
          </div>
          {lastReportedAt && (
            <div
              className="meta"
              style={{ marginTop: '4px', fontSize: '12px' }}
            >
              <span style={{ color: 'var(--text-muted)' }}>
                Last updated: {formatLastSeen(lastReportedAt)}
              </span>
            </div>
          )}
        </div>
        <div className={`status-pill ${status?.toLowerCase()}`}>
          <div className="dot"></div>
          {status || 'Unknown'}
        </div>
      </div>

      {/* Switch Metric Cards */}
      {isSwitch && ports_statuses.length > 0 && (
        <div className="metric-cards-grid">
          <MetricCard
            icon="⚡"
            label="PoE Energy"
            value={totalPoeEnergy}
            unit="Wh"
            gauge={{ min: 0, max: 500, color: 'warning' }}
            status="normal"
            statusMessage="Active"
          />
          <MetricCard
            icon="👥"
            label="Connected Clients"
            value={totalConnectedClients}
            gauge={{
              min: 0,
              max: Math.max(50, totalConnectedClients),
              color: 'info',
            }}
            status="normal"
          />
          {uptime != null && (
            <MetricCard
              icon="⏱️"
              label="Uptime"
              value={getUptimeDays(uptime)}
              unit=" days"
              secondaryValue={formatUptime(uptime) || undefined}
              status="normal"
              statusMessage="Running"
            />
          )}
          <MetricCard
            icon="🔌"
            label="Connected Ports"
            value={
              ports_statuses.filter(
                (p) => p.status?.toLowerCase() === 'connected'
              ).length
            }
            secondaryValue={`of ${ports_statuses.length} total`}
            gauge={{
              min: 0,
              max: ports_statuses.length,
              color: 'success',
            }}
            status="normal"
          />
        </div>
      )}

      {/* Wireless AP Metric Cards */}
      {isWireless && (
        <div className="metric-cards-grid">
          <MetricCard
            icon="👥"
            label="Connected Clients"
            value={deviceClients.length}
            gauge={{
              min: 0,
              max: Math.max(50, deviceClients.length),
              color: 'info',
            }}
            status="normal"
          />
          {device.basicServiceSets && (
            <MetricCard
              icon="📶"
              label="Active SSIDs"
              value={device.basicServiceSets.filter((b) => b.enabled).length}
              secondaryValue={`of ${device.basicServiceSets.length} total`}
              gauge={{
                min: 0,
                max: device.basicServiceSets.length || 1,
                color: 'success',
              }}
              status="normal"
            />
          )}
          {uptime != null && (
            <MetricCard
              icon="⏱️"
              label="Uptime"
              value={getUptimeDays(uptime)}
              unit=" days"
              secondaryValue={formatUptime(uptime) || undefined}
              status="normal"
              statusMessage="Running"
            />
          )}
        </div>
      )}

      {/* Appliance Metric Cards */}
      {isAppliance && (
        <div className="metric-cards-grid">
          <MetricCard
            icon="🌐"
            label="WAN Status"
            value={status === 'online' ? 'Online' : 'Offline'}
            status={status === 'online' ? 'normal' : 'critical'}
            statusMessage={status === 'online' ? 'Connected' : 'Disconnected'}
          />
          {uptime != null && (
            <MetricCard
              icon="⏱️"
              label="Uptime"
              value={getUptimeDays(uptime)}
              unit=" days"
              secondaryValue={formatUptime(uptime) || undefined}
              status="normal"
              statusMessage="Running"
            />
          )}
        </div>
      )}

      {/* Camera Metric Cards */}
      {isCamera && (
        <div className="metric-cards-grid">
          <MetricCard
            icon="🔴"
            label="Recording"
            value={status === 'online' ? 'Active' : 'Inactive'}
            status={status === 'online' ? 'normal' : 'inactive'}
            statusMessage={
              status === 'online' ? 'Recording to cloud' : 'Camera offline'
            }
          />
          <MetricCard
            icon="👁️"
            label="Motion Detection"
            value="Enabled"
            status="normal"
            statusMessage="Monitoring"
          />
        </div>
      )}

      {/* Info Cards Grid */}
      <div className="cards-grid">
        {/* Device Information card - hidden for switches, sensors, and wireless since info is in header */}
        {!isSwitch && !isSensor && !isWireless && (
          <div className="info-card">
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '16px',
              }}
            >
              <h3 style={{ margin: 0 }}>ℹ️ Device Information</h3>
              {lastReportedAt && (
                <span
                  style={{
                    fontSize: '11px',
                    color: 'var(--text-muted)',
                    fontWeight: 400,
                  }}
                >
                  Updated: {formatLastSeen(lastReportedAt)}
                </span>
              )}
            </div>
            <div className="info-grid">
              {lanIp && (
                <div className="info-item">
                  <div className="label">LAN IP</div>
                  <div className="value">{lanIp}</div>
                </div>
              )}
              {mac && (
                <div className="info-item">
                  <div className="label">MAC Address</div>
                  <div className="value mono">{mac}</div>
                </div>
              )}
              {firmware && (
                <div className="info-item">
                  <div className="label">Firmware</div>
                  <div className="value">{firmware}</div>
                </div>
              )}
              {uptime != null && !isWireless && !isAppliance && (
                <div className="info-item">
                  <div className="label">Uptime</div>
                  <div className="value">{formatUptime(uptime)}</div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Switch Port Visualization */}
      {isSwitch && ports_statuses.length > 0 && (
        <SwitchPortVisualization
          deviceName={name || serial}
          model={model}
          ports={ports_statuses}
        />
      )}

      {/* Sensor Readings */}
      {isSensor && readings && (
        <div className="readings-grid">
          {readings.temperature != null && (
            <SensorReading
              type="temperature"
              value={readings.temperature}
              temperatureUnit={temperatureUnit}
              status="normal"
            />
          )}
          {readings.humidity != null && (
            <SensorReading
              type="humidity"
              value={readings.humidity}
              status="normal"
            />
          )}
          {readings.indoorAirQuality != null && (
            <SensorReading
              type="indoorAirQuality"
              value={readings.indoorAirQuality}
              status={
                readings.indoorAirQuality >= 70
                  ? 'normal'
                  : readings.indoorAirQuality >= 50
                  ? 'warning'
                  : 'critical'
              }
            />
          )}
          {readings.tvoc != null && (
            <SensorReading
              type="tvoc"
              value={readings.tvoc}
              status={
                readings.tvoc <= 400
                  ? 'normal'
                  : readings.tvoc <= 800
                  ? 'warning'
                  : 'critical'
              }
            />
          )}
          {readings.pm25 != null && (
            <SensorReading
              type="pm25"
              value={readings.pm25}
              status={
                readings.pm25 <= 35
                  ? 'normal'
                  : readings.pm25 <= 75
                  ? 'warning'
                  : 'critical'
              }
            />
          )}
          {readings.co2 != null && (
            <SensorReading
              type="co2"
              value={readings.co2}
              status={
                readings.co2 <= 1000
                  ? 'normal'
                  : readings.co2 <= 2000
                  ? 'warning'
                  : 'critical'
              }
            />
          )}
          {readings.noise != null && (
            <SensorReading
              type="noise"
              value={readings.noise}
              status={
                readings.noise <= 60
                  ? 'normal'
                  : readings.noise <= 80
                  ? 'warning'
                  : 'critical'
              }
            />
          )}
        </div>
      )}

      {/* Status Messages */}
      {status_messages.length > 0 && (
        <div
          className="info-card"
          style={{ borderLeft: '4px solid var(--warning)' }}
        >
          <h3>⚠️ Status Messages</h3>
          <ul
            style={{
              margin: 0,
              paddingLeft: '20px',
              color: 'var(--text-secondary)',
            }}
          >
            {status_messages.map((msg: string, index: number) => (
              <li key={index} style={{ marginBottom: '8px' }}>
                {msg}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Entities (filtered to exclude hero readings) */}
      {filteredEntities.length > 0 && (
        <div className="info-card">
          <h3>🔗 Entities ({filteredEntities.length})</h3>
          <table className="device-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Entity ID</th>
                <th>State</th>
              </tr>
            </thead>
            <tbody>
              {filteredEntities.map((entity) => (
                <tr
                  key={entity.entity_id}
                  className="device-row"
                  onClick={() => handleEntityClick(entity.entity_id)}
                >
                  <td>{entity.name}</td>
                  <td
                    style={{
                      fontFamily: 'monospace',
                      fontSize: '13px',
                      color: 'var(--text-muted)',
                    }}
                  >
                    {entity.entity_id}
                  </td>
                  <td>
                    <span className="detail-badge">{entity.state}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Connected Clients Section */}
      {deviceClients.length > 0 && (
        <div className="info-card">
          <h3>👥 Connected Clients ({deviceClients.length})</h3>
          <table className="device-table">
            <thead>
              <tr>
                <th>Client</th>
                <th>IP Address</th>
                <th>Connection</th>
              </tr>
            </thead>
            <tbody>
              {deviceClients.slice(0, 10).map((client) => (
                <tr
                  key={client.id || client.mac}
                  className="device-row"
                  onClick={() =>
                    setActiveView({ view: 'clients', clientId: client.id })
                  }
                  style={{ cursor: 'pointer' }}
                >
                  <td>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                      }}
                    >
                      <span style={{ fontSize: '18px' }}>
                        {client.os?.toLowerCase().includes('ios') ||
                        client.manufacturer?.toLowerCase().includes('apple')
                          ? '📱'
                          : client.os?.toLowerCase().includes('windows')
                          ? '💻'
                          : '🔌'}
                      </span>
                      <div>
                        <div style={{ fontWeight: 500 }}>
                          {client.description || client.mac}
                        </div>
                        {client.manufacturer && (
                          <div
                            style={{
                              fontSize: '12px',
                              color: 'var(--text-muted)',
                            }}
                          >
                            {client.manufacturer}
                          </div>
                        )}
                      </div>
                    </div>
                  </td>
                  {client.ip && (
                    <td style={{ fontFamily: 'monospace', fontSize: '13px' }}>
                      {client.ip}
                    </td>
                  )}
                  {!client.ip && <td></td>}
                  <td>
                    {(client.ssid || client.switchport) && (
                      <span className="detail-badge">
                        {client.ssid || client.switchport}
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {deviceClients.length > 10 && (
            <div
              style={{
                textAlign: 'center',
                padding: '12px',
                color: 'var(--text-muted)',
                fontSize: '13px',
              }}
            >
              Showing 10 of {deviceClients.length} clients •{' '}
              <button
                onClick={() => setActiveView({ view: 'clients' })}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--primary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                  fontSize: '13px',
                }}
              >
                View All Clients
              </button>
            </div>
          )}
        </div>
      )}

      {/* Camera-specific View */}
      {isCamera && (
        <div className="info-card">
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '16px',
            }}
          >
            <h3 style={{ margin: 0 }}>📹 Camera</h3>
            <button
              onClick={() => setShowCameraConfig(!showCameraConfig)}
              style={{
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--border)',
                background: 'var(--bg-secondary)',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              ⚙️ Link Camera
            </button>
          </div>

          {/* Camera Linking Configuration */}
          {showCameraConfig && (
            <div
              style={{
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                marginBottom: '16px',
                border: '1px solid var(--border)',
              }}
            >
              <h4 style={{ margin: '0 0 12px 0', fontSize: '14px' }}>
                🔗 Link to External Camera (e.g., Blue Iris)
              </h4>
              <p
                style={{
                  fontSize: '13px',
                  color: 'var(--text-muted)',
                  marginBottom: '12px',
                }}
              >
                Link this Meraki camera to another camera entity in Home
                Assistant. Useful when RTSP goes to an NVR (like Blue Iris)
                first.
              </p>
              <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                <select
                  value={linkedCameraId}
                  onChange={(e) => setLinkedCameraId(e.target.value)}
                  style={{
                    flex: 1,
                    minWidth: '200px',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border)',
                    background: 'var(--bg-secondary)',
                    color: 'var(--text-primary)',
                    fontSize: '14px',
                  }}
                >
                  <option value="">-- No linked camera --</option>
                  {availableCameras.map((cam) => (
                    <option key={cam.entity_id} value={cam.entity_id}>
                      {cam.friendly_name} ({cam.entity_id})
                    </option>
                  ))}
                </select>
                <button
                  onClick={() => saveCameraMapping(linkedCameraId)}
                  style={{
                    padding: '8px 16px',
                    borderRadius: 'var(--radius-sm)',
                    border: 'none',
                    background: 'var(--primary)',
                    color: 'white',
                    cursor: 'pointer',
                    fontWeight: 500,
                  }}
                >
                  Save
                </button>
              </div>
              {linkedCameraId && (
                <p
                  style={{
                    fontSize: '12px',
                    color: 'var(--success)',
                    marginTop: '8px',
                    marginBottom: 0,
                  }}
                >
                  ✓ Linked to: {linkedCameraId}
                </p>
              )}
            </div>
          )}

          {/* View Toggle - only show if linked camera is configured */}
          {linkedCameraId && (
            <div
              style={{
                display: 'flex',
                gap: '4px',
                marginBottom: '16px',
                background: 'var(--bg-primary)',
                borderRadius: 'var(--radius-md)',
                padding: '4px',
              }}
            >
              <button
                onClick={() => setViewLinkedCamera(false)}
                style={{
                  flex: 1,
                  padding: '8px 16px',
                  borderRadius: 'var(--radius-sm)',
                  border: 'none',
                  background: !viewLinkedCamera
                    ? 'var(--primary)'
                    : 'transparent',
                  color: !viewLinkedCamera ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                  transition: 'all 0.2s',
                }}
              >
                📷 Meraki Snapshot
              </button>
              <button
                onClick={() => setViewLinkedCamera(true)}
                style={{
                  flex: 1,
                  padding: '8px 16px',
                  borderRadius: 'var(--radius-sm)',
                  border: 'none',
                  background: viewLinkedCamera
                    ? 'var(--primary)'
                    : 'transparent',
                  color: viewLinkedCamera ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                  transition: 'all 0.2s',
                }}
              >
                🎬 Linked Camera
              </button>
            </div>
          )}

          {/* Content Area */}
          <div
            style={{
              background: 'var(--bg-primary)',
              borderRadius: 'var(--radius-md)',
              padding: '16px',
              textAlign: 'center',
              marginBottom: '16px',
            }}
          >
            {viewLinkedCamera && linkedCameraId ? (
              /* Linked Camera Stream (e.g., Blue Iris) */
              <div>
                {linkedCameraLoading ? (
                  <div style={{ padding: '40px', color: 'var(--text-muted)' }}>
                    ⏳ Loading camera...
                  </div>
                ) : linkedCameraUrl ? (
                  <img
                    src={linkedCameraUrl}
                    alt={`Linked camera: ${linkedCameraId}`}
                    style={{
                      maxWidth: '100%',
                      borderRadius: 'var(--radius-md)',
                      marginBottom: '12px',
                    }}
                    onError={() => {
                      console.error('Failed to load linked camera image');
                      setLinkedCameraUrl(null);
                    }}
                  />
                ) : (
                  <div style={{ padding: '40px', color: 'var(--text-muted)' }}>
                    📹 Unable to load camera feed
                  </div>
                )}
                <div
                  style={{
                    display: 'flex',
                    gap: '12px',
                    justifyContent: 'center',
                    flexWrap: 'wrap',
                    marginTop: '12px',
                  }}
                >
                  <button
                    onClick={() => fetchLinkedCameraUrl()}
                    disabled={linkedCameraLoading}
                    style={{
                      padding: '10px 20px',
                      borderRadius: 'var(--radius-md)',
                      border: 'none',
                      background: 'var(--primary)',
                      color: 'white',
                      cursor: linkedCameraLoading ? 'wait' : 'pointer',
                      fontWeight: 500,
                    }}
                  >
                    {linkedCameraLoading ? '⏳ Loading...' : '🔄 Refresh'}
                  </button>
                  <button
                    onClick={() => handleEntityClick(linkedCameraId)}
                    style={{
                      padding: '10px 20px',
                      borderRadius: 'var(--radius-md)',
                      border: '1px solid var(--border)',
                      background: 'var(--bg-secondary)',
                      color: 'var(--text-primary)',
                      cursor: 'pointer',
                      fontWeight: 500,
                    }}
                  >
                    📺 Open Camera Entity
                  </button>
                </div>
                <p
                  style={{
                    fontSize: '12px',
                    color: 'var(--text-muted)',
                    marginTop: '12px',
                    marginBottom: 0,
                  }}
                >
                  Viewing: {linkedCameraId}
                </p>
              </div>
            ) : (
              /* Snapshot View */
              <>
                {snapshotUrl ? (
                  <img
                    src={snapshotUrl}
                    alt={`${name || serial} snapshot`}
                    style={{
                      maxWidth: '100%',
                      borderRadius: 'var(--radius-md)',
                      marginBottom: '12px',
                    }}
                  />
                ) : (
                  <div
                    style={{
                      padding: '40px',
                      color: 'var(--text-muted)',
                      fontSize: '48px',
                    }}
                  >
                    📹
                  </div>
                )}

                {/* Action Buttons */}
                <div
                  style={{
                    display: 'flex',
                    gap: '12px',
                    justifyContent: 'center',
                    flexWrap: 'wrap',
                    marginTop: '12px',
                  }}
                >
                  <button
                    onClick={fetchSnapshot}
                    disabled={snapshotLoading}
                    style={{
                      padding: '10px 20px',
                      borderRadius: 'var(--radius-md)',
                      border: 'none',
                      background: 'var(--primary)',
                      color: 'white',
                      cursor: snapshotLoading ? 'wait' : 'pointer',
                      fontWeight: 500,
                      display: 'flex',
                      alignItems: 'center',
                      gap: '8px',
                    }}
                  >
                    {snapshotLoading ? '⏳ Loading...' : '📷 Refresh Snapshot'}
                  </button>

                  {cloudVideoUrl && (
                    <button
                      onClick={openInDashboard}
                      style={{
                        padding: '10px 20px',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border)',
                        background: 'var(--bg-secondary)',
                        color: 'var(--text-primary)',
                        cursor: 'pointer',
                        fontWeight: 500,
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                      }}
                    >
                      🌐 Open in Meraki Dashboard
                    </button>
                  )}
                </div>
              </>
            )}
          </div>

          {/* Stream Info */}
          <div
            style={{
              fontSize: '13px',
              color: 'var(--text-muted)',
              textAlign: 'center',
            }}
          >
            <p style={{ margin: '0 0 8px 0' }}>
              💡 <strong>RTSP Streaming:</strong> Enable in Meraki Dashboard →
              Camera Settings → External RTSP
            </p>
            <p style={{ margin: 0 }}>
              For live streaming in Home Assistant dashboards, use the camera
              entity
            </p>
          </div>
        </div>
      )}

      {/* Wireless AP-specific View with BSS Details */}
      {isWireless && (
        <div className="info-card">
          <h3>📶 Wireless Access Point</h3>
          {device.basicServiceSets && device.basicServiceSets.length > 0 ? (
            <div>
              <table className="device-table" style={{ marginTop: '16px' }}>
                <thead>
                  <tr>
                    <th>SSID</th>
                    <th>Band</th>
                    <th>Channel</th>
                    <th>Width</th>
                    <th>Power</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {device.basicServiceSets
                    .filter((bss) => bss.enabled)
                    .map((bss, idx) => (
                      <tr key={`bss-${idx}`}>
                        <td>
                          <div style={{ fontWeight: 500 }}>
                            {bss.ssidName || `SSID ${bss.ssidNumber}`}
                          </div>
                          {bss.bssid && (
                            <div
                              style={{
                                fontSize: '11px',
                                color: 'var(--text-muted)',
                                fontFamily: 'monospace',
                              }}
                            >
                              {bss.bssid}
                            </div>
                          )}
                        </td>
                        <td>
                          <span
                            className="detail-badge"
                            style={{
                              background: bss.band?.includes('2.4')
                                ? 'rgba(245, 158, 11, 0.15)'
                                : 'rgba(6, 182, 212, 0.15)',
                              color: bss.band?.includes('2.4')
                                ? 'var(--warning)'
                                : 'var(--primary)',
                            }}
                          >
                            {bss.band}
                          </span>
                        </td>
                        <td>{bss.channel}</td>
                        <td>{bss.channelWidth}</td>
                        <td style={{ color: 'var(--warning)' }}>
                          {bss.power}
                        </td>
                        <td>
                          <span
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '6px',
                              color: bss.broadcasting
                                ? 'var(--success)'
                                : 'var(--text-muted)',
                            }}
                          >
                            <span
                              style={{
                                width: '8px',
                                height: '8px',
                                borderRadius: '50%',
                                background: bss.broadcasting
                                  ? 'var(--success)'
                                  : 'var(--text-muted)',
                                boxShadow: bss.broadcasting
                                  ? '0 0 8px var(--success)'
                                  : 'none',
                              }}
                            ></span>
                            {bss.broadcasting ? 'Broadcasting' : 'Off'}
                          </span>
                        </td>
                      </tr>
                    ))}
                </tbody>
              </table>
              {device.basicServiceSets.filter((bss) => !bss.enabled).length >
                0 && (
                <div
                  style={{
                    marginTop: '12px',
                    fontSize: '13px',
                    color: 'var(--text-muted)',
                  }}
                >
                  {
                    device.basicServiceSets.filter((bss) => !bss.enabled)
                      .length
                  }{' '}
                  disabled SSIDs not shown
                </div>
              )}
            </div>
          ) : (
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Connected Clients</div>
                <div className="value primary">{deviceClients.length}</div>
              </div>
              <div className="info-item">
                <div className="label">Radio Bands</div>
                <div className="value">2.4 GHz / 5 GHz</div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default DeviceView;
