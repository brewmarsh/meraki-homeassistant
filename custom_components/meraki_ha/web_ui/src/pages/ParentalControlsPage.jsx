import { useState, useEffect } from 'react';

function ParentalControlsPage() {
  const [contentFilteringPolicies, setContentFilteringPolicies] = useState([]);
  const [selectedPolicy, setSelectedPolicy] = useState('');
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [networkId, setNetworkId] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);

        // First, get the list of networks to find a networkId
        const networksResponse = await fetch('/api/networks');
        const networksData = await networksResponse.json();
        if (networksData.length > 0) {
          const firstNetworkId = networksData[0].id;
          setNetworkId(firstNetworkId);

          // Fetch content filtering settings
          const contentFilteringResponse = await fetch(`/api/networks/${firstNetworkId}/appliance/contentFiltering`);
          const contentFilteringData = await contentFilteringResponse.json();
          // Assuming the API returns a list of policies. This might need adjustment.
          setContentFilteringPolicies(contentFilteringData.allowedUrlPatterns || ['Kids', 'Homework', 'Standard']);
          setSelectedPolicy(contentFilteringData.urlCategoryListSize || 'topSites');

          // Fetch clients for the network
          const clientsResponse = await fetch('/api/clients');
          const clientsData = await clientsResponse.json();
          const networkClients = clientsData.filter(c => c.networkId === firstNetworkId);
          setClients(networkClients);
        }

      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handlePolicyChange = (e) => {
    setSelectedPolicy(e.target.value);
  };

  const handleSaveChanges = async () => {
    if (!networkId) return;
    try {
      await fetch(`/api/networks/${networkId}/appliance/contentFiltering`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ urlCategoryListSize: selectedPolicy }),
      });
      alert('Content filtering policy updated successfully!');
    } catch (e) {
      alert(`Error updating policy: ${e.message}`);
    }
  };

  const handleToggleClientBlock = async (client) => {
    if (!networkId) return;
    try {
      const rulesResponse = await fetch(`/api/networks/${networkId}/appliance/firewall/l7FirewallRules`);
      const rulesData = await rulesResponse.json();
      let rules = rulesData.rules || [];

      const ruleComment = `Managed by Home Assistant: ${client.mac}`;
      const existingRuleIndex = rules.findIndex(r => r.comment === ruleComment);

      if (existingRuleIndex > -1) {
        // Rule exists, so we are unblocking (removing the rule)
        rules.splice(existingRuleIndex, 1);
      } else {
        // Rule does not exist, so we are blocking (adding the rule)
        rules.push({
          policy: 'deny',
          type: 'host',
          value: client.ip,
          comment: ruleComment,
        });
      }

      await fetch(`/api/networks/${networkId}/appliance/firewall/l7FirewallRules`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ rules: rules }),
      });

      // Optimistically update UI
      setClients(clients.map(c =>
        c.id === client.id ? { ...c, blocked: existingRuleIndex === -1 } : c
      ));

      alert(`Client ${client.description || client.mac} has been ${existingRuleIndex > -1 ? 'unblocked' : 'blocked'}.`);

    } catch (e) {
      alert(`Error updating firewall rule: ${e.message}`);
    }
  };

  if (loading) return <p className="text-center">Loading parental controls...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-light-card dark:bg-dark-card shadow rounded-lg mb-6">
        <div className="p-6">
          <h2 className="text-2xl font-bold mb-4">Content Filtering</h2>
          <div className="flex items-center space-x-4">
            <label htmlFor="policy-select" className="font-medium">Network Policy:</label>
            <select
              id="policy-select"
              value={selectedPolicy}
              onChange={handlePolicyChange}
              className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-light-border dark:border-dark-border focus:outline-none focus:ring-cisco-blue focus:border-cisco-blue sm:text-sm rounded-md bg-light-background dark:bg-dark-background"
            >
              {contentFilteringPolicies.map(policy => (
                <option key={policy} value={policy}>{policy}</option>
              ))}
            </select>
            <button
              onClick={handleSaveChanges}
              className="px-4 py-2 bg-cisco-blue text-white font-semibold rounded-md shadow-sm hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cisco-blue"
            >
              Save
            </button>
          </div>
        </div>
      </div>

      <div className="bg-light-card dark:bg-dark-card shadow rounded-lg">
        <div className="p-6">
          <h2 className="text-2xl font-bold">Client Devices</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-light-border dark:divide-dark-border">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Name</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">IP Address</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Internet Access</th>
              </tr>
            </thead>
            <tbody className="bg-light-card dark:bg-dark-card divide-y divide-light-border dark:divide-dark-border">
              {clients.map((client) => (
                <tr key={client.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">{client.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">{client.ip}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <button
                      onClick={() => handleToggleClientBlock(client.id)}
                      className={`relative inline-flex flex-shrink-0 h-6 w-11 border-2 border-transparent rounded-full cursor-pointer transition-colors ease-in-out duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cisco-blue ${client.blocked ? 'bg-red-600' : 'bg-green-500'}`}
                    >
                      <span
                        aria-hidden="true"
                        className={`inline-block h-5 w-5 rounded-full bg-white shadow transform ring-0 transition ease-in-out duration-200 ${client.blocked ? 'translate-x-5' : 'translate-x-0'}`}
                      />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default ParentalControlsPage;
