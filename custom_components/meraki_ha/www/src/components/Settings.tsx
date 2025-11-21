import React, { useState } from 'react';

interface SettingsProps {
  options: Record<string, any>;
  configEntryId: string;
  onClose: () => void;
}

const Settings: React.FC<SettingsProps> = ({
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
    // Send update to backend
    try {
      const hass = (window as any).hass;
      if (hass && hass.connection) {
        await hass.connection.sendMessagePromise({
          type: 'meraki_ha/update_options',
          config_entry_id: configEntryId,
          options: localOptions,
        });
      } else {
        // Fallback for dev/standalone mode using a new socket if needed, or just log
        // For now assuming standard HA env for saving
        console.log('Saving options:', localOptions);
      }
    } catch (e) {
      console.error('Failed to save options:', e);
      alert('Failed to save settings.');
    } finally {
      setSaving(false);
      onClose();
      // Optionally reload page or data
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

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <ha-card class="p-6 w-full max-w-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 shadow-lg rounded-lg">
        <div className="card-header flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Integration Settings</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700"
          >
            <ha-icon icon="mdi:close"></ha-icon>
          </button>
        </div>
        <div className="card-content space-y-4 max-h-96 overflow-y-auto">
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
        <div className="card-actions flex justify-end mt-6 gap-4">
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
