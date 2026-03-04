export interface MerakiNetwork {
  id: string;
  name: string;
  is_enabled: boolean;
  ssids: any[];
  productTypes?: string[];
  [key: string]: any;
}

export interface MerakiData {
  networks: MerakiNetwork[];
  devices: any[];
  ssids?: any[];
  vlans?: Record<string, any[]>;
  options?: Record<string, boolean>;
  version?: string;
}

export interface AppProps {
  hass: any;
  panel?: {
    config?: {
      config_entry_id?: string;
    };
    [key: string]: any;
  };
  config_entry_id?: string;
}
