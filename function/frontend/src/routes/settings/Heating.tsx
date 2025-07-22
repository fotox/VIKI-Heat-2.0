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
import {
  ManufacturerSelect,
  SelectedManufacturerType,
  getManufacturerLabel
} from "@/components/selectors/ManufacturerSelect";
import { maskText } from "@/hooks/useMaskText";

interface HeatingModule {
  id: number
  description: string
  manufacturer: SelectedManufacturerType
  ip: string | null
  api_key: string | null
  buffer: number
}

export default function Heating() {
  const [modules, setModules] = useState<HeatingModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<HeatingModule | null>(null)
  const [description, setDescription] = useState<string>('')
  const [selectedManufacturer, setSelectedManufacturer] = useState<SelectedManufacturerType | null>(null)
  const [manufacturers, setManufacturers] = useState<SelectedManufacturerType[]>([])
  const [ip, setIp] = useState<string>('')
  const [api_key, setApiKey] = useState<string>('')
  const [buffer, setBuffer] = useState<number | null>(0)

  useEffect(() => {
    fetch("/api/settings/manufacturer", { credentials: "include" })
      .then((res) => res.json())
      .then((data) =>
        setManufacturers(
          data.manufacturers.map((m: any) => ({
            id: m.id,
            label: `${m.manufacturer} - ${m.model_type}`,
          }))
        )
      )
  }, [])

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/heating', {
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

  // Delete Modules
  const handleDelete = async (id: number) => {
    if (!confirm('Energiequelle wirklich löschen?')) return
    await fetch(`/api/settings/heating/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/heating', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id, ip: ip,
        api_key: api_key, buffer: buffer })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: HeatingModule) => {
    setEditModule(mod)
    setDescription(mod.description)
    const found = manufacturers.find((m) =>
        m.id === mod.manufacturer?.id || m.id === Number(mod.manufacturer))
    setSelectedManufacturer(found ?? null)
    setIp(String(mod.ip))
    setApiKey(String(mod.api_key))
    setBuffer(mod.buffer)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/heating/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id, ip: ip,
        api_key: api_key, buffer: buffer })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription("")
    setSelectedManufacturer(null)
    setIp("")
    setApiKey("")
    setBuffer(0)
  }

  useEffect(() => {
    fetchModules()
  }, [])

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Wärmeerzeugungs-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neues Wärmeerzeugungs-Modul hinzufügen</DialogTitle>
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
                <label htmlFor="manufacturer">Hersteller:</label>
                <ManufacturerSelect
                    value={selectedManufacturer}
                    onChange={setSelectedManufacturer}
                    manufacturers={manufacturers}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="ip">IP-Adresse:</label>
                <Input
                    id="ip"
                    type="string"
                    value={ip} onChange={e => setIp(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="api_key">API-Key:</label>
                <Input
                    id="api_key"
                    type="password"
                    value={api_key} onChange={e => setApiKey(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="buffer">Puffer:</label>
                <Input
                    id="buffer"
                    type="number"
                    value={buffer ?? 0} onChange={e => setBuffer(Number(e.target.value))}
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
                <p><strong>Hersteller:</strong> {getManufacturerLabel(manufacturers, Number(mod.manufacturer))}</p>
                <p><strong>IP-Adresse:</strong> {mod.ip}</p>
                <p><strong>API-Key:</strong> {maskText(mod.api_key)}</p>
                <p><strong>Puffer:</strong> {mod.buffer}</p>
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
                <label htmlFor="manufacturer">Hersteller:</label>
                <ManufacturerSelect
                    value={selectedManufacturer}
                    onChange={setSelectedManufacturer}
                    manufacturers={manufacturers}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="ip">IP-Adresse:</label>
                <Input
                    id="ip"
                    type="string"
                    value={ip} onChange={e => setIp(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="api_key">API-Key:</label>
                <Input
                    id="api_key"
                    type="password"
                    value={maskText(api_key) ?? ''} onChange={e => setApiKey(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="buffer">Puffer:</label>
                <Input
                    id="buffer"
                    type="number"
                    value={buffer ?? 0} onChange={e => setBuffer(Number(e.target.value))}
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
