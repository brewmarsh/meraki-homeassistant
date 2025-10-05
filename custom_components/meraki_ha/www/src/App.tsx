import React, { useState, useEffect, useMemo } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import CircularProgress from '@mui/material/CircularProgress';
import Alert from '@mui/material/Alert';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';

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
      <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
        <Paper
          square
          elevation={1}
          sx={{
            p: 2,
            backgroundColor: 'var(--app-header-background-color, #18bcf2)',
            color: 'var(--app-header-text-color, #fff)',
          }}
        >
          <Typography variant="h4" component="h1">
            Meraki Integration Control
          </Typography>
        </Paper>
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
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
            <>
              <NetworkView data={data} />
              <EventLog />
            </>
          )}
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default App;