/**
 * TypeScript definitions for Home Assistant frontend objects.
 * These types represent the objects passed to custom panels by Home Assistant.
 */

/**
 * Represents the Home Assistant connection for WebSocket communication.
 */
export interface HassConnection {
  /**
   * Send a WebSocket message and get a promise for the result.
   * @param message - The message to send (must include 'type' field)
   * @returns Promise resolving to the result
   */
  sendMessagePromise<T = unknown>(message: HassMessage): Promise<T>;

  /**
   * Subscribe to messages of a specific type.
   * @param callback - Function called when messages are received
   * @param message - The subscription message
   * @returns Promise resolving to an unsubscribe function
   */
  subscribeMessage<T = unknown>(
    callback: (message: T) => void,
    message: HassMessage
  ): Promise<() => void>;

  /**
   * Subscribe to events.
   * @param callback - Function called when events occur
   * @param eventType - Optional event type to filter
   * @returns Promise resolving to an unsubscribe function
   */
  subscribeEvents<T = unknown>(
    callback: (event: T) => void,
    eventType?: string
  ): Promise<() => void>;
}

/**
 * Represents a WebSocket message to Home Assistant.
 */
export interface HassMessage {
  type: string;
  [key: string]: unknown;
}

/**
 * Represents an entity state in Home Assistant.
 */
export interface HassEntityState {
  entity_id: string;
  state: string;
  attributes: Record<string, unknown>;
  last_changed: string;
  last_updated: string;
  context: {
    id: string;
    parent_id: string | null;
    user_id: string | null;
  };
}

/**
 * Represents a Home Assistant service.
 */
export interface HassService {
  name?: string;
  description?: string;
  fields?: Record<string, unknown>;
  target?: unknown;
}

/**
 * The main Home Assistant object passed to custom panels.
 */
export interface HomeAssistant {
  /** The authenticated user */
  user?: {
    id: string;
    name: string;
    is_admin: boolean;
    is_owner: boolean;
  };

  /** Current language */
  language: string;

  /** All entity states, keyed by entity_id */
  states: Record<string, HassEntityState>;

  /** All services, keyed by domain */
  services: Record<string, Record<string, HassService>>;

  /** The WebSocket connection */
  connection: HassConnection;

  /** Current theme */
  themes: {
    default_theme: string;
    default_dark_theme: string | null;
    themes: Record<string, unknown>;
    darkMode: boolean;
  };

  /** Locale settings */
  locale: {
    language: string;
    number_format: string;
    time_format: string;
  };

  /**
   * Call a Home Assistant service.
   * @param domain - The service domain (e.g., 'light')
   * @param service - The service name (e.g., 'turn_on')
   * @param serviceData - Optional service data
   * @param target - Optional target for the service
   */
  callService(
    domain: string,
    service: string,
    serviceData?: Record<string, unknown>,
    target?: { entity_id?: string | string[] }
  ): Promise<void>;

  /**
   * Call a WebSocket command (shorthand for connection.sendMessagePromise).
   * @param message - The WebSocket message
   */
  callWS<T = unknown>(message: HassMessage): Promise<T>;
}

/**
 * Panel configuration passed to custom panels.
 */
export interface PanelInfo {
  /** The component name */
  component_name: string;

  /** The URL path for this panel */
  url_path: string;

  /** The sidebar title */
  title: string | null;

  /** The sidebar icon */
  icon: string | null;

  /** Custom configuration passed from the integration */
  config: {
    /** The config entry ID for this integration instance */
    config_entry_id: string;
    /** Any additional custom config */
    [key: string]: unknown;
  };
}

/**
 * Route information for navigation.
 */
export interface RouteInfo {
  /** The current path */
  path: string;

  /** URL prefix for this panel */
  prefix: string;
}

/**
 * Props passed to a Home Assistant custom panel element.
 */
export interface HaPanelProps {
  /** The Home Assistant object */
  hass: HomeAssistant;

  /** Panel configuration */
  panel: PanelInfo;

  /** Whether to render in narrow/mobile mode */
  narrow: boolean;

  /** Current route information */
  route: RouteInfo;
}
