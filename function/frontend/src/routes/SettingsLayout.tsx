import React from 'react';
import { NavLink, Outlet } from 'react-router-dom';

export default function SettingsLayout() {
  const tabs = [
    { path: 'photovoltaik', label: 'Photovoltaik' },
    { path: 'wasserspeicher', label: 'Wasserspeicher' },
    { path: 'wetter', label: 'Wetter' },
    { path: 'others', label: 'Weitere' }
  ];

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold">Einstellungen</h2>
      <nav className="mt-4 border-b">
        <ul className="flex space-x-4">
          {tabs.map(tab => (
            <li key={tab.path}>
              <NavLink
                to={tab.path}
                className={({ isActive }) =>
                  `pb-2 ${isActive ? 'border-b-2 border-blue-500 font-semibold' : 'text-gray-600'}`
                }
              >
                {tab.label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>
      <div className="mt-6">
        <Outlet />
      </div>
    </div>
  );
}
