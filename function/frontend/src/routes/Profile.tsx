import React, { useEffect, useState, ChangeEvent } from 'react'
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
  Label,
  Input,
  Button,
  Avatar,
  AvatarImage,
  AvatarFallback
} from '@/components/ui'
import { Image, Lock } from 'lucide-react'

export default function Profile() {
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('')
  const [phone, setPhone] = useState('')
  const [firstName, setFirstName] = useState('')
  const [lastName, setLastName] = useState('')
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [preview, setPreview] = useState<string>('/api/auth/profile/photo')

  useEffect(() => {
    (async () => {
      const res = await fetch('/api/auth/profile', { credentials: 'include' })
      if (res.ok) {
        const { user } = await res.json()
        setUsername(user.username)
        setRole(user.role)
      }
    })()
  }, [])

  const onFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    if (!['image/png','image/jpeg'].includes(f.type)) {
      return alert('Nur PNG/JPEG erlaubt')
    }
    if (f.size > 5 * 1024 * 1024) {
      return alert('Maximale Dateigröße: 5 MB')
    }
    setFile(f)
    setPreview(URL.createObjectURL(f))
  }

  // Form-Submit
  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (newPassword && newPassword !== confirmPassword) {
      return alert('Passwörter stimmen nicht überein')
    }
    const form = new FormData()
    form.append('username', username)
    if (currentPassword && newPassword) {
      form.append('password', newPassword)
      form.append('current_password', currentPassword)
    }
    if (file) {
      form.append('photo', file)
    }

    const res = await fetch('/api/auth/profile', {
      method: 'PUT',
      credentials: 'include',
      body: form,
    })
    if (res.ok) {
      window.location.reload()
    } else {
      const data = await res.json()
      alert(data.msg || 'Fehler beim Speichern')
    }
  }

  return (
    <Card className="max-w-3xl mx-auto">
      <CardHeader>
        <CardTitle>Benutzerdaten</CardTitle>
        <CardDescription>
          Aktualisiere deine persönlichen Daten und dein Foto hier.
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <form onSubmit={onSubmit} className="space-y-6">
          {/* Grid für Basis-Daten */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <Label>Vorname</Label>
              <Input
                value={firstName}
                onChange={e => setFirstName(e.target.value)}
                placeholder="Vorname"
              />
            </div>
            <div>
              <Label>Nachname</Label>
              <Input
                value={lastName}
                onChange={e => setLastName(e.target.value)}
                placeholder="Nachname"
              />
            </div>
            <div>
              <Label>Benutzername</Label>
              <Input
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="Username"
                required
              />
            </div>
            <div>
              <Label>Rolle</Label>
              <Input
                value={role}
                onChange={e => setRole(e.target.value)}
                placeholder="Rolle"
              />
            </div>
            <div>
              <Label>E-Mail Adresse</Label>
              <Input
                type="email"
                value={email}
                onChange={e => setEmail(e.target.value)}
                placeholder="name@beispiel.de"
              />
            </div>
            <div>
              <Label>Telefonnummer</Label>
              <Input
                value={phone}
                onChange={e => setPhone(e.target.value)}
                placeholder="+49 123 456789"
              />
            </div>
          </div>

          {/* Passwort ändern */}
          <div className="space-y-2">
            <Label className="flex items-center space-x-2">
              <Lock className="h-4 w-4 text-gray-500" />
              <span>Passwort ändern</span>
            </Label>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Input
                type="password"
                placeholder="Aktuelles Passwort"
                value={currentPassword}
                onChange={e => setCurrentPassword(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Neues Passwort"
                value={newPassword}
                onChange={e => setNewPassword(e.target.value)}
              />
              <Input
                type="password"
                placeholder="Passwort bestätigen"
                value={confirmPassword}
                onChange={e => setConfirmPassword(e.target.value)}
              />
            </div>
          </div>

          {/* Foto-Upload */}
          <div className="space-y-2">
            <Label className="flex items-center space-x-2">
              <Image className="h-4 w-4 text-gray-500" />
              <span>Foto</span>
            </Label>
            <div className="flex items-center space-x-6">
              <Avatar className="h-24 w-24">
                <AvatarImage
                  src={preview}
                  alt="Profilfoto"
                />
                <AvatarFallback className="text-2xl">
                  {username.charAt(0).toUpperCase()}
                </AvatarFallback>
              </Avatar>
              <div>
                <input
                  type="file"
                  accept="image/png,image/jpeg"
                  onChange={onFileChange}
                  className="block text-sm"
                />
                <p className="text-xs text-gray-500 mt-1">PNG oder JPEG, max. 5 MB</p>
              </div>
            </div>
          </div>

          {/* Save-Button */}
          <CardFooter className="flex justify-end">
            <Button type="submit">Speichern</Button>
          </CardFooter>
        </form>
      </CardContent>
    </Card>
  )
}
