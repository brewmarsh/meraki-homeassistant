// Simplified Javascript that fetches data from the local REST API.

function render(path, data) {
  const root = document.querySelector('#root');
  if (!root) {
    return;
  }

  let html = `
    <header class="p-4 bg-gray-100 dark:bg-gray-800 shadow">
      <nav class="flex items-center justify-between">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Meraki Control</h1>
        <div>
          <a href="/" class="text-blue-500 hover:underline px-4">Dashboard</a>
          <a href="/settings" class="text-blue-500 hover:underline px-4">Settings</a>
        </div>
      </nav>
    </header>
    <main class="p-4">
  `;

  if (path === '/') {
    if (!data) {
      html += '<p>Loading networks...</p>';
    } else if (data.error) {
      html += `<p class="text-red-500">Error: ${data.error}</p>`;
    } else {
      html += '<h2 class="text-xl font-semibold mb-2">Networks</h2>';
      html += '<div data-testid="network-list" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">';
      data.forEach(network => {
        html += `
          <div data-testid="network-card" class="bg-white dark:bg-gray-700 rounded-lg shadow p-4">
            <a href="/networks/${network.id}" class="text-lg font-bold text-blue-600 dark:text-blue-400 hover:underline">${network.name}</a>
            <p class="text-sm text-gray-600 dark:text-gray-400">ID: ${network.id}</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Clients: ${network.clientCount || 'N/A'}</p>
          </div>
        `;
      });
      html += '</div>';
    }
  } else if (path.startsWith('/networks/')) {
    // This is a simplified view. A real implementation would fetch network details.
    html += '<h1>Network Information</h1><p>Navigated to network detail view.</p>';
    html += '<a href="/" class="text-blue-500 hover:underline">Back to Dashboard</a>';
  } else if (path === '/settings') {
    html += '<h1 data-testid="settings-header">Settings</h1><p>Settings page placeholder.</p>';
  } else {
    html += '<h1>Page Not Found</h1>';
  }

  html += '</main>';
  root.innerHTML = html;

  // Add click listeners to all local links to handle client-side routing
  root.querySelectorAll('a[href^="/"]').forEach(anchor => {
    anchor.addEventListener('click', (event) => {
      event.preventDefault();
      const url = new URL(anchor.href);
      window.history.pushState({}, '', url.pathname);
      // Re-render based on the new path. For simplicity, we don't re-fetch data on nav.
      // A full SPA would have more complex state management.
      render(url.pathname, data);
    });
  });
}

function fetchDataAndRender() {
  // Initial render with a loading state
  render(window.location.pathname, null);

  fetch('/api/networks')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Re-render with the fetched data
      render(window.location.pathname, data);
    })
    .catch(error => {
      console.error('Error fetching networks:', error);
      // Render an error message
      render(window.location.pathname, { error: error.message });
    });
}

// Initial fetch and render
fetchDataAndRender();

// Handle back/forward buttons
window.addEventListener('popstate', () => {
  // We need to re-fetch data or have it stored to re-render correctly.
  // For this simplified version, we'll just re-run the initial fetch.
  fetchDataAndRender();
});
