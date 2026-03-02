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
    <div className="bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md mb-4 border border-light-border dark:border-dark-border">
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
        className="w-full p-2 mb-4 border rounded-lg bg-light-background dark:bg-dark-background dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-[var(--primary-color)] text-[var(--primary-text-color)]"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead>
            <tr className="border-b border-light-border dark:border-dark-border">
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
                className="border-b border-light-border dark:border-dark-border hover:bg-light-hover dark:hover:bg-dark-hover"
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
    </div>
  );
};

export default VlanTable;
