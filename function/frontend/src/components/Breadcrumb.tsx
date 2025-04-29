// src/components/Breadcrumb.tsx
import React from 'react'
import { NavLink } from 'react-router-dom'
import { ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'

interface BreadcrumbProps {
  path: string
}

export default function Breadcrumb({ path }: BreadcrumbProps) {
  // Wir teilen den Pfad und ignorieren leere Segmente
  const segments = path
    .split('/')
    .filter(Boolean)
    .map((seg, i, arr) => ({
      // Wir mappen englische Route auf deutsche Bezeichnung
      name: {
        dashboard:     'Dashboard',
        analytics:     'Analyse',
        settings:      'Einstellungen',
        photovoltaic:  'Photovoltaik',
        profile:       'Profil'
      }[seg] ?? seg.charAt(0).toUpperCase() + seg.slice(1),
      // Pfad zum jeweiligen Segment
      to: '/' + arr.slice(0, i + 1).join('/')
    }))

  return (
    <nav aria-label="breadcrumb" className="flex items-center space-x-2 text-sm">
      {/* Startseite-Link */}
      <NavLink
        to="/dashboard"
        className="text-gray-500 hover:text-gray-700"
      >
        Startseite
      </NavLink>

      {segments.map(seg => (
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
