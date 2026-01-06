import React from 'react';
import ReactDOM from 'react-dom/client';
<<<<<<< HEAD
<<<<<<< HEAD
import App from './App.tsx';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
=======
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
import App from './App';
import style from './index.css?inline';
import { version } from '../package.json';

console.info(
  `%c 🌐 Meraki HA 🌐 %c ${version} `,
  'color: white; background: #2E7D32; font-weight: 700;',
  'color: #2E7D32; background: white; font-weight: 700;'
);

class MerakiPanel extends HTMLElement {
  private _root: ReactDOM.Root | null = null;
  private _hass: any;
  private _panel: any;
  private _mountPoint?: HTMLDivElement;

  connectedCallback() {
    if (!this.shadowRoot) {
      this.attachShadow({ mode: 'open' });
      this._mountPoint = document.createElement('div');
      this._mountPoint.id = 'root';

      const styleElement = document.createElement('style');
      styleElement.textContent = style;

      this.shadowRoot!.appendChild(styleElement);
      this.shadowRoot!.appendChild(this._mountPoint);
      this._root = ReactDOM.createRoot(this._mountPoint);
    }
    this._render();
  }

  set hass(hass: any) {
    this._hass = hass;

    if (this._mountPoint) {
      if (hass?.themes?.darkMode) {
        this._mountPoint.classList.add('dark');
      } else {
        this._mountPoint.classList.remove('dark');
      }
    }

    this._render();
  }

  set panel(panel: any) {
    this._panel = panel;
    this._render();
  }

  private _render() {
    if (!this._root || !this._hass || !this._panel) {
      return;
    }
    this._root.render(
      <React.StrictMode>
        <App hass={this._hass} panel={this._panel} />
      </React.StrictMode>
    );
  }
}

if (!customElements.get('meraki-panel')) {
  customElements.define('meraki-panel', MerakiPanel);
}
<<<<<<< HEAD
>>>>>>> origin/fix/meraki-load-fail-cleanup-7732058548349983668
=======
>>>>>>> origin/fix/wireless-ipsk-crash-14368601733312930129
