// Simplified Javascript for E2E testing with hardcoded data and routing

function render(path) {
  const root = document.querySelector('#root');
  if (!root) {
    return;
  }

  // Hardcoded data that matches the mock data used in the E2E tests
  const MOCK_ALL_DATA = {
      "networks": [{
          "id": "N_12345",
          "organizationId": "test-org",
          "name": "Test Network",
          "productTypes": ["appliance", "switch", "wireless", "cellularGateway"],
          "tags": "e2e-test",
          "clientCount": 5,
      }],
      "devices": [],
      "ssids": [],
      "clients": [],
      "l7_firewall_rules": {},
  };

  let html = `
    <header>
      <nav>
        <a href="/">Dashboard</a>
        <a href="/settings">Settings</a>
      </nav>
    </header>
    <main>
  `;

  if (path === '/') {
    html += '<h1>Meraki Data</h1>';
    if (MOCK_ALL_DATA.networks) {
      html += '<h2>Networks</h2>';
      html += '<ul data-testid="network-list">';
      MOCK_ALL_DATA.networks.forEach(network => {
        html += `<li data-testid="network-card"><a href="/networks/${network.id}">${network.name}</a></li>`;
      });
      html += '</ul>';
    }
  } else if (path.startsWith('/networks/')) {
    html += '<h1>Network Information</h1>';
  } else if (path === '/settings') {
    html += '<h1 data-testid="settings-header">Settings</h1>';
  } else {
    html += '<h1>Page Not Found</h1>';
  }

  html += '</main>';
  root.innerHTML = html;

  // Add click listeners to all local links
  root.querySelectorAll('a').forEach(anchor => {
    if (anchor.href.startsWith(window.location.origin)) {
      anchor.addEventListener('click', (event) => {
        event.preventDefault();
        const url = new URL(anchor.href);
        window.history.pushState({}, '', url.pathname);
        render(url.pathname);
      });
    }
  });
}

// Initial render
render(window.location.pathname);

// Handle back/forward buttons
window.addEventListener('popstate', () => {
  render(window.location.pathname);
});
