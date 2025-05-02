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
import {CheckboxItem} from "@radix-ui/react-dropdown-menu";

interface HeatingModule {
  id: number
  system_id: string
  manufacturer: number
  api: string
  ip: string
  url: string
  price: number
  power_factor: number
  selected: boolean
}

export default function Heating() {
  const [modules, setModules] = useState<HeatingModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<HeatingModule | null>(null)
  const [systemId, setSystemId] = useState<string>('')
  const [manufacturer, setManufacturer] = useState<number>(0)
  const [api, setApi] = useState<string>('')
  const [ip, setIp] = useState<string>('')
  const [url, setUrl] = useState<string>('')
  const [price, setPrice] = useState<number>('')
  const [power_factor, setPowerFactor] = useState<number>('')
  const [selected, setSelected] = useState<boolean>('')

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

  useEffect(() => {
    fetchModules()
  }, [])

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
      body: JSON.stringify({ system_id: systemId, manufacturer: manufacturer, api: api, ip: ip, url: url,
        price: price, power_factor: power_factor, selected: selected })
    })
    setSystemId(''); setManufacturer(0); setApi(''); setIp(''); setUrl('');
    setPrice(0.0); setPowerFactor(0.0); setSelected(false)
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: HeatingModule) => {
    setEditModule(mod)
    setSystemId(mod.system_id)
    setManufacturer(mod.manufacturer)
    setIp(mod.api)
    setIp(mod.ip)
    setUrl(mod.url)
    setPrice(mod.price)
    setPowerFactor(mod.power_factor)
    setSelected(mod.selected)
  }
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/heating/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_id: systemId, manufacturer: manufacturer, api: api, ip: ip, url: url,
        price: price, power_factor: power_factor, selected: selected })
    })
    setEditModule(null)
    fetchModules()
  }

  // TODO: Load manufacturer name by id and add select bar with manufacturer infos

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Wärmeerzeugungs-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Neues Wärmeerzeugungs-Modul hinzufügen</DialogTitle>
            </DialogHeader>

            <form onSubmit={handleAdd} className="space-y-4">
              Bezeichnung: <Input
                label="System-ID"
                value={systemId}
                onChange={e => setSystemId(e.target.value)}
                required
              />
              Hersteller: <Input
                label="Hersteller"
                value={manufacturer}
                type="number"
                onChange={e => setManufacturer(e.target.value)}
                required
              />
              IP-Adresse: <Input
                label="IP-Adresse"
                type="string"
                value={ip}
                onChange={e => setIp(e.target.value)}
                required
              />
              URL: <Input
                label="URL"
                type="string"
                value={url}
                onChange={e => setUrl(e.target.value)}
                required
              />
              API: <Input
                label="API"
                type="string"
                value={api}
                onChange={e => setIp(e.target.value)}
                required
              />
              Preis (€/kWh): <Input
                label="Preis"
                type="number"
                value={price}
                onChange={e => setPrice(e.target.value)}
              />
              Leistungsfaktor (1:...): <Input
                label="Leistungsfaktor"
                type="number"
                value={power_factor}
                onChange={e => setPowerFactor(e.target.value)}
              />
              Aktiv: <Input
                label="Aktiv"
                type="boolean"
                value={selected}
                onChange={e => setSelected(e.target.value)}
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
              <p><strong>Hersteller:</strong> {mod.manufacturer}</p>
              <p><strong>IP-Adresse:</strong> {mod.ip}</p>
              <p><strong>URL:</strong> {mod.url}</p>
              <p><strong>API:</strong> {mod.api}</p>
              <p><strong>Preis (€/kWh):</strong> {mod.price}</p>
              <p><strong>Leistungsfaktor (1:...):</strong> {mod.power_factor}</p>
              <p><strong>Aktiv:</strong> {mod.selected}</p>
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
              Hersteller: <Input
                label="Hersteller"
                value={manufacturer}
                type="number"
                onChange={e => setManufacturer(e.target.value)}
                required
              />
              IP-Adresse: <Input
                label="IP-Adresse"
                type="string"
                value={ip}
                onChange={e => setIp(e.target.value)}
                required
              />
              URL: <Input
                label="URL"
                type="string"
                value={url}
                onChange={e => setUrl(e.target.value)}
                required
              />
              API: <Input
                label="API"
                type="string"
                value={api}
                onChange={e => setIp(e.target.value)}
                required
              />
              Preis (€/kWh): <Input
                label="Preis"
                type="number"
                value={price}
                onChange={e => setPrice(e.target.value)}
              />
              Leistungsfaktor (1:...): <Input
                label="Leistungsfaktor"
                type="number"
                value={power_factor}
                onChange={e => setPowerFactor(e.target.value)}
              />
              Aktiv: <Input  // TODO: Change to Checkbox
                label="Aktiv"
                type="boolean"
                value={selected}
                onChange={e => setSelected(e.target.value)}
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
