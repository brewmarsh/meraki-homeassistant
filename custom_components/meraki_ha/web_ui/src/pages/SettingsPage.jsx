import { useState, useEffect } from 'react';
import {
    CONF_SCAN_INTERVAL,
    CONF_DEVICE_NAME_FORMAT,
    CONF_AUTO_ENABLE_RTSP,
    CONF_USE_LAN_IP_FOR_RTSP,
    CONF_ENABLE_DEVICE_TRACKER,
    CONF_HIDE_UNCONFIGURED_SSIDS,
    CONF_IGNORED_NETWORKS
} from '../const';

function SettingsPage() {
  const [settings, setSettings] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saveStatus, setSaveStatus] = useState('');

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/settings');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setSettings(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchSettings();
  }, []);

  const handleSave = async () => {
    setSaveStatus('Saving...');
    try {
      const response = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(settings),
      });
      if (!response.ok) throw new Error('Failed to save settings.');
      setSaveStatus('Settings saved successfully! The integration will now reload.');
    } catch (e) {
      setSaveStatus(`Error: ${e.message}`);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const finalValue = type === 'checkbox' ? checked : (type === 'number' ? parseInt(value, 10) : value);
    setSettings(prev => ({ ...prev, [name]: finalValue }));
  };

  if (loading) return <p className="text-center">Loading settings...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  const renderToggle = (name, label, description) => (
    <div className="flex items-start">
      <div className="flex items-center h-5">
        <input
          id={name}
          name={name}
          type="checkbox"
          className="focus:ring-cisco-blue h-4 w-4 text-cisco-blue border-gray-300 rounded"
          checked={settings[name] || false}
          onChange={handleChange}
        />
      </div>
      <div className="ml-3 text-sm">
        <label htmlFor={name} className="font-medium">{label}</label>
        <p className="text-gray-500 dark:text-gray-400">{description}</p>
      </div>
    </div>
  );

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-light-card dark:bg-dark-card shadow rounded-lg">
        <form onSubmit={(e) => { e.preventDefault(); handleSave(); }} className="p-6 space-y-8">
          <div>
            <h2 className="text-2xl font-bold" data-testid="settings-header">Integration Settings</h2>
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
              Changes will be applied after saving, which reloads the integration.
            </p>
          </div>

          <div className="space-y-6">
            <div>
              <label htmlFor="scan_interval" className="block text-sm font-medium">Scan Interval (seconds)</label>
              <input
                type="number"
                name="scan_interval"
                id="scan_interval"
                className="mt-1 block w-full border border-light-border dark:border-dark-border rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-cisco-blue focus:border-cisco-blue sm:text-sm bg-light-background dark:bg-dark-background"
                value={settings.scan_interval || 300}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="device_name_format" className="block text-sm font-medium">Device Name Format</label>
              <select
                id="device_name_format"
                name="device_name_format"
                className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-light-border dark:border-dark-border focus:outline-none focus:ring-cisco-blue focus:border-cisco-blue sm:text-sm rounded-md bg-light-background dark:bg-dark-background"
                value={settings.device_name_format || 'prefix'}
                onChange={handleChange}
              >
                <option>prefix</option>
                <option>suffix</option>
                <option>omit</option>
              </select>
            </div>

            <fieldset className="space-y-5">
              {renderToggle('enable_device_tracker', 'Enable Device Tracker', 'Track network clients as devices in Home Assistant.')}
              {renderToggle('hide_unconfigured_ssids', 'Hide Unconfigured SSIDs', 'Only show data for SSIDs that are enabled.')}
              {renderToggle('auto_enable_rtsp', 'Auto-enable Camera RTSP', 'Automatically enable RTSP streams for all compatible cameras.')}
              {renderToggle('use_lan_ip_for_rtsp', 'Use LAN IP for RTSP Stream', 'Use the camera\'s LAN IP instead of the public IP for RTSP (requires local network access).')}
            </fieldset>

            <div>
              <label htmlFor="ignored_networks" className="block text-sm font-medium">Ignored Networks</label>
              <p className="text-sm text-gray-500 dark:text-gray-400">Comma-separated list of network names to ignore completely.</p>
              <textarea
                id="ignored_networks"
                name="ignored_networks"
                rows={3}
                className="mt-1 block w-full shadow-sm sm:text-sm border-light-border dark:border-dark-border rounded-md bg-light-background dark:bg-dark-background"
                value={settings.ignored_networks || ''}
                onChange={handleChange}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="px-4 py-2 bg-cisco-blue text-white font-semibold rounded-md shadow-sm hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cisco-blue"
            >
              Save Settings
            </button>
            {saveStatus && <p className="text-sm text-gray-600 dark:text-gray-300 mt-2">{saveStatus}</p>}
          </div>
        </form>
      </div>
    </div>
  );
}

export default SettingsPage;
