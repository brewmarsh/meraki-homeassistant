export interface HomeAssistant {
  callWS<T>(msg: { type: string; [key: string]: any }): Promise<T>;
  callService(domain: string, service: string, serviceData?: object): Promise<void>;
  config: {
    components: string[];
  };
  connection: any;
}
