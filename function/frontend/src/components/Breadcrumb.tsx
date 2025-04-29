// src/components/Breadcrumb.tsx
import React from 'react'
import { NavLink } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function Breadcrumb({ path }: { path: string }) {
  const segments = path
    .split('/')
    .filter(Boolean)
    .map((seg, i, arr) => ({
      name: seg.charAt(0).toUpperCase() + seg.slice(1),
      to: '/' + arr.slice(0, i + 1).join('/')
    }))

  return (
    <nav aria-label="Breadcrumb" className="flex items-center space-x-2 text-sm">
      <NavLink to="/dashboard" className="text-gray-500 hover:text-gray-700">
        Home
      </NavLink>
      {segments.map((seg, idx) => (
        <React.Fragment key={seg.to}>
          <ChevronRight className="h-4 w-4 text-gray-400" />
          <NavLink
            to={seg.to}
            className={({ isActive }) =>
              cn(
                'hover:text-gray-700',
                isActive ? 'font-medium text-gray-900' : 'text-gray-500'
              )
            }
          >
            {seg.name}
          </NavLink>
        </React.Fragment>
      ))}
    </nav>
  )
}
