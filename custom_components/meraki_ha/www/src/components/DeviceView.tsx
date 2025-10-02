import React from 'react';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const DeviceView: React.FC<DeviceViewProps> = ({ activeView, setActiveView, data }) => {
  const device = data.devices.find((d: any) => d.serial === activeView.deviceId);

  if (!device) {
    return <Typography>Device not found</Typography>;
  }

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
            Device Details
          </Typography>
          <Typography>Name: {device.name || device.mac}</Typography>
          <Typography>Status: {device.status}</Typography>
          <Typography>Model: {device.model}</Typography>
          <Typography>MAC Address: {device.mac}</Typography>
          <Typography>Serial: {device.serial}</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DeviceView;
