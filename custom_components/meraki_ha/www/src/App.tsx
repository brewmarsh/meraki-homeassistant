import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';

// Define a simplified type for the Home Assistant object
interface Hass {
  connection: {
    subscribeMessage: (callback: (message: any) => void, subscription: any) => Promise<() => void>;
  };
  // Add other properties of hass object if needed
}

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {
  hass: Hass;
  config_entry_id: string;
}

import ThemeSelector from './components/ThemeSelector';

const App: React.FC<AppProps> = ({ hass, config_entry_id }) => {
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('theme');
    return savedTheme || 'system';
  });

  useEffect(() => {
    localStorage.setItem('theme', theme);

    const root = window.document.documentElement;
    const isDark = theme === 'dark' || (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

    root.classList.toggle('dark', isDark);

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (theme === 'system') {
        root.classList.toggle('dark', mediaQuery.matches);
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [theme]);
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState({ view: 'dashboard', deviceId: undefined });

  useEffect(() => {
    if (!hass || !hass.connection) {
      setError("Home Assistant connection object not found.");
      setLoading(false);
      return;
    }

    const subscribe = async () => {
      try {
        const unsub = await hass.connection.subscribeMessage(
          (message) => {
            if (message.type === 'result') {
              if (message.success) {
                setData(message.result);
              } else {
                setError(`Subscription failed: ${message.error.message}`);
              }
              setLoading(false);
            } else if (message.type === 'event') {
              setData(message.event.data);
            } else {
              setData(message);
              setLoading(false);
            }
          },
          {
            type: 'meraki_ha/subscribe_meraki_data',
            config_entry_id: config_entry_id,
          }
        );
        return unsub;
      } catch (err) {
        console.error('Error subscribing to Meraki data:', err);
        setError('Failed to subscribe to Meraki data. See console for details.');
        setLoading(false);
      }
    };

    const unsubscribePromise = subscribe();

    return () => {
      unsubscribePromise.then(unsub => {
        if (unsub) {
          unsub();
        }
      });
    };
  }, [hass, config_entry_id]);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Meraki HA Web UI</h1>
        <ThemeSelector theme={theme} setTheme={setTheme} />
      </div>
      {activeView.view === 'dashboard' ? (
        <Dashboard setActiveView={setActiveView} data={data} />
      ) : (
        <DeviceView activeView={activeView} setActiveView={setActiveView} data={data} />
      )}
    </div>
  );
};

export default App;
