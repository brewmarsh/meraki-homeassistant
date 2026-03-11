import { html, css } from 'lit';

export const renderWarning = (title: string, message: string) => html`
  <div class="meraki-warning">
    <ha-icon icon="mdi:information"></ha-icon>
    <div class="warning-content">
      <strong>${title}</strong>
      <p>${message}</p>
    </div>
  </div>
`;

export const renderLoading = (title: string) => html`
  <div class="meraki-loading">
    <ha-circular-progress active></ha-circular-progress>
    <span>${title}</span>
  </div>
`;

export const sharedStyles = css`
  .meraki-warning {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
    background-color: var(--warning-color);
    color: var(--primary-text-color);
    border-radius: 8px;
  }
  .warning-content strong {
    display: block;
    margin-bottom: 4px;
  }
  .warning-content p {
    margin: 0;
    font-size: 0.9em;
    opacity: 0.9;
  }
  .meraki-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 24px;
    gap: 12px;
  }
  .version {
    font-size: 9px;
    color: var(--secondary-text-color);
    text-align: right;
    padding: 4px 12px;
    opacity: 0.4;
  }
`;
