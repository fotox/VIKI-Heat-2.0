import React, { useEffect, useState } from 'react'
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
import { Trash2, Edit3, Plus } from 'lucide-react'

interface PVModule {
  id: number
  system_id: string
  duration: number
  angle: number
  max_output: number
}

export default function Photovoltaic() {
  const [modules, setModules] = useState<PVModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<PVModule | null>(null)
  const [systemId, setSystemId] = useState('')
  const [duration, setDuration] = useState<number>(0.0)
  const [angle, setAngle] = useState<number>(0.0)
  const [maxOutput, setMaxOutput] = useState<number>(0)

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/photovoltaic', {
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
    if (!confirm('Modul wirklich löschen?')) return
    await fetch(`/api/settings/photovoltaic/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/photovoltaic', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_id: systemId, duration: duration, angle: angle, max_output: maxOutput })
    })
    setSystemId(''); setDuration(''); setAngle(''); setMaxOutput(0)
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: PVModule) => {
    setEditModule(mod)
    setSystemId(mod.system_id)
    setDuration(mod.duration)
    setAngle(mod.angle)
    setMaxOutput(mod.max_output)
  }
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/photovoltaic/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_id: systemId, duration: duration, angle: angle, max_output: maxOutput })
    })
    setEditModule(null)
    fetchModules()
  }

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Photovoltaik-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Neues PV-Modul hinzufügen</DialogTitle>
            </DialogHeader>

            <form onSubmit={handleAdd} className="space-y-4">
              Bezeichnung: <Input
                label="System-ID"
                value={systemId}
                onChange={e => setSystemId(e.target.value)}
                required
              />
              Ausrichtung: <Input
                label="Ausrichtung"
                value={duration}
                type="number"
                onChange={e => setDuration(Number(e.target.value))}
                required
              />
              Anstellwinkel: <Input
                label="Anstellwinkel"
                type="number"
                value={angle}
                onChange={e => setAngle(Number(e.target.value))}
                required
              />
              Leistung (Wp): <Input
                label="Leistung (Wp)"
                type="number"
                value={maxOutput}
                onChange={e => setMaxOutput(Number(e.target.value))}
                required
              />
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

      {/* Module-Liste */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modules.map((mod) => (
          <Card key={mod.id} className="relative p-4">
            <div className="space-y-2">
              <p><strong>System:</strong> {mod.system_id}</p>
              <p><strong>Ausrichtung:</strong> {mod.duration}</p>
              <p><strong>Anstellwinkel:</strong> {mod.angle}</p>
              <p><strong>Leistung (Wp):</strong> {mod.max_output} kW</p>
            </div>
            {/* Edit/Delete Buttons */}
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

      {/* Edit-Dialog */}
      {editModule && (
        <Dialog open onOpenChange={open => !open && setEditModule(null)}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Modul bearbeiten</DialogTitle>
            </DialogHeader>
            <form onSubmit={handleEdit} className="space-y-4">
              Bezeichnung: <Input
                label="System-ID"
                value={systemId}
                onChange={e => setSystemId(e.target.value)}
                required
              />
              Ausrichtung: <Input
                label="Ausrichtung"
                value={duration}
                type="number"
                onChange={e => setDuration(Number(e.target.value))}
                required
              />
              Anstellwinkel: <Input
                label="Anstellwinkel"
                type="number"
                value={angle}
                onChange={e => setAngle(Number(e.target.value))}
                required
              />
              Leistung (Wp): <Input
                label="Leistung (Wp)"
                type="number"
                value={maxOutput}
                onChange={e => setMaxOutput(Number(e.target.value))}
                required
              />
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
