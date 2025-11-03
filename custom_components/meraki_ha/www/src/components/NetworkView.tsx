import React, { useState } from 'react';
import Typography from '@mui/material/Typography';
import Collapse from '@mui/material/Collapse';
import IconButton, { IconButtonProps } from '@mui/material/IconButton';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';

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
  color: theme.palette.text.secondary,
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
        <Paper sx={{ p: 2, backgroundColor: 'background.paper', borderRadius: 2 }}>
            <Typography variant="h5" sx={{ mb: 2, color: 'text.primary' }}>
                Networks
            </Typography>
            <Grid container spacing={2}>
                {networks.map((network: any) => {
                    const networkDevices = devices.filter((d: any) => d.networkId === network.id);
                    const isExpanded = expanded === network.id;

                    return (
                        <Grid item xs={12} key={network.id}>
                            <Box
                                sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    cursor: 'pointer',
                                    p: 2,
                                    borderRadius: 1,
                                    backgroundColor: 'action.hover',
                                    '&:hover': {
                                        backgroundColor: 'action.selected',
                                    }
                                }}
                                onClick={() => handleExpandClick(network.id)}
                            >
                                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                                    {network.name}
                                </Typography>
                                <ExpandMore
                                    expand={isExpanded}
                                    aria-expanded={isExpanded}
                                    aria-label="show more"
                                >
                                    <ExpandMoreIcon />
                                </ExpandMore>
                            </Box>
                            <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                                <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'divider' }}>
                                    <DeviceView devices={networkDevices} />
                                </Box>
                            </Collapse>
                        </Grid>
                    );
                })}
            </Grid>
        </Paper>
    );
};

export default NetworkView;