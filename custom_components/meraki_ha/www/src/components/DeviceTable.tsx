import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

interface DeviceTableProps {
  devices: any[];
  setActiveView: (view: { view: string; deviceId?: string }) => void;
}

const DeviceTable: React.FC<DeviceTableProps> = ({ devices, setActiveView }) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>Model</TableCell>
            <TableCell>MAC Address</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {devices.map((device) => (
            <TableRow
              key={device.serial}
              onClick={() => {
                const view = device.model?.startsWith('MV') ? 'camera' : 'device';
                setActiveView({ view, deviceId: device.serial });
              }}
              sx={{ cursor: 'pointer', '&:hover': { backgroundColor: 'action.hover' } }}
            >
              <TableCell component="th" scope="row">
                {device.name || device.mac}
              </TableCell>
              <TableCell>{device.status}</TableCell>
              <TableCell>{device.model}</TableCell>
              <TableCell>{device.mac}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default DeviceTable;
