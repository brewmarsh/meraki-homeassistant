import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import NetworkView from './components/NetworkView';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

const App: React.FC = () => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState<{ view: string; deviceId?: string; networkId?: string }>({ view: 'dashboard' });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/config');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setData(result);
      } catch (e) {
        console.error('Error fetching Meraki data:', e);
        if (e instanceof Error) {
            setError(`Failed to fetch Meraki data: ${e.message}`);
        } else {
            setError('An unknown error occurred while fetching data.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

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
