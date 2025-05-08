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

export type SelectedCategoryType = {
  id: number
  label: string
}

type Props = {
  value: SelectedCategoryType | null
  onChange: (category: SelectedCategoryType | null) => void
  categories: SelectedCategoryType[]
}

export function getCategoryLabel(
  categories: SelectedCategoryType[],
  id: number
): string {
  return (
    categories.find(
      (c) => c.id === id
    )?.label ?? `${id}`
  )
}

export function CategorySelect({ value, onChange, categories }: Props) {
  const [open, setOpen] = useState(false)

  return (
    <div className="flex flex-col space-y-1">
      <Popover open={open} onOpenChange={setOpen}>
        <PopoverTrigger asChild>
          <Button variant="outline" className="w-full justify-start">
            {value ? value.label : <>+ Kategorie wählen</>}
          </Button>
        </PopoverTrigger>
        <PopoverContent className="p-0" side="right" align="start">
          <Command>
            <CommandInput placeholder="Suchen..." />
            <CommandList>
              <CommandEmpty>
                Keine Kategorie gefunden.{" "}
                <Button
                  variant="link"
                  onClick={() => window.location.href = "/settings/category"}
                >
                  Jetzt hinzufügen
                </Button>
              </CommandEmpty>
              <CommandGroup>
                {categories.map((cat) => (
                  <CommandItem
                    key={cat.id}
                    value={cat.label}
                    onSelect={() => {
                      onChange(cat)
                      setOpen(false)
                    }}
                  >
                    {cat.label}
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
