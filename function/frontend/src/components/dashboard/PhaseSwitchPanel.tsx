import React, { useState, useEffect } from "react"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"

export function PhaseSwitchPanel() {
  const [states, setStates] = useState([false, false, false])

  const fetchState = async (phase: number) => {
    const res = await fetch(`/api/modules/heat_pipe/${phase + 1}`, { credentials: "include" })
    if (res.ok) {
      const { state } = await res.json()
      setStates(prev => {
        const copy = [...prev]
        copy[phase] = state
        return copy
      })
    }
  }

  const toggleState = async (phase: number) => {
    const newState = !states[phase]
    await fetch(`/api/modules/heat_pipe/${phase + 1}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: newState }),
      credentials: "include"
    })
    fetchState(phase)
  }

  useEffect(() => {
    const interval = setInterval(() => {
      [0, 1, 2].forEach(fetchState)
    }, 2000) // TODO: In productive 500
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="flex flex-col gap-4">
      {[0, 1, 2].map((phase) => (
          <div key={phase} className="flex items-center space-x-2">
            <Switch
                id={`phase-${phase + 1}`}
                checked={states[phase]}
                onCheckedChange={() => toggleState(phase)}
            />
            <Label htmlFor={`phase-${phase + 1}`}>Heizstabphase {phase + 1}</Label>
          </div>
      ))}
    </div>
  )
}
