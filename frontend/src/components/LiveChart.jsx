import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

export default function LiveChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/data/latest");
        const json = await res.json();
        setData(json.values || []);
      } catch (e) {
        console.log("Fetch error:", e);
      }
    }, 400);

    return () => clearInterval(interval);
  }, []);

  const option = {
    backgroundColor: "#1a1a1a",
    textStyle: { color: "#ddd" },
    xAxis: {
      type: "category",
      data: data.map((_, i) => i),
      axisLine: { lineStyle: { color: "#888" } },
    },
    yAxis: {
      type: "value",
      axisLine: { lineStyle: { color: "#888" } },
      splitLine: { lineStyle: { color: "#333" } },
    },
    series: [
      {
        type: "line",
        data,
        smooth: true,
        lineStyle: { color: "#00ff88", width: 1.5 },
        symbol: "none",
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: 300 }} />;
}
