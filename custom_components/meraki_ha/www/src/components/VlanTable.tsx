import React, { useState, memo } from 'react';

interface Vlan {
  id: string;
  name: string;
  subnet?: string;
  applianceIp?: string;
}

// Memoized VLAN row - only re-renders when this VLAN changes
interface VlanRowProps {
  vlan: Vlan;
}

const VlanRow = memo<VlanRowProps>(
  ({ vlan }) => (
    <tr>
      <td>{vlan.id}</td>
      <td>{vlan.name}</td>
      <td className="text-mono">{vlan.subnet || '—'}</td>
      <td className="text-mono">{vlan.applianceIp || '—'}</td>
    </tr>
  ),
  (prev, next) =>
    prev.vlan.id === next.vlan.id &&
    prev.vlan.name === next.vlan.name &&
    prev.vlan.subnet === next.vlan.subnet &&
    prev.vlan.applianceIp === next.vlan.applianceIp
);

interface VlanTableProps {
  vlans: Vlan[];
}

const VlanTableComponent: React.FC<VlanTableProps> = ({ vlans }) => {
  const [searchTerm, setSearchTerm] = useState('');

  if (!vlans || vlans.length === 0) {
    return null;
  }

  const filteredVlans = vlans.filter(
    (vlan) =>
      vlan.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      vlan.id.includes(searchTerm)
  );

  return (
    <div className="info-card">
      <h3>🔗 VLANs</h3>
      <input
        type="text"
        placeholder="Search VLANs..."
        className="search-input mb-5"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <table className="device-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Subnet</th>
            <th>Appliance IP</th>
          </tr>
        </thead>
        <tbody>
          {filteredVlans.map((vlan) => (
            <VlanRow key={vlan.id} vlan={vlan} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

// Memoize VlanTable to prevent unnecessary re-renders
const VlanTable = memo(VlanTableComponent, (prevProps, nextProps) => {
  if (prevProps.vlans.length !== nextProps.vlans.length) return false;
  return prevProps.vlans.every(
    (vlan, i) =>
      vlan.id === nextProps.vlans[i].id &&
      vlan.name === nextProps.vlans[i].name &&
      vlan.subnet === nextProps.vlans[i].subnet &&
      vlan.applianceIp === nextProps.vlans[i].applianceIp
  );
});

export default VlanTable;
