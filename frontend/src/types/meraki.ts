export interface Network {
  id: string;
  name: string;
  productTypes: string[];
}

export interface SSID {
  name: string;
  number: number;
  enabled: boolean;
  networkId: string;
  authMode?: string;
}

export interface GroupPolicy {
  networkId: string;
  groupPolicyId: string;
  name: string;
  id?: string;
}
