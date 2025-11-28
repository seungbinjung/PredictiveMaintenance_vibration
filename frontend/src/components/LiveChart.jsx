// frontend/src/components/LiveChart.jsx
import { useEffect, useRef } from "react";
import useVibrationSSE from "../hooks/useVibrationSSE";
import Chart from "chart.js/auto";

const MAX_POINTS = 200;  // 화면에 보일 포인트 수 (약 2초 분량)

export default function LiveChart() {
  const value = useVibrationSSE("http://localhost:8000/sse/vibration");
  const chartRef = useRef(null);
  const chartInstanceRef = useRef(null);

  // Chart.js 초기화
  useEffect(() => {
    if (!chartRef.current) return;

    const ctx = chartRef.current.getContext("2d");

    chartInstanceRef.current = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Real-time Vibration",
            data: [],
            borderColor: "rgb(75, 192, 192)",
            borderWidth: 1.2,
            tension: 0.3,
            pointRadius: 0,
          },
        ],
      },
      options: {
        animation: false,
        normalized: true,
        responsive: true,
        scales: {
          x: {
            display: false,
          },
          y: {
            // beginAtZero: true,
            min: -0.1,
            max: 0.1,
          },
        },
      },
    });

    return () => chartInstanceRef.current?.destroy();
  }, []);

  // SSE 데이터 들어올 때마다 차트 업데이트
  useEffect(() => {
    if (value === null || !chartInstanceRef.current) return;

    const chart = chartInstanceRef.current;

    chart.data.labels.push("");       // x축 dummy label
    chart.data.datasets[0].data.push(value);

    // 오래된 값 제거 (슬라이딩 윈도우)
    if (chart.data.labels.length > MAX_POINTS) {
      chart.data.labels.shift();
      chart.data.datasets[0].data.shift();
    }

    chart.update("none"); // 애니메이션 없이 빠르게 업데이트
  }, [value]);

  return (
    <div className="w-full h-full p-4">
      <canvas ref={chartRef} />
    </div>
  );
}
