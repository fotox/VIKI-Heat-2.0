import React, { useEffect, useState } from 'react';
import { Button, Input } from '@shadcn/ui';

export default function Profile() {
  const [username, setUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    // Hole Profil-Daten, falls API vorhanden
    fetch('/api/auth/profile', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setUsername(data.username))
      .catch(() => setUsername(''));
  }, []);

  const handleChangePassword = async () => {
    const res = await fetch('/api/auth/reset-password', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        master_key: prompt('Master-Key eingeben') || '',
        username,
        new_password: newPassword
      })
    });
    if (res.ok) {
      setStatus('Passwort erfolgreich geändert');
    } else {
      const { msg } = await res.json();
      setStatus('Fehler: ' + msg);
    }
  };

  return (
    <div className="p-6 max-w-md mx-auto space-y-4">
      <h2 className="text-2xl font-bold">Profil</h2>
      <div>
        <label className="block text-sm font-medium">Benutzername</label>
        <Input value={username} disabled />
      </div>
      <div>
        <label className="block text-sm font-medium">Neues Passwort</label>
        <Input
          type="password"
          value={newPassword}
          onChange={e => setNewPassword(e.target.value)}
        />
      </div>
      <Button onClick={handleChangePassword}>Passwort ändern</Button>
      {status && <p className="mt-2 text-sm">{status}</p>}
    </div>
  );
}
