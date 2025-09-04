(function() {
    const root = document.getElementById('root');

    function render(data) {
        if (!data || !data.networks) {
            root.innerHTML = '<div class="p-4 text-red-500">Error: Invalid data received</div>';
            return;
        }
        const { networks } = data;
        const networksHtml = networks.map(network => `
            <div data-testid="network-card" class="bg-white dark:bg-gray-800 rounded-lg shadow p-4 cursor-pointer" onclick="window.location.href='/networks/${network.id}'">
                <p class="font-medium text-gray-900 dark:text-white">${network.name}</p>
            </div>
        `).join('');

        const settingsLink = `<a href="/settings">Settings</a>`;

        root.innerHTML = `
            <h1 class="text-2xl font-bold mb-4">Meraki HA Web UI</h1>
            ${settingsLink}
            <main>
                <h2 class="text-xl font-semibold mb-4">Networks</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    ${networksHtml}
                </div>
            </main>
        `;
    }

    async function init() {
        if (!window.hass || !window.hass.connection) {
            console.error("Home Assistant connection object not found.");
            root.innerHTML = '<div class="p-4 text-red-500">Error: Home Assistant connection object not found.</div>';
            return;
        }

        try {
            await window.hass.connection.subscribeMessage(
                (message) => {
                    if (message.type === 'result' && message.success) {
                        render(message.result);
                    } else if (message.type === 'event') {
                        render(message.event);
                    }
                },
                {
                    type: 'meraki_ha/subscribe_meraki_data',
                    config_entry_id: window.CONFIG_ENTRY_ID,
                }
            );
        } catch (err) {
            console.error('Error subscribing to Meraki data:', err);
            root.innerHTML = '<div class="p-4 text-red-500">Error: Failed to subscribe to Meraki data. See console for details.</div>';
        }
    }

    init();
})();
