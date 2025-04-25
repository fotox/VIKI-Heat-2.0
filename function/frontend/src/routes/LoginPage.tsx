import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input } from '@shadcn/ui';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      navigate('/dashboard');
    } else {
      alert('Login fehlgeschlagen');
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleLogin} className="space-y-4 p-6 bg-white rounded shadow">
        <h1 className="text-xl font-bold">Login</h1>
        <Input
          type="text"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Passwort"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <Button type="submit">Anmelden</Button>
      </form>
    </div>
  );
}
