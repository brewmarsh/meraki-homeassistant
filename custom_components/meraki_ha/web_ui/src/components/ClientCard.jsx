import React from 'react';
import { Link } from 'react-router-dom';

function ClientCard({ client }) {
  return (
    <Link to={`/clients/${client.mac}`} className="block hover:bg-light-background dark:hover:bg-dark-background">
      <div className="py-4 px-6">
        <p className="font-medium text-cisco-blue truncate">{client.description || 'No description'}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">MAC: {client.mac}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">IP: {client.ip || 'N/A'}</p>
      </div>
    </Link>
  );
}

export default ClientCard;
