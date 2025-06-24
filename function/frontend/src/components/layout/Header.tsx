import React from 'react'
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui'
import { Menu } from 'lucide-react';

export default function Header({isAuthenticated, onOpenSidebar}: {
    isAuthenticated: boolean
    onOpenSidebar: () => void
}) {
    const navigate = useNavigate();

   const handleLogout = () => {
     document.cookie = 'access_token=; Max-Age=0; path=/'
     navigate('/login')
   }

    return (
        <header className="flex items-center justify-between h-12 px-4 border-b bg-white">
            <Button variant="ghost" className="md:hidden" onClick={onOpenSidebar}>
                <Menu className="h-5 w-5"/>
            </Button>
            <div className="hidden md:block"/>
            <span className="text-xl font-bold">VIKI</span>
            {
                isAuthenticated ? (
                    <Button variant="ghost" onClick={handleLogout}>
                        Logout
                    </Button>
                ) : (
                    <Button variant="ghost" onClick={() => navigate('/login')}>
                        Login
                    </Button>
                )
            }
        </header>
    )
}
