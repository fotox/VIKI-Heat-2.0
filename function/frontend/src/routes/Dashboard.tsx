import React, { useEffect, useState } from 'react'
import { Card } from '@/components/ui'
import io from 'socket.io-client'

interface Device { id: number; name: string; state: boolean; }

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([])
  const [error, setError] = useState<string | null>(null)
  const socket = React.useMemo(() => io(), [])

  useEffect(() => {
    const fetchDevices = async () => {
      try {
        const csrf = document.cookie
          .split("; ")
          .find(row => row.startsWith("csrf_access_token="))
          ?.split("=")[1] || "";
        const res = await fetch('/api/dashboard/', { credentials: 'include', headers: { "X-CSRF-TOKEN": csrf } })
        if (!res.ok) {
          throw new Error(`Server-Antwort: ${res.status}`)
        }
        const json = await res.json()
        setDevices(json.devices ?? [])
      } catch (err: any) {
        setError(err.message)
      }
    }

    fetchDevices()

    socket.on('switch_updated', d => {
      setDevices(curr =>
        curr.map(dev =>
          dev.id === d.id ? { ...dev, state: d.new_state } : dev
        )
      )
    })

    return () => { socket.disconnect() }
  }, [socket])

  const toggle = async (id: number) => {
    try {
      const res = await fetch(`/api/dashboard/${id}/toggle`, {
        method: 'POST',
        credentials: 'include'
      })
      if (!res.ok) {
        throw new Error(`Toggle fehlgeschlagen: ${res.status}`)
      }
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
                className="px-3 py-1 bg-blue-500 text-white rounded"
                onClick={() => toggle(dev.id)}
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
