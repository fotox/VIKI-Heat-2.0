import React, { useEffect, useState, useCallback } from 'react'
import io from 'socket.io-client'
import {
  Button,
  Card,
  Dialog,
  DialogContent,
  DialogTrigger
} from "@/components/ui"
import { Trash2 } from "lucide-react"
import {Plus} from "lucide-react";

interface Device {
  id: number;
  name: string;
  state: boolean
}

interface DashboardModule {
  id: string;
  module_type: string
}

const AVAILABLE_MODULES: DashboardModule[] = [
  { id: "switches", module_type: "Phasen Schalt-Panel" },
  { id: "energyChart", module_type: "Energie-Daten Chart" },
  { id: "inverterProductionChart", module_type: "Wechselrichter-Produktion Chart" },
  { id: "inverterConsumeChart", module_type: "Wechselrichter-Verbrauch Chart" },
  { id: "inverterCoverChart", module_type: "Wechselrichter-Strombillanz Chart" },
  { id: "inverterAccuCapacityChart", module_type: "Wechselrichter-Verbrauch Chart" },
  { id: "heatingTankRingChart", module_type: "Warmwasserspeicher Chart" },
  { id: "bufferTankRingChart", module_type: "Pufferspeicher Chart" },
]

import { PhaseSwitchPanel } from "@/components/dashboard/PhaseSwitchPanel"
import { EnergyChart } from "@/components/dashboard/EnergyChart"
import { HeatingTankRingChart, BufferTankRingChart } from "@/components/dashboard/TankRingChart";
import { InverterProduction, InverterConsume, InverterCover, InverterAccuCapacity } from "@/components/dashboard/InverterChart"

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([])
  const [error, setError] = useState<string | null>(null)
  const [modules, setModules] = useState<DashboardModule[]>([])
  const [open, setOpen] = useState(false)
  const socket = React.useMemo(() => io(), [])

  useEffect(() => {
    fetch("/api/dashboard/modules", { credentials: "include" })
      .then(res => res.json())
      .then(data => {
        const sorted = [...data].sort((a, b) => (a.position ?? 0) - (b.position ?? 0));
        setModules(sorted);
      })
    fetchDevices()
  }, [])

  const fetchDevices = useCallback(async () => {
    try {
      const csrf = document.cookie.split('; ').find(row => row.startsWith('csrf_access_token='))?.split('=')[1] || ''
      const res = await fetch('/api/dashboard/modules', { credentials: 'include', headers: { 'X-CSRF-TOKEN': csrf } })
      if (!res.ok) throw new Error(`Status ${res.status}`)
      const json = await res.json()
      setDevices(json.devices ?? [])
    } catch (err: any) {
      setError(err.message)
    }
  }, [])

  const handleRemoveModule = (id: number) => {
    fetch(`/api/dashboard/modules/${id}`, {
      method: "DELETE",
      credentials: "include"
    })
      .then(() => setModules(prev => prev.filter(m => m.id !== id)))
  }

  const handleAddModule = (module: DashboardModule) => {
    fetch("/api/dashboard/modules", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ module_type: module.id }),
      credentials: "include"
    })
      .then(res => res.json())
      .then(savedModule => setModules(prev => [...prev, savedModule]))
  }

  const moveModule = (index: number, direction: 'up' | 'down') => {
    const newModules = [...modules];
    const targetIndex = direction === 'up' ? index - 1 : index + 1;

    if (targetIndex < 0 || targetIndex >= newModules.length) return;

    [newModules[index], newModules[targetIndex]] = [newModules[targetIndex], newModules[index]];
    setModules(newModules);

    fetch("/api/dashboard/modules/reorder", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(newModules.map((m, idx) => ({ id: m.id, position: idx })))
    });
  };

  if (error) {
    return (
      <div className="p-6 text-red-600">
        <h2 className="text-xl font-bold">Fehler im Dashboard</h2>
        <p>{error}</p>
      </div>
    )
  }

  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        {modules.map((mod, index) => (
          <div
            key={`${mod.id}-${index}`}
            className={`mt-4 ${mod.module_type === "energyChart" ? "col-span-4" : ""}`}
          >
            <Card className="relative p-4 pb-12">
              <div className="absolute bottom-4 right-4">
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => moveModule(index, 'up')}
                  title="Nach oben verschieben"
                  disabled={index === 0}
                >
                  ↑
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => moveModule(index, 'down')}
                  title="Nach unten verschieben"
                  disabled={index === modules.length - 1}
                >
                  ↓
                </Button>
                <Button
                  size="icon"
                  variant="ghost"
                  onClick={() => handleRemoveModule(mod.id)}
                  title="Modul entfernen"
                >
                  <Trash2 className="h-4 w-4 text-red-600" />
                </Button>
              </div>
              <div className="space-y-2">
                {mod.module_type === "inverterProductionChart" && <InverterProduction />}
                {mod.module_type === "inverterConsumeChart" && <InverterConsume />}
                {mod.module_type === "inverterCoverChart" && <InverterCover />}
                {mod.module_type === "inverterAccuCapacityChart" && <InverterAccuCapacity />}
                {mod.module_type === "switches" && <PhaseSwitchPanel />}
                {mod.module_type === "energyChart" && <EnergyChart />}
                {mod.module_type === "heatingTankRingChart" && <HeatingTankRingChart />}
                {mod.module_type === "bufferTankRingChart" && <BufferTankRingChart  />}
              </div>
            </Card>
          </div>
        ))}
      </div>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild>
          <Button variant="outline">
            <Plus className="mr-2 h-4 w-4"/> Neues Modul
          </Button>
        </DialogTrigger>
        <DialogContent className="p-4">
          <h3 className="text-lg font-medium mb-2">Modul auswählen</h3>
          <div className="space-y-2">
            {AVAILABLE_MODULES.map(mod => (
              <Button key={mod.id} variant="outline" className="w-full" onClick={() => handleAddModule(mod)}>
                {mod.module_type}
              </Button>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  )
}
