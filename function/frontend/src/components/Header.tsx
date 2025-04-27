// @ts-ignore
import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui';

export default function Header() {
  const navigate = useNavigate();

  const handleLogout = async () => {
    // Optional: API-Logout aufrufen, dann Cookie löschen
    document.cookie = 'access_token=; Max-Age=0; path=/';
    navigate('/login');
  };

  return (
    <header className="bg-white shadow p-4 flex justify-between items-center">
      <nav className="space-x-4">
        <NavLink to="/dashboard" className="font-medium hover:underline">
          Dashboard
        </NavLink>
        <NavLink to="/analytics" className="font-medium hover:underline">
          Analytics
        </NavLink>
        <NavLink to="/settings" className="font-medium hover:underline">
          Settings
        </NavLink>
        <NavLink to="/profile" className="font-medium hover:underline">
          Profile
        </NavLink>
      </nav>
      <Button variant="ghost" onClick={handleLogout}>
        Logout
      </Button>
    </header>
  );
}
