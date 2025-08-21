import { useState, useEffect, useCallback } from 'react';

function ParentalControlsPage() {
  const [resources, setResources] = useState([]);
  const [selectedResourceId, setSelectedResourceId] = useState('');
  const [categories, setCategories] = useState([]);
  const [blockedCategories, setBlockedCategories] = useState([]);
  const [clients, setClients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch initial resources and categories
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        const [resourcesRes, categoriesRes] = await Promise.all([
          fetch('/api/parental_controls/resources'),
          fetch('/api/contentFiltering/categories'),
        ]);

        if (!resourcesRes.ok || !categoriesRes.ok) {
          throw new Error('Failed to fetch initial data');
        }

        const resourcesData = await resourcesRes.json();
        const categoriesData = await categoriesRes.json();

        setResources(resourcesData);
        setCategories(categoriesData);

        if (resourcesData.length > 0) {
          setSelectedResourceId(JSON.stringify(resourcesData[0]));
        }
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  // Fetch details when a resource is selected
  const fetchResourceDetails = useCallback(async () => {
    if (!selectedResourceId) return;

    try {
      setLoading(true);
      const resource = JSON.parse(selectedResourceId);
      let filteringUrl;
      if (resource.type === 'network') {
        filteringUrl = `/api/networks/${resource.network_id}/appliance/contentFiltering`;
      } else {
        filteringUrl = `/api/networks/${resource.network_id}/ssids/${resource.ssid_number}/contentFiltering`;
      }

      const [filteringRes, clientsRes] = await Promise.all([
        fetch(filteringUrl),
        fetch('/api/clients'),
      ]);

      if (!filteringRes.ok || !clientsRes.ok) {
        throw new Error('Failed to fetch resource details');
      }

      const filteringData = await filteringRes.json();
      const clientsData = await clientsRes.json();

      setBlockedCategories(filteringData.blockedUrlCategories || []);
      setClients(clientsData.filter(c => c.networkId === resource.network_id));

    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [selectedResourceId]);

  useEffect(() => {
    fetchResourceDetails();
  }, [fetchResourceDetails]);

  const handleResourceChange = (e) => {
    setSelectedResourceId(e.target.value);
  };

  const handleCategoryToggle = (categoryId) => {
    setBlockedCategories(prev => {
      const isBlocked = prev.some(cat => cat.id === categoryId);
      if (isBlocked) {
        return prev.filter(cat => cat.id !== categoryId);
      } else {
        const category = categories.find(cat => cat.id === categoryId);
        return [...prev, { id: category.id, name: category.name }];
      }
    });
  };

  const handleSaveChanges = async () => {
    if (!selectedResourceId) return;
    const resource = JSON.parse(selectedResourceId);
    let filteringUrl;
    if (resource.type === 'network') {
      filteringUrl = `/api/networks/${resource.network_id}/appliance/contentFiltering`;
    } else {
      filteringUrl = `/api/networks/${resource.network_id}/ssids/${resource.ssid_number}/contentFiltering`;
    }

    try {
      await fetch(filteringUrl, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ blockedUrlCategories: blockedCategories }),
      });
      alert('Content filtering policy updated successfully!');
    } catch (e) {
      alert(`Error updating policy: ${e.message}`);
    }
  };

  if (error) return <p className="text-center text-red-500">Error: {error}</p>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-light-card dark:bg-dark-card shadow rounded-lg mb-6 p-6">
        <h2 className="text-2xl font-bold mb-4">Select Resource</h2>
        <select
          value={selectedResourceId}
          onChange={handleResourceChange}
          className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-light-border dark:border-dark-border focus:outline-none focus:ring-cisco-blue focus:border-cisco-blue sm:text-sm rounded-md bg-light-background dark:bg-dark-background"
          disabled={loading}
        >
          {resources.map(res => (
            <option key={JSON.stringify(res)} value={JSON.stringify(res)}>
              {res.name} ({res.type})
            </option>
          ))}
        </select>
      </div>

      {loading && <p className="text-center">Loading...</p>}

      {!loading && selectedResourceId && (
        <>
          <div className="bg-light-card dark:bg-dark-card shadow rounded-lg mb-6">
            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-2xl font-bold">Content Filtering Categories</h2>
                <button
                  onClick={handleSaveChanges}
                  className="px-4 py-2 bg-cisco-blue text-white font-semibold rounded-md shadow-sm hover:bg-opacity-80 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cisco-blue"
                >
                  Save Changes
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {categories.map(category => (
                  <div key={category.id} className="flex items-start">
                    <div className="flex items-center h-5">
                      <input
                        id={category.id}
                        name={category.id}
                        type="checkbox"
                        checked={blockedCategories.some(cat => cat.id === category.id)}
                        onChange={() => handleCategoryToggle(category.id)}
                        className="focus:ring-cisco-blue h-4 w-4 text-cisco-blue border-gray-300 rounded"
                      />
                    </div>
                    <div className="ml-3 text-sm">
                      <label htmlFor={category.id} className="font-medium">{category.name}</label>
                      <p className="text-gray-500 dark:text-gray-400">{category.description}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-light-card dark:bg-dark-card shadow rounded-lg">
            <div className="p-6">
              <h2 className="text-2xl font-bold">Client Devices</h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Client blocking is managed at the network level.</p>
            </div>
            {/* Client blocking UI would go here, simplified for this refactor */}
          </div>
        </>
      )}
    </div>
  );
}

export default ParentalControlsPage;
