import { HomeAssistant } from '../types/ha';

export const safeCallWS = async <T>(
  hass: HomeAssistant,
  msg: { type: string; [key: string]: unknown }
): Promise<T> => {
  if (!hass) {
    throw new Error('Home Assistant object is not available.');
  }
  try {
    if (typeof hass.callWS === 'function') {
      return await hass.callWS<T>(msg);
    }
    if (
      hass.connection &&
      typeof hass.connection.sendMessagePromise === 'function'
    ) {
      return await hass.connection.sendMessagePromise<T>(msg);
    }
    throw new Error(
      'Home Assistant WebSocket communication methods not found.'
    );
  } catch (err) {
    console.error(`Cisco Meraki HA: WebSocket error [${msg.type}]:`, err);
    throw err;
  }
};
