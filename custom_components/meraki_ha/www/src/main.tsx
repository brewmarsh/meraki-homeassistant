import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

// Define the types for the properties Home Assistant will pass to the panel
interface PanelInfo {
  config: {
    config_entry_id: string;
  };
  // Add other panel properties if needed
}

interface HassObject {
  // Define a minimal hass object type
  connection: any;
  connected: boolean;
}

class MerakiPanel extends HTMLElement {
  private _root?: ReactDOM.Root;
  private _hass?: HassObject;
  private _panel?: PanelInfo;

  connectedCallback() {
    this._root = ReactDOM.createRoot(this);
    this._render();
  }

  disconnectedCallback() {
    if (this._root) {
      this._root.unmount();
      this._root = undefined;
    }
  }

  set hass(hass: HassObject) {
    this._hass = hass;
    this._render();
  }

  set panel(panel: PanelInfo) {
    console.log("Panel config:", panel);
    this._panel = panel;
    this._render();
  }

  private _render() {
    if (!this._root || !this._hass || !this._panel) {
      return;
    }

    this._root.render(
      <React.StrictMode>
        <App hass={this._hass} config_entry_id={this._panel.config.config_entry_id} />
      </React.StrictMode>
    );
  }
}

customElements.define('meraki-panel', MerakiPanel);
