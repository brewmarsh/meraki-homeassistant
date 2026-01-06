/**
 * Home Assistant Custom Panel Entry Point
 *
 * This file creates a Web Component that wraps the React application,
 * allowing Home Assistant to pass the `hass` and `panel` objects to React.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
// Import CSS as string and inject it into the document
import styles from './index.css?inline';
import type { HomeAssistant, PanelInfo, RouteInfo } from './types/hass';

// Inject CSS into document head (since HA only loads the JS file)
const injectStyles = () => {
  if (!document.getElementById('meraki-panel-styles')) {
    const styleEl = document.createElement('style');
    styleEl.id = 'meraki-panel-styles';
    styleEl.textContent = styles;
    document.head.appendChild(styleEl);
  }
};
injectStyles();

/**
 * MerakiPanel Web Component
 *
 * This custom element acts as a bridge between Home Assistant's panel system
 * and our React application. Home Assistant will set the `hass`, `panel`,
 * `narrow`, and `route` properties, which we then pass to React.
 */
class MerakiPanelElement extends HTMLElement {
  private _hass: HomeAssistant | null = null;
  private _panel: PanelInfo | null = null;
  private _narrow: boolean = false;
  private _route: RouteInfo | null = null;
  private _root: ReactDOM.Root | null = null;
  private _mountPoint: HTMLDivElement | null = null;

  /**
   * Called when the element is added to the DOM.
   */
  connectedCallback(): void {
    // Create a mount point for React
    this._mountPoint = document.createElement('div');
    this._mountPoint.id = 'meraki-panel-root';
    this._mountPoint.style.height = '100%';
    this._mountPoint.style.width = '100%';
    this.appendChild(this._mountPoint);

    // Create React root
    this._root = ReactDOM.createRoot(this._mountPoint);

    // Initial render
    this._render();
  }

  /**
   * Called when the element is removed from the DOM.
   */
  disconnectedCallback(): void {
    if (this._root) {
      this._root.unmount();
      this._root = null;
    }
    if (this._mountPoint) {
      this._mountPoint.remove();
      this._mountPoint = null;
    }
  }

  /**
   * Home Assistant sets this property with the hass object.
   * This is called frequently as state changes.
   */
  set hass(hass: HomeAssistant) {
    this._hass = hass;
    this._render();
  }

  get hass(): HomeAssistant | null {
    return this._hass;
  }

  /**
   * Home Assistant sets this property with panel configuration.
   * This is called once when the panel is loaded.
   */
  set panel(panel: PanelInfo) {
    this._panel = panel;
    this._render();
  }

  get panel(): PanelInfo | null {
    return this._panel;
  }

  /**
   * Home Assistant sets this to indicate narrow/mobile mode.
   */
  set narrow(narrow: boolean) {
    this._narrow = narrow;
    this._render();
  }

  get narrow(): boolean {
    return this._narrow;
  }

  /**
   * Home Assistant sets this with route information.
   */
  set route(route: RouteInfo) {
    this._route = route;
    this._render();
  }

  get route(): RouteInfo | null {
    return this._route;
  }

  /**
   * Render the React application with current props.
   */
  private _render(): void {
    if (!this._root || !this._hass) {
      return;
    }

    this._root.render(
      <React.StrictMode>
        <App
          hass={this._hass}
          panel={this._panel}
          narrow={this._narrow}
          route={this._route}
        />
      </React.StrictMode>
    );
  }
}

// Register the custom element with the name Home Assistant expects
// Guard against duplicate registration (can happen with HMR or cache issues)
if (!customElements.get('meraki-panel')) {
  customElements.define('meraki-panel', MerakiPanelElement);
}
