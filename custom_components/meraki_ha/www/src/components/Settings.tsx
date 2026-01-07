import React, { useState } from 'react';

interface SettingsProps {
  hass: any;
  options: Record<string, any>;
  configEntryId: string;
  onClose: () => void;
}

const Settings: React.FC<SettingsProps> = ({
  hass,
  options,
  configEntryId,
  onClose,
}) => {
  const [localOptions, setLocalOptions] = useState(options);
  const [saving, setSaving] = useState(false);

  const handleToggle = (key: string) => {
    setLocalOptions((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (hass) {
        await hass.callWS({
          type: 'meraki_ha/update_options',
          config_entry_id: configEntryId,
          options: localOptions,
        });
      } else {
        console.log('Saving options (dev):', localOptions);
      }
    } catch (e) {
      console.error('Failed to save options:', e);
      alert('Failed to save settings.');
    } finally {
      setSaving(false);
      onClose();
      window.location.reload();
    }
  };

  const sections = [
    {
      key: 'enable_device_status',
      label: 'Device & Entity Model',
      description: 'Enable basic device status and entity modeling.',
    },
    {
      key: 'enable_org_sensors',
      label: 'Organization-Wide Sensors',
      description:
        'Enable sensors that aggregate data across the entire organization.',
    },
    {
      key: 'enable_camera_entities',
      label: 'Camera Entities & Sensors',
      description:
        'Enable cameras and their associated sensors (motion, analytics).',
    },
    {
      key: 'enable_device_sensors',
      label: 'Physical Device Sensors',
      description:
        'Enable sensors for physical device metrics (e.g. MT sensors).',
    },
    {
      key: 'enable_network_sensors',
      label: 'Network Sensors',
      description: 'Enable network-level sensors and switches.',
    },
    {
      key: 'enable_vlan_sensors',
      label: 'VLAN Sensors',
      description: 'Enable VLAN status monitoring.',
    },
    {
      key: 'enable_port_sensors',
      label: 'Appliance Port Sensors',
      description: 'Enable sensors for switch ports and appliance uplinks.',
    },
    {
      key: 'enable_ssid_sensors',
      label: 'SSID Sensors',
      description: 'Enable sensors and switches for SSIDs.',
    },
  ];

  const handleRangeChange = (
    key: string,
    field: 'min' | 'max',
    value: string
  ) => {
    const numValue = parseFloat(value);
    setLocalOptions((prev) => ({
      ...prev,
      sensor_ranges: {
        ...(prev.sensor_ranges || {}),
        [key]: {
          ...(prev.sensor_ranges?.[key] || {}),
          [field]: isNaN(numValue) ? undefined : numValue,
        },
      },
    }));
  };

  const sensorRanges = [
    {
      key: 'temperature',
      label: 'Temperature',
      unit: '°',
      defaultMin: 32,
      defaultMax: 100,
    },
    {
      key: 'humidity',
      label: 'Humidity',
      unit: '%',
      defaultMin: 0,
      defaultMax: 100,
    },
    {
      key: 'co2',
      label: 'CO₂',
      unit: 'ppm',
      defaultMin: 300,
      defaultMax: 2000,
    },
    {
      key: 'tvoc',
      label: 'TVOC',
      unit: 'ppb',
      defaultMin: 0,
      defaultMax: 1000,
    },
    {
      key: 'pm25',
      label: 'PM2.5',
      unit: 'µg/m³',
      defaultMin: 0,
      defaultMax: 150,
    },
    {
      key: 'noise',
      label: 'Noise',
      unit: 'dB',
      defaultMin: 30,
      defaultMax: 100,
    },
  ];

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        background: 'rgba(0, 0, 0, 0.7)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '20px',
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: 'var(--card-bg)',
          border: '1px solid var(--card-border)',
          borderRadius: 'var(--radius-lg)',
          width: '100%',
          maxWidth: '800px',
          maxHeight: '90vh',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: 'var(--shadow-lg)',
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '20px 24px',
            borderBottom: '1px solid var(--card-border)',
          }}
        >
          <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 600 }}>
            ⚙️ Integration Settings
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '20px',
              cursor: 'pointer',
              color: 'var(--text-muted)',
              padding: '4px 8px',
            }}
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div
          style={{
            flex: 1,
            overflowY: 'auto',
            padding: '24px',
          }}
        >
          {/* Entity Toggles Section */}
          <h3
            style={{
              fontSize: '14px',
              fontWeight: 600,
              color: 'var(--text-muted)',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
              marginBottom: '16px',
            }}
          >
            Entity Settings
          </h3>
          <div style={{ marginBottom: '32px' }}>
            {sections.map((section) => (
              <div
                key={section.key}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 0',
                  borderBottom: '1px solid var(--card-border)',
                }}
              >
                <div style={{ flex: 1 }}>
                  <div
                    style={{
                      fontWeight: 500,
                      marginBottom: '2px',
                      color: 'var(--text-primary)',
                    }}
                  >
                    {section.label}
                  </div>
                  <div
                    style={{
                      fontSize: '12px',
                      color: 'var(--text-muted)',
                    }}
                  >
                    {section.description}
                  </div>
                </div>
                <div
                  onClick={() => handleToggle(section.key)}
                  style={{
                    width: '44px',
                    height: '24px',
                    borderRadius: '12px',
                    background:
                      localOptions[section.key] !== false
                        ? 'var(--success)'
                        : 'var(--bg-tertiary)',
                    cursor: 'pointer',
                    position: 'relative',
                    transition: 'background 0.2s',
                    marginLeft: '16px',
                    flexShrink: 0,
                  }}
                >
                  <div
                    style={{
                      position: 'absolute',
                      top: '2px',
                      left:
                        localOptions[section.key] !== false ? '22px' : '2px',
                      width: '20px',
                      height: '20px',
                      borderRadius: '50%',
                      background: 'white',
                      transition: 'left 0.2s',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.3)',
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Sensor Range Configuration */}
          <h3
            style={{
              fontSize: '14px',
              fontWeight: 600,
              color: 'var(--text-muted)',
              textTransform: 'uppercase',
              letterSpacing: '0.5px',
              marginBottom: '8px',
            }}
          >
            Sensor Gauge Ranges
          </h3>
          <p
            style={{
              fontSize: '12px',
              color: 'var(--text-muted)',
              marginBottom: '16px',
            }}
          >
            Customize the min/max values for sensor gauge displays. Leave empty
            for defaults.
          </p>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
              gap: '12px',
            }}
          >
            {sensorRanges.map((range) => {
              const currentRange =
                localOptions.sensor_ranges?.[range.key] || {};
              return (
                <div
                  key={range.key}
                  style={{
                    padding: '12px',
                    background: 'var(--bg-secondary)',
                    borderRadius: 'var(--radius-sm)',
                  }}
                >
                  <div
                    style={{
                      fontWeight: 500,
                      marginBottom: '8px',
                      fontSize: '13px',
                    }}
                  >
                    {range.label} ({range.unit})
                  </div>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <div style={{ flex: 1 }}>
                      <label
                        style={{
                          fontSize: '10px',
                          color: 'var(--text-muted)',
                          textTransform: 'uppercase',
                        }}
                      >
                        Min
                      </label>
                      <input
                        type="number"
                        placeholder={String(range.defaultMin)}
                        value={currentRange.min ?? ''}
                        onChange={(e) =>
                          handleRangeChange(range.key, 'min', e.target.value)
                        }
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--card-border)',
                          background: 'var(--bg-primary)',
                          color: 'var(--text-primary)',
                          fontSize: '13px',
                        }}
                      />
                    </div>
                    <div style={{ flex: 1 }}>
                      <label
                        style={{
                          fontSize: '10px',
                          color: 'var(--text-muted)',
                          textTransform: 'uppercase',
                        }}
                      >
                        Max
                      </label>
                      <input
                        type="number"
                        placeholder={String(range.defaultMax)}
                        value={currentRange.max ?? ''}
                        onChange={(e) =>
                          handleRangeChange(range.key, 'max', e.target.value)
                        }
                        style={{
                          width: '100%',
                          padding: '6px 8px',
                          borderRadius: 'var(--radius-sm)',
                          border: '1px solid var(--card-border)',
                          background: 'var(--bg-primary)',
                          color: 'var(--text-primary)',
                          fontSize: '13px',
                        }}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '12px',
            padding: '16px 24px',
            borderTop: '1px solid var(--card-border)',
          }}
        >
          <button
            onClick={onClose}
            disabled={saving}
            style={{
              padding: '10px 20px',
              borderRadius: 'var(--radius-md)',
              border: '1px solid var(--card-border)',
              background: 'var(--bg-secondary)',
              color: 'var(--text-primary)',
              cursor: 'pointer',
              fontWeight: 500,
              fontSize: '14px',
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={saving}
            style={{
              padding: '10px 20px',
              borderRadius: 'var(--radius-md)',
              border: 'none',
              background: 'var(--primary)',
              color: 'white',
              cursor: 'pointer',
              fontWeight: 500,
              fontSize: '14px',
              opacity: saving ? 0.7 : 1,
            }}
          >
            {saving ? 'Saving...' : 'Save & Reload'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
