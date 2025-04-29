import React, { useEffect, useState } from 'react'
import { Card } from '@/components/ui'

interface HeatingData {
  timestamp: string
  power: number
}

export default function Heating() {
  const [data, setData] = useState<HeatingData[]>([])

  useEffect(() => {
    fetch('/api/settings/heating', { credentials: 'include' })
      .then(res => res.json())
      .then(json => setData(json.records))
      .catch(console.error)
  }, [])

  return (
    <div className="space-y-4 p-6">
      <h3 className="text-xl font-semibold">Wärmeerzeugung-Einstellungen</h3>
      {data.length === 0 ? (
        <p>Keine Daten vorhanden.</p>
      ) : (
        data.map((rec, i) => (
          <Card key={i} className="p-4">
            <div className="flex justify-between">
              <span>{new Date(rec.timestamp).toLocaleString()}</span>
              <span>{rec.power} kW</span>
            </div>
          </Card>
        ))
      )}
    </div>
  )
}
