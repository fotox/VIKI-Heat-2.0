import React, { useEffect, useState } from "react"
import {
  EnergyDataPoint,
  EnergyResponse,
  EnergyPriceEntry
} from "@/hooks/dataTypes";
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
} from "recharts"


export function EnergyChart() {
  const [data, setData] = useState<(EnergyDataPoint & { time: string })[]>([]);
  const [prices, setPrices] = useState<Record<string, number>>({});

  useEffect(() => {
    fetch("/api/modules/energy_data", { credentials: "include" })
      .then(res => res.json())
      .then((rawData: EnergyResponse) => {
        const formatted = Object.entries(rawData).map(([time, values]) => ({
          time,
          ...values
        }));
        setData(formatted);
      });

    fetch("/api/modules/energy_price", { credentials: "include" })
      .then(res => res.json())
      .then((priceArray: EnergyPriceEntry[]) => {
        const priceMap = priceArray.reduce((acc: Record<string, number>, entry) => {
          const date = new Date(entry.startsAt);
          const hour = date.getHours().toString().padStart(2, '0');
          acc[hour] = entry.total;
          return acc;
        }, {});
        setPrices(priceMap);
      });
  }, [])

  const chartData = data.map((d) => ({
    ...d,
    price: prices[d.time] ?? 0,
  }));

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis yAxisId="left" orientation="left" />
        <YAxis yAxisId="right" orientation="right" />
        <Tooltip />
        <Legend />

        <Bar yAxisId="left" dataKey="heating" stackId="a" fill="#8884d8" />
        <Bar yAxisId="left" dataKey="consumer" stackId="a" fill="#82ca9d" />
        <Bar yAxisId="left" dataKey="regular" stackId="a" fill="#ffc658" />
        <Bar yAxisId="left" dataKey="production" fill="#ff7300" />

        <Line
          yAxisId="right"
          type="stepAfter"
          dataKey="price"
          stroke="#ff0000"
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
