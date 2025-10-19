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

export type SelectedLocationType = {
  id: number
  label: string
}

type Props = {
  value: SelectedLocationType | null
  onChange: (location: SelectedLocationType | null) => void
  locations: SelectedLocationType[]
}

export function getLocationLabel(
  locations: SelectedLocationType[],
  id: number
): string {
  return (
    locations.find(
      (l) => l.id === id
    )?.label ?? `${id}`
  )
}

export function LocationSelect({ value, onChange, locations }: Props) {
  const [open, setOpen] = useState(false)

  return (
    <div className="flex flex-col space-y-1">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-start">
            {value ? value.label : <>+ Standort wählen</>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="p-0" side="right" align="start">
          <Command>
            <CommandInput placeholder="Suchen..." />
            <CommandList>
              <CommandEmpty>
                Kein Standort gefunden.{" "}
                <Button
                  variant="link"
                  onClick={() => window.location.href = "/settings/location"}
                >
                  Jetzt hinzufügen
                </Button>
              </CommandEmpty>
              <CommandGroup>
                {locations.map((man) => (
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
