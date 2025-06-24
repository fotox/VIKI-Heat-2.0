import { useEffect, useState } from "react";

export function useTankData(apiEndpoint: string) {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const fetchState = async () => {
      try {
        const res = await fetch(apiEndpoint, { credentials: "include" });
        if (res.ok) {
          const tankData = await res.json();
          setData(tankData);
        }
      } catch (error) {
        console.error("Error by calling ring chart data:", error);
      }
    };

    fetchState();
    const interval = setInterval(fetchState, 2 * 60 * 1000);

    return () => clearInterval(interval);
  }, [apiEndpoint]);

  return data;
}
