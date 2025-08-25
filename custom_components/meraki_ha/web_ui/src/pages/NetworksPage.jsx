import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function NetworksPage() {
  const [networks, setNetworks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNetworks = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/networks');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setNetworks(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };
    fetchNetworks();
  }, []);

  const handleIgnore = async (networkName) => {
    try {
      // First, fetch the current settings
      const settingsResponse = await fetch('/api/settings');
      if (!settingsResponse.ok) {
        throw new Error('Failed to fetch current settings.');
      }
      const currentSettings = await settingsResponse.json();

      // Update the ignored_networks list
      const ignoredNetworks = currentSettings.ignored_networks || '';
      const ignoredList = ignoredNetworks ? ignoredNetworks.split(',').map(n => n.trim()) : [];
      if (!ignoredList.includes(networkName)) {
        ignoredList.push(networkName);
      }
      const newIgnoredNetworks = ignoredList.join(', ');

      // Create the new settings payload
      const newSettings = { ...currentSettings, ignored_networks: newIgnoredNetworks };

      // Now, post the updated settings
      const postResponse = await fetch('/api/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newSettings),
      });

      if (!postResponse.ok) {
        throw new Error('Failed to save updated settings.');
      }

      // Optionally, refetch networks to update the UI or just filter it out locally
      setNetworks(networks.filter(n => n.name !== networkName));
      alert(`Network "${networkName}" has been ignored. The integration will now reload.`);

    } catch (e) {
      alert(`Error ignoring network: ${e.message}`);
    }
  };

  if (loading) return <p className="text-center">Loading networks...</p>;
  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-light-card dark:bg-dark-card shadow rounded-lg">
        <div className="p-6">
          <h2 className="text-2xl font-bold">Networks</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-light-border dark:divide-dark-border">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Name</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Product Types</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Tags</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-light-card dark:bg-dark-card divide-y divide-light-border dark:divide-dark-border">
              {networks.map((network) => (
                <tr key={network.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <Link to={`/networks/${network.id}`} className="text-cisco-blue hover:underline">
                      {network.name}
                    </Link>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {network.productTypes.join(', ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                    {network.tags.join(', ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <button onClick={() => handleIgnore(network.name)} className="text-red-600 hover:text-red-900">Ignore</button>
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

export default NetworksPage;
