import React, { useState } from 'react';

interface Vlan {
  id: string;
  name: string;
  subnet?: string;
  applianceIp?: string;
}

interface VlanTableProps {
  vlans: Vlan[];
}

const VlanTable: React.FC<VlanTableProps> = ({ vlans }) => {
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
            <tr key={vlan.id}>
              <td>{vlan.id}</td>
              <td>{vlan.name}</td>
              <td className="text-mono">{vlan.subnet || '—'}</td>
              <td className="text-mono">{vlan.applianceIp || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VlanTable;
