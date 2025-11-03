
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

const mockHass = {
  connection: {
    sendMessagePromise: async (message: any) => {
      console.log('Mock sendMessagePromise called with:', message);
      return Promise.resolve({
        networks: [{ id: 'net-1', name: 'Marshmallow Home' }, { id: 'net-2', name: 'Shenanibarn' }],
        devices: [
          { networkId: 'net-1', name: 'Living Room AP', model: 'MR33', serial: 'Q2JD-XXXX-YYYY', status: 'online', lanIp: '192.168.1.1' },
          { networkId: 'net-2', name: 'Barn Camera', model: 'MV12', serial: 'Q2LD-XXXX-ZZZZ', status: 'online', lanIp: '10.0.0.1' },
        ],
      });
    }
  },
  themes: {
    darkMode: true,
  },
};

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App hass={mockHass} config_entry_id="mock-entry-id" />
  </React.StrictMode>
);
