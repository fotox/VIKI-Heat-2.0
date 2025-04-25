import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './routes/LoginPage';
import RegisterPage from './routes/RegisterPage';
import Dashboard from './routes/Dashboard';
import Analytics from './routes/Analytics';
import SettingsLayout from './routes/SettingsLayout';
import Profile from './routes/Profile';
import Header from './components/Header';

function App() {
  const isAuthenticated = document.cookie.includes('access_token');

  return (
    <div className="min-h-screen bg-gray-50">
      {isAuthenticated && <Header />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/"
          element={
            isAuthenticated ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
          }
        />
        <Route
          path="/dashboard"
          element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />}
        />
        <Route
          path="/analytics"
          element={isAuthenticated ? <Analytics /> : <Navigate to="/login" />}
        />
        <Route path="/settings/*" element={<SettingsLayout />} />
        <Route
          path="/profile"
          element={isAuthenticated ? <Profile /> : <Navigate to="/login" />}
        />
        <Route
          path="/register"
          element={<RegisterPage />}
        />
        <Route
          path="/analytics"
          element={<Analytics />}
        />
        <Route
          path="/settings/*"
          element={<SettingsLayout />}>
          {/* Nested routes hier */}
        </Route>
        <Route
          path="/profile"
          element={<Profile />}
        />
      </Routes>
    </div>
  );
}

export default App;
