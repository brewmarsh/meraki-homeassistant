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
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="mb-4">
        <Link to="/" className="text-cisco-blue hover:underline">&larr; Back to Dashboard</Link>
      </div>

      {loading && <p className="text-center">Loading network details...</p>}
      {error && <p className="text-center text-red-500">Error: {error}</p>}

      {network && (
        <div className="bg-light-card dark:bg-dark-card shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-light-border dark:border-dark-border">
            <h3 className="text-lg leading-6 font-medium">
              Network Information
            </h3>
            <p className="mt-1 max-w-2xl text-sm text-gray-500 dark:text-gray-400">
              Details for network: {network.name}
            </p>
          </div>
          <div className="border-t border-light-border dark:border-dark-border">
            <dl>
              {Object.entries(network).map(([key, value], index) => (
                <div key={key} className={`${index % 2 === 0 ? 'bg-light-card dark:bg-dark-card' : 'bg-light-background dark:bg-dark-background'} px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6`}>
                  <dt className="text-sm font-medium text-gray-500 dark:text-gray-400 capitalize">{key}</dt>
                  <dd className="mt-1 text-sm sm:mt-0 sm:col-span-2">
                    {typeof value === 'boolean' ? value.toString() : JSON.stringify(value, null, 2)}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      )}
    </div>
  );
}

export default NetworkDetailPage;
