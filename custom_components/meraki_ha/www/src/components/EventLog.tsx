<<<<<<< HEAD
<<<<<<< HEAD
import React from 'react';

const EventLog: React.FC = () => {
  return (
    <div className="card-content">
      <p>Integration-specific events will be displayed here.</p>
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
import React, { useState, useEffect } from 'react';

interface EventLogProps {
  hass: any;
  networkId?: string;
  configEntryId: string;
  productTypes?: string[];
}

interface MerakiEvent {
  occurredAt: string;
  type: string;
  description: string;
  clientId?: string;
  clientDescription?: string;
  deviceSerial?: string;
  deviceName?: string;
}

const EventLog: React.FC<EventLogProps> = ({
  hass,
  networkId,
  configEntryId,
  productTypes,
}) => {
  const [events, setEvents] = useState<MerakiEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      if (!networkId) return;

      // Determine product type to use
      const productType =
        productTypes && productTypes.length > 0 ? productTypes[0] : undefined;

      // If no product type, and meraki api requires it, we might skip fetching or try without it.
      // But given the error, let's try to send it if available.

      setLoading(true);
      setError(null);

      try {
        if (window.location.hostname === 'localhost') {
          // Mock data for development
          setEvents([
            {
              occurredAt: new Date().toISOString(),
              type: 'client_connect',
              description: 'Client connected',
              clientDescription: 'iPhone',
            },
            {
              occurredAt: new Date(Date.now() - 3600000).toISOString(),
              type: 'device_online',
              description: 'Device came online',
              deviceName: 'Living Room AP',
            },
          ]);
          setLoading(false);
          return;
        }

        if (!hass) {
          throw new Error('Hass connection not available');
        }

        const response = await hass.callWS({
          type: 'meraki_ha/get_network_events',
          config_entry_id: configEntryId,
          network_id: networkId,
          per_page: 10,
          product_type: productType,
        });

        if (response && response.events) {
          setEvents(response.events);
        } else {
          setEvents([]);
        }
      } catch (err: any) {
        console.error('Error fetching events:', err);
        setError(err.message || 'Failed to fetch events');
      } finally {
        setLoading(false);
      }
    };

    fetchEvents();
  }, [hass, networkId, configEntryId, productTypes]);

  if (!networkId) {
    return (
      <div className="p-4 text-gray-500">Select a network to view events.</div>
    );
  }

  return (
    <div className="mt-4">
      <h3 className="text-lg font-semibold mb-2">Recent Events</h3>
      {loading && <p>Loading events...</p>}
      {error && <p className="text-red-500">Error: {error}</p>}
      {!loading && !error && events.length === 0 && <p>No events found.</p>}

      {!loading && !error && events.length > 0 && (
        <div className="overflow-x-auto bg-light-card dark:bg-dark-card rounded-lg shadow-md">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="border-b border-light-border dark:border-dark-border bg-gray-50 dark:bg-gray-800">
                <th className="text-left p-3 font-medium">Time</th>
                <th className="text-left p-3 font-medium">Type</th>
                <th className="text-left p-3 font-medium">Description</th>
                <th className="text-left p-3 font-medium">Source</th>
              </tr>
            </thead>
            <tbody>
              {events.map((event, index) => (
                <tr
                  key={index}
                  className="border-b border-light-border dark:border-dark-border hover:bg-gray-50 dark:hover:bg-gray-700"
                >
                  <td className="p-3 whitespace-nowrap">
                    {new Date(event.occurredAt).toLocaleString()}
                  </td>
                  <td className="p-3">{event.type}</td>
                  <td className="p-3">{event.description}</td>
                  <td className="p-3">
                    {event.clientDescription ||
                      event.deviceName ||
                      event.clientId ||
                      event.deviceSerial ||
                      '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
    </div>
  );
};

<<<<<<< HEAD
<<<<<<< HEAD
export default EventLog;
=======
export default EventLog;
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
export default EventLog;
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
