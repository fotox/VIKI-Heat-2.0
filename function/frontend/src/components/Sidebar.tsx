import React from 'react'
import { NavLink } from 'react-router-dom'
import {
  HomeIcon,
  ChartPieIcon,
  SettingsIcon,
  UserIcon,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react'
import { cn } from '@/lib/utils'

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: HomeIcon },
  { to: '/analytics', label: 'Analytics', icon: ChartPieIcon },
  { to: '/settings', label: 'Settings', icon: SettingsIcon },
  { to: '/profile', label: 'Profile', icon: UserIcon },
]

export default function Sidebar({
  className,
  collapsed = false,
  onClose,
  onToggleCollapse,
}: {
  className?: string
  collapsed?: boolean
  onClose?: () => void
  onToggleCollapse?: () => void
}) {
  return (
    <aside
      className={cn(
        // Breite je nach collapsed-Flag
        collapsed ? 'w-15' : 'w-64',
        'flex flex-col h-screen border-r bg-white transition-width duration-200',
        className
      )}
    >
      {/* Logo & Collapse-Button */}
      <div className="flex items-center justify-between h-16 px-3">
        {!collapsed && <span className="text-xl font-bold">VIKI</span>}
        {onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="p-1 rounded hover:bg-gray-100"
          >
            {collapsed ? (
              <ChevronRight className="h-5 w-5" />
            ) : (
              <ChevronLeft className="h-5 w-5" />
            )}
          </button>
        )}
      </div>

      {/* Ganz unten: Profil-Icon */}
      <div className="mt-auto p-4">
        <NavLink
          to="/settings/profile"
          onClick={onClose}
          className="block w-12 h-12 rounded-full overflow-hidden mx-auto hover:ring-2 ring-offset-2 ring-blue-500"
        >
          <img
            src="/api/auth/profile/photo"
            alt="Dein Profil"
            className="object-cover w-full h-full"
          />
        </NavLink>
      </div>

      <nav className="flex-1 px-2 py-4 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            onClick={onClose}
            className={({ isActive }) =>
              cn(
                'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors',
                isActive
                  ? 'bg-gray-100 text-gray-900'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              )
            }
          >
            {/* Icon immer rendern */}
            <item.icon className="h-5 w-5 flex-shrink-0" />
            {/* Label nur, wenn nicht collapsed */}
            {!collapsed && <span className="ml-3">{item.label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
