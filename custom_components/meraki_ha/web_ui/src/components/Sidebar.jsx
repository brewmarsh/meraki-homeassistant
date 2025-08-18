import React from 'react';
import { NavLink } from 'react-router-dom';

const navigation = [
  { name: 'Dashboard', href: '/' },
  { name: 'Networks', href: '/networks' },
  { name: 'Clients', href: '/clients' },
  { name: 'Settings', href: '/settings' },
];

function Sidebar() {
  const navLinkClass = ({ isActive }) =>
    `flex items-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
      isActive
        ? 'bg-cisco-blue/10 text-cisco-blue dark:bg-cisco-blue/20 dark:text-cisco-blue'
        : 'hover:bg-light-background dark:hover:bg-dark-card'
    }`;

  return (
    <div className="flex flex-col h-full bg-light-card dark:bg-dark-card border-r border-light-border dark:border-dark-border">
      <div className="flex items-center justify-center h-16 border-b border-light-border dark:border-dark-border">
        <h1 className="text-xl font-bold">Meraki UI</h1>
      </div>
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={navLinkClass}
            end={item.href === '/'}
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}

export default Sidebar;
