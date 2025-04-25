import React, { useEffect, useState } from 'react';
import { Button, Card } from '@shadcn/ui';
import io from 'socket.io-client';

interface Device { id: number; name: string; state: boolean; }

export default function Dashboard() {
  const [devices, setDevices] = useState<Device[]>([]);
  const socket = React.useMemo(() => io(), []);

  useEffect(() => {
    fetch('/api/devices/', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setDevices(data.devices));

    socket.on('switch_updated', (d: Device) => {
      setDevices(curr =>
        curr.map(dev => (dev.id === d.id ? { ...dev, state: d.new_state } : dev))
      );
    });

    return () => { socket.disconnect(); };
  }, [socket]);

  const toggle = async (id: number) => {
    await fetch(`/api/devices/${id}/toggle`, {
      method: 'POST',
      credentials: 'include'
    });
  };

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold">Geräte</h2>
      <div className="grid grid-cols-2 gap-4">
        {devices.map(dev => (
          <Card key={dev.id}>
            <div className="flex justify-between items-center">
              <span>{dev.name}</span>
              <Button onClick={() => toggle(dev.id)}>
                {dev.state ? 'Aus' : 'An'}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
