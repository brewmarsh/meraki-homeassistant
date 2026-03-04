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
    <ha-card className="p-4 mb-4">
      <div className="flex items-center mb-4 text-[var(--primary-text-color)]">
        <ha-icon
          icon="mdi:lan-connect"
          style={{ marginRight: '8px', color: 'var(--primary-color)' }}
        ></ha-icon>
        <h3 className="text-lg font-semibold m-0">VLANs</h3>
      </div>
      <input
        type="text"
        placeholder="Search VLANs..."
        className="w-full p-2 mb-4 border border-[var(--divider-color)] rounded-lg bg-[var(--card-background-color)] text-[var(--primary-text-color)] focus:outline-none focus:ring-1 focus:ring-[var(--primary-color)]"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-[var(--divider-color)]">
              <th className="text-left p-4 font-semibold text-[var(--primary-text-color)]">ID</th>
              <th className="text-left p-4 font-semibold text-[var(--primary-text-color)]">Name</th>
              <th className="text-left p-4 font-semibold text-[var(--primary-text-color)]">Subnet</th>
              <th className="text-left p-4 font-semibold text-[var(--primary-text-color)]">Appliance IP</th>
            </tr>
          </thead>
          <tbody>
            {filteredVlans.map((vlan) => (
              <tr
                key={vlan.id}
                className="border-b border-[var(--divider-color)] last:border-0 hover:bg-[var(--secondary-background-color)]"
              >
                <td className="p-4 text-[var(--primary-text-color)]">{vlan.id}</td>
                <td className="p-4 text-[var(--primary-text-color)]">{vlan.name}</td>
                <td className="p-4 text-[var(--primary-text-color)]">{vlan.subnet || '-'}</td>
                <td className="p-4 text-[var(--primary-text-color)]">{vlan.applianceIp || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </ha-card>
  );
};

export default VlanTable;
