export interface HomeAssistant {
  callWS<T>(msg: { type: string; [key: string]: unknown }): Promise<T>;
  callService(
    domain: string,
    service: string,
    serviceData?: object
  ): Promise<void>;
  config: {
    components: string[];
  };
  connection: {
    sendMessagePromise<T>(msg: {
      type: string;
      [key: string]: unknown;
    }): Promise<T>;
  };
  states: {
    [entity_id: string]: {
      state: string;
      attributes: { [key: string]: unknown };
    };
  };
  user: {
    name: string;
    id: string;
    is_owner: boolean;
    is_admin: boolean;
  };
}
