import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Collapse from '@mui/material/Collapse';
import IconButton, { IconButtonProps } from '@mui/material/IconButton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import DeviceView from './DeviceView';

interface ExpandMoreProps extends IconButtonProps {
  expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
  marginLeft: 'auto',
  transition: theme.transitions.create('transform', {
    duration: theme.transitions.duration.shortest,
  }),
}));

interface NetworkViewProps {
    data: any;
}

const NetworkView: React.FC<NetworkViewProps> = ({ data }) => {
    const { networks = [], devices = [] } = data;
    const [expanded, setExpanded] = useState<string | false>(false);

    const handleExpandClick = (panel: string) => {
      setExpanded(expanded === panel ? false : panel);
    };

    return (
        <Box>
            {networks.map((network: any) => {
                const networkDevices = devices.filter((d: any) => d.networkId === network.id);
                const isExpanded = expanded === network.id;

                return (
                    <Card key={network.id} sx={{ mb: 2 }}>
                        <Box
                          sx={{ display: 'flex', alignItems: 'center', cursor: 'pointer', p: 2 }}
                          onClick={() => handleExpandClick(network.id)}
                        >
                            <Typography variant="h5">{network.name}</Typography>
                            <ExpandMore
                                expand={isExpanded}
                                aria-expanded={isExpanded}
                                aria-label="show more"
                            >
                                <ExpandMoreIcon />
                            </ExpandMore>
                        </Box>
                        <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                            <CardContent>
                                <DeviceView devices={networkDevices} />
                            </CardContent>
                        </Collapse>
                    </Card>
                );
            })}
        </Box>
    );
};

export default NetworkView;