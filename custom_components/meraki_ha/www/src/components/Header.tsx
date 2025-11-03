import React from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

const Header: React.FC = () => {
    return (
        <Box sx={{
            backgroundColor: 'background.paper',
            p: 2.5,
            borderBottom: '1px solid',
            borderColor: 'divider',
        }}>
            <Typography variant="h4" component="h1">
                Meraki Integration Control
            </Typography>
        </Box>
    );
};

export default Header;