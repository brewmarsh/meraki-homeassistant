import React from 'react';
import { Link } from 'react-router-dom';

function NetworkCard({ network }) {
  return (
    <Link to={`/networks/${network.id}`} className="block hover:bg-gray-50">
      <div className="py-4 px-4">
        <p className="font-medium text-indigo-600 truncate">{network.name}</p>
        <p className="text-sm text-gray-500">ID: {network.id}</p>
        <p className="text-sm text-gray-500">Clients: {network.clientCount || 'N/A'}</p>
      </div>
    </Link>
  );
}

export default NetworkCard;
