import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';

const EventLog: React.FC = () => {
  return (
    <Card sx={{ mt: 4 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Event Log
        </Typography>
        <Typography>
          Integration-specific events will be displayed here.
        </Typography>
      </CardContent>
    </Card>
  );
};

export default EventLog;