import React from 'react';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

interface DeviceViewProps {
    devices: any[];
}

const DeviceView: React.FC<DeviceViewProps> = ({ devices }) => {
    const deviceTypes = {
        'Routing': devices.filter(d => d.model?.startsWith('MX')),
        'Switches': devices.filter(d => d.model?.startsWith('MS')),
        'Wireless': devices.filter(d => d.model?.startsWith('MR')),
        'Cameras': devices.filter(d => d.model?.startsWith('MV')),
    };

    const filteredDeviceTypes = Object.entries(deviceTypes).filter(([, deviceList]) => deviceList.length > 0);

    return (
        <Grid container spacing={2}>
            {filteredDeviceTypes.map(([type, deviceList]) => (
                <Grid item xs={12} key={type}>
                    <Typography variant="h6" sx={{ mb: 1, color: 'text.secondary' }}>
                        {type}
                    </Typography>
                    <Grid container spacing={2}>
                        {deviceList.map((device: any) => (
                            <Grid item xs={12} sm={6} md={4} key={device.serial}>
                                <Paper
                                    sx={{
                                        p: 2,
                                        borderRadius: 1,
                                        backgroundColor: 'action.hover',
                                    }}
                                >
                                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                        {device.name || 'Unnamed Device'}
                                    </Typography>
                                    <Typography variant="body2" color="text.secondary">
                                        {device.model} ({device.mac})
                                    </Typography>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </Grid>
            ))}
        </Grid>
    );
};

export default DeviceView;