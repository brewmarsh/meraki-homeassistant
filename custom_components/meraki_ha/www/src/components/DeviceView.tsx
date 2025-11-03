import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Divider from '@mui/material/Divider';

interface Device {
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
}

interface DeviceViewProps {
  devices: Device[];
}

const DeviceView: React.FC<DeviceViewProps> = ({ devices }) => {
  if (!devices || devices.length === 0) {
    return <Typography variant="body2">No devices found in this network.</Typography>;
  }

  return (
    <Box sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        Devices
      </Typography>
      <Paper elevation={1}>
        <List dense>
          {devices.map((device, index) => (
            <React.Fragment key={device.serial}>
              <ListItem>
                <ListItemText
                  primary={device.name || 'Unnamed Device'}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="text.primary">
                        Model: {device.model} | Status: {device.status}
                      </Typography>
                      <br />
                      {device.lanIp && `IP: ${device.lanIp} | `}
                      {device.mac && `MAC: ${device.mac}`}
                    </>
                  }
                />
              </ListItem>
              {index < devices.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default DeviceView;
