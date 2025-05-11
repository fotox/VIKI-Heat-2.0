import React, { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"

export function PhaseSwitchPanel() {
  const [states, setStates] = useState([false, false, false])

  const fetchState = async (phase: number) => {
    const res = await fetch(`/api/heat_pipe/${phase + 1}`, { credentials: "include" })
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
    await fetch(`/api/heat_pipe/${phase + 1}`, {
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
        <div key={phase} className="flex items-center justify-between">
          <Button
            variant={states[phase] ? "default" : "outline"}
            onClick={() => toggleState(phase)}
          >
            {states[phase] ? "AUS" : "AN"}
          </Button>
          <span>Phase {phase + 1}</span>
        </div>
      ))}
    </div>
  )
}
