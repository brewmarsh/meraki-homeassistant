import React, { useRef, memo } from 'react';
import SwitchPortVisualization from './SwitchPortVisualization';
import SensorReading from './SensorReading';
import MetricCard from './MetricCard';

// === Memoized Sub-components for granular updates ===

// Entity row props
interface EntityRowProps {
  entity: { entity_id: string; name: string; state: string };
  onClick: () => void;
}

// Memoized entity row - only re-renders when this specific entity changes
const EntityRow = memo<EntityRowProps>(
  ({ entity, onClick }) => (
    <tr className="device-row" onClick={onClick}>
      <td>{entity.name}</td>
      <td className="text-mono text-sm text-muted">{entity.entity_id}</td>
      <td>
        <span className="detail-badge">{entity.state}</span>
      </td>
    </tr>
  ),
  (prev, next) =>
    prev.entity.entity_id === next.entity.entity_id &&
    prev.entity.name === next.entity.name &&
    prev.entity.state === next.entity.state
);

// Device client row props
interface DeviceClientRowProps {
  client: {
    id: string;
    mac: string;
    description?: string;
    ip?: string;
    manufacturer?: string;
    os?: string;
    ssid?: string;
    switchport?: string;
  };
  onClick: () => void;
}

// Memoized client row for device view - only re-renders when this client changes
const DeviceClientRow = memo<DeviceClientRowProps>(
  ({ client, onClick }) => (
    <tr className="device-row clickable" onClick={onClick}>
      <td>
        <div className="client-row-cell">
          <span className="client-row-icon">
            {client.os?.toLowerCase().includes('ios') ||
            client.manufacturer?.toLowerCase().includes('apple')
              ? '📱'
              : client.os?.toLowerCase().includes('windows')
              ? '💻'
              : '🔌'}
          </span>
          <div className="client-row-info">
            <div className="font-medium">
              {client.description || client.mac}
            </div>
            {client.manufacturer && (
              <div className="text-sm text-muted">{client.manufacturer}</div>
            )}
          </div>
        </div>
      </td>
      {client.ip && <td className="text-mono text-sm">{client.ip}</td>}
      {!client.ip && <td></td>}
      <td>
        {(client.ssid || client.switchport) && (
          <span className="detail-badge">
            {client.ssid || client.switchport}
          </span>
        )}
      </td>
    </tr>
  ),
  (prev, next) =>
    prev.client.id === next.client.id &&
    prev.client.mac === next.client.mac &&
    prev.client.description === next.client.description &&
    prev.client.ip === next.client.ip &&
    prev.client.manufacturer === next.client.manufacturer &&
    prev.client.os === next.client.os &&
    prev.client.ssid === next.client.ssid &&
    prev.client.switchport === next.client.switchport
);

// BSS row props
interface BSSRowProps {
  bss: {
    ssidName?: string;
    ssidNumber?: number;
    bssid?: string;
    band?: string;
    channel?: number;
    channelWidth?: string;
    power?: string;
    broadcasting?: boolean;
  };
  index: number;
}

// Memoized BSS row - only re-renders when this BSS entry changes
const BSSRow = memo<BSSRowProps>(
  ({ bss }) => (
    <tr>
      <td>
        <div className="font-medium">
          {bss.ssidName || `SSID ${bss.ssidNumber}`}
        </div>
        {bss.bssid && <div className="bssid-text">{bss.bssid}</div>}
      </td>
      <td>
        <span
          className={`band-badge ${
            bss.band?.includes('2.4') ? 'band-2_4' : 'band-5'
          }`}
        >
          {bss.band}
        </span>
      </td>
      <td>{bss.channel}</td>
      <td>{bss.channelWidth}</td>
      <td className="text-warning">{bss.power}</td>
      <td>
        <span
          className={`broadcast-status ${
            bss.broadcasting ? 'active' : 'inactive'
          }`}
        >
          <span className="broadcast-dot"></span>
          {bss.broadcasting ? 'Broadcasting' : 'Off'}
        </span>
      </td>
    </tr>
  ),
  (prev, next) =>
    prev.bss.ssidName === next.bss.ssidName &&
    prev.bss.ssidNumber === next.bss.ssidNumber &&
    prev.bss.bssid === next.bss.bssid &&
    prev.bss.band === next.bss.band &&
    prev.bss.channel === next.bss.channel &&
    prev.bss.channelWidth === next.bss.channelWidth &&
    prev.bss.power === next.bss.power &&
    prev.bss.broadcasting === next.bss.broadcasting
);

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
  rtspEnabled?: boolean;
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

const DeviceViewComponent: React.FC<DeviceViewProps> = ({
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
  const [linkedCameraUrl, setLinkedCameraUrl] = React.useState<string | null>(
    null
  );
  const [linkedCameraLoading, setLinkedCameraLoading] = React.useState(false);
  const [_linkedCameraFailed, setLinkedCameraFailed] = React.useState(false);

  // RTSP stream state
  const [rtspStreamUrl, setRtspStreamUrl] = React.useState<string | null>(
    null
  );
  const [rtspLoading, setRtspLoading] = React.useState(false);
  const [_rtspFailed, setRtspFailed] = React.useState(false);

  // Track which video source is active: 'linked' | 'rtsp' | 'snapshot' | 'none'
  const [activeVideoSource, setActiveVideoSource] = React.useState<
    'linked' | 'rtsp' | 'snapshot' | 'none'
  >('none');

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
      // Reset video state and reload stream with new camera
      setLinkedCameraUrl(null);
      setActiveVideoSource('none');
      // Delay slightly to ensure state is updated, then load the stream
      if (entityId) {
        setTimeout(() => loadVideoStream(), 100);
      }
    } catch (err) {
      console.error('Failed to save camera mapping:', err);
    }
  };

  // Fetch signed camera stream URL from Home Assistant (MJPEG live stream)
  const fetchLinkedCameraUrl = async (): Promise<boolean> => {
    const currentHass = hassRef.current;
    if (!currentHass || !linkedCameraId) return false;

    setLinkedCameraLoading(true);
    setLinkedCameraFailed(false);
    try {
      // Use camera_proxy_stream for live MJPEG video (not camera_proxy which is snapshot)
      const result = (await currentHass.callWS({
        type: 'auth/sign_path',
        path: `/api/camera_proxy_stream/${linkedCameraId}`,
        expires: 300, // URL valid for 5 minutes for continuous streaming
      })) as { path?: string };

      if (result?.path) {
        setLinkedCameraUrl(result.path);
        setActiveVideoSource('linked');
        return true;
      }
      setLinkedCameraFailed(true);
      return false;
    } catch (err) {
      console.error('Failed to get signed camera stream URL:', err);
      setLinkedCameraUrl(null);
      setLinkedCameraFailed(true);
      return false;
    } finally {
      setLinkedCameraLoading(false);
    }
  };

  // Fetch RTSP stream URL from Meraki API
  const fetchRtspStreamUrl = async (): Promise<boolean> => {
    const currentHass = hassRef.current;
    if (!currentHass || !device?.serial || !configEntryId) return false;

    setRtspLoading(true);
    setRtspFailed(false);
    try {
      const result = (await currentHass.callWS({
        type: 'meraki_ha/get_rtsp_url',
        config_entry_id: configEntryId,
        serial: device.serial,
      })) as { rtsp_url?: string };

      if (result?.rtsp_url) {
        setRtspStreamUrl(result.rtsp_url);
        setActiveVideoSource('rtsp');
        return true;
      }
      setRtspFailed(true);
      return false;
    } catch (err) {
      console.error('Failed to get RTSP stream URL:', err);
      setRtspStreamUrl(null);
      setRtspFailed(true);
      return false;
    } finally {
      setRtspLoading(false);
    }
  };

  // Auto-load video stream with fallback chain: linked camera → RTSP → snapshot
  const loadVideoStream = async () => {
    // Try linked camera first
    if (linkedCameraId) {
      const linkedSuccess = await fetchLinkedCameraUrl();
      if (linkedSuccess) return;
    }

    // Fallback to RTSP if available
    if (device?.rtsp_url || device?.rtspEnabled) {
      const rtspSuccess = await fetchRtspStreamUrl();
      if (rtspSuccess) return;
    }

    // Final fallback to snapshot
    if (snapshotUrl) {
      setActiveVideoSource('snapshot');
    } else {
      setActiveVideoSource('none');
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

  // Auto-load video stream when linked camera ID is available or changes
  React.useEffect(() => {
    const isCameraDevice =
      device &&
      (device.model?.toUpperCase().startsWith('MV') ||
        device.productType === 'camera');

    if (isCameraDevice && hassRef.current) {
      // Load video with fallback chain
      loadVideoStream();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [linkedCameraId, device?.serial, snapshotUrl]);

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

      {/* Camera Live Video Stream - positioned after metric cards, before entities */}
      {isCamera && (
        <div className="info-card" style={{ marginTop: '24px' }}>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: '16px',
            }}
          >
            <h3 style={{ margin: 0 }}>📹 Live View</h3>
            <button
              onClick={() => setShowCameraConfig(!showCameraConfig)}
              style={{
                padding: '6px 12px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid var(--card-border)',
                background: 'var(--bg-secondary)',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                fontSize: '13px',
              }}
            >
              ⚙️ Configure
            </button>
          </div>

          {/* Camera Linking Configuration */}
          {showCameraConfig && (
            <div
              style={{
                background: 'var(--bg-tertiary)',
                borderRadius: 'var(--radius-md)',
                padding: '16px',
                marginBottom: '16px',
                border: '1px solid var(--card-border)',
              }}
            >
              <h4 style={{ margin: '0 0 12px 0', fontSize: '14px' }}>
                🔗 Link to Camera Stream
              </h4>
              <p
                style={{
                  fontSize: '13px',
                  color: 'var(--text-secondary)',
                  marginBottom: '12px',
                }}
              >
                Select a camera entity to display live video. This can be the
                Meraki camera&apos;s RTSP stream via an NVR (like Blue Iris) or
                any other camera in Home Assistant.
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
                    border: '1px solid var(--card-border)',
                    background: 'var(--bg-secondary)',
                    color: 'var(--text-primary)',
                    fontSize: '14px',
                  }}
                >
                  <option value="">-- Select camera entity --</option>
                  {availableCameras.map((cam) => (
                    <option key={cam.entity_id} value={cam.entity_id}>
                      {cam.friendly_name}
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
              {device.rtsp_url && (
                <div
                  style={{
                    marginTop: '12px',
                    padding: '8px 12px',
                    background: 'var(--bg-secondary)',
                    borderRadius: 'var(--radius-sm)',
                    fontSize: '12px',
                  }}
                >
                  <strong>RTSP URL:</strong>{' '}
                  <code
                    style={{
                      fontFamily: 'monospace',
                      color: 'var(--text-secondary)',
                    }}
                  >
                    {device.rtsp_url}
                  </code>
                </div>
              )}
            </div>
          )}

          {/* Live Video Area - responsive 16:9 aspect ratio */}
          <div
            style={{
              background: '#000',
              borderRadius: 'var(--radius-md)',
              overflow: 'hidden',
              position: 'relative',
              width: '100%',
              maxWidth: '100%',
              aspectRatio: '16/9',
              marginBottom: '16px',
            }}
          >
            {/* Loading state */}
            {(linkedCameraLoading || rtspLoading) && (
              <div
                style={{
                  position: 'absolute',
                  inset: 0,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-muted)',
                  zIndex: 10,
                }}
              >
                ⏳ Loading{' '}
                {linkedCameraLoading ? 'linked camera' : 'RTSP stream'}...
              </div>
            )}

            {/* Linked Camera Stream (highest priority) */}
            {activeVideoSource === 'linked' && linkedCameraUrl && (
              <img
                src={linkedCameraUrl}
                alt={`Live view: ${name || serial}`}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                }}
                onError={() => {
                  console.error(
                    'Linked camera stream failed, trying fallback'
                  );
                  setLinkedCameraUrl(null);
                  setLinkedCameraFailed(true);
                  // Try RTSP fallback
                  if (device?.rtsp_url || device?.rtspEnabled) {
                    fetchRtspStreamUrl();
                  } else if (snapshotUrl) {
                    setActiveVideoSource('snapshot');
                  } else {
                    setActiveVideoSource('none');
                  }
                }}
              />
            )}

            {/* RTSP Stream (second priority) */}
            {activeVideoSource === 'rtsp' && rtspStreamUrl && (
              <div
                style={{
                  width: '100%',
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'var(--text-muted)',
                  gap: '12px',
                }}
              >
                <span style={{ fontSize: '48px' }}>🎥</span>
                <span>RTSP Stream Available</span>
                <code
                  style={{
                    fontSize: '11px',
                    padding: '8px 12px',
                    background: 'rgba(255,255,255,0.1)',
                    borderRadius: 'var(--radius-sm)',
                    maxWidth: '90%',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {rtspStreamUrl}
                </code>
                <span style={{ fontSize: '12px', opacity: 0.7 }}>
                  Open this URL in VLC or a compatible player
                </span>
              </div>
            )}

            {/* Snapshot (third priority / fallback) */}
            {activeVideoSource === 'snapshot' && snapshotUrl && (
              <img
                src={snapshotUrl}
                alt={`${name || serial} snapshot`}
                style={{
                  width: '100%',
                  height: '100%',
                  objectFit: 'contain',
                }}
              />
            )}

            {/* No video source available */}
            {activeVideoSource === 'none' &&
              !linkedCameraLoading &&
              !rtspLoading && (
                <div
                  style={{
                    position: 'absolute',
                    inset: 0,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'var(--text-muted)',
                    gap: '12px',
                  }}
                >
                  <span style={{ fontSize: '48px' }}>📹</span>
                  <span>No live stream available</span>
                  <div
                    style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}
                  >
                    <button
                      onClick={() => loadVideoStream()}
                      style={{
                        padding: '8px 16px',
                        borderRadius: 'var(--radius-sm)',
                        border: 'none',
                        background: 'var(--primary)',
                        color: 'white',
                        cursor: 'pointer',
                        fontSize: '13px',
                      }}
                    >
                      🔄 Retry
                    </button>
                    <button
                      onClick={() => setShowCameraConfig(true)}
                      style={{
                        padding: '8px 16px',
                        borderRadius: 'var(--radius-sm)',
                        border: '1px solid var(--border)',
                        background: 'transparent',
                        color: 'var(--text-primary)',
                        cursor: 'pointer',
                        fontSize: '13px',
                      }}
                    >
                      ⚙️ Link Camera
                    </button>
                  </div>
                </div>
              )}

            {/* Video source indicator badge */}
            {activeVideoSource !== 'none' &&
              !linkedCameraLoading &&
              !rtspLoading && (
                <div
                  style={{
                    position: 'absolute',
                    top: '8px',
                    left: '8px',
                    padding: '4px 8px',
                    borderRadius: 'var(--radius-sm)',
                    background: 'rgba(0,0,0,0.6)',
                    color: 'white',
                    fontSize: '11px',
                    fontWeight: 500,
                    textTransform: 'uppercase',
                  }}
                >
                  {activeVideoSource === 'linked' && '● Live'}
                  {activeVideoSource === 'rtsp' && '● RTSP'}
                  {activeVideoSource === 'snapshot' && '📷 Snapshot'}
                </div>
              )}
          </div>

          {/* Action Buttons */}
          <div
            style={{
              display: 'flex',
              gap: '12px',
              justifyContent: 'center',
              flexWrap: 'wrap',
            }}
          >
            {/* Refresh button - always available */}
            <button
              onClick={() => loadVideoStream()}
              disabled={linkedCameraLoading || rtspLoading}
              style={{
                padding: '10px 20px',
                borderRadius: 'var(--radius-md)',
                border: 'none',
                background: 'var(--primary)',
                color: 'white',
                cursor:
                  linkedCameraLoading || rtspLoading ? 'wait' : 'pointer',
                fontWeight: 500,
              }}
            >
              {linkedCameraLoading || rtspLoading
                ? '⏳ Loading...'
                : '🔄 Refresh Stream'}
            </button>

            {/* Full screen for linked camera */}
            {activeVideoSource === 'linked' && linkedCameraId && (
              <button
                onClick={() => handleEntityClick(linkedCameraId)}
                style={{
                  padding: '10px 20px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--card-border)',
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                }}
              >
                📺 Full Screen
              </button>
            )}

            {/* Get snapshot button */}
            <button
              onClick={fetchSnapshot}
              disabled={snapshotLoading}
              style={{
                padding: '10px 20px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--card-border)',
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                cursor: snapshotLoading ? 'wait' : 'pointer',
                fontWeight: 500,
              }}
            >
              {snapshotLoading ? '⏳...' : '📷 Snapshot'}
            </button>

            {/* Link/config camera button */}
            <button
              onClick={() => setShowCameraConfig(true)}
              style={{
                padding: '10px 20px',
                borderRadius: 'var(--radius-md)',
                border: '1px solid var(--card-border)',
                background: 'var(--bg-secondary)',
                color: 'var(--text-primary)',
                cursor: 'pointer',
                fontWeight: 500,
              }}
            >
              ⚙️ {linkedCameraId ? 'Change' : 'Link'} Camera
            </button>

            {cloudVideoUrl && (
              <button
                onClick={openInDashboard}
                style={{
                  padding: '10px 20px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--card-border)',
                  background: 'var(--bg-secondary)',
                  color: 'var(--text-primary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                }}
              >
                🌐 Meraki Dashboard
              </button>
            )}
          </div>

          {/* Source indicator */}
          {linkedCameraId && (
            <div
              style={{
                marginTop: '12px',
                textAlign: 'center',
                fontSize: '12px',
                color: 'var(--text-muted)',
              }}
            >
              Streaming from: {linkedCameraId}
            </div>
          )}
        </div>
      )}

      {/* Switch Port Visualization */}
      {isSwitch && ports_statuses.length > 0 && (
        <SwitchPortVisualization
          deviceName={name || serial}
          model={model}
          ports={ports_statuses}
          clients={deviceClients}
          onClientClick={(clientId) =>
            setActiveView({ view: 'clients', clientId })
          }
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

      {/* Entities (filtered to exclude hero readings) - hidden for switches */}
      {filteredEntities.length > 0 && !isSwitch && (
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
                <EntityRow
                  key={entity.entity_id}
                  entity={entity}
                  onClick={() => handleEntityClick(entity.entity_id)}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Connected Clients Section - hidden for switches (shown per-port instead) */}
      {deviceClients.length > 0 && !isSwitch && (
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
                <DeviceClientRow
                  key={client.id || client.mac}
                  client={client}
                  onClick={() =>
                    setActiveView({ view: 'clients', clientId: client.id })
                  }
                />
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
                      <BSSRow key={`bss-${idx}`} bss={bss} index={idx} />
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

// Memoize DeviceView to prevent unnecessary re-renders
const DeviceView = memo(DeviceViewComponent, (prevProps, nextProps) => {
  // Only re-render if the viewed device or its data changed
  if (prevProps.activeView.deviceId !== nextProps.activeView.deviceId) {
    return false; // Different device selected
  }

  // Find the current device in both props
  const prevDevice = prevProps.data.devices.find(
    (d) => d.serial === prevProps.activeView.deviceId
  );
  const nextDevice = nextProps.data.devices.find(
    (d) => d.serial === nextProps.activeView.deviceId
  );

  // Compare device status
  if (prevDevice?.status !== nextDevice?.status) {
    return false;
  }

  // Compare port count for switches
  if (
    prevDevice?.ports_statuses?.length !== nextDevice?.ports_statuses?.length
  ) {
    return false;
  }

  // Compare client count
  const prevClients = prevProps.data.clients?.filter(
    (c) => c.recentDeviceSerial === prevDevice?.serial
  ).length;
  const nextClients = nextProps.data.clients?.filter(
    (c) => c.recentDeviceSerial === nextDevice?.serial
  ).length;
  if (prevClients !== nextClients) {
    return false;
  }

  return true; // No meaningful changes
});

export default DeviceView;
