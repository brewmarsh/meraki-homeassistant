import React from 'react';
import { Link } from 'react-router-dom';

function ClientCard({ client }) {
  return (
    <Link to={`/clients/${client.mac}`} className="block hover:bg-gray-50">
      <div className="py-4 px-4">
        <p className="font-medium text-indigo-600 truncate">{client.description || 'No description'}</p>
        <p className="text-sm text-gray-500">MAC: {client.mac}</p>
        <p className="text-sm text-gray-500">IP: {client.ip || 'N/A'}</p>
      </div>
    </Link>
  );
}

export default ClientCard;
