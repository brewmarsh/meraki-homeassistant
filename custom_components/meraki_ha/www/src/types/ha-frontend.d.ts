import React from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
      'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string; slot?: string }, HTMLElement>;
      'ha-settings-row': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { narrow?: boolean; slot?: string }, HTMLElement>;
      'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; disabled?: boolean }, HTMLElement>;
      'ha-circular-progress': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { active?: boolean; alt?: string }, HTMLElement>;
      'ha-tabs': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { selected?: string; "attr-for-selected"?: string; scrollable?: boolean }, HTMLElement>;
      'paper-tab': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { name?: string }, HTMLElement>;
    }
  }
}
export {};
