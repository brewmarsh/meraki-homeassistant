import React from 'react';

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'ha-card': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { header?: string }, HTMLElement>;
      'ha-icon': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { icon?: string; slot?: string }, HTMLElement>;
      'ha-settings-row': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { narrow?: boolean; slot?: string }, HTMLElement>;
      'ha-switch': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { checked?: boolean; disabled?: boolean }, HTMLElement>;
      'ha-circular-progress': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { active?: boolean; alt?: string }, HTMLElement>;
      'ha-tabs': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { selected?: string; "attr-for-selected"?: string; scrollable?: boolean; "onIron-select"?: (e: CustomEvent) => void }, HTMLElement>;
      'paper-tab': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { name?: string }, HTMLElement>;
      'ha-textfield': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { label?: string; value?: string | number; placeholder?: string; disabled?: boolean; type?: string; icon?: string; iconTrailing?: string; required?: boolean; errorMessage?: string; validationMessage?: string; }, HTMLElement>;
      'ha-select': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { label?: string; value?: string; disabled?: boolean; fixedMenuPosition?: boolean; naturalMenuWidth?: boolean; required?: boolean; }, HTMLElement>;
      'ha-button': React.DetailedHTMLProps<React.ButtonHTMLAttributes<HTMLButtonElement> & { disabled?: boolean; raised?: boolean; }, HTMLElement>;
      'ha-alert': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { 'alert-type'?: 'info' | 'warning' | 'error' | 'success'; title?: string; dismissable?: boolean; }, HTMLElement> & { onClose?: (e: any) => void };
      'ha-list-item': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { value?: string; selected?: boolean; disabled?: boolean; }, HTMLElement>;
    }
  }
}

export interface HaTabsElement extends HTMLElement {
  selected: string;
}
