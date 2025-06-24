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

interface LocationModule {
  id: number
  description: string
  latitude: number
  longitude: number
  city_code: number
  city: string
  street: string
  street_number: number
}

export default function Location() {
  const [modules, setModules] = useState<LocationModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<LocationModule | null>(null)
  const [description, setDescription] = useState<string>('')
  const [latitude, setLatitude] = useState<number>(0.0)
  const [longitude, setLongitude] = useState<number>(0.0)
  const [cityCode, setCityCode] = useState<number>(0)
  const [city, setCity] = useState<string>('')
  const [street, setStreet] = useState<string>('')
  const [streetNumber, setStreetNumber] = useState<number>(0)

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/location', {
        credentials: 'include'
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const json = await res.json()
      setModules(json.locations || [])
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
    if (!confirm('Standort wirklich löschen?')) return
    await fetch(`/api/settings/location/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/location', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, latitude: latitude, longitude: longitude, city_code: cityCode,
        city: city, street: street, street_number: streetNumber })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: LocationModule) => {
    setEditModule(mod)
    setDescription(mod.description)
    setLatitude(mod.latitude)
    setLongitude(mod.longitude)
    setCityCode(mod.city_code)
    setCity(mod.city)
    setStreet(mod.street)
    setStreetNumber(mod.street_number)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/location/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, latitude: latitude, longitude: longitude, city_code: cityCode,
        city: city, street: street, street_number: streetNumber })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription("")
    setLatitude(0.0)
    setLongitude(0.0)
    setCityCode(0)
    setCity("")
    setStreet("")
    setStreetNumber(0)
  }

  if (loading) return <p>Lädt Standorte…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Standorte-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neuen Standort hinzufügen</DialogTitle>
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
                <label htmlFor="latitude">Latitude:</label>
                <Input
                    id="latitude"
                    type="number"
                    value={latitude} onChange={e => setLatitude(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="longitude">Longitude:</label>
                <Input
                    id="longitude"
                    type="number"
                    value={longitude} onChange={e => setLongitude(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="cityCode">Postleitzahl:</label>
                <Input
                    id="cityCode"
                    type="number"
                    value={cityCode} onChange={e => setCityCode(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="city">Stadt:</label>
                <Input
                    id="city"
                    type="string"
                    value={city} onChange={e => setCity(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="street">Straße:</label>
                <Input
                    id="street"
                    type="string"
                    value={street} onChange={e => setStreet(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="streetNumber">Hausnummer:</label>
                <Input
                    id="streetNumber"
                    type="number"
                    value={streetNumber} onChange={e => Number(e.target.value)}
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
                <p><strong>Latitude:</strong> {mod.latitude}</p>
                <p><strong>Longitude:</strong> {mod.longitude}</p>
                <p><strong>Postleitzahl:</strong> {mod.city_code}</p>
                <p><strong>Stadt:</strong> {mod.city}</p>
                <p><strong>Straße:</strong> {mod.street}</p>
                <p><strong>Hausnummer:</strong> {mod.street_number}</p>
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
                <label htmlFor="latitude">Latitude:</label>
                <Input
                    id="latitude"
                    type="number"
                    value={latitude} onChange={e => setLatitude(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="longitude">Longitude:</label>
                <Input
                    id="longitude"
                    type="number"
                    value={longitude} onChange={e => setLongitude(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="cityCode">Postleitzahl:</label>
                <Input
                    id="cityCode"
                    type="number"
                    value={cityCode} onChange={e => setCityCode(Number(e.target.value))}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="city">Stadt:</label>
                <Input
                    id="city"
                    type="string"
                    value={city} onChange={e => setCity(e.target.value)}
                    required
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="street">Straße:</label>
                <Input
                    id="street"
                    type="string"
                    value={street} onChange={e => setStreet(e.target.value)}
                />
              </div>
              <div className="grid grid-cols-2 items-center gap-2">
                <label htmlFor="streetNumber">Hausnummer:</label>
                <Input
                    id="streetNumber"
                    type="number"
                    value={streetNumber} onChange={e => Number(e.target.value)}
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
