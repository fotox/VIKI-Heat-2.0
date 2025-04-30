import React, { useEffect, useState } from 'react'
import {
  Routes,
  Route,
  Navigate,
  useLocation,
} from 'react-router-dom'

import LoginPage from './routes/LoginPage'
import Dashboard from './routes/Dashboard'
import Analytics from './routes/Analytics'
import SettingsLayout from './routes/SettingsLayout'
import Energy from './routes/settings/Energy'
import Photovoltaic from './routes/settings/Photovoltaic'
import Heating from './routes/settings/Heating'
import Tanks from './routes/settings/Tanks'
import Weather from './routes/settings/Weather'
import Sensors from './routes/settings/Sensors'
import Location from './routes/settings/Location'
import Profile from './routes/Profile'

import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Breadcrumb from './components/Breadcrumb'
type AuthStatus = 'loading' | 'authenticated' | 'unauthenticated'

export default function App() {
  const [authStatus, setAuthStatus] = useState<AuthStatus>('loading')
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false)
  const location = useLocation()

  useEffect(() => {
    fetch('/api/auth/profile', { credentials: 'include' })
      .then(res => {
        if (res.ok) setAuthStatus('authenticated')
        else setAuthStatus('unauthenticated')
      })
      .catch(() => setAuthStatus('unauthenticated'))
  }, [])

  if (authStatus === 'loading') {
    return <div className="flex items-center justify-center h-screen">Loading…</div>
  }
  const isAuthenticated = authStatus === 'authenticated'

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar
        className={`${sidebarOpen ? 'block' : 'hidden'} md:block`}
        collapsed={sidebarCollapsed}
        onClose={() => setSidebarOpen(false)}
        onToggleCollapse={() => setSidebarCollapsed(c => !c)}
      />

      <div className="flex flex-col flex-1 overflow-hidden">
        <Header
          isAuthenticated={isAuthenticated}
          onOpenSidebar={() => setSidebarOpen(true)}
        />

        <div className="border-b bg-white px-4 py-2">
          <Breadcrumb path={location.pathname} />
        </div>

        <main className="flex-1 overflow-auto p-4">
          <Routes>
            <Route path="/login" element={<LoginPage onLogin={() => setAuthStatus('authenticated')} />} />
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />

            {isAuthenticated && (
              <>
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/settings" element={<SettingsLayout />}>
                  <Route path="energy" element={<Energy />} />
                  <Route path="photovoltaic" element={<Photovoltaic />} />
                  <Route path="sensors" element={<Sensors />} />
                  <Route path="heating" element={<Heating />} />
                  <Route path="tanks" element={<Tanks />} />
                  <Route path="location" element={<Location />} />
                  <Route path="weather" element={<Weather />} />
                </Route>
                <Route path="/profile" element={<Profile />} />
              </>
            )}

            {!isAuthenticated && (
              <Route path="*" element={<Navigate to="/login" replace />} />
            )}
          </Routes>
        </main>
      </div>
    </div>
  )
}
