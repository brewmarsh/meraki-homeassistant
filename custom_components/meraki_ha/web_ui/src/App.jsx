import { useState, useEffect } from 'react';

function App() {
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
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Meraki Control</h1>
        </div>
      </header>
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {loading && <p className="text-center">Loading data...</p>}
        {error && <p className="text-center text-red-500">Error: {error}</p>}

        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Networks Card */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Networks ({networks.length})</h2>
              <ul className="divide-y divide-gray-200">
                {networks.map(network => (
                  <li key={network.id} className="py-2">
                    <p className="font-medium text-gray-800">{network.name}</p>
                    <p className="text-sm text-gray-500">ID: {network.id}</p>
                  </li>
                ))}
              </ul>
            </div>

            {/* Clients Card */}
            <div className="bg-white shadow rounded-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Clients ({clients.length})</h2>
              <ul className="divide-y divide-gray-200">
                {clients.map(client => (
                  <li key={client.id} className="py-2">
                     <p className="font-medium text-gray-800">{client.description || 'No description'}</p>
                    <p className="text-sm text-gray-500">MAC: {client.mac}</p>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App
