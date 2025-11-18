import React, { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {}

const App: React.FC<AppProps> = () => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [activeView, setActiveView] = useState({
    view: 'dashboard',
    deviceId: undefined,
  });

  useEffect(() => {
    let accessToken = localStorage.getItem('meraki_ha_llat');
    if (!accessToken) {
      accessToken = prompt(
        'Please enter your Home Assistant Long-Lived Access Token:'
      );
      if (accessToken) {
        localStorage.setItem('meraki_ha_llat', accessToken);
      } else {
        setError('No access token provided.');
        setLoading(false);
        return;
      }
    }

    const haUrl = (window as any).HA_URL.replace(/^http/, 'ws');
    const wsUrl = `${haUrl}/api/websocket`;
    const socket = new WebSocket(wsUrl);
    let messageId = 1;

    socket.onopen = () => {
      console.log('WebSocket connection established');
      socket.send(
        JSON.stringify({
          type: 'auth',
          access_token: accessToken,
        })
      );
    };

    socket.onmessage = (event) => {
      const message = JSON.parse(event.data);

      if (message.type === 'auth_ok') {
        console.log('Authenticated successfully');
        socket.send(
          JSON.stringify({
            id: messageId,
            type: 'meraki_ha/get_config',
            config_entry_id: (window as any).CONFIG_ENTRY_ID,
          })
        );
      } else if (message.type === 'auth_invalid') {
        console.error('Authentication failed:', message.message);
        setError('Authentication failed. Please check your token.');
        setLoading(false);
        localStorage.removeItem('meraki_ha_llat');
      } else if (message.id === messageId) {
        if (message.type === 'result') {
          if (message.success) {
            setData(message.result);
          } else {
            console.error('Failed to fetch Meraki data:', message.error);
            setError(`Failed to fetch Meraki data: ${message.error.message}`);
          }
          setLoading(false);
        }
      }
    };

    socket.onerror = (err) => {
      console.error('WebSocket error:', err);
      setError('WebSocket connection error. See console for details.');
      setLoading(false);
    };

    socket.onclose = () => {
      console.log('WebSocket connection closed');
    };

    return () => {
      if (socket.readyState === 1) {
        socket.close();
      }
    };
  }, []);

  if (loading) {
    return <div className="p-4">Loading...</div>;
  }

  if (error) {
    return <div className="p-4 text-red-500">Error: {error}</div>;
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Meraki HA Web UI</h1>
      {activeView.view === 'dashboard' ? (
        <Dashboard setActiveView={setActiveView} data={data} />
      ) : (
        <DeviceView
          activeView={activeView}
          setActiveView={setActiveView}
          data={data}
        />
      )}
    </div>
  );
};

export default App;
