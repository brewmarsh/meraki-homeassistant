import React, { useState, useEffect } from 'react';

interface EventLogProps {
  hass: any;
  networkId?: string;
  configEntryId: string;
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

interface MerakiEventsResponse {
  events: MerakiEvent[];
  pageLink?: string; // Meraki API returns pagination links in headers, client wrapper might handle this differently.
  // But for now let's assume the standard response body structure or just the list.
  // Wait, the API returns a dict with 'events' and 'pageLink' usually if wrapper processes it,
  // or just the list if using meraki library directly?
  // The `getNetworkEvents` method in meraki library returns a dict.
}

const EventLog: React.FC<EventLogProps> = ({
  hass,
  networkId,
  configEntryId,
}) => {
  const [events, setEvents] = useState<MerakiEvent[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchEvents = async () => {
      if (!networkId) return;

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
  }, [hass, networkId, configEntryId]);

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
    </div>
  );
};

export default EventLog;
