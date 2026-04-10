import { html, css } from 'lit';

export const renderWarning = (title: string, message: string, version?: string) => html`
  <ha-card class="status-card warning">
    <div class="card-content flex-col align-center p-8">
      <ha-icon icon="mdi:alert-circle" style="--mdc-icon-size: 48px; margin-bottom: 16px;"></ha-icon>
      <h1 class="status-title">${title}</h1>
      <div class="status-message mt-4">${message}</div>
    </div>
    ${version ? html`<div class="version">v${version}</div>` : ''}
  </ha-card>
`;

export const renderLoadingState = (title: string, message: string, version: string) => html`
  <ha-card class="status-card loading">
    <div class="card-content flex-col align-center p-8">
      <h1 class="status-title">${title}</h1>
      <ha-circular-progress active></ha-circular-progress>
      <div class="status-message mt-4">${message}</div>
    </div>
    <div class="version">v${version}</div>
  </ha-card>
`;

export const renderLoading = (title: string) => html`
  <div class="meraki-loading">
    <ha-circular-progress active></ha-circular-progress>
    <span>${title}</span>
  </div>
`;

export const sharedStyles = css`
  ha-card.status-card {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
    border-radius: 12px;
    overflow: hidden;
  }
  ha-card.status-card.loading {
    --ha-card-background: var(--info-color, #2196f3);
    background-color: var(--info-color, #2196f3) !important;
  }
  ha-card.status-card.warning {
    --ha-card-background: var(--warning-color, #ffeb3b);
    background-color: var(--warning-color, #ffeb3b) !important;
  }

  /* Force high-contrast dark text on bright colored backgrounds in light mode */
  .status-card .status-title,
  .status-card .status-message {
    color: #111111 !important;
    text-align: center;
  }

  .status-card .status-title {
    margin: 0;
    font-size: 1.5rem;
    font-weight: bold;
  }

  @media (prefers-color-scheme: dark) {
    ha-card.status-card.warning {
      --ha-card-background: rgba(255, 193, 7, 0.2);
      background-color: rgba(255, 193, 7, 0.2) !important;
    }
    ha-card.status-card.loading {
      --ha-card-background: rgba(33, 150, 243, 0.2);
      background-color: rgba(33, 150, 243, 0.2) !important;
    }
    .status-card .status-title,
    .status-card .status-message {
      color: var(--primary-text-color) !important;
    }
  }

  .flex-col { display: flex; flex-direction: column; }
  .flex-col-center { display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .align-center { align-items: center; }
  .p-8 { padding: 32px; }
  .mt-4 { margin-top: 16px; }

  .qr-container {
    background: white;
    padding: 16px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: var(--ha-card-box-shadow, 0 2px 2px 0 rgba(0, 0, 0, 0.14));
  }

  .qr-container svg {
    width: 100%;
    height: 100%;
  }

  .copyable-code {
    background: var(--card-background-color);
    padding: 4px 8px;
    border-radius: 4px;
    border: 1px solid var(--divider-color);
    font-family: var(--code-font-family, monospace);
    user-select: all;
  }

  .version {
    font-size: 9px;
    color: var(--secondary-text-color);
    text-align: right;
    padding: 4px 12px;
    opacity: 0.4;
  }

  /* Legacy styles for backward compatibility during transition */
  .meraki-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background-color: var(--warning-color);
    color: var(--primary-text-color);
    border-radius: 8px;
  }
  .meraki-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    gap: 12px;
  }
`;
