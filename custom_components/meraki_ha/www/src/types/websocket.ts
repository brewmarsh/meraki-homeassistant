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
  UPDATE_ENABLED_NETWORKS = 'meraki_ha/update_enabled_networks',
  CREATE_GUEST_KEY = 'meraki_ha/ipsk/create',
  GET_GUEST_KEYS = 'meraki_ha/ipsk/get',
  REVOKE_GUEST_KEY = 'meraki_ha/ipsk/revoke',
  TIMED_ACCESS_GET_POLICIES = 'meraki_ha/timed_access/get_policies',
}

/**
 * WebSocket Message Payload Interface
 */
export interface WsMessagePayload {
  type: WsCommand | string;
  [key: string]: any;
}

/**
 * IPSK Key Interface
 */
export interface WsIpskKey {
  identity_psk_id: string;
  network_id: string;
  ssid_number: string;
  name: string;
  passphrase: string;
  expires_at: string;
  config_entry_id: string;
}

/**
 * IPSK Create Payload
 */
export interface WsIpskCreatePayload extends WsMessagePayload {
  type: WsCommand.CREATE_GUEST_KEY;
  configEntryId: string;
  networkId: string;
  ssidNumber: string;
  durationMinutes: number;
  name?: string;
  passphrase?: string;
  groupPolicyId?: string;
}

/**
 * IPSK Get Payload
 */
export interface WsIpskGetPayload extends WsMessagePayload {
  type: WsCommand.GET_GUEST_KEYS;
  configEntryId?: string;
  networkId?: string;
}

/**
 * IPSK Revoke Payload
 */
export interface WsIpskRevokePayload extends WsMessagePayload {
  type: WsCommand.REVOKE_GUEST_KEY;
  identityPskId: string;
}

/**
 * Group Policy Get Payload
 */
export interface WsGroupPolicyGetPayload extends WsMessagePayload {
  type: WsCommand.TIMED_ACCESS_GET_POLICIES;
  configEntryId: string;
  networkId: string;
}
