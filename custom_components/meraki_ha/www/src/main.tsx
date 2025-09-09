import React from 'react';
import ReactDOM from 'react-dom/client';

class MerakiHaPanel extends HTMLElement {
  connectedCallback() {
    this.attachShadow({ mode: 'open' });
    const rootDiv = document.createElement('div');
    rootDiv.id = 'root';
    this.shadowRoot!.appendChild(rootDiv);
    const root = ReactDOM.createRoot(rootDiv);
    root.render(
      <React.StrictMode>
        <h1>Hello from Meraki!</h1>
      </React.StrictMode>
    );
  }
}

customElements.define('meraki-ha-panel', MerakiHaPanel);
