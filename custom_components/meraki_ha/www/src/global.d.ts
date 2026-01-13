declare namespace JSX {
  interface IntrinsicElements {
    'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
    'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string }, HTMLElement>;
<<<<<<< HEAD
=======
    'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; onchange?: (e: any) => void }, HTMLElement>;
>>>>>>> 500a6a1 (Merge branch 'main' into test/config-flow-errors-4148457084909740722)
  }
}
