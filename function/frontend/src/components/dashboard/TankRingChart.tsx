import React from "react";
import {useTankData} from "@/components/hooks/useTankData";

interface TankRingChartProps {
  apiEndpoint: string;
  title: string;
}

export function HeatingTankRingChart() {
  return <TankRingChart apiEndpoint="/api/modules/heating_tank_temp" title="Heizungsspeicher" />;
}

export function BufferTankRingChart() {
  return <TankRingChart apiEndpoint="/api/modules/buffer_tank_temp" title="Pufferspeicher" />;
}

export function TankRingChart({ apiEndpoint, title }: TankRingChartProps) {
  const data = useTankData(apiEndpoint);

  if (!data) return <div>Lade Daten...</div>;

  const sensors = [data.sensor_1, data.sensor_2, data.sensor_3];
  const minTemp = 5;
  const maxTemp = 80;
  const centerTemp = Math.round(data.dest_temp);

  const getPosition = (temp: number) => {
    const ratio = (temp - minTemp) / (maxTemp - minTemp);
    const angle = Math.PI * (1 + ratio);
    const radius = 100;
    const centerX = 150;
    const centerY = 150;
    return {
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    };
  };

  const gradientId = `${title.replace(/\s+/g, '-')}-gradient`;

  return (
    <div className="w-full max-w-md mx-auto p-4">
      <h2 className="text-xl font-bold mb-2 text-center">{title}</h2>
      <svg viewBox="0 0 300 200" className="w-full h-auto">
        <defs>
          <linearGradient id={gradientId} x1="0%" y1="100%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#00f" />
            <stop offset="100%" stopColor="#f00" />
          </linearGradient>
        </defs>

        <path
          d="M50,150 A100,100 0 0,1 250,150"
          stroke={`url(#${gradientId})`}
          strokeWidth="20"
          fill="transparent"
          strokeLinecap="butt"
        />

        {sensors.map((temp: number | null, index: number) => {
          if (temp === null) return null;
          const pos = getPosition(temp);
          return (
            <g key={index}>
              <circle cx={pos.x} cy={pos.y} r="15" fill="#fff" stroke="#000" strokeWidth="2" />
              <text
                x={pos.x}
                y={pos.y + 4}
                textAnchor="middle"
                fontSize="10"
                fill="#000"
              >
                {temp.toFixed(1)}°C
              </text>
            </g>
          );
        })}

        <text x="50" y="175" textAnchor="middle" fontSize="12" fill="#000">
          5°C
        </text>
        <text x="250" y="175" textAnchor="middle" fontSize="12" fill="#000">
          80°C
        </text>

        <text x="150" y="120" textAnchor="middle" fontSize="32" fill="#000">
          {centerTemp}°C
        </text>
      </svg>
    </div>
  );
}
