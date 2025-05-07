import React, { useEffect, useState } from 'react'
import {Edit3, Plus, Trash2} from "lucide-react";
import {
    Button, Card,
    Dialog, DialogClose,
    DialogContent, DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger, Input
} from '@/components/ui'

interface ManufacturerData {
  description: string
  manufacturer: string
  model_type: string
  url: string
  api: string
  power_factor: number
  power_size:number
}

export default function Manufacturer() {
  const [modules, setModules] = useState<ManufacturerData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [editModule, setEditModule] = useState<ManufacturerData | null>(null)
  const [description, setDescription] = useState<string>('')
  const [manufacturer, setManufacturer] = useState<string>('')
  const [modelType, setModelType] = useState<string>('')
  const [url, setUrl] = useState<string>('')
  const [api, setApi] = useState<string>('')
  const [powerFactor, setPowerFactor] = useState<number>(0.0)
  const [powerSize, setPowerSize] = useState<number>(0)

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/manufacturer', {
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
    await fetch(`/api/settings/manufacturer/${id}`, {
      method: 'DELETE',
      credentials: 'include'
    })
    fetchModules()
  }

  // Create Modules
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    await fetch('/api/settings/manufacturer', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: manufacturer, model_type: modelType,
          url: url, api: api, power_factor: powerFactor, power_size: powerSize })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: ManufacturerData) => {
    setEditModule(mod)
    setDescription(mod.description)
    setManufacturer(mod.manufacturer)
    setModelType(mod.model_type)
    setUrl(mod.url)
    setApi(mod.api)
    setPowerFactor(mod.power_factor)
    setPowerSize(mod.power_size)
  }

  // Edit Module
  const handleEdit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!editModule) return
    await fetch(`/api/settings/manufacturer/${editModule.id}`, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description: description, manufacturer: manufacturer, model_type: modelType,
          url: url, api: api, power_factor: powerFactor, power_size: powerSize })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription('')
    setManufacturer('')
    setModelType('')
    setUrl('')
    setApi('')
    setPowerFactor(0.0)
    setPowerSize(0)
  }

  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Hersteller-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline" onClick={() => resetForm()}>
              <Plus className="mr-2 h-4 w-4" /> Neues Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-max">
            <DialogHeader>
              <DialogTitle>Neues Hersteller-Modul hinzufügen</DialogTitle>
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
                      <Input
                          id="manufacturer"
                          type="string"
                          value={manufacturer} onChange={e => setManufacturer(e.target.value)}
                          required
                      />
                  </div>
                  <div className="grid grid-cols-2 items-center gap-2">
                      <label htmlFor="modelType">Modellbezeichnung:</label>
                      <Input
                          id="modelType"
                          type="string"
                          value={modelType} onChange={e => setModelType(e.target.value)}
                          required
                      />
                  </div>
                  <div className="grid grid-cols-2 items-center gap-2">
                      <label htmlFor="url">URL:</label>
                      <Input
                          id="url"
                          type="string"
                          value={url} onChange={e => setUrl(e.target.value)}
                          required
                      />
                  </div>
                  <div className="grid grid-cols-2 items-center gap-2">
                      <label htmlFor="api">API:</label>
                      <Input
                          id="api"
                          type="string"
                          value={api} onChange={e => setApi(e.target.value)}
                          required
                      />
                  </div>
                  <div className="grid grid-cols-2 items-center gap-2">
                      <label htmlFor="powerFactor">Leistungsfaktor:</label>
                      <Input
                          id="powerFactor"
                          type="number"
                          value={powerFactor} onChange={e => setPowerFactor(Number(e.target.value))}
                          required
                      />
                  </div>
                  <div className="grid grid-cols-2 items-center gap-2">
                      <label htmlFor="powerSize">Leistung (W/Wp):</label>
                      <Input
                          id="powerSize"
                          type="number"
                          value={powerSize} onChange={e => setPowerSize(Number(e.target.value))}
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
                <p><strong>Bezeichnung:</strong> {mod.description}</p>
                <p><strong>Hersteller:</strong> {getManufacturerLabel(manufacturers, Number(mod.manufacturer))}</p>
                <p><strong>Ausrichtung:</strong> {mod.model_type}</p>
                <p><strong>Anstellwinkel:</strong> {mod.url}</p>
                <p><strong>Module:</strong> {mod.module_count} </p>
                <p><strong>Gesamtleitung:</strong> {mod.module_count * Number(getManufacturerPowerSize(manufacturers, Number(mod.manufacturer)))}</p>
                <p><strong>Standort:</strong> {getLocationLabel(locations, Number(mod.manufacturer))}</p>
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
                        <Input
                            id="manufacturer"
                            type="string"
                            value={manufacturer} onChange={e => setManufacturer(e.target.value)}
                            required
                        />
                    </div>
                    <div className="grid grid-cols-2 items-center gap-2">
                        <label htmlFor="modelType">Modellbezeichnung:</label>
                        <Input
                            id="modelType"
                            type="string"
                            value={modelType} onChange={e => setModelType(e.target.value)}
                            required
                        />
                    </div>
                    <div className="grid grid-cols-2 items-center gap-2">
                        <label htmlFor="url">URL:</label>
                        <Input
                            id="url"
                            type="string"
                            value={url} onChange={e => setUrl(e.target.value)}
                            required
                        />
                    </div>
                    <div className="grid grid-cols-2 items-center gap-2">
                        <label htmlFor="api">API:</label>
                        <Input
                            id="api"
                            type="string"
                            value={api} onChange={e => setApi(e.target.value)}
                            required
                        />
                    </div>
                    <div className="grid grid-cols-2 items-center gap-2">
                        <label htmlFor="powerFactor">Leistungsfaktor:</label>
                        <Input
                            id="powerFactor"
                            type="number"
                            value={powerFactor} onChange={e => setPowerFactor(Number(e.target.value))}
                            required
                        />
                    </div>
                    <div className="grid grid-cols-2 items-center gap-2">
                        <label htmlFor="powerSize">Leistung (W/Wp):</label>
                        <Input
                            id="powerSize"
                            type="number"
                            value={powerSize} onChange={e => setPowerSize(Number(e.target.value))}
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
