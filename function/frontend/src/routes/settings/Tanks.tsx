import React, { useEffect, useState } from 'react'
import { Trash2, Edit3, Plus } from 'lucide-react'
import {
  Card,
  Input,
  Button,
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose
} from '@/components/ui'

interface TankModule {
  id: number
  description: string
  volume: number
}

export default function Tank() {
  const [modules, setModules] = useState<TankModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<TankModule | null>(null)
  const [description, setDescription] = useState<string>('')
  const [volume, setVolume] = useState<number>(0)

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/tank', {
        credentials: 'include'
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const json = await res.json()
      setModules(json.modules || [])
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => {
    fetchModules()
  }, [])

  // Delete Modules
  const handleDelete = async (id: number) => {
    if (!confirm('Speichertank wirklich löschen?')) return
    await fetch(`/api/settings/tank/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/tank', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, volume: volume })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: TankModule) => {
    setEditModule(mod)
    setDescription(mod.description)
    setVolume(mod.volume)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/tank/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, volume: volume })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription("")
    setVolume(0)
  }

  if (loading) return <p>Lädt Speichertanks…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Speichertank-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neuen Speichertank hinzufügen</DialogTitle>
            </DialogHeader>

            <form onSubmit={handleAdd} className="space-y-4">
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="description">Bezeichnung:</label>
                <Input
                    id="description"
                    type="string"
                    value={description} onChange={e => setDescription(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="volume">Volumen:</label>
                <Input
                    id="volume"
                    type="number"
                    value={volume} onChange={e => setVolume(Number(e.target.value))}
                    required
                />
              </div>
              <DialogFooter>
                <Button type="submit">Hinzufügen</Button>
                <DialogClose asChild>
                  <Button variant="ghost">Abbrechen</Button>
                </DialogClose>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modules.map((mod) => (
            <Card key={mod.id} className="relative p-4">
              <div className="space-y-2">
                <p><strong>System:</strong> {mod.description}</p>
                <p><strong>Volumen:</strong> {mod.volume}</p>
              </div>
              <div className="absolute bottom-4 right-4 flex space-x-2">
              <Button
                size="icon"
                variant="ghost"
                onClick={() => openEdit(mod)}
              >
                <Edit3 className="h-4 w-4" />
              </Button>
              <Button
                size="icon"
                variant="ghost"
                onClick={() => handleDelete(mod.id)}
              >
                <Trash2 className="h-4 w-4 text-red-600" />
              </Button>
            </div>
          </Card>
        ))}
      </div>

      {editModule && (
        <Dialog open onOpenChange={open => !open && setEditModule(null)}>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Modul bearbeiten</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleEdit} className="space-y-4">
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="description">Bezeichnung:</label>
                <Input
                    id="description"
                    type="string"
                    value={description} onChange={e => setDescription(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="volume">Volumen:</label>
                <Input
                    id="volume"
                    type="number"
                    value={volume} onChange={e => setVolume(Number(e.target.value))}
                    required
                />
              </div>
              <DialogFooter>
                <Button type="submit">Speichern</Button>
                <DialogClose asChild>
                  <Button variant="ghost">Abbrechen</Button>
                </DialogClose>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      )}
    </div>
  )
}
