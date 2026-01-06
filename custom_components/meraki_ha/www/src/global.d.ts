/**
 * Global TypeScript declarations for the Meraki HA Panel
 */

// Home Assistant custom elements used in the UI
declare namespace JSX {
  interface IntrinsicElements {
    'ha-card': React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & { header?: string },
      HTMLElement
    >;
    'ha-icon': React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & { icon?: string },
      HTMLElement
    >;
    'ha-switch': React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & {
        checked?: boolean;
        onchange?: (e: Event & { target: { checked: boolean } }) => void;
      },
      HTMLElement
    >;
    'ha-icon-button': React.DetailedHTMLProps<
      React.HTMLAttributes<HTMLElement> & { icon?: string },
      HTMLElement
    >;
  }
}

// Extend Window interface for development mode
declare global {
  interface Window {
    // These may be set by Home Assistant in production
    HA_URL?: string;
    CONFIG_ENTRY_ID?: string;
  }
}

export {};
