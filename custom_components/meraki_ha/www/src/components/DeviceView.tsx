import React from 'react';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';

interface DeviceViewProps {
    devices: any[];
}

const DeviceView: React.FC<DeviceViewProps> = ({ devices }) => {
    const deviceTypes = {
        'Switches': devices.filter(d => d.model?.startsWith('MS')),
        'Wireless': devices.filter(d => d.model?.startsWith('MR')),
        'Cameras': devices.filter(d => d.model?.startsWith('MV')),
        'Routing': devices.filter(d => d.model?.startsWith('MX')),
    };

    return (
        <Box sx={{ pl: 4, pt: 2 }}>
            {Object.entries(deviceTypes).map(([type, deviceList]) => (
                deviceList.length > 0 && (
                    <Box key={type} sx={{ mb: 2 }}>
                        <Typography variant="h6">{type}</Typography>
                        {deviceList.map((device: any) => (
                            <Card key={device.serial} sx={{ mb: 1, backgroundColor: 'background.paper' }}>
                                <CardContent>
                                    <Typography>{device.name || device.mac}</Typography>
                                </CardContent>
                            </Card>
                        ))}
                    </Box>
                )
            ))}
        </Box>
    );
};

export default DeviceView;