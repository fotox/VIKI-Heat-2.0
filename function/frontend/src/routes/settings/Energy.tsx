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

interface EnergyModule {
  id: number
  system_id: string
  manufacturer: number
  ip: string
  url: string
  battery_api: string
  feed_in_api: string
  production_api: string
}

export default function Energy() {
  const [modules, setModules] = useState<EnergyModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<EnergyModule | null>(null)
  const [systemId, setSystemId] = useState<string>('')
  const [manufacturer, setManufacturer] = useState<number>(0)
  const [ip, setIp] = useState<string>('')
  const [url, setUrl] = useState<string>('')
  const [battery_api, setBatteryApi] = useState<string>('')
  const [feed_in_api, setFeedInApi] = useState<string>('')
  const [production_api, setProductionApi] = useState<string>('')

  // TODO: Hersteller als Dropdown einbinden

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/energy', {
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
    await fetch(`/api/settings/energy/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/energy', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_id: systemId, manufacturer: manufacturer, ip: ip, url: url,
        battery_api: battery_api, feed_in_api: feed_in_api, production_api: production_api })
    })
    setSystemId(''); setManufacturer(0); setIp(''); setUrl(''); setBatteryApi('');
    setFeedInApi(''); setProductionApi('')
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: EnergyModule) => {
    setEditModule(mod)
    setSystemId(mod.system_id)
    setManufacturer(mod.manufacturer)
    setIp(mod.ip)
    setUrl(mod.url)
    setBatteryApi(mod.battery_api)
    setFeedInApi(mod.feed_in_api)
    setProductionApi(mod.production_api)
  }
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/energy/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system_id: systemId, manufacturer: manufacturer, ip: ip, url: url,
        battery_api: battery_api, feed_in_api: feed_in_api, production_api: production_api })
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
        <h3 className="text-xl font-semibold">Wechselrichter-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Neues Energy-Modul hinzufügen</DialogTitle>
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
              Batterie-API: <Input
                label="Batterie-API"
                type="string"
                value={battery_api}
                onChange={e => setBatteryApi(e.target.value)}
              />
              Energiebezug-API: <Input
                label="Energiebezug-API"
                type="string"
                value={feed_in_api}
                onChange={e => setFeedInApi(e.target.value)}
              />
              Produktions-API: <Input
                label="Produktion-API"
                type="string"
                value={production_api}
                onChange={e => setProductionApi(e.target.value)}
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
              <p><strong>Batterie-API:</strong> {mod.battery_api}</p>
              <p><strong>Energiebezug-API:</strong> {mod.feed_in_api}</p>
              <p><strong>Produktion-API:</strong> {mod.production_api}</p>
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
              Batterie-API: <Input
                label="Batterie-API"
                type="string"
                value={battery_api}
                onChange={e => setBatteryApi(e.target.value)}
              />
              Energiebezug-API: <Input
                label="Energiebezug-API"
                type="string"
                value={feed_in_api}
                onChange={e => setFeedInApi(e.target.value)}
              />
              Produktions-API: <Input
                label="Produktion-API"
                type="string"
                value={production_api}
                onChange={e => setProductionApi(e.target.value)}
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
