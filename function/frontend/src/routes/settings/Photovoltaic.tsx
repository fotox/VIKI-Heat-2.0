import React, { useEffect, useState } from 'react'
import { Card, Input, Button } from '@/components/ui'

interface PVModule {
  id: number
  system_id: string
  location: string
  max_output: number
}

export default function Photovoltaic() {
  const [modules, setModules] = useState<PVModule[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Formular-State
  const [systemId, setSystemId] = useState('')
  const [location, setLocation] = useState('')
  const [maxOutput, setMaxOutput] = useState<number>(0)

  // 1) GET alle Module
  const fetchModules = async () => {
    setLoading(true)
    try {
      const res = await fetch('/api/settings/photovoltaic', {
        credentials: 'include'
      })
      if (!res.ok) throw new Error(`Fehler ${res.status}`)
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

  // 2) POST neues Modul
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/settings/photovoltaic', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_id: systemId,
          location: location,
          max_output: maxOutput
        })
      })
      if (!res.ok) {
        const { msg } = await res.json()
        throw new Error(msg || `Fehler ${res.status}`)
      }
      // Formular zurücksetzen
      setSystemId('')
      setLocation('')
      setMaxOutput(0)
      // Liste neu laden
      fetchModules()
    } catch (err: any) {
      alert('Fehler: ' + err.message)
    }
  }

  if (loading) return <p>Lädt PV-Module…</p>
  if (error)   return <p className="text-red-600">Fehler: {error}</p>

  return (
    <div className="p-6 space-y-6">
      <h3 className="text-xl font-semibold">Photovoltaik-Module</h3>

      {modules.length === 0 ? (
        <p>Keine Module vorhanden. Lege ein neues an:</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {modules.map((mod) => (
            <Card key={mod.id} className="p-4">
              <div className="flex justify-between">
                <div>
                  <p><strong>ID:</strong> {mod.id}</p>
                  <p><strong>System:</strong> {mod.system_id}</p>
                  <p><strong>Ort:</strong> {mod.location}</p>
                </div>
                <p className="text-lg font-bold">{mod.max_output} kW</p>
              </div>
            </Card>
          ))}
        </div>
      )}

      <form onSubmit={handleAdd} className="space-y-4 bg-white p-4 rounded shadow">
        <h4 className="font-medium">Neues Modul hinzufügen</h4>
        System-ID: <Input
          label="System-ID"
          value={systemId}
          onChange={e => setSystemId(e.target.value)}
          required
        />
        Ort: <Input
          label="Ort"
          value={location}
          onChange={e => setLocation(e.target.value)}
          required
        />
        Max. Output (kW): <Input
          label="Max. Output (kW)"
          type="number"
          value={maxOutput}
          onChange={e => setMaxOutput(Number(e.target.value))}
          required
        />
        <Button type="submit">Hinzufügen</Button>
      </form>
    </div>
  )
}
