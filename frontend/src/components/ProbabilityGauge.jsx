import { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";

export default function ProbabilityGauge() {
  const [value, setValue] = useState(0);

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/results/latest");
        const json = await res.json();
        setValue(json.probability || 0);
      } catch (e) {
        console.log("Fetch error:", e);
      }
    }, 800);
    return () => clearInterval(interval);
  }, []);

  const option = {
    series: [
      {
        type: "gauge",
        min: 0,
        max: 100,
        progress: { show: true, width: 12 },
        axisLine: { lineStyle: { width: 12 } },
        detail: {
          formatter: "{value}%",
          color: "#fff",
          fontSize: 24,
        },
        data: [{ value: (value * 100).toFixed(2) }],
      },
    ],
  };

  return <ReactECharts option={option} style={{ height: 260 }} />;
}
