import React, { useEffect, useState } from 'react'
import {Button, Card, Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger} from '@/components/ui'
import {Plus} from "lucide-react";

interface SensorData {
  timestamp: string
  power: number
}

export default function Energy() {
  const [data, setData] = useState<SensorData[]>([])

  useEffect(() => {
    fetch('/api/settings/sensors', { credentials: 'include' })
      .then(res => res.json())
      .then(json => setData(json.records))
      .catch(console.error)
  }, [])

  // TODO: Komplettes UI einbinden

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Sensor-Module</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">
              <Plus className="mr-2 h-4 w-4" /> Neues Sensor-Modul
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Neues Sensor-Module hinzufügen</DialogTitle>
            </DialogHeader>
              // TODO: Add Code
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
