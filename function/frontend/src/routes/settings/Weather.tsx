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
  getManufacturerLabel,
  getManufacturerPowerSize
} from "@/components/selectors/ManufacturerSelect";
import {
  LocationSelect,
  SelectedLocationType,
  getLocationLabel
} from "@/components/selectors/LocationSelect";
import { maskText } from "@/components/Helper";

interface WeatherModule {
  id: number
  description: string
  manufacturer: SelectedManufacturerType
  location: SelectedLocationType
  ip: string
  api_key: string
}

export default function Weather() {
  const [modules, setModules] = useState<WeatherModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<WeatherModule | null>(null)
  const [description, setDescription] = useState('')
  const [selectedManufacturer, setSelectedManufacturer] = useState<SelectedManufacturerType | null>(null)
  const [manufacturers, setManufacturers] = useState<SelectedManufacturerType[]>([])
  const [selectedLocation, setSelectedLocation] = useState<SelectedLocationType | null>(null)
  const [locations, setLocations] = useState<SelectedLocationType[]>([])
  const [ip, setIp] = useState<string | null>(null)
  const [api_key, setApiKey] = useState<string | null>(null)

  useEffect(() => {
    fetch("/api/settings/manufacturer", { credentials: "include" })
      .then((res) => res.json())
      .then((data) =>
        setManufacturers(
          data.manufacturers.map((m: any) => ({
            id: m.id,
            label: `${m.manufacturer} - ${m.model_type}`,
            power_size: m.power_size,
          }))
        )
      )
  }, [])

  useEffect(() => {
    fetch("/api/settings/location", { credentials: "include" })
      .then((res) => res.json())
      .then((data) =>
        setLocations(
          data.locations.map((l: any) => ({
            id: l.id,
            label: `${l.description}`,
          }))
        )
      )
  }, [])

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/weather', {
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
    await fetch(`/api/settings/weather/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/weather', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id,
        location: selectedLocation?.id, ip: ip, api_key: api_key })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: WeatherModule) => {
    setEditModule(mod)
    setDescription(mod.description)
    const found_manufacturer = manufacturers.find((m) =>
        m.id === mod.manufacturer?.id || m.id === Number(mod.manufacturer))
    setSelectedManufacturer(found_manufacturer ?? null)
    const found_location = locations.find((l) =>
        l.id === mod.location?.id || l.id === Number(mod.location))
    setSelectedLocation(found_location ?? null)
    setIp(mod.ip)
    setApiKey(mod.api_key)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/weather/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id,
        location: selectedLocation?.id, ip: ip, api_key: api_key })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription("")
    setSelectedManufacturer(null)
    setSelectedLocation(null)
    setIp("")
    setApiKey("")
  }

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Wetter-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neues Wetter-Modul hinzufügen</DialogTitle>
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
                <label htmlFor="location">Standort:</label>
                <LocationSelect
                    value={selectedLocation}
                    onChange={setSelectedLocation}
                    locations={locations}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="ip">IP-Adresse:</label>
                <Input
                    id="ip"
                    type="string"
                    value={ip} onChange={e => setIp(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="api_key">API-Key:</label>
                <Input
                    id="api_key"
                    type="password"
                    value={api_key} onChange={e => setApiKey(e.target.value)}
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

      {/* Module-Liste */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {modules.map((mod) => (
            <Card key={mod.id} className="relative p-4">
              <div className="space-y-2">
                <p><strong>System:</strong> {mod.description}</p>
                <p><strong>Hersteller:</strong> {getManufacturerLabel(manufacturers, Number(mod.manufacturer))}</p>
                <p><strong>Standort:</strong> {getLocationLabel(locations, Number(mod.location))}</p>
                <p><strong>IP-Adress:</strong> {mod.ip}</p>
                <p><strong>API-Key:</strong> {maskText(mod.api_key)}</p>
              </div>
              {/* Edit/Delete Buttons */}
              <div className="absolute bottom-4 right-4 flex space-x-2">
                <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => openEdit(mod)}
                >
                  <Edit3 className="h-4 w-4"/>
                </Button>
                <Button
                    size="icon"
                    variant="ghost"
                    onClick={() => handleDelete(mod.id)}
                >
                  <Trash2 className="h-4 w-4 text-red-600"/>
                </Button>
              </div>
            </Card>
        ))}
      </div>

      {/* Edit-Dialog */}
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
                <label htmlFor="location">Standort:</label>
                <LocationSelect
                    value={selectedLocation}
                    onChange={setSelectedLocation}
                    locations={locations}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="ip">IP-Adresse:</label>
                <Input
                    id="ip"
                    type="string"
                    value={ip} onChange={e => setIp(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="api_key">API-Key:</label>
                <Input
                    id="api_key"
                    type="password"
                    value={maskText(api_key)} onChange={e => setApiKey(e.target.value)}
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
      )}
    </div>
  )
}
