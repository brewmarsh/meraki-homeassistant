declare namespace JSX {
  interface IntrinsicElements {
    'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
    'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string }, HTMLElement>;
    'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; onchange?: (e: any) => void }, HTMLElement>;
  }
}
