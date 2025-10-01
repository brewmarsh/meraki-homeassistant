import React from 'react';

// Define a simplified type for the Home Assistant object
interface Hass {
  connection: {
    sendMessagePromise: (message: any) => Promise<any>;
  };
  // Add other properties of hass object if needed
}


interface AppProps {
  hass: Hass;
  panel: any;
}

const App: React.FC<AppProps> = ({ panel }) => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Panel Debug Information</h1>
      <pre>
        {JSON.stringify(panel, null, 2)}
      </pre>
    </div>
  );
};

export default App;