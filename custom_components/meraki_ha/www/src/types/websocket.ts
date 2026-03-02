/**
 * WebSocket Command Enum
 */
export enum WsCommand {
  GET_CONFIG = 'meraki_ha/get_config',
  SUBSCRIBE_MERAKI_DATA = 'meraki_ha/subscribe_meraki_data',
  GET_CAMERA_STREAM_URL = 'meraki_ha/get_camera_stream_url',
  GET_CAMERA_SNAPSHOT = 'meraki_ha/get_camera_snapshot',
  GET_VERSION = 'meraki_ha/get_version',
  GET_NETWORK_EVENTS = 'meraki_ha/get_network_events',
  UPDATE_OPTIONS = 'meraki_ha/update_options',
  UPDATE_ENABLED_NETWORKS = 'meraki_ha/update_enabled_networks',
  TIMED_ACCESS_GET_KEYS = 'meraki_ha/timed_access/get_keys',
  TIMED_ACCESS_GET_POLICIES = 'meraki_ha/timed_access/get_policies',
  TIMED_ACCESS_CREATE = 'meraki_ha/timed_access/create',
  TIMED_ACCESS_DELETE = 'meraki_ha/timed_access/delete',
}

/**
 * WebSocket Message Payload Interface
 */
export interface WsMessagePayload {
  type: WsCommand | string;
  [key: string]: any;
}
