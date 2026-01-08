/**
 * Global TypeScript declarations for the Meraki HA Panel
 */

import 'react';

// Vite-specific CSS module imports
declare module '*.css?inline' {
  const content: string;
  export default content;
}

declare module '*.css' {
  const content: string;
  export default content;
}

// Extend React's JSX IntrinsicElements to include Home Assistant custom elements
declare module 'react' {
  namespace JSX {
    interface IntrinsicElements {
      'ha-card': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          header?: string;
          class?: string;
        },
        HTMLElement
      >;
      'ha-icon': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & { icon?: string },
        HTMLElement
      >;
      'ha-switch': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          checked?: boolean;
          disabled?: boolean;
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
