import React from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui'

export default function Header({ isAuthenticated }: { isAuthenticated: boolean }) {
  const navigate = useNavigate()

  const handleLogout = () => {
    document.cookie = 'access_token=; Max-Age=0; path=/'
    navigate('/login')
  }

  return (
    <header className="bg-white shadow p-4 flex justify-between items-center">
      <nav className="space-x-4">
        <NavLink to="/dashboard">Dashboard</NavLink>
        {isAuthenticated && <NavLink to="/analytics">Analytics</NavLink>}
        {isAuthenticated && <NavLink to="/settings">Settings</NavLink>}
        {isAuthenticated && <NavLink to="/profile">Profile</NavLink>}
      </nav>
      {isAuthenticated ? (
        <Button variant="ghost" onClick={handleLogout}>Logout</Button>
      ) : (
        <Button variant="ghost" onClick={() => navigate('/login')}>Login</Button>
      )}
    </header>
  )
}
