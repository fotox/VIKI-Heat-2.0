import React, { useEffect, useState } from "react"
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
} from "recharts"

export function EnergyChart() {
  const [data, setData] = useState([])
  const [prices, setPrices] = useState([])

  useEffect(() => {
    fetch("/api/energy_data", { credentials: "include" })
      .then(res => res.json())
      .then(rawData => {
        const formatted = Object.entries(rawData).map(([time, values]: [string, any]) => ({
          time,
          ...values
        }))
        setData(formatted)
      })

    fetch("/api/energy_price", { credentials: "include" })
      .then(res => res.json())
      .then(priceData => setPrices(priceData))
  }, [])

  return (
    <ResponsiveContainer width="100%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Bar dataKey="heating" stackId="a" fill="#8884d8" />
        <Bar dataKey="consumer" stackId="a" fill="#82ca9d" />
        <Bar dataKey="regular" stackId="a" fill="#ffc658" />
        <Bar dataKey="production" fill="#ff7300" />
        <LineChart data={data}>
          <Line type="monotone" dataKey={(entry) => prices[entry.time] ?? 0} stroke="#ff0000" dot={false} />
        </LineChart>
      </BarChart>
    </ResponsiveContainer>
  )
}
