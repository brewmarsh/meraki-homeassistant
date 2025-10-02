import React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

interface StatusCardProps {
  title: string;
  value: number | string;
  icon: React.ReactNode;
}

const StatusCard: React.FC<StatusCardProps> = ({ title, value, icon }) => {
  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Box sx={{ fontSize: '2rem', mr: 2 }}>{icon}</Box>
          <div>
            <Typography color="text.secondary">{title}</Typography>
            <Typography variant="h5" component="div">
              {value}
            </Typography>
          </div>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatusCard;
