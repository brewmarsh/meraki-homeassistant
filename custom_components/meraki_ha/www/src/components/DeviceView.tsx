import React from 'react';

interface DeviceViewProps {
  activeView: { view: string; deviceId?: string };
  setActiveView: (view: { view: string; deviceId?: string }) => void;
  data: any;
}

const DeviceView: React.FC<DeviceViewProps> = ({
  activeView,
  setActiveView,
  data,
}) => {
  const device = data.devices.find(
    (d: any) => d.serial === activeView.deviceId
  );

  if (!device) {
    return (
      <div>
        <button
          onClick={() => setActiveView({ view: 'dashboard' })}
          className="text-blue-500 mb-4"
        >
          &larr; Back to Dashboard
        </button>
        <p>Device not found.</p>
      </div>
    );
  }

  const {
    name,
    model,
    serial,
    firmware,
    status,
    status_messages = [],
    entities = [],
  } = device;

  return (
    <div>
      <button
        onClick={() => setActiveView({ view: 'dashboard' })}
        className="text-blue-500 mb-4 hover:underline"
      >
        &larr; Back to Dashboard
      </button>

      <div className="bg-light-card dark:bg-dark-card p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-bold mb-2">{name}</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div>
            <strong>Model:</strong> {model}
          </div>
          <div>
            <strong>Serial:</strong> {serial}
          </div>
          <div>
            <strong>Firmware:</strong> {firmware}
          </div>
          <div>
            <strong>Status:</strong>{' '}
            <span className="capitalize">{status}</span>
          </div>
        </div>
      </div>

      {status_messages.length > 0 && (
        <div className="mb-8">
          <h3 className="text-xl font-semibold mb-2">Status Messages</h3>
          <div className="bg-yellow-100 dark:bg-yellow-900 border-l-4 border-yellow-500 text-yellow-700 dark:text-yellow-200 p-4 rounded-lg">
            <ul>
              {status_messages.map((msg: string, index: number) => (
                <li key={index} className="mb-1">
                  {msg}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      <div>
        <h3 className="text-xl font-semibold mb-4">Entities</h3>
        <div className="overflow-x-auto bg-light-card dark:bg-dark-card p-4 rounded-lg shadow-md">
          <table className="min-w-full">
            <thead>
              <tr className="border-b border-light-border dark:border-dark-border">
                <th className="text-left p-4 font-semibold">Name</th>
                <th className="text-left p-4 font-semibold">Entity ID</th>
                <th className="text-left p-4 font-semibold">State</th>
              </tr>
            </thead>
            <tbody>
              {entities.map((entity: any) => (
                <tr
                  key={entity.entity_id}
                  className="border-b border-light-border dark:border-dark-border last:border-b-0"
                >
                  <td className="p-4">{entity.name}</td>
                  <td className="p-4">{entity.entity_id}</td>
                  <td className="p-4">{entity.state}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DeviceView;
