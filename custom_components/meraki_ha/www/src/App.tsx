import React, { useState, useEffect, useMemo } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

import Header from './components/Header';
import NetworkView from './components/NetworkView';
import EventLog from './components/EventLog';
import { createDynamicTheme } from './theme';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

// Define a more complete type for the Home Assistant object
interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
  };
  themes: {
    darkMode: boolean;
  };
}

// Define the types for our data
interface Network {
  id: string;
  name: string;
}

interface Device {
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
}

interface MerakiData {
  networks: Network[];
  devices: Device[];
}

interface AppProps {
  hass: Hass;
  config_entry_id: string;
}

const App: React.FC<AppProps> = ({ hass, config_entry_id }) => {
  const [data, setData] = useState<MerakiData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Create the theme based on Home Assistant's dark mode setting
  const theme = useMemo(() => createDynamicTheme(hass?.themes?.darkMode ?? true), [hass]);

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

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ p: 3, backgroundColor: theme.palette.background.default, minHeight: '100vh' }}>
        <Header />
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
        {!loading && !error && data && (
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <Paper elevation={2} sx={{ p: 2 }}>
                <NetworkView data={data} />
              </Paper>
            </Grid>
            <Grid item xs={12}>
               <Paper elevation={2} sx={{ p: 2 }}>
                <EventLog />
              </Paper>
            </Grid>
          </Grid>
        )}
      </Box>
    </ThemeProvider>
  );
};

export default App;
