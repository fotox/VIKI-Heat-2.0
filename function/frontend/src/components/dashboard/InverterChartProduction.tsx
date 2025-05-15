import React, { useEffect, useState } from "react"
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts"

const COLORS = ["#22c55e", "#e5e7eb"];

export function InverterChartProduction() {
  const [data, setData] = useState([])

  const fetchState = async () => {
    const res = await fetch(`/api/modules/inverter_data`, {credentials: "include"})
    if (res.ok) {
      const inverterData = await res.json()
      setData(prev => {
        return inverterData
      })
    }
  }

  const productionData = [
    { name: "production", value: data['production'] },
    { name: "production_rest", value: 10000 - data['production'] },
  ];

   useEffect(() => {
    const interval = setInterval(() => {
      [0, 1, 2].forEach(fetchState)
    }, 2000) // TODO: In productive 500
    return () => clearInterval(interval)
  }, [])

  return (
      <ResponsiveContainer height={250}>
        <div className="w-full flex flex-col items-center">
          <h2 className="text-xl font-bold mb-2">Produktion</h2>
          <PieChart width={150} height={150}>
            <Pie
                data={productionData}
                innerRadius={35}
                outerRadius={60}
                dataKey="value"
                stroke="none"
            >
              {productionData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]}/>
              ))}
            </Pie>
          </PieChart>
          <div className="text-center">
            <div className="text-2xl font-bold">{productionData[1].value} W</div>
            <div className="text-sm text-muted-foreground">von 10000 W</div>
          </div>
        </div>
      </ResponsiveContainer>
  )
}
