import React, { useEffect, useState } from 'react';
import { Card } from '@shadcn/ui';

interface AnalyticsData {
  timestamp: string;
  value: number;
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData[]>([]);

  useEffect(() => {
    fetch('/api/analytics', { credentials: 'include' })
      .then(res => res.json())
      .then(d => setData(d.records || []))
      .catch(console.error);
  }, []);

  return (
    <div className="p-6 space-y-4">
      <h2 className="text-2xl font-bold">Analytics</h2>
      {data.length === 0 ? (
        <p>Keine Daten verfügbar.</p>
      ) : (
        data.map((rec, idx) => (
          <Card key={idx} className="p-4">
            <div className="flex justify-between">
              <span>{new Date(rec.timestamp).toLocaleString()}</span>
              <span>{rec.value}</span>
            </div>
          </Card>
        ))
      )}
    </div>
  );
}
