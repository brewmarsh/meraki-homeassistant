import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import List from '@mui/material/List';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import Collapse from '@mui/material/Collapse';
import ExpandLess from '@mui/icons-material/ExpandLess';
import ExpandMore from '@mui/icons-material/ExpandMore';
import DeviceView from './DeviceView'; // Assuming DeviceView is in the same directory
import Box from '@mui/material/Box';

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
  networkId?: string; // networkId is optional on devices
}

interface NetworkViewProps {
  data: {
    networks: Network[];
    devices: Device[];
  };
}

const NetworkView: React.FC<NetworkViewProps> = ({ data }) => {
  const [openNetworkId, setOpenNetworkId] = useState<string | null>(null);

  const handleNetworkClick = (networkId: string) => {
    setOpenNetworkId(openNetworkId === networkId ? null : networkId);
  };

  const { networks, devices } = data;

  if (!networks || networks.length === 0) {
    return <Typography>No networks found.</Typography>;
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Networks
      </Typography>
      <List component="nav">
        {networks.map((network) => (
          <React.Fragment key={network.id}>
            <ListItemButton onClick={() => handleNetworkClick(network.id)}>
              <ListItemText primary={network.name} />
              {openNetworkId === network.id ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
            <Collapse in={openNetworkId === network.id} timeout="auto" unmountOnExit>
              <Box sx={{ pl: 4, py: 1 }}>
                <DeviceView devices={devices.filter((d) => d.networkId === network.id)} />
              </Box>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default NetworkView;
