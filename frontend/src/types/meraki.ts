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
}
