import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import NetworkView from './components/NetworkView';

// The Hass object is no longer used

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {
  // No props are needed now
}

const App: React.FC<AppProps> = () => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<{ view: string; deviceId?: string; networkId?: string }>({ view: 'dashboard' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Use a relative path to fetch all data from the integration's web server
        const response = await fetch('/api/all_data');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setData(data);
      } catch (err) {
        console.error('Error fetching Meraki data:', err);
        setError(err instanceof Error ? err.message : 'An unknown error occurred.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []); // The empty dependency array means this effect runs once on mount.

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
