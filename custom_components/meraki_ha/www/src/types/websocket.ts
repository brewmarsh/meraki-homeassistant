export enum WsCommand {
  GET_CONFIG = 'meraki_ha/get_config',
  SUBSCRIBE_MERAKI_DATA = 'meraki_ha/subscribe_meraki_data',
  GET_CAMERA_STREAM_URL = 'meraki_ha/get_camera_stream_url',
  GET_CAMERA_SNAPSHOT = 'meraki_ha/get_camera_snapshot',
  GET_VERSION = 'meraki_ha/get_version',
  GET_NETWORK_EVENTS = 'meraki_ha/get_network_events',
  UPDATE_ENABLED_NETWORKS = 'meraki_ha/update_enabled_networks',
  CREATE_GUEST_KEY = 'meraki_ha/ipsk/create',
  GET_GUEST_KEYS = 'meraki_ha/ipsk/get',
  REVOKE_GUEST_KEY = 'meraki_ha/ipsk/revoke',
  TIMED_ACCESS_GET_POLICIES = 'meraki_ha/timed_access/get_policies',
}

export interface WsMessagePayload {
  type: string;
  [key: string]: any;
}
