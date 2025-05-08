import React, { useEffect, useState } from 'react'
import {Edit3, Plus, Trash2} from "lucide-react";
import {
    Button, Card,
    Dialog, DialogClose,
    DialogContent, DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    Input
} from '@/components/ui'
import {
  Command,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

import {CategorySelect, SelectedCategoryType, getCategoryLabel } from "@/components/selectors/CategorySelect";

interface ManufacturerData {
  id: number
  description: string
  category: SelectedCategoryType
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
  const [categories, setCategories] = useState<SelectedCategoryType[]>([])
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedManufacturers, setSelectedManufacturers] = useState<string[]>([])
  const [selectedCategory, setSelectedCategory] = useState<SelectedCategoryType | null>(null)
  const [filteredManufacturer, setFilteredManufacturer] = useState<ManufacturerData[]>([])
  const [openDropdown, setOpenDropdown] = useState(false)
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])
  const [openCategoryDropdown, setOpenCategoryDropdown] = useState(false)

  useEffect(() => {
    fetch("/api/settings/category", { credentials: "include" })
      .then((res) => res.json())
      .then((data) =>
        setCategories(
          data.categories.map((c: any) => ({
            id: c.id,
            label: c.description,
          }))
        )
      )
  }, [])

  // Load Modules
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/manufacturer', {
        credentials: 'include'
      })
      if (!res.ok) throw new Error(`Error ${res.status}`)
      const json = await res.json()
      setModules(json.manufacturers || [])
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

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
      body: JSON.stringify({ description: description, category: selectedCategory?.id,
          manufacturer: manufacturer, model_type: modelType, url: url, api: api, power_factor: powerFactor,
          power_size: powerSize })
    })
    fetchModules()
  }

  // Update Modules
  const openEdit = (mod: ManufacturerData) => {
    setEditModule(mod)
    setDescription(mod.description)
    const found = categories.find((c) =>
        c.id === mod.category?.id || c.id === mod.category)
    setSelectedCategory(found ?? null)
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
      body: JSON.stringify({ description: description, categories: selectedCategory?.id,
          manufacturer: manufacturer, model_type: modelType, url: url, api: api, power_factor: powerFactor,
          power_size: powerSize })
    })
    setEditModule(null)
    fetchModules()
  }

  // Reset Prefill
  const resetForm = () => {
    setEditModule(null)
    setDescription('')
    setSelectedCategory(null)
    setManufacturer('')
    setModelType('')
    setUrl('')
    setApi('')
    setPowerFactor(0.0)
    setPowerSize(0)
  }

  // Filter Result
  const applyFilters = () => {
    let filtered = [...modules]

    if (searchTerm.trim()) {
      const term = searchTerm.toLowerCase()
      filtered = filtered.filter(mod =>
        mod.description.toLowerCase().includes(term) ||
        mod.manufacturer.toLowerCase().includes(term) ||
        mod.model_type.toLowerCase().includes(term) ||
        mod.api.toLowerCase().includes(term)
      )
    }

    if (selectedManufacturers.length > 0) {
      filtered = filtered.filter(mod =>
        selectedManufacturers.includes(mod.manufacturer)
      )
    }

    if (selectedCategories.length > 0) {
      filtered = filtered.filter(mod =>
        selectedCategories.includes(mod.category?.label ?? "")
      )
    }

    setFilteredManufacturer(filtered)
  }


  useEffect(() => {
    fetchModules()
  }, [])

  useEffect(() => {
    applyFilters()
  }, [modules])


  if (loading) return <p>Lädt Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
      <div className="p-6 space-y-6">
          <div className="flex items-center justify-between">
              <h3 className="text-xl font-semibold">Hersteller-Module</h3>
              <Dialog>
                  <DialogTrigger asChild>
                      <Button variant="outline" onClick={() => resetForm()}>
                          <Plus className="mr-2 h-4 w-4"/> Neues Modul
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
                              <label htmlFor="category">Kategorie:</label>
                              <CategorySelect
                                value={selectedCategory}
                                onChange={setSelectedCategory}
                                categories={categories}
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
                              <Button type="submit">Speichern</Button>
                              <DialogClose asChild>
                                  <Button variant="ghost">Abbrechen</Button>
                              </DialogClose>
                          </DialogFooter>
                      </form>
                  </DialogContent>
              </Dialog>
          </div>

          {/* Search Module */}
          <div className="flex flex-col md:flex-row gap-4 items-start justify-between w-full">
              {/* Freitextsuche */}
              <Input
                  placeholder="Suche nach Beschreibung, Modell, API..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full md:w-1/2"
              />

              {/* Rechte Seite: Dropdown + Button */}
              <div className="flex flex-wrap items-center gap-4 w-full md:w-1/2 justify-end">
                  {/* Multiselect Dropdown */}
                  <Popover open={openDropdown} onOpenChange={setOpenDropdown}>
                      <PopoverTrigger asChild>
                          <Button variant="outline" className="min-w-[200px] justify-between">
                              {selectedManufacturers.length > 0
                                  ? `${selectedManufacturers.length} Hersteller`
                                  : "Hersteller wählen"}
                          </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-[220px] p-0">
                          <Command>
                              <CommandInput placeholder="Hersteller filtern..."/>
                              <CommandList>
                                  <CommandGroup>
                                      {[...new Set(modules.map(mod => mod.manufacturer))].map(manu => (
                                          <CommandItem key={manu} value={manu}>
                                              <label className="flex items-center gap-2">
                                                  <input
                                                      type="checkbox"
                                                      checked={selectedManufacturers.includes(manu)}
                                                      onChange={(e) => {
                                                          const checked = e.target.checked
                                                          setSelectedManufacturers(prev =>
                                                              checked
                                                                  ? [...prev, manu]
                                                                  : prev.filter(m => m !== manu)
                                                          )
                                                      }}
                                                  />
                                                  {manu}
                                              </label>
                                          </CommandItem>
                                      ))}
                                  </CommandGroup>
                              </CommandList>
                          </Command>
                      </PopoverContent>
                  </Popover>

                  {/* Kategorie-Dropdown */}
                  <Popover open={openCategoryDropdown} onOpenChange={setOpenCategoryDropdown}>
                    <PopoverTrigger asChild>
                      <Button variant="outline" className="min-w-[200px] justify-between">
                        {selectedCategories.length > 0
                          ? `${selectedCategories.length} Kategorie(n)`
                          : "Kategorie wählen"}
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-[220px] p-0">
                          <Command>
                              <CommandInput placeholder="Kategorie filtern..."/>
                              <CommandList>
                                  <CommandGroup>
                                      {[...new Set(categories.map(cat => cat.label))].map(cat => (
                                          <CommandItem key={cat} value={cat}>
                                              <label className="flex items-center gap-2">
                                                  <input
                                                      type="checkbox"
                                                      checked={selectedCategories.includes(cat)}
                                                      onChange={(e) => {
                                                          const checked = e.target.checked
                                                          setSelectedCategories(prev =>
                                                              checked
                                                                  ? [...prev, cat]
                                                                  : prev.filter(c => c !== cat)
                                                          )
                                                      }}
                                                  />
                                                  {cat}
                                              </label>
                                          </CommandItem>
                                      ))}
                                  </CommandGroup>
                              </CommandList>
                          </Command>
                      </PopoverContent>
                  </Popover>

                  {/* Suchen-Button */}
                  <Button onClick={applyFilters}>Suchen</Button>
              </div>
          </div>

          {/* Module-Liste */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredManufacturer.map((mod) => (
                  <Card key={mod.id} className="relative p-4">
                      <div className="space-y-2">
                          <p><strong>Bezeichnung:</strong> {mod.description}</p>
                          <p><strong>Kategorie:</strong> {getCategoryLabel(categories, mod.category)}</p>
                          <p><strong>Hersteller:</strong> {mod.manufacturer}</p>
                          <p><strong>Modellbezeichnung:</strong> {mod.model_type}</p>
                          <p><strong>URL:</strong> {mod.url}</p>
                          <p><strong>API:</strong> {mod.api} </p>
                          <p><strong>Leistungsfaktor:</strong> {mod.power_factor}</p>
                          <p><strong>Leistung (W/Wp):</strong> {mod.power_size}</p>
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
                              <label htmlFor="category">Kategorie:</label>
                              <CategorySelect
                                  value={selectedCategory}
                                  onChange={setSelectedCategory}
                                  categories={categories}
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
