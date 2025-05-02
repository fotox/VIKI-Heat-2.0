import React, {useState} from 'react'
import { NavLink } from 'react-router-dom'
import {
  HomeIcon,
  ChartPieIcon,
  SettingsIcon,
  UserIcon,
  ChevronLeft,
  ChevronRight,
  Image
} from 'lucide-react'
import { cn } from '@/lib/utils'
import {Avatar, AvatarFallback, AvatarImage} from "@/components/ui";

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
  const [username, setUsername] = useState('')
  const [preview, setPreview] = useState<string>('/api/auth/profile/photo')


  return (
      <aside
          className={cn(
              // Breite je nach collapsed-Flag
              collapsed ? 'w-15' : 'w-50',
              'flex flex-col h-screen border-r bg-white transition-width duration-200',
              className
          )}
      >
        {/* Logo & Collapse-Button */}
        <div className="flex justify-left h-16 px-6">
          {onToggleCollapse && (
              <button
                  onClick={onToggleCollapse}
                  className="p-1 rounded hover:bg-gray-100"
              >
                {collapsed ? (
                    <ChevronRight className="h-5 w-5"/>
                ) : (
                    <ChevronLeft className="h-5 w-5"/>
                )}
              </button>
          )}
        </div>
        <div className="mt-auto flex justify-center p-4">
          <NavLink
              to="/profile"
              onClick={onClose}
              className="block"
          >
            <Avatar className="h-24 w-24">
              <AvatarImage
                src={preview}
                alt="Profilfoto"
                className={cn(
                    collapsed ? 'w-10 h-10' : 'w-20 h-20'  // TODO: Rounded small image wrong
                )}
              />
              <AvatarFallback className="text-2xl">
                {username.charAt(0).toUpperCase()}
              </AvatarFallback>
            </Avatar>
          </NavLink>
        </div>
        <nav className="flex-1 px-5 py-4 space-y-1">
          {navItems.map((item) => (
              <NavLink
                  key={item.to}
                  to={item.to}
                  onClick={onClose}
                  className={({isActive}) =>
                      cn(
                          'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors',
                          isActive
                              ? 'bg-gray-100 text-gray-900'
                              : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      )
                  }
              >
                {/* Icon immer rendern */}
                <item.icon className="h-5 w-5 flex-shrink-0"/>
                {/* Label nur, wenn nicht collapsed */}
                {!collapsed && <span className="ml-3">{item.label}</span>}
              </NavLink>
          ))}
        </nav>
      </aside>
  )
}
