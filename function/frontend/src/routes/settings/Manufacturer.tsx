import React, { useEffect, useState } from 'react'
import {Plus} from "lucide-react";
import {
    Button,
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger
} from '@/components/ui'

interface ManufacturerData {
  description: string
  manufacturer: string
  model_type: string
  url: string
  api: string
  power_factor: string
  power_size: string
}

export default function Manufacturer() {
  const [data, setData] = useState<ManufacturerData[]>([])

  useEffect(() => {
    fetch('/api/settings/manufacturer', { credentials: 'include' })
      .then(res => res.json())
      .then(json => setData(json.records))
      .catch(console.error)
  }, [])

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">Hersteller</h3>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">
              <Plus className="mr-2 h-4 w-4" /> Neuer Hersteller
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>Neuen Hersteller hinzufügen</DialogTitle>
            </DialogHeader>
              // TODO: Add Code
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
