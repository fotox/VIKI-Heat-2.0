import React, { useEffect, useState } from 'react'
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
import {data} from "autoprefixer";

export type SelectedManufacturerType = {
  id: number
  label: string
}

type Props = {
  value: SelectedManufacturerType | null
  onChange: (manufacturer: SelectedManufacturerType | null) => void
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

export function ManufacturerSelect({ value, onChange }: Props) {
  const [open, setOpen] = useState(false)
  const [manufacturers, setManufacturers] = useState<SelectedManufacturerType[]>([])

  useEffect(() => {
    fetch("/api/settings/manufacturer", { credentials: "include" })
      .then((res) => res.json())
      .then((data) =>
        setManufacturers(
          data.manufacturers.map((m: any) => ({
            id: m.id,
            label: `${m.manufacturer} - ${m.model_type}`,
          }))
        )
      )
  }, [])

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
