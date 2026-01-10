declare namespace JSX {
  interface IntrinsicElements {
    'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
    'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string }, HTMLElement>;
<<<<<<< HEAD
=======
    'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; onchange?: (e: any) => void }, HTMLElement>;
>>>>>>> d5ccb99 (Merge pull request #604 from brewmarsh/fix/resolve-jq-parse-error-in-deploy-local-workflow-2298884834713058677)
  }
}
