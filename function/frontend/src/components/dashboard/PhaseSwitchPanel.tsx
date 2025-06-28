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
  const [states, setStates] = useState<boolean[]>([false, false, false]);
  const [mode, setMode] = useState("Automatik");

  const fetchStates = async () => {
    const res = await fetch("/api/modules/heat_pipes", { credentials: "include" });
    if (!res.ok) return;

    const obj = await res.json();
    const arr = [obj["1"], obj["2"], obj["3"]];
    setStates(arr);
  };

  const toggleState = async (phase: number) => {
    setStates(prev => {
      const next = [...prev];
      next[phase] = !next[phase];
      return next;
    });

    const newState = !states[phase];
    await fetch(`/api/modules/heat_pipe/${phase + 1}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ state: newState })
    });

    fetchStates();
  };

  const fetchHeatingMode = async () => {
    const res = await fetch("/api/modules/heating_mode", {
      method: "GET",
      credentials: "include",
    });
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    const data: { mode: string; choices: string[] } = await res.json();
    setMode(data.mode);
  };
  fetchHeatingMode();

  const handleModeChange = async (newMode: string) => {
    setMode(newMode);
    const res = await fetch("/api/modules/heating_mode", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mode: newMode }),
      credentials: "include",
    });
  };

  React.useEffect(() => {
    const interval = setInterval(() => {
      [0, 1, 2].forEach(fetchStates);
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col gap-4 px-6 py-4">
      <h2 className="text-lg font-semibold text-center">Heizstab</h2>

      {[0, 1, 2].map(phase => (
        <div
          key={phase}
          className="flex items-center justify-between border-b pb-2"
        >
          <Label htmlFor={`phase-${phase + 1}`} className="text-base">
            Phase {phase + 1}
          </Label>

          <Switch
            id={`phase-${phase + 1}`}
            checked={states[phase] ?? false}
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
                  onClick={() => handleModeChange(option)}
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
