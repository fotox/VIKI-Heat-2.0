import React, { useEffect, useState, useCallback } from 'react'
import { Card } from '@/components/ui'
import io from 'socket.io-client'

interface Device { id: number; name: string; state: boolean }

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([])
  const [error,   setError]   = useState<string | null>(null)
  const socket = React.useMemo(() => io(), [])

  const fetchDevices = useCallback(async () => {
    try {
      const csrf = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_access_token='))
        ?.split('=')[1] || ''
      const res = await fetch('/api/dashboard/', {
        credentials: 'include',
        headers: { 'X-CSRF-TOKEN': csrf }
      })
      if (!res.ok) throw new Error(`Status ${res.status}`)
      const json = await res.json()
      setDevices(json.devices ?? [])
    } catch (err: any) {
      setError(err.message)
    }
  }, [])

  useEffect(() => {
    fetchDevices()

    socket.on('switch_updated', (d: {id:number, new_state:boolean}) => {
      setDevices(curr =>
        curr.map(dev =>
          dev.id === d.id ? { ...dev, state: d.new_state } : dev
        )
      )
    })

    const interval = setInterval(fetchDevices, 2000) // in prod switch to 500

    return () => {
      clearInterval(interval)
      socket.disconnect()
    }
  }, [socket, fetchDevices])

  // 3) Toggle-Handler: sofort setzen & auf Server-Antwort vertrauen
  const handleToggle = async (id: number) => {
    try {
      const csrf = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrf_access_token='))
        ?.split('=')[1] || ''

      const res = await fetch(`/api/dashboard/${id}/toggle`, {
        method:      'POST',
        credentials: 'include',
        headers:     { 'X-CSRF-TOKEN': csrf }
      })
      if (!res.ok) throw new Error(`Status ${res.status}`)

      const { new_state } = await res.json()
      setDevices(curr =>
        curr.map(dev =>
          dev.id === id
            ? { ...dev, state: new_state }
            : dev
        )
      )
    } catch (err: any) {
      setError(err.message)
    }
  }

  if (error) {
    return (
      <div className="p-6 text-red-600">
        <h2 className="text-xl font-bold">Fehler im Dashboard</h2>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold">Geräte</h2>
      <div className="grid grid-cols-2 gap-4">
        {devices.length === 0 && (
          <p className="col-span-2">Keine Geräte gefunden.</p>
        )}
        {devices.map(dev => (
          <Card key={dev.id}>
            <div className="flex justify-between items-center">
              <span>{dev.name}</span>
              <button
                className={`px-3 py-1 rounded ${
                  dev.state ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                }`}
                onClick={() => handleToggle(dev.id)}
              >
                {dev.state ? 'Aus' : 'An'}
              </button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
