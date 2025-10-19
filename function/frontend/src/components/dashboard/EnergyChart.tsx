import React, { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from "recharts";

export type EnergyDataPoint = {
  heating: number;
  consumer: number;
  regular: number;
  production: number;
};
export type EnergyResponse = Record<string, EnergyDataPoint>;

export type EnergyPriceEntry = {
  startsAt: string;
  total: number;
};

const pad = (n: number) => n.toString().padStart(2, "0");

const toLocalHourKey = (d: Date) =>
  `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(
    d.getHours()
  )}`;

const extractIso = (s: string): string | null => {
  const m = s.match(
    /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}[+-]\d{2}:\d{2}/
  );
  return m ? m[0] : null;
};


export function EnergyChart() {
  const [chartData, setChartData] = useState<
    (EnergyDataPoint & { price: number | null; time: string })[]
  >([]);

  useEffect(() => {
    (async () => {
      const [rawEnergy, rawPrices] = await Promise.all([
        fetch("/api/modules/energy_data", { credentials: "include" }).then(
          (r) => r.json()
        ),
        fetch("/api/modules/energy_price", { credentials: "include" }).then(
          (r) => r.json()
        )
      ]);

      const todayMidnight = new Date();
      todayMidnight.setHours(0, 0, 0, 0);

      const timeSlots = Array.from({ length: 48 }, (_, i) => {
        const d = new Date(todayMidnight.getTime() + i * 3600_000);
        return {
          key: toLocalHourKey(d),
          label: d.toLocaleString("de-DE", {
            weekday: "short",
            hour: "2-digit",
            hour12: false
          })
        };
      });

      const energyMap: Record<string, EnergyDataPoint> = {};
      Object.entries(rawEnergy as EnergyResponse).forEach(([rawKey, values]) => {
        const iso = extractIso(rawKey);
        if (!iso) return; // überspringen, falls kein Timestamp gefunden
        const key = toLocalHourKey(new Date(iso));
        energyMap[key] = values;
      });

      const priceMap: Record<string, number> = (rawPrices as EnergyPriceEntry[])
        .reduce((acc, p) => {
          const key = toLocalHourKey(new Date(p.startsAt));
          acc[key] = p.total;
          return acc;
        }, {} as Record<string, number>);

      const filled = timeSlots.map(({ key, label }) => {
        const e = energyMap[key] ?? {
          heating: 0,
          consumer: 0,
          regular: 0,
          production: 0
        };
        return {
          time: label,
          ...e,
          price: priceMap[key] ?? null
        };
      });

      setChartData(filled);
    })();
  }, []);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={chartData}>
        <defs>
          <filter id="priceGlow" height="130%">
            <feDropShadow
              dx="0"
              dy="0"
              stdDeviation="1"
              floodColor="#2973BD"
              floodOpacity="0.6"
            />
          </filter>
        </defs>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="time"
          interval={1}
          angle={-45}
          textAnchor="end"
          height={60}
        />
        <YAxis yAxisId="left" orientation="left" />
        <YAxis yAxisId="right" orientation="right" />

        <Tooltip />
        <Legend
          verticalAlign="bottom"
          align="center"
          wrapperStyle={{ paddingTop: 20 }}
        />

        <Bar yAxisId="left" dataKey="heating" stackId="a" fill="#8884d8" />
        <Bar yAxisId="left" dataKey="consumer" stackId="a" fill="#82ca9d" />
        <Bar yAxisId="left" dataKey="regular" stackId="a" fill="#ffc658" />
        <Bar yAxisId="left" dataKey="production" fill="#ff7300" />

        <Line
          yAxisId="right"
          type="stepAfter"
          dataKey="price"
          stroke="#2973BD"
          strokeWidth={2}
          dot={false}
          connectNulls={false}
          filter="url(#priceGlow)"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
