import React from 'react';
import StatusCard from './StatusCard';
import DeviceTable from './DeviceTable';

interface DashboardProps {
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const Dashboard: React.FC<DashboardProps> = ({ setActiveView, data }) => {
  if (!data) {
    return <div>Loading dashboard...</div>;
  }

  const { devices = [], ssids = [] } = data;

  const metrics = {
    totalDevices: devices.length,
    wirelessAps: devices.filter((d: any) => d.model?.startsWith('MR')).length,
    switches: devices.filter((d: any) => d.model?.startsWith('MS')).length,
    cameras: devices.filter((d: any) => d.model?.startsWith('MV')).length,
    ssids: ssids.length,
  };

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-8">
        <StatusCard
          title="Total Devices"
          value={metrics.totalDevices}
          icon="📱"
        />
        <StatusCard
          title="Wireless APs"
          value={metrics.wirelessAps}
          icon="📡"
        />
        <StatusCard title="Switches" value={metrics.switches} icon="🔄" />
        <StatusCard title="Cameras" value={metrics.cameras} icon="📹" />
        <StatusCard title="Virtual SSIDs" value={metrics.ssids} icon="📶" />
      </div>

      <h2 className="text-xl font-semibold mb-4">All Devices</h2>
      <DeviceTable hass={null} devices={devices} setActiveView={setActiveView} />
    </div>
  );
};

export default Dashboard;
