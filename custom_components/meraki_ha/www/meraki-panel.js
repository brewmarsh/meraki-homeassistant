// Simplified renderer for e2e testing
function render(data) {
  const root = document.getElementById('root');
  if (!root) {
    console.error('No root element found');
    return;
  }

  if (!data || !data.networks) {
    root.innerHTML = '<p class="error">Error: No data received</p>';
    return;
  }

  let html = '<h1>Meraki Dashboard</h1>';
  data.networks.forEach(network => {
    html += `
      <div class="card" data-testid="network-card">
        <p>${network.name}</p>
      </div>
    `;
  });
  root.innerHTML = html;
}

// Mock the hass object if it's not available (for direct browser testing)
if (!window.hass) {
  console.log('Mocking window.hass for testing');
  window.hass = {
    connection: {
      subscribeMessage: async (callback, subscription) => {
        console.log('Mock subscription:', subscription);
        // Simulate a delay
        await new Promise(resolve => setTimeout(resolve, 500));
        // Provide mock data
        const mockData = {
          org_name: 'Test Org',
          networks: [{ id: 'N_12345', name: 'Test Network' }],
          devices: [],
          clients: []
        };
        callback({ type: 'result', success: true, result: mockData });
        return () => Promise.resolve();
      }
    }
  };
}

// Subscribe to data and render
window.hass.connection.subscribeMessage(
  (message) => {
    if (message.type === 'result' && message.success) {
      render(message.result);
    } else {
      console.error('Failed to get data:', message);
      render(null);
    }
  },
  { type: 'meraki_ha/get_config' } // This matches the test's expectation
);