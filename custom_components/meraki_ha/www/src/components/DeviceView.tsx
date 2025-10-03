import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';

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
        <Box>
            {filteredDeviceTypes.map(([type, deviceList], index) => (
                <Box key={type} sx={{ mb: index === filteredDeviceTypes.length - 1 ? 0 : 3 }}>
                    <Typography variant="h6" sx={{ mb: 1.5, color: 'text.secondary' }}>
                        {type}
                    </Typography>
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                        {deviceList.map((device: any) => (
                            <Box
                                key={device.serial}
                                sx={{
                                    p: 2,
                                    borderRadius: 1.5,
                                    backgroundColor: 'action.hover',
                                    border: '1px solid',
                                    borderColor: 'divider',
                                }}
                            >
                                <Grid container alignItems="center" spacing={2}>
                                    <Grid item xs={12} sm={6}>
                                        <Typography variant="body1" sx={{ fontWeight: 500 }}>
                                            {device.name || 'Unnamed Device'}
                                        </Typography>
                                    </Grid>
                                    <Grid item xs={12} sm={6} sx={{ textAlign: { sm: 'right' } }}>
                                        <Typography variant="body2" color="text.secondary">
                                            {device.model} ({device.mac})
                                        </Typography>
                                    </Grid>
                                </Grid>
                            </Box>
                        ))}
                    </Box>
                </Box>
            ))}
        </Box>
    );
};

export default DeviceView;