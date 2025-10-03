import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

const EventLog: React.FC = () => {
  return (
    <Box sx={{ mt: 4 }}>
        <Typography variant="h5" component="h2" sx={{ mb: 2 }}>
            Event Log
        </Typography>
        <Card
            sx={{
                borderRadius: 2,
                boxShadow: 'none',
                border: '1px solid',
                borderColor: 'rgba(255, 255, 255, 0.12)',
            }}
        >
            <CardContent sx={{ p: 2.5 }}>
                <Typography color="text.secondary">
                    Integration-specific events will be displayed here.
                </Typography>
            </CardContent>
        </Card>
    </Box>
  );
};

export default EventLog;