declare global {
    namespace JSX {
      interface IntrinsicElements {
        'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement>, HTMLElement> & {
            header?: string;
        };
      }
    }
  }

  export {};