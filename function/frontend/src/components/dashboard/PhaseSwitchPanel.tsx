import React, { useState } from "react";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";

export function PhaseSwitchPanel() {
  const [states, setStates] = useState([false, false, false]);
  const [mode, setMode] = useState("Automatik");

  const fetchState = async (phase: number) => {
    const res = await fetch(`/api/modules/heat_pipe/${phase + 1}`, {
      credentials: "include",
    });
    if (res.ok) {
      const { state } = await res.json();
      setStates((prev) => {
        const copy = [...prev];
        copy[phase] = state;
        return copy;
      });
    }
  };

  const toggleState = async (phase: number) => {
    const newState = !states[phase];
    await fetch(`/api/modules/heat_pipe/${phase + 1}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: newState }),
      credentials: "include",
    });
    fetchState(phase);
  };

  const handleModeChange = async (newMode: string) => {
    setMode(newMode);
    await fetch("/api/modules/heating_mode", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: newMode }),
      credentials: "include",
    });
  };

  React.useEffect(() => {
    const interval = setInterval(() => {
      [0, 1, 2].forEach(fetchState);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col gap-4 px-6 py-4">
      <h2 className="text-lg font-semibold text-center">Heizstab</h2>

      {[0, 1, 2].map((phase) => (
        <div
          key={phase}
          className="flex items-center justify-between border-b pb-2"
        >
          <Label htmlFor={`phase-${phase + 1}`} className="text-base">
            Phase {phase + 1}
          </Label>
          <Switch
            id={`phase-${phase + 1}`}
            checked={states[phase]}
            onCheckedChange={() => toggleState(phase)}
          />
        </div>
      ))}

      <div className="flex justify-center mt-4">
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="outline">{mode}</Button>
          </PopoverTrigger>
          <PopoverContent className="w-48">
            <div className="flex flex-col gap-2">
              {["Automatik", "Manuell", "Schnell heizen", "Urlaub"].map((option) => (
                <Button
                  key={option}
                  variant="ghost"
                  className="justify-start"
                  onClick={() => handleModeChange(option)}  // TODO: Load active mode and displayed
                >
                  {option}
                </Button>
              ))}
            </div>
          </PopoverContent>
        </Popover>
      </div>
    </div>
  );
}
