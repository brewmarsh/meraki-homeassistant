import React, { useState } from 'react';

interface SettingsProps {
  hass: any; // Add hass to props
  options: Record<string, any>;
  configEntryId: string;
  onClose: () => void;
}

const Settings: React.FC<SettingsProps> = ({
  hass, // Destructure hass from props
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
      // Use the hass prop directly
      if (hass) {
        await hass.callWS({
          type: 'meraki_ha/update_options',
          config_entry_id: configEntryId,
          options: localOptions,
        });
      } else {
        // Fallback for dev/standalone mode
        console.log('Saving options (dev):', localOptions);
      }
    } catch (e) {
      console.error('Failed to save options:', e);
      alert('Failed to save settings.');
    } finally {
      setSaving(false);
      onClose();
      // Reload to apply changes
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

  // Sensor range options
  const handleRangeChange = (key: string, field: 'min' | 'max', value: string) => {
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
    { key: 'temperature', label: 'Temperature', unit: '°', defaultMin: 32, defaultMax: 100 },
    { key: 'humidity', label: 'Humidity', unit: '%', defaultMin: 0, defaultMax: 100 },
    { key: 'co2', label: 'CO₂', unit: 'ppm', defaultMin: 300, defaultMax: 2000 },
    { key: 'tvoc', label: 'TVOC', unit: 'ppb', defaultMin: 0, defaultMax: 1000 },
    { key: 'pm25', label: 'PM2.5', unit: 'µg/m³', defaultMin: 0, defaultMax: 150 },
    { key: 'noise', label: 'Noise', unit: 'dB', defaultMin: 30, defaultMax: 100 },
  ];

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50 p-4">
      <ha-card class="p-6 w-full max-w-2xl bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-lg rounded-lg" style={{ maxHeight: '90vh', display: 'flex', flexDirection: 'column' }}>
        <div className="card-header flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Integration Settings</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <ha-icon icon="mdi:close"></ha-icon>
          </button>
        </div>
        <div className="card-content overflow-y-auto" style={{ flex: 1 }}>
          {/* Entity Toggles Section */}
          <h3 className="text-lg font-semibold mb-3 text-gray-700 dark:text-gray-300">Entity Settings</h3>
          <div className="space-y-3 mb-6">
            {sections.map((section) => (
              <div
                key={section.key}
                className="flex items-center justify-between p-2 border-b border-gray-200 dark:border-gray-700"
              >
                <div className="flex flex-col">
                  <span className="font-medium">{section.label}</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {section.description}
                  </span>
                </div>
                <ha-switch
                  checked={localOptions[section.key] !== false} // Default to true if undefined
                  onClick={(e: any) => {
                    e.stopPropagation();
                    handleToggle(section.key);
                  }}
                ></ha-switch>
              </div>
            ))}
          </div>

          {/* Sensor Range Configuration */}
          <h3 className="text-lg font-semibold mb-3 text-gray-700 dark:text-gray-300">Sensor Gauge Ranges</h3>
          <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">
            Customize the min/max values for sensor gauge displays. Leave empty for defaults.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {sensorRanges.map((range) => {
              const currentRange = localOptions.sensor_ranges?.[range.key] || {};
              return (
                <div key={range.key} className="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="font-medium mb-2">{range.label} ({range.unit})</div>
                  <div className="flex gap-3">
                    <div className="flex-1">
                      <label className="text-xs text-gray-500 dark:text-gray-400">Min</label>
                      <input
                        type="number"
                        className="w-full px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm"
                        placeholder={String(range.defaultMin)}
                        value={currentRange.min ?? ''}
                        onChange={(e) => handleRangeChange(range.key, 'min', e.target.value)}
                      />
                    </div>
                    <div className="flex-1">
                      <label className="text-xs text-gray-500 dark:text-gray-400">Max</label>
                      <input
                        type="number"
                        className="w-full px-2 py-1 rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm"
                        placeholder={String(range.defaultMax)}
                        value={currentRange.max ?? ''}
                        onChange={(e) => handleRangeChange(range.key, 'max', e.target.value)}
                      />
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        <div className="card-actions flex justify-end mt-4 gap-4 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded border border-gray-300 text-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:text-gray-300 dark:hover:bg-gray-700"
            disabled={saving}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save & Reload'}
          </button>
        </div>
      </ha-card>
    </div>
  );
};

export default Settings;
