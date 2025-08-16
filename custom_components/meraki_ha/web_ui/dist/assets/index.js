console.log("Meraki HA Web UI Simulated App v2 Loaded");

// --- Helper Functions ---

function renderLayout(title) {
  const root = document.getElementById('root');
  root.innerHTML = `
    <div class="bg-gray-100 min-h-screen font-sans">
      <header class="bg-white shadow">
        <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 class="text-3xl font-bold text-gray-900">${title}</h1>
        </div>
      </header>
      <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8" id="content">
        <p id="loading" class="text-center">Loading data...</p>
      </main>
    </div>
  `;
  return document.getElementById('content');
}

function renderError(element, e) {
    element.innerHTML = `<p class="text-center text-red-500">Error: ${e.message}</p>`;
}

// --- Page Renderers ---

async function renderDashboard() {
    const content = renderLayout('Meraki Control');
    try {
        const [networksRes, clientsRes] = await Promise.all([
            fetch('/api/networks'),
            fetch('/api/clients')
        ]);
        if (!networksRes.ok || !clientsRes.ok) throw new Error('Failed to fetch data');
        const networks = await networksRes.json();
        const clients = await clientsRes.json();

        content.innerHTML = '';
        const grid = document.createElement('div');
        grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-6';

        // Network Card
        const networkCard = document.createElement('div');
        networkCard.className = 'bg-white shadow rounded-lg';
        networkCard.innerHTML = `<div class="p-6"><h2 class="text-xl font-semibold">Networks (${networks.length})</h2></div>`;
        const networkList = document.createElement('div');
        networkList.className = 'divide-y divide-gray-200';
        networks.forEach(n => {
            networkList.innerHTML += `<a href="/networks/${n.id}" class="block hover:bg-gray-50"><div class="py-4 px-4"><p class="font-medium text-indigo-600 truncate">${n.name}</p><p class="text-sm text-gray-500">ID: ${n.id}</p></div></a>`;
        });
        networkCard.appendChild(networkList);

        // Client Card
        const clientCard = document.createElement('div');
        clientCard.className = 'bg-white shadow rounded-lg';
        clientCard.innerHTML = `<div class="p-6"><h2 class="text-xl font-semibold">Clients (${clients.length})</h2></div>`;
        const clientList = document.createElement('div');
        clientList.className = 'divide-y divide-gray-200';
        clients.forEach(c => {
            clientList.innerHTML += `<a href="/clients/${c.mac}" class="block hover:bg-gray-50"><div class="py-4 px-4"><p class="font-medium text-indigo-600 truncate">${c.description || 'No desc'}</p><p class="text-sm text-gray-500">MAC: ${c.mac}</p></div></a>`;
        });
        clientCard.appendChild(clientList);

        grid.appendChild(networkCard);
        grid.appendChild(clientCard);
        content.appendChild(grid);
    } catch (e) {
        renderError(content, e);
    }
}

async function renderDetailPage(type, id) {
    const content = renderLayout('Detail View');
    try {
        const res = await fetch(`/api/${type}/${id}`);
        if (!res.ok) throw new Error(`Failed to fetch ${type} detail`);
        const data = await res.json();

        content.innerHTML = `
            <div class="mb-4">
                <a href="/" class="text-indigo-600 hover:text-indigo-800">&larr; Back to Dashboard</a>
            </div>
            <div class="bg-white shadow overflow-hidden sm:rounded-lg">
                <div class="px-4 py-5 sm:px-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900">${type === 'networks' ? 'Network' : 'Client'} Information</h3>
                    <p class="mt-1 max-w-2xl text-sm text-gray-500">Details for ${data.name || data.description || data.mac}</p>
                </div>
                <div class="border-t border-gray-200" id="detail-list"></div>
            </div>
        `;
        const detailList = document.getElementById('detail-list');
        const dl = document.createElement('dl');
        Object.entries(data).forEach(([key, value]) => {
            const item = document.createElement('div');
            item.className = 'bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6';
            item.innerHTML = `<dt class="text-sm font-medium text-gray-500 capitalize">${key}</dt><dd class="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">${JSON.stringify(value)}</dd>`;
            dl.appendChild(item);
        });
        detailList.appendChild(dl);

    } catch (e) {
        renderError(content, e);
    }
}


// --- Main Router ---

function router() {
    const path = window.location.pathname;
    const networkMatch = path.match(/^\/networks\/([^/]+)/);
    if (networkMatch) {
        renderDetailPage('networks', networkMatch[1]);
        return;
    }

    const clientMatch = path.match(/^\/clients\/([^/]+)/);
    if (clientMatch) {
        renderDetailPage('clients', clientMatch[1]);
        return;
    }

    renderDashboard();
}

// Since this isn't a real SPA, we can't rely on popstate events easily.
// For the test, we just need to run the router logic on initial load.
// The test's `page.goto` or `page.click` will cause a full page load,
// which will re-execute this script.
router();
