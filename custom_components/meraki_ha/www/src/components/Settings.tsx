import React, { useState, useEffect, memo } from 'react';

interface SettingsProps {
  hass: any;
  options: Record<string, any>;
  configEntryId: string;
  onClose: () => void;
}

type ThemeMode = 'auto' | 'dark' | 'light';

const THEME_STORAGE_KEY = 'meraki_ha_theme_mode';

const SettingsComponent: React.FC<SettingsProps> = ({
  hass,
  options,
  configEntryId,
  onClose,
}) => {
  const [localOptions, setLocalOptions] = useState(options);
  const [saving, setSaving] = useState(false);
  const [themeMode, setThemeMode] = useState<ThemeMode>('auto');

  // Load theme preference from localStorage on mount
  useEffect(() => {
    const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) as ThemeMode;
    if (savedTheme && ['auto', 'dark', 'light'].includes(savedTheme)) {
      setThemeMode(savedTheme);
    }
  }, []);

  const handleThemeModeChange = (mode: ThemeMode) => {
    setThemeMode(mode);
    localStorage.setItem(THEME_STORAGE_KEY, mode);
    // Dispatch event so the theme hook can react immediately
    window.dispatchEvent(
      new CustomEvent('meraki-theme-change', { detail: mode })
    );
  };

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
    <div className="settings-overlay" onClick={onClose}>
      <div className="settings-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="settings-header">
          <h2>⚙️ Integration Settings</h2>
          <button className="settings-close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="settings-content">
          {/* Theme Mode Section */}
          <h3 className="section-label">Appearance</h3>
          <div className="settings-section">
            <div className="settings-row">
              <div className="settings-row-info">
                <div className="settings-row-label">Theme Mode</div>
                <div className="settings-row-description">
                  Choose dark, light, or auto-detect from Home Assistant theme.
                </div>
              </div>
              <div className="theme-toggle-group">
                {(['auto', 'dark', 'light'] as ThemeMode[]).map((mode) => (
                  <button
                    key={mode}
                    onClick={() => handleThemeModeChange(mode)}
                    className={`theme-toggle-btn ${
                      themeMode === mode ? 'active' : ''
                    }`}
                  >
                    {mode === 'auto'
                      ? '🔄 Auto'
                      : mode === 'dark'
                      ? '🌙 Dark'
                      : '☀️ Light'}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Entity Toggles Section */}
          <h3 className="section-label">Entity Settings</h3>
          <div className="settings-section">
            {sections.map((section) => (
              <div key={section.key} className="settings-row">
                <div className="settings-row-info">
                  <div className="settings-row-label">{section.label}</div>
                  <div className="settings-row-description">
                    {section.description}
                  </div>
                </div>
                <div
                  className={`toggle-switch ${
                    localOptions[section.key] !== false ? 'on' : 'off'
                  }`}
                  onClick={() => handleToggle(section.key)}
                >
                  <div className="toggle-knob" />
                </div>
              </div>
            ))}
          </div>

          {/* Sensor Range Configuration */}
          <h3 className="section-label">Sensor Gauge Ranges</h3>
          <p className="description">
            Customize the min/max values for sensor gauge displays. Leave empty
            for defaults.
          </p>
          <div className="sensor-ranges-grid">
            {sensorRanges.map((range) => {
              const currentRange =
                localOptions.sensor_ranges?.[range.key] || {};
              return (
                <div key={range.key} className="sensor-range-card">
                  <div className="sensor-range-label">
                    {range.label} ({range.unit})
                  </div>
                  <div className="sensor-range-inputs">
                    <div className="sensor-range-input">
                      <label className="field-label">Min</label>
                      <input
                        type="number"
                        placeholder={String(range.defaultMin)}
                        value={currentRange.min ?? ''}
                        onChange={(e) =>
                          handleRangeChange(range.key, 'min', e.target.value)
                        }
                      />
                    </div>
                    <div className="sensor-range-input">
                      <label className="field-label">Max</label>
                      <input
                        type="number"
                        placeholder={String(range.defaultMax)}
                        value={currentRange.max ?? ''}
                        onChange={(e) =>
                          handleRangeChange(range.key, 'max', e.target.value)
                        }
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Footer */}
        <div className="settings-footer">
          <button
            className="btn btn-secondary"
            onClick={onClose}
            disabled={saving}
          >
            Cancel
          </button>
          <button
            className="btn btn-primary"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save & Reload'}
          </button>
        </div>
      </div>
    </div>
  );
};

// Memoize Settings - re-render only when options change
const Settings = memo(SettingsComponent);

export default Settings;
