import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';

import Dashboard from './components/Dashboard';
import DeviceView from './components/DeviceView';
import NetworkView from './components/NetworkView';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

// Define a simplified type for the Home Assistant object
interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
  };
}

// Define the types for our data
interface MerakiData {
  [key: string]: any;
}

interface AppProps {
  hass: Hass;
  config_entry_id: string;
}

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

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

  const renderView = () => {
    switch (activeView.view) {
      case 'dashboard':
        return <Dashboard setActiveView={setActiveView} data={data} />;
      case 'device':
        return <DeviceView activeView={activeView} setActiveView={setActiveView} data={data} />;
      case 'network':
        return <NetworkView activeView={activeView} setActiveView={setActiveView} data={data} />;
      default:
        return <Typography>Unknown view</Typography>;
    }
  };

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Meraki Control
        </Typography>
        {loading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        {!loading && !error && renderView()}
      </Container>
    </ThemeProvider>
  );
};

export default App;