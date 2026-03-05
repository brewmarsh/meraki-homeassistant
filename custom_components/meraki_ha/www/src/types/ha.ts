export interface HomeAssistant {
  hassUrl(path: string): string;
  callWS<T>(msg: any): Promise<T>;
  callService(domain: string, service: string, data: any): Promise<void>;
  connection: any;
  connected: boolean;
  states: any;
  services: any;
  config: any;
  themes: any;
  selectedTheme: any;
  panels: any;
  user: any;
  userid: string;
  language: string;
  resources: any;
  localize: any;
  translationMetadata: any;
  dockedSidebar: string;
  defaultPanel: string;
  moreInfoEntityId: string;
}
