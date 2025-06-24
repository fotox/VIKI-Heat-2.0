import React from "react";
import {useTankData} from "@/hooks/useTankData";

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
      <div className="w-full flex flex-col items-center min-h-[230px] max-h-[230px]">
        <h2 className="text-xl font-bold mb-2">{title}</h2>
        <svg viewBox="0 0 300 200" className="w-full h-auto">
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="100%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#00f"/>
              <stop offset="100%" stopColor="#f00"/>
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
                <circle
                    key={index}
                    cx={pos.x}
                    cy={pos.y}
                    r="9"
                    fill="#FFFFFF55"
                    stroke="#FFF"
                    strokeWidth="3"
                />
            );
          })}

          <text x="50" y="175" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#000">
            5°C
          </text>
          <text x="250" y="175" textAnchor="middle" fontSize="14" fontWeight="bold" fill="#000">
            80°C
          </text>

          <text x="150" y="120" textAnchor="middle" fontSize="35" fontWeight="bold" fill="#000">
            {centerTemp}°C
          </text>
        </svg>
        <div className="text-center mb-2 text-sm font-semibold">
          {sensors[0]?.toFixed(1) ?? "-"}°C &nbsp;|&nbsp;
          {sensors[1]?.toFixed(1) ?? "-"}°C &nbsp;|&nbsp;
          {sensors[2]?.toFixed(1) ?? "-"}°C
        </div>
      </div>
  );
}
