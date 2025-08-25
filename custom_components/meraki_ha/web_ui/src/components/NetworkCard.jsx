import React from 'react';
import { Link } from 'react-router-dom';

function NetworkCard({ network }) {
  return (
    <Link to={`/networks/${network.id}`} className="block hover:bg-light-background dark:hover:bg-dark-background">
      <div className="py-4 px-6">
        <p className="font-medium text-cisco-blue truncate">{network.name}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">ID: {network.id}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">Clients: {network.clientCount || 'N/A'}</p>
      </div>
    </Link>
  );
}

export default NetworkCard;
