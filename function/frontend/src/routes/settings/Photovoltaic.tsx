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

interface PVModule {
  id: number
  description: string
  manufacturer: SelectedManufacturerType
  duration: number
  angle: number
  module_count: number
  location: SelectedLocationType
}

export default function Photovoltaic() {
  const [modules, setModules] = useState<PVModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<PVModule | null>(null)
  const [description, setDescription] = useState('')
  const [selectedManufacturer, setSelectedManufacturer] = useState<SelectedManufacturerType | null>(null)
  const [manufacturers, setManufacturers] = useState<SelectedManufacturerType[]>([])
  const [duration, setDuration] = useState<number>(0.0)
  const [angle, setAngle] = useState<number>(0.0)
  const [moduleCount, setModuleCount] = useState<number>(0)
  const [selectedLocation, setSelectedLocation] = useState<SelectedLocationType | null>(null)
  const [locations, setLocations] = useState<SelectedLocationType[]>([])

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
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id, duration: duration,
        angle: angle, module_count: moduleCount, location: selectedLocation?.id })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: PVModule) => {
    setEditModule(mod)
    setDescription(mod.description)
    const found_manufacturer = manufacturers.find((m) =>
        m.id === mod.manufacturer?.id || m.id === Number(mod.manufacturer))
    setSelectedManufacturer(found_manufacturer ?? null)
    setDuration(mod.duration)
    setAngle(mod.angle)
    setModuleCount(mod.module_count)
    const found_location = locations.find((l) =>
        l.id === mod.location?.id || l.id === Number(mod.location))
    setSelectedLocation(found_location ?? null)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/photovoltaic/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: selectedManufacturer?.id, duration: duration,
        angle: angle, module_count: moduleCount, location: selectedLocation?.id })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription("")
    setSelectedManufacturer(null)
    setDuration(0.0)
    setAngle(0.0)
    setModuleCount(0)
    setSelectedLocation(null)
  }

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Photovoltaik-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neues Photovoltaik-Modul hinzufügen</DialogTitle>
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
                <label htmlFor="duration">Ausrichtung:</label>
                <Input
                    id="duration"
                    type="number"
                    value={duration} onChange={e => setDuration(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="angle">Anstellwinkel:</label>
                <Input
                    id="angle"
                    type="number"
                    value={angle} onChange={e => setAngle(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="module_count">Anzahl der Module:</label>
                <Input
                    id="module_count"
                    type="number"
                    value={moduleCount} onChange={e => setModuleCount(Number(e.target.value))}
                    required
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
                <p><strong>Ausrichtung:</strong> {mod.duration}</p>
                <p><strong>Anstellwinkel:</strong> {mod.angle}</p>
                <p><strong>Module:</strong> {mod.module_count} </p>
                <p><strong>Gesamtleitung:</strong> {mod.module_count * getManufacturerPowerSize(manufacturers, Number(mod.manufacturer))} Wp</p>
                <p><strong>Standort:</strong> {getLocationLabel(locations, Number(mod.location))}</p>
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
                  <label htmlFor="duration">Ausrichtung:</label>
                  <Input
                      id="duration"
                      type="number"
                      value={duration} onChange={e => setDuration(Number(e.target.value))}
                      required
                  />
                </div>
                <div className="grid grid-cols-2 items-center gap-2">
                  <label htmlFor="angle">Anstellwinkel:</label>
                  <Input
                      id="angle"
                      type="number"
                      value={angle} onChange={e => setAngle(Number(e.target.value))}
                      required
                  />
                </div>
                <div className="grid grid-cols-2 items-center gap-2">
                  <label htmlFor="module_count">Anzahl der Module:</label>
                  <Input
                      id="module_count"
                      type="number"
                      value={moduleCount} onChange={e => setModuleCount(Number(e.target.value))}
                      required
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
