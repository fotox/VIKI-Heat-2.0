import React, { useState } from 'react'
import { Button } from "@/components/ui/button"
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command"
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover"

export type SelectedTankType = {
  id: number
  label: string
}

type Props = {
  value: SelectedTankType | null
  onChange: (tank: SelectedTankType | null) => void
  tanks: SelectedTankType[]
}

export function getTankLabel(
  locations: SelectedTankType[],
  id: number
): string {
  return (
    locations.find(
      (l) => l.id === id
    )?.label ?? `${id}`
  )
}

export function TankSelect({ value, onChange, tanks }: Props) {
  const [open, setOpen] = useState(false)

  return (
    <div className="flex flex-col space-y-1">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-start">
            {value ? value.label : <>+ Tank wählen</>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="p-0" side="right" align="start">
          <Command>
            <CommandInput placeholder="Suchen..." />
            <CommandList>
              <CommandEmpty>
                Kein Tank gefunden.{" "}
                <Button
                  variant="link"
                  onClick={() => window.location.href = "/settings/tank"}
                >
                  Jetzt hinzufügen
                </Button>
              </CommandEmpty>
              <CommandGroup>
                {tanks.map((man) => (
                  <CommandItem
                    key={man.id}
                    value={man.label}
                    onSelect={() => {
                      onChange(man)
                      setOpen(false)
                    }}
                  >
                    {man.label}
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
    </div>
  )
}
