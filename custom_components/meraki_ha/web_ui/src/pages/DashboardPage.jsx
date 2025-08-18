import { useState, useEffect } from 'react';
import NetworkCard from '../components/NetworkCard';
import ClientCard from '../components/ClientCard';

function DashboardPage() {
  const [networks, setNetworks] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const networksResponse = await fetch('/api/networks');
        if (!networksResponse.ok) {
          throw new Error(`HTTP error! status: ${networksResponse.status}`);
        }
        const networksData = await networksResponse.json();
        setNetworks(networksData);

        const clientsResponse = await fetch('/api/clients');
        if (!clientsResponse.ok) {
          throw new Error(`HTTP error! status: ${clientsResponse.status}`);
        }
        const clientsData = await clientsResponse.json();
        setClients(clientsData);

      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      {loading && <p className="text-center">Loading data...</p>}
      {error && <p className="text-center text-red-500">Error: {error}</p>}

      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Networks Card */}
          <div className="bg-white shadow rounded-lg">
            <div className="p-6">
              <h2 className="text-xl font-semibold">Networks ({networks.length})</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {networks.map(network => (
                <NetworkCard key={network.id} network={network} />
              ))}
            </div>
          </div>

          {/* Clients Card */}
          <div className="bg-white shadow rounded-lg">
            <div className="p-6">
              <h2 className="text-xl font-semibold">Clients ({clients.length})</h2>
            </div>
            <div className="divide-y divide-gray-200">
              {clients.map(client => (
                <ClientCard key={client.id} client={client} />
              ))}
            </div>
          </div>
        </div>
      )}
    </main>
  )
}

export default DashboardPage;
