import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import NetworkView from './components/NetworkView';

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

const App: React.FC<AppProps> = ({ hass, config_entry_id }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<{ view: string; deviceId?: string; networkId?: string }>({ view: 'dashboard' });

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

  const renderView = () => {
    switch (activeView.view) {
      case 'dashboard':
        return <Dashboard setActiveView={setActiveView} data={data} />;
      case 'device':
        return <DeviceView activeView={activeView} setActiveView={setActiveView} data={data} />;
      case 'network':
        return <NetworkView activeView={activeView} setActiveView={setActiveView} data={data} />;
      default:
        return <Dashboard setActiveView={setActiveView} data={data} />;
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Meraki HA Web UI</h1>
      {renderView()}
    </div>
  );
};

export default App;
