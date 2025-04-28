import React, { useEffect, useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './routes/LoginPage'
import Dashboard from './routes/Dashboard'
import Analytics from './routes/Analytics'
import SettingsLayout from './routes/SettingsLayout'
import Photovoltaic from './routes/settings/Photovoltaic'
import Wasserspeicher from './routes/settings/Wasserspeicher'
import Wetter from './routes/settings/Wetter'
import Others from './routes/settings/Others'
import Profile from './routes/Profile'
import Header from './components/Header'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false)

  useEffect(() => {
    fetch('/api/auth/profile', {
      credentials: 'include'
    })
      .then(res => setIsAuthenticated(res.ok))
      .catch(() => setIsAuthenticated(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      <Header isAuthenticated={isAuthenticated} />
      <Routes>
        <Route path="/login" element={<LoginPage onLogin={() => setIsAuthenticated(true)} />} />
        <Route path="/" element={<Navigate to="/dashboard" />} />
        <Route path="/dashboard" element={<Dashboard />} />
        {isAuthenticated && (
          <>
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<SettingsLayout />}>
              <Route index element={<div>Wähle eine Settings-Kategorie aus.</div>} />
              <Route path="photovoltaik" element={<Photovoltaic />} />
              <Route path="wasserspeicher" element={<Wasserspeicher />} />
              <Route path="wetter" element={<Wetter />} />
              <Route path="others" element={<Others />} />
            </Route>
          </>
        )}
        {/* Fallback: nicht angemeldet und falsche Route */}
        {!isAuthenticated && <Route path="*" element={<Navigate to="/login" replace />} />}
      </Routes>
    </div>
  )
}

export default App
