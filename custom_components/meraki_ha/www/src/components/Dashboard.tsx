import React from 'react';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import DevicesIcon from '@mui/icons-material/Devices';
import WifiIcon from '@mui/icons-material/Wifi';
import RouterIcon from '@mui/icons-material/Router';
import VideocamIcon from '@mui/icons-material/Videocam';
import WifiTetheringIcon from '@mui/icons-material/WifiTethering';

import StatusCard from './StatusCard';
import DeviceTable from './DeviceTable';

interface DashboardProps {
  setActiveView: (view: { view: string; deviceId?: string; networkId?: string }) => void;
  data: any;
}

const Dashboard: React.FC<DashboardProps> = ({ setActiveView, data }) => {
  if (!data) {
    return <Typography>Loading dashboard...</Typography>;
  }

  const { devices = [], ssids = [], networks = [] } = data;

  const metrics = {
    totalDevices: devices.length,
    wirelessAps: devices.filter((d: any) => d.model?.startsWith('MR')).length,
    switches: devices.filter((d: any) => d.model?.startsWith('MS')).length,
    cameras: devices.filter((d: any) => d.model?.startsWith('MV')).length,
    ssids: ssids.length,
  };

  return (
    <Grid container spacing={3}>
      {/* Status Cards */}
      <Grid item xs={12} sm={6} md={2.4}>
        <StatusCard title="Total Devices" value={metrics.totalDevices} icon={<DevicesIcon />} />
      </Grid>
      <Grid item xs={12} sm={6} md={2.4}>
        <StatusCard title="Wireless APs" value={metrics.wirelessAps} icon={<WifiIcon />} />
      </Grid>
      <Grid item xs={12} sm={6} md={2.4}>
        <StatusCard title="Switches" value={metrics.switches} icon={<RouterIcon />} />
      </Grid>
      <Grid item xs={12} sm={6} md={2.4}>
        <StatusCard title="Cameras" value={metrics.cameras} icon={<VideocamIcon />} />
      </Grid>
      <Grid item xs={12} sm={6} md={2.4}>
        <StatusCard title="Virtual SSIDs" value={metrics.ssids} icon={<WifiTetheringIcon />} />
      </Grid>

      {/* Networks */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom>
          Networks
        </Typography>
        <Grid container spacing={2}>
          {networks.map((network: any) => (
            <Grid item xs={12} sm={6} md={4} key={network.id}>
              <Card>
                <CardActionArea onClick={() => setActiveView({ view: 'network', networkId: network.id })}>
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                      {network.name}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Grid>

      {/* All Devices Table */}
      <Grid item xs={12}>
        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
          All Devices
        </Typography>
        <DeviceTable devices={devices} setActiveView={setActiveView} />
      </Grid>
    </Grid>
  );
};

export default Dashboard;
