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

export type SelectedManufacturerType = {
  id: number
  label: string
  powerFactor: number
}

type Props = {
  value: SelectedManufacturerType | null
  onChange: (manufacturer: SelectedManufacturerType | null) => void
  manufacturers: SelectedManufacturerType[]
}

export function getManufacturerLabel(
  manufacturers: SelectedManufacturerType[],
  id: number
): string {
  return (
    manufacturers.find(
      (m) => m.id === id
    )?.label ?? `${id}`
  )
}

export function getManufacturerPowerSize(
  manufacturers: SelectedManufacturerType[],
  id: number
): number {
  return (
    Number(manufacturers.find(
      (m) => m.id === id
    )?.powerFactor)
  )
}

export function ManufacturerSelect({ value, onChange, manufacturers }: Props) {
  const [open, setOpen] = useState(false)

  return (
    <div className="flex flex-col space-y-1">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-start">
            {value ? value.label : <>+ Hersteller wählen</>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="p-0" side="right" align="start">
          <Command>
            <CommandInput placeholder="Suchen..." />
            <CommandList>
              <CommandEmpty>
                Kein Hersteller gefunden.{" "}
                <Button
                  variant="link"
                  onClick={() => window.location.href = "/settings/manufacturer"}
                >
                  Jetzt hinzufügen
                </Button>
              </CommandEmpty>
              <CommandGroup>
                {manufacturers.map((man) => (
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
