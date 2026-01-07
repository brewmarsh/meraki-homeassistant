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
      <div className="empty-state-message">
        Select a network to view events.
      </div>
    );
  }

  return (
    <div className="info-card">
      <h3>📋 Recent Events</h3>
      {loading && <p className="text-muted">Loading events...</p>}
      {error && <p className="text-error">Error: {error}</p>}
      {!loading && !error && events.length === 0 && (
        <p className="text-muted">No events found.</p>
      )}

      {!loading && !error && events.length > 0 && (
        <table className="device-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Type</th>
              <th>Description</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {events.map((event, index) => (
              <tr key={index}>
                <td className="text-mono text-sm">
                  {new Date(event.occurredAt).toLocaleString()}
                </td>
                <td>
                  <span className="detail-badge">{event.type}</span>
                </td>
                <td>{event.description}</td>
                <td className="text-muted">
                  {event.clientDescription ||
                    event.deviceName ||
                    event.clientId ||
                    event.deviceSerial ||
                    '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default EventLog;
