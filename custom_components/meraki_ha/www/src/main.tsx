import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import style from './index.css?inline';

class MerakiPanel extends HTMLElement {
  private _root: ReactDOM.Root | null = null;
  private _hass: any;
  private _panel: any;

  connectedCallback() {
    if (!this.shadowRoot) {
      this.attachShadow({ mode: 'open' });
      const mountPoint = document.createElement('div');
      mountPoint.id = 'root';

      const styleElement = document.createElement('style');
      styleElement.textContent = style;

      this.shadowRoot!.appendChild(styleElement);
      this.shadowRoot!.appendChild(mountPoint);
      this._root = ReactDOM.createRoot(mountPoint);
    }
    this._render();
  }

  set hass(hass: any) {
    this._hass = hass;
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
