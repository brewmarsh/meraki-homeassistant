import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function NetworkDetailPage() {
  const { networkId } = useParams();
  const [network, setNetwork] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchNetworkDetail = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/networks/${networkId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        setNetwork(data);
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNetworkDetail();
  }, [networkId]);

  return (
    <main className="max-w-4xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="mb-4">
        <Link to="/" className="text-indigo-600 hover:text-indigo-800">&larr; Back to Dashboard</Link>
      </div>

      {loading && <p className="text-center">Loading network details...</p>}
      {error && <p className="text-center text-red-500">Error: {error}</p>}

      {network && (
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Network Information
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500">
              Details for network: {network.name}
            </p>
          </div>
          <div className="border-t border-gray-200">
            <dl>
              {Object.entries(network).map(([key, value]) => (
                <div key={key} className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500 capitalize">{key}</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    {typeof value === 'boolean' ? value.toString() : value}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      )}
    </main>
  );
}

export default NetworkDetailPage;
