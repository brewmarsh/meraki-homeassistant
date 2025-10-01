import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import NetworkView from './components/NetworkView';

// Define a simplified type for the Home Assistant object
interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
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

    const fetchData = async () => {
      try {
        const result = await hass.connection.sendMessagePromise({
          type: 'meraki_ha/get_config',
          config_entry_id: config_entry_id,
        });
        setData(result);
      } catch (err: any) {
        console.error('Error fetching Meraki data:', err);
        setError(`Failed to fetch Meraki data: ${err.message || 'Unknown error'}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
        return <div>Unknown view</div>;
    }
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Meraki Control</h1>
      {renderView()}
    </div>
  );
};

export default App;