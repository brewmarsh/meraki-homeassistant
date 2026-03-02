import React, { useState } from 'react';
import { safeCallWS } from '../utils/api';
import { WsCommand } from '../types/websocket';
import HaSwitch from './HaSwitch';

interface SettingsProps {
  hass: any;
  options: Record<string, any>;
  configEntryId: string;
}

const Settings: React.FC<SettingsProps> = ({
  hass,
  options,
  configEntryId,
}) => {
  const [localOptions, setLocalOptions] = useState(options);
  const [saving, setSaving] = useState(false);

  const handleToggle = (key: string, checked: boolean) => {
    setLocalOptions((prev) => ({
      ...prev,
      [key]: checked,
    }));
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      if (hass) {
        await safeCallWS(hass, {
          type: WsCommand.UPDATE_OPTIONS,
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
      window.location.reload();
    }
  };

  const sections = [
    {
      key: 'enable_device_status',
      label: 'Device & entity model',
      description: 'Enable basic device status and entity modeling.',
    },
    {
      key: 'enable_org_sensors',
      label: 'Organization-wide sensors',
      description:
        'Enable sensors that aggregate data across the entire organization.',
    },
    {
      key: 'enable_camera_entities',
      label: 'Camera entities & sensors',
      description:
        'Enable cameras and their associated sensors (motion, analytics).',
    },
    {
      key: 'enable_device_sensors',
      label: 'Physical device sensors',
      description: 'Enable sensors for device-specific metrics (e.g. MT sensors).',
    },
    {
      key: 'enable_network_sensors',
      label: 'Network sensors',
      description: 'Enable network-level sensors and switches.',
    },
    {
      key: 'enable_vlan_sensors',
      label: 'VLAN sensors',
      description: 'Enable VLAN status monitoring.',
    },
    {
      key: 'enable_port_sensors',
      label: 'Appliance port sensors',
      description: 'Enable sensors for switch ports and appliance uplinks.',
    },
    {
      key: 'enable_ssid_sensors',
      label: 'SSID sensors',
      description: 'Enable sensors and switches for SSIDs.',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto">
      <ha-card className="bg-[var(--card-background-color)] text-[var(--primary-text-color)] shadow-lg rounded-lg overflow-hidden">
        <div className="p-4 border-b border-[var(--divider-color)] flex justify-between items-center">
          <h2 className="text-xl font-bold">Integration settings</h2>
        </div>
        <div>
          {sections.map((section) => (
            <ha-settings-row key={section.key} className="border-b border-[var(--divider-color)] last:border-0">
              <span slot="heading">{section.label}</span>
              <span slot="description">{section.description}</span>
              <HaSwitch
                checked={localOptions[section.key] !== false}
                onChange={(checked) => handleToggle(section.key, checked)}
              />
            </ha-settings-row>
          ))}
        </div>
        <div className="p-4 flex justify-end gap-4 border-t border-[var(--divider-color)]">
          <button
            onClick={handleSave}
            className="px-4 py-2 rounded bg-[var(--primary-color)] text-white hover:opacity-90 disabled:opacity-50"
            disabled={saving}
          >
            {saving ? 'Saving...' : 'Save & reload'}
          </button>
        </div>
      </ha-card>
    </div>
  );
};

export default Settings;
