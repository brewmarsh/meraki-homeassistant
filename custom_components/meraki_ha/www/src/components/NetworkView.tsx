import React from 'react';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Box from '@mui/material/Box';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

interface NetworkViewProps {
    activeView: { view: string; networkId?: string };
    setActiveView: (view: { view:string; deviceId?: string, networkId?: string }) => void;
    data: any;
}

const NetworkView: React.FC<NetworkViewProps> = ({ activeView, setActiveView, data }) => {
    const network = data.networks.find((n: any) => n.id === activeView.networkId);

    if (!network) {
        return <Typography>Network not found</Typography>;
    }

    return (
        <Box>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => setActiveView({ view: 'dashboard' })}
                sx={{ mb: 2 }}
            >
                Back to Dashboard
            </Button>
            <Card>
                <CardContent>
                    <Typography variant="h6" gutterBottom>
                        Network Information
                    </Typography>
                    <Typography>Name: {network.name}</Typography>
                    <Typography>ID: {network.id}</Typography>
                    <Typography>Product Types: {network.product_types.join(', ')}</Typography>
                </CardContent>
            </Card>
        </Box>
    );
};

export default NetworkView;
