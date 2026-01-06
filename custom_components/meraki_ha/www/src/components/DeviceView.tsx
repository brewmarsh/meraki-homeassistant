import React, { useRef } from 'react';
import SwitchPortVisualization from './SwitchPortVisualization';
import SensorReading from './SensorReading';

interface PortStatus {
  portId: string;
  status: string;
  enabled: boolean;
  speed?: string;
  duplex?: string;
  usageInKb?: { total: number };
  poe?: { isAllocated?: boolean; enabled?: boolean };
  powerUsageInWh?: number;
  clientName?: string;
  clientMac?: string;
  vlan?: number;
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
  };
  uptime?: number;
  lastReportedAt?: string;
  cloud_video_url?: string;
  rtsp_url?: string;
}

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: {
    devices: Device[];
  };
  hass?: {
    callWS: (params: Record<string, unknown>) => Promise<unknown>;
  };
  configEntryId?: string;
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
  hass,
  configEntryId,
}) => {
  const device = data.devices.find((d) => d.serial === activeView.deviceId);
  const [snapshotUrl, setSnapshotUrl] = React.useState<string | null>(null);
  const [snapshotLoading, setSnapshotLoading] = React.useState(false);
  const [cloudVideoUrl, setCloudVideoUrl] = React.useState<string | null>(null);
  
  // Linked camera state
  const [availableCameras, setAvailableCameras] = React.useState<Array<{entity_id: string; friendly_name: string}>>([]);
  const [linkedCameraId, setLinkedCameraId] = React.useState<string>('');
  const [showCameraConfig, setShowCameraConfig] = React.useState(false);
  const [viewLinkedCamera, setViewLinkedCamera] = React.useState(false);

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
    
    if (modelUpper.startsWith('MS') || type === 'switch') return '⚡';
    if (modelUpper.startsWith('MV') || type === 'camera') return '📹';
    if (modelUpper.startsWith('MR') || type === 'wireless') return '📶';
    if (modelUpper.startsWith('MT') || type === 'sensor') return '🌡️';
    if (modelUpper.startsWith('MX') || modelUpper.startsWith('Z') || type === 'appliance') return '🔒';
    return '📱';
  };

  const getDeviceTypeClass = (): string => {
    const modelUpper = model.toUpperCase();
    const type = productType?.toLowerCase() || '';
    
    if (modelUpper.startsWith('MS') || type === 'switch') return 'switch';
    if (modelUpper.startsWith('MV') || type === 'camera') return 'camera';
    if (modelUpper.startsWith('MR') || type === 'wireless') return 'wireless';
    if (modelUpper.startsWith('MT') || type === 'sensor') return 'sensor';
    if (modelUpper.startsWith('MX') || modelUpper.startsWith('Z') || type === 'appliance') return 'appliance';
    return '';
  };

  const isSwitch = model.toUpperCase().startsWith('MS') || productType === 'switch';
  const isSensor = model.toUpperCase().startsWith('MT') || productType === 'sensor';
  const isCamera = model.toUpperCase().startsWith('MV') || productType === 'camera';
  const isWireless = model.toUpperCase().startsWith('MR') || productType === 'wireless';

  const formatUptime = (seconds?: number): string => {
    if (!seconds) return '—';
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    return `${days} days, ${hours} hours`;
  };

  const formatLastSeen = (timestamp?: string): string => {
    if (!timestamp) return 'Just now';
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} min ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours} hours ago`;
    return `${Math.floor(diffHours / 24)} days ago`;
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
      const result = await currentHass.callWS({
        type: 'meraki_ha/get_camera_snapshot',
        config_entry_id: configEntryId,
        serial: device.serial,
      }) as { url?: string };
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
      const result = await currentHass.callWS({
        type: 'meraki_ha/get_camera_stream_url',
        config_entry_id: configEntryId,
        serial: device.serial,
        stream_source: 'cloud',
      }) as { url?: string };
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

  // Fetch available cameras for linking
  const fetchAvailableCameras = async () => {
    const currentHass = hassRef.current;
    if (!currentHass) return;
    try {
      const result = await currentHass.callWS({
        type: 'meraki_ha/get_available_cameras',
      }) as { cameras?: Array<{entity_id: string; friendly_name: string}> };
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
      const result = await currentHass.callWS({
        type: 'meraki_ha/get_camera_mappings',
        config_entry_id: configEntryId,
      }) as { mappings?: Record<string, string> };
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
    } catch (err) {
      console.error('Failed to save camera mapping:', err);
    }
  };

  // Get the HA camera proxy URL for a linked camera
  const getLinkedCameraStreamUrl = (entityId: string): string => {
    // HA camera proxy URL format
    return `/api/camera_proxy_stream/${entityId}`;
  };

  // Load camera data when viewing a camera device - only fetch once per device
  React.useEffect(() => {
    const isCameraDevice = device && (device.model?.toUpperCase().startsWith('MV') || device.productType === 'camera');
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

  // Calculate PoE stats for switches
  const poePorts = ports_statuses.filter((p) => p.poe?.isAllocated || p.poe?.enabled);
  const totalPoePower = ports_statuses.reduce((acc, p) => acc + (p.powerUsageInWh || 0), 0);

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
            <span><strong>Model:</strong> {model}</span>
            <span><strong>Serial:</strong> {serial}</span>
            {firmware && <span><strong>Firmware:</strong> {firmware}</span>}
          </div>
        </div>
        <div className={`status-pill ${status?.toLowerCase()}`}>
          <div className="dot"></div>
          {status || 'Unknown'}
        </div>
      </div>

      {/* Info Cards Grid */}
      <div className="cards-grid">
        <div className="info-card">
          <h3>ℹ️ Device Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <div className="label">LAN IP</div>
              <div className="value">{lanIp || '—'}</div>
            </div>
            <div className="info-item">
              <div className="label">MAC Address</div>
              <div className="value mono">{mac || '—'}</div>
            </div>
            <div className="info-item">
              <div className="label">Uptime</div>
              <div className="value">{formatUptime(uptime)}</div>
            </div>
            <div className="info-item">
              <div className="label">Last Seen</div>
              <div className="value">{formatLastSeen(lastReportedAt)}</div>
            </div>
          </div>
        </div>

        {/* Switch-specific Power Summary */}
        {isSwitch && ports_statuses.length > 0 && (
          <div className="info-card">
            <h3>⚡ Power Summary</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Total PoE Power</div>
                <div className="value warning">{totalPoePower.toFixed(1)} W</div>
              </div>
              <div className="info-item">
                <div className="label">PoE Budget</div>
                <div className="value">370 W</div>
              </div>
              <div className="info-item">
                <div className="label">Active PoE Ports</div>
                <div className="value">{poePorts.length} of {ports_statuses.length}</div>
              </div>
              <div className="info-item">
                <div className="label">Utilization</div>
                <div className="value success">{((totalPoePower / 370) * 100).toFixed(1)}%</div>
              </div>
            </div>
          </div>
        )}

        {/* Sensor-specific Battery Info */}
        {isSensor && readings && (
          <div className="info-card">
            <h3>🔋 Sensor Status</h3>
            <div className="info-grid">
              <div className="info-item">
                <div className="label">Battery</div>
                <div className="value success">{readings.battery || 98}%</div>
              </div>
              <div className="info-item">
                <div className="label">Last Update</div>
                <div className="value">{formatLastSeen(lastReportedAt)}</div>
              </div>
              <div className="info-item">
                <div className="label">Network</div>
                <div className="value">Main Office</div>
              </div>
              <div className="info-item">
                <div className="label">Uptime</div>
                <div className="value">{formatUptime(uptime)}</div>
              </div>
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
              min={0}
              max={50}
              status="normal"
            />
          )}
          {readings.humidity != null && (
            <SensorReading
              type="humidity"
              value={readings.humidity}
              min={0}
              max={100}
              status="normal"
            />
          )}
        </div>
      )}

      {/* Status Messages */}
      {status_messages.length > 0 && (
        <div className="info-card" style={{ borderLeft: '4px solid var(--warning)' }}>
          <h3>⚠️ Status Messages</h3>
          <ul style={{ margin: 0, paddingLeft: '20px', color: 'var(--text-secondary)' }}>
            {status_messages.map((msg: string, index: number) => (
              <li key={index} style={{ marginBottom: '8px' }}>
                {msg}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Entities */}
      {entities.length > 0 && (
        <div className="info-card">
          <h3>🔗 Entities</h3>
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
                  <td style={{ fontFamily: 'monospace', fontSize: '13px', color: 'var(--text-muted)' }}>
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

      {/* Camera-specific View */}
      {isCamera && (
        <div className="info-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
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
                fontSize: '13px'
              }}
            >
              ⚙️ Link Camera
            </button>
          </div>

          {/* Camera Linking Configuration */}
          {showCameraConfig && (
            <div style={{
              background: 'var(--bg-primary)',
              borderRadius: 'var(--radius-md)',
              padding: '16px',
              marginBottom: '16px',
              border: '1px solid var(--border)'
            }}>
              <h4 style={{ margin: '0 0 12px 0', fontSize: '14px' }}>
                🔗 Link to External Camera (e.g., Blue Iris)
              </h4>
              <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginBottom: '12px' }}>
                Link this Meraki camera to another camera entity in Home Assistant. 
                Useful when RTSP goes to an NVR (like Blue Iris) first.
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
                    fontSize: '14px'
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
                    fontWeight: 500
                  }}
                >
                  Save
                </button>
              </div>
              {linkedCameraId && (
                <p style={{ fontSize: '12px', color: 'var(--success)', marginTop: '8px', marginBottom: 0 }}>
                  ✓ Linked to: {linkedCameraId}
                </p>
              )}
            </div>
          )}
          
          {/* View Toggle - only show if linked camera is configured */}
          {linkedCameraId && (
            <div style={{ 
              display: 'flex', 
              gap: '4px', 
              marginBottom: '16px',
              background: 'var(--bg-primary)',
              borderRadius: 'var(--radius-md)',
              padding: '4px'
            }}>
              <button
                onClick={() => setViewLinkedCamera(false)}
                style={{
                  flex: 1,
                  padding: '8px 16px',
                  borderRadius: 'var(--radius-sm)',
                  border: 'none',
                  background: !viewLinkedCamera ? 'var(--primary)' : 'transparent',
                  color: !viewLinkedCamera ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                  transition: 'all 0.2s'
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
                  background: viewLinkedCamera ? 'var(--primary)' : 'transparent',
                  color: viewLinkedCamera ? 'white' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  fontWeight: 500,
                  transition: 'all 0.2s'
                }}
              >
                🎬 Linked Camera
              </button>
            </div>
          )}
          
          {/* Content Area */}
          <div style={{ 
            background: 'var(--bg-primary)', 
            borderRadius: 'var(--radius-md)',
            padding: '16px',
            textAlign: 'center',
            marginBottom: '16px'
          }}>
            {viewLinkedCamera && linkedCameraId ? (
              /* Linked Camera Stream (e.g., Blue Iris) */
              <div>
                <img
                  src={`/api/camera_proxy/${linkedCameraId}?token=${Date.now()}`}
                  alt={`Linked camera: ${linkedCameraId}`}
                  style={{
                    maxWidth: '100%',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '12px'
                  }}
                />
                <div style={{ 
                  display: 'flex', 
                  gap: '12px', 
                  justifyContent: 'center',
                  flexWrap: 'wrap',
                  marginTop: '12px'
                }}>
                  <button
                    onClick={() => {
                      // Force refresh by updating the image src
                      const img = document.querySelector(`img[alt="Linked camera: ${linkedCameraId}"]`) as HTMLImageElement;
                      if (img) img.src = `/api/camera_proxy/${linkedCameraId}?token=${Date.now()}`;
                    }}
                    style={{
                      padding: '10px 20px',
                      borderRadius: 'var(--radius-md)',
                      border: 'none',
                      background: 'var(--primary)',
                      color: 'white',
                      cursor: 'pointer',
                      fontWeight: 500
                    }}
                  >
                    🔄 Refresh
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
                      fontWeight: 500
                    }}
                  >
                    📺 Open Camera Entity
                  </button>
                </div>
                <p style={{ 
                  fontSize: '12px', 
                  color: 'var(--text-muted)', 
                  marginTop: '12px',
                  marginBottom: 0 
                }}>
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
                      marginBottom: '12px'
                    }}
                  />
                ) : (
                  <div style={{ 
                    padding: '40px', 
                    color: 'var(--text-muted)',
                    fontSize: '48px'
                  }}>
                    📹
                  </div>
                )}
                
                {/* Action Buttons */}
                <div style={{ 
                  display: 'flex', 
                  gap: '12px', 
                  justifyContent: 'center',
                  flexWrap: 'wrap',
                  marginTop: '12px'
                }}>
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
                      gap: '8px'
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
                        gap: '8px'
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
          <div style={{ 
            fontSize: '13px', 
            color: 'var(--text-muted)',
            textAlign: 'center'
          }}>
            <p style={{ margin: '0 0 8px 0' }}>
              💡 <strong>RTSP Streaming:</strong> Enable in Meraki Dashboard → Camera Settings → External RTSP
            </p>
            <p style={{ margin: 0 }}>
              For live streaming in Home Assistant dashboards, use the camera entity
            </p>
          </div>
        </div>
      )}

      {/* Wireless AP-specific View */}
      {isWireless && (
        <div className="info-card">
          <h3>📶 Wireless Access Point</h3>
          <div className="info-grid">
            <div className="info-item">
              <div className="label">Connected Clients</div>
              <div className="value primary">—</div>
            </div>
            <div className="info-item">
              <div className="label">Radio Channels</div>
              <div className="value">2.4 GHz / 5 GHz</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DeviceView;
