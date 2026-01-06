declare namespace JSX {
  interface IntrinsicElements {
<<<<<<< HEAD
<<<<<<< HEAD
    'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
    'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string }, HTMLElement>;
    'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; onchange?: (e: any) => void }, HTMLElement>;
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
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
        onchange?: (e: any) => void;
      },
      HTMLElement
    >;
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
  }
}
