export interface HaState {
  entity_id: string;
  state: string;
  attributes: Record<string, any>;
  last_changed: string;
  last_updated: string;
  context: {
    id: string;
    parent_id: string | null;
    user_id: string | null;
  };
}

export interface HomeAssistant {
  states: Record<string, HaState>;
  callWS: <T = any>(message: any) => Promise<T>;
  connection?: {
    sendMessagePromise: <T = any>(message: any) => Promise<T>;
  };
  [key: string]: any;
}
