import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CircularProgress from '@mui/material/CircularProgress';

interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
  };
}

interface CameraViewProps {
  hass: Hass;
  config_entry_id: string;
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const CameraView: React.FC<CameraViewProps> = ({ hass, config_entry_id, activeView, setActiveView, data }) => {
  const device = data.devices.find((d: any) => d.serial === activeView.deviceId);
  const [streamUrl, setStreamUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);


  if (!device) {
    return <Typography>Camera not found</Typography>;
  }

  const fetchStreamUrl = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await hass.connection.sendMessagePromise({
        type: 'meraki_ha/get_camera_stream_url',
        config_entry_id: config_entry_id,
        serial: device.serial,
      });
      setStreamUrl(result.url);
    } catch (err: any) {
      console.error('Error fetching camera stream URL:', err);
      setError(`Failed to fetch stream URL: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => setActiveView({ view: 'dashboard' })}
        sx={{ mb: 2 }}
      >
        Back to Dashboard
      </Button>
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Camera: {device.name || device.mac}
          </Typography>
          <Button variant="contained" onClick={fetchStreamUrl} disabled={loading}>
            Get RTSP Stream URL
          </Button>
          {loading && <CircularProgress size={24} sx={{ ml: 2 }} />}
          {error && <Typography color="error" sx={{ mt: 2 }}>{error}</Typography>}
          {streamUrl && (
            <Box sx={{ mt: 2 }}>
              <Typography>RTSP Stream URL:</Typography>
              <Typography component="pre" sx={{ wordBreak: 'break-all' }}>
                {streamUrl}
              </Typography>
                <Typography variant="caption">
                    You can open this URL with a media player that supports RTSP streams, like VLC.
                </Typography>
            </Box>
          )}
          {!streamUrl && streamUrl !== null && !loading && (
            <Typography sx={{ mt: 2 }}>
                No stream URL available for this camera. It might be an unsupported model (e.g., MV2 series) or offline.
            </Typography>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

export default CameraView;