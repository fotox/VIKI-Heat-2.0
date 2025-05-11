import React, { useEffect, useState } from "react"
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
  const [data, setData] = useState([])
  const [prices, setPrices] = useState({})

  useEffect(() => {
    fetch("/api/modules/energy_data", { credentials: "include" })
      .then(res => res.json())
      .then(rawData => {
        const formatted = Object.entries(rawData).map(([time, values]: [string, any]) => ({
          time,
          ...values
        }))
        setData(formatted)
      })

    fetch("/api/modules/energy_price", { credentials: "include" })
      .then(res => res.json())
      .then(priceData => setPrices(priceData))
  }, [])

  const chartData = data.map(d => ({
    ...d,
    price: prices[d.time] ?? 0
  }))

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
          type="monotone"
          dataKey="price"
          stroke="#ff0000"
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  )
}
