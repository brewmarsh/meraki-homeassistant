import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import style from './index.css?inline';

class MerakiPanel extends HTMLElement {
  connectedCallback() {
    if (!this.shadowRoot) {
      this.attachShadow({ mode: 'open' });
      const mountPoint = document.createElement('div');
      mountPoint.id = 'root';

      // Create style element
      const styleElement = document.createElement('style');
      styleElement.textContent = style;

      this.shadowRoot!.appendChild(styleElement);
      this.shadowRoot!.appendChild(mountPoint);

      const root = ReactDOM.createRoot(mountPoint);
      root.render(
        <React.StrictMode>
          <App />
        </React.StrictMode>
      );
    }
  }
}

if (!customElements.get('meraki-panel')) {
  customElements.define('meraki-panel', MerakiPanel);
}
