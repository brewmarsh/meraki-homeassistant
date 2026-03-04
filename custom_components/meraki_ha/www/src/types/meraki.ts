export interface SSID {
  number: number;
  name: string;
  enabled: boolean;
  networkId: string;
  entity_id?: string;
}

export interface Vlan {
  id: string;
  name: string;
  subnet?: string;
  applianceIp?: string;
}

export interface Network {
  id: string;
  name: string;
  ssids: SSID[];
  is_enabled: boolean;
  productTypes?: string[];
}

export interface Device {
  entity_id: string;
  name: string;
  model: string;
  serial: string;
  status: string;
  lanIp?: string;
  mac?: string;
  networkId?: string;
  ports_statuses?: any[];
  wan1Ip?: string;
  wan2Ip?: string;
}

export interface DeviceGroup {
  label: string;
  devices: Device[];
  icon: string;
  type: string;
}

export interface NetworkData {
  networks: Network[];
  devices: Device[];
  vlans?: Record<string, Vlan[]>;
}
