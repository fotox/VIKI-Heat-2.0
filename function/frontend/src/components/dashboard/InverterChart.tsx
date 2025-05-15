import React, { useEffect, useState } from "react"
import {
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts"

const COLORS = ["#22c55e", "#e5e7eb"];

export function useInverterData() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchState = async () => {
      try {
        const res = await fetch(`/api/modules/inverter_data`, { credentials: "include" });
        if (res.ok) {
          const inverterData = await res.json();
          setData(inverterData);
        }
      } catch (error) {
        console.error("Fehler beim Abrufen der Inverter-Daten:", error);
      }
    };

    fetchState();
    const interval = setInterval(fetchState, 2000);

    return () => clearInterval(interval);
  }, []);

  return data;
}



export function InverterProduction() {
  const data = useInverterData();
  if (!data) return <div>Lade Produktionsdaten...</div>;

  const productionData = [
    { name: "production", value: data['production'] },
    { name: "production_rest", value: 10000 - data['production'] },
  ];

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
            <div className="text-2xl font-bold">{productionData[0].value} W</div>
            <div className="text-sm text-muted-foreground">von 10000 W</div>
          </div>
        </div>
      </ResponsiveContainer>
  )
}


export function InverterConsume() {
  const data = useInverterData();
  if (!data) return <div>Lade Verbrauchsdaten...</div>;

  const consumeData = [
    { name: "consume", value: data['consume'] },
    { name: "consume_rest", value: 20000 - data['consume'] },
  ];

  return (
      <ResponsiveContainer height={250}>
        <div className="w-full flex flex-col items-center">
          <h2 className="text-xl font-bold mb-2">Verbrauch</h2>
          <PieChart width={150} height={150}>
            <Pie
                data={consumeData}
                innerRadius={35}
                outerRadius={60}
                dataKey="value"
                stroke="none"
            >
              {consumeData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]}/>
              ))}
            </Pie>
          </PieChart>
          <div className="text-center">
            <div className="text-2xl font-bold">{consumeData[0].value} W</div>
            <div className="text-sm text-muted-foreground">von 20000 W</div>
          </div>
        </div>
      </ResponsiveContainer>
  )
}
