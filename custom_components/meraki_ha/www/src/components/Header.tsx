import React from 'react';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';

const Header: React.FC = () => {
  return (
    <Paper
      elevation={2}
      sx={{
        p: 2,
        mb: 3,
        textAlign: 'center',
      }}
    >
      <Typography variant="h4" component="h1">
        Meraki Integration Control
      </Typography>
    </Paper>
  );
};

export default Header;
