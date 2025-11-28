import { useEffect, useRef } from "react";
import useResultSSE from "../hooks/useResultSSE";
import Chart from "chart.js/auto";

const LABEL_MAP = {
  0: "정상",
  1: "회전체불평형",
  2: "축정렬불량",
};

const COLOR_MAP = {
  0: "#4CAF50",  // green
  1: "#FFEB3B",  // yellow
  2: "#F44336",  // red
};

export default function ProbabilityGauge() {
  const latest = useResultSSE("http://127.0.0.1:8000/sse/results");
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  // Chart.js 초기 세팅
  useEffect(() => {
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext("2d");

    chartInstanceRef.current = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["정상", "회전체불평형", "축정렬불량"],
        datasets: [
          {
            data: [0, 0, 0],  // 초기 확률
            backgroundColor: [
              COLOR_MAP[0],
              COLOR_MAP[1],
              COLOR_MAP[2]
            ],
            borderWidth: 0,
          },
        ],
      },
      options: {
        cutout: "70%",
        animation: false,
        plugins: {
          tooltip: { enabled: true },
          legend: { display: false },
        },
      },
    });

    return () => chartInstanceRef.current?.destroy();
  }, []);

  // SSE 데이터 업데이트 시 도넛 반영
  useEffect(() => {
    if (!latest || !chartInstanceRef.current) return;
    if (!latest.probabilities) return;

    const probs = latest.probabilities;
    const prediction = latest.prediction;

    const chart = chartInstanceRef.current;

    // 도넛 그래프 전체 확률 업데이트
    chart.data.datasets[0].data = [
      probs[0],
      probs[1],
      probs[2]
    ];

    chart.update("none");
  }, [latest]);

  return (
    <div className="relative w-60 h-60 flex items-center justify-center">

      {/* 도넛 차트 */}
      <canvas ref={chartRef} className="absolute" />

      {/* 중앙 표시 텍스트 */}
      <div className="absolute text-center">
        <div className="text-lg font-bold text-white">
          {latest ? LABEL_MAP[latest.prediction] : "-"}
        </div>

        <div className="text-3xl font-semibold mt-1"
          style={{ color: COLOR_MAP[latest?.prediction] || "white" }}
        >
          {latest && latest.probabilities
            ? Math.round(latest.probabilities[latest.prediction] * 100) + "%"
            : "0%"}
        </div>
      </div>
    </div>
  );
}
