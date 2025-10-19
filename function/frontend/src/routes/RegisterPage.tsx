import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, Input, Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState<'admin' | 'user'>('user');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password, role })
    });
    if (res.ok) {
      alert('Benutzer angelegt');
      navigate('/dashboard');
    } else {
      const { msg } = await res.json();
      alert('Fehler: ' + msg);
    }
  };

  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={handleRegister} className="space-y-4 p-6 bg-white rounded shadow-md w-full max-w-sm">
        <h1 className="text-xl font-bold">Neuen Nutzer anlegen</h1>
        <Input
          type="text"
          placeholder="Benutzername"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <Input
          type="password"
          placeholder="Passwort"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        <Select onValueChange={val => setRole(val as 'admin' | 'user')}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Rolle wählen" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="user">User</SelectItem>
            <SelectItem value="admin">Admin</SelectItem>
          </SelectContent>
        </Select>
        <Button type="submit" className="w-full">
          Registrieren
        </Button>
      </form>
    </div>
  );
}
