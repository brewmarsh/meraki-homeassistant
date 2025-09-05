// Simplified Javascript that fetches data from the local REST API.

function render(path, data) {
  const root = document.querySelector('#root');
  if (!root) {
    console.error("Root element not found for rendering.");
    return;
  }

  // Basic layout with a main tag for the test to find
  let html = '<main class="p-4">';

  if (path === '/') {
    if (!data) {
      html += '<p>Loading networks...</p>';
    } else if (data.error) {
      html += `<p class="text-red-500">Error: ${data.error}</p>`;
    } else {
      html += '<h2 class="text-xl font-semibold mb-4">Networks</h2>';
      html += '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">';
      if (data.networks && Array.isArray(data.networks)) {
        data.networks.forEach(network => {
          html += `
            <div data-testid="network-card" class="bg-white dark:bg-gray-700 rounded-lg shadow p-4 cursor-pointer" onclick="navigateTo('/networks/${network.id}')">
              <p class="font-medium text-gray-900 dark:text-white">${network.name}</p>
            </div>
          `;
        });
      }
      html += '</div>';
    }
  } else if (path.startsWith('/networks/')) {
    html += '<h1>Network Information</h1>';
    html += '<a href="/" onclick="navigateTo(\'/\'); return false;">Back to Dashboard</a>';
  } else {
    html += '<h1>Page Not Found</h1>';
  }

  html += '</main>';
  root.innerHTML = html;
}

// Client-side navigation handler
window.navigateTo = (path) => {
  window.history.pushState({}, '', path);
  // In this simplified model, we don't re-fetch data on navigation.
  // We just re-render the appropriate view. A full app would need state management.
  // We need to get the data again to pass to render.
  fetchDataAndRender(path);
};


function fetchDataAndRender(path) {
  const currentPath = path || window.location.pathname;

  // Render loading state, but only for the dashboard view
  if (currentPath === '/') {.
    render(currentPath, null);
  }

  fetch('/api/all_data')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Re-render with the fetched data
      render(currentPath, data);
    })
    .catch(error => {
      console.error('Error fetching data:', error);
      // Render an error message
      render(currentPath, { error: error.message });
    });
}

// Initial fetch and render
fetchDataAndRender();

// Handle back/forward buttons
window.addEventListener('popstate', () => {
  fetchDataAndRender();
});
