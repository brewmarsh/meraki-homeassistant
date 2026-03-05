import { WsMessagePayload } from '../types/websocket';

/**
 * Utility for making safe WebSocket calls to Home Assistant.
 */

export const safeCallWS = async <T = any>(hass: any, message: WsMessagePayload): Promise<T> => {
  if (!hass) {
    throw new Error('Home Assistant object is not available.');
  }

  try {
    // Attempt to use callWS if available (standard for newer HA)
    if (typeof hass.callWS === 'function') {
      return await hass.callWS(message);
    }

    // Fallback to connection.sendMessagePromise (common in custom panels)
    if (hass.connection && typeof hass.connection.sendMessagePromise === 'function') {
      return await hass.connection.sendMessagePromise(message);
    }

    throw new Error('Home Assistant WebSocket communication methods not found.');
  } catch (error: any) {
    // Log the error for easier debugging
    console.error(`Meraki HA: WebSocket error [${message.type}]:`, error);
    // Rethrow to let the component handle it
    throw error;
  }
};
