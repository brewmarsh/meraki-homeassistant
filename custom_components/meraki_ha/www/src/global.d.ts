declare module '*.css?inline' {
  const content: string;
  export default content;
}

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
        disabled?: boolean;
        onchange?: (e: any) => void;
      },
      HTMLElement
    >;
  }
}
