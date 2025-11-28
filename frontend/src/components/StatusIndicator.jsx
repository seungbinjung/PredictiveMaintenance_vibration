import { useEffect, useState } from "react";

export default function SystemStatus() {
  const [status, setStatus] = useState({
    fastapi: false,
    redis: false,
    postgresql: false,
    colab: false,
  });

  // 1초마다 상태 갱신
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/system/status");
        const json = await res.json();
        setStatus(json);
      } catch (err) {
        console.log("Status fetch error:", err);
      }
    };

    fetchStatus();
    const timer = setInterval(fetchStatus, 1000);

    return () => clearInterval(timer);
  }, []);

  const getStatusDot = (ok) =>
    ok ? (
      <span className="text-green-400">●</span>
    ) : (
      <span className="text-red-500">●</span>
    );

  return (
    <div className="space-y-3 text-white p-4">
      <h2 className="text-xl font-bold mb-4">시스템 상태</h2>

      <div className="flex justify-between">
        <span>FastAPI 서버</span> {getStatusDot(status.fastapi)}
      </div>

      <div className="flex justify-between">
        <span>Redis</span> {getStatusDot(status.redis)}
      </div>

      <div className="flex justify-between">
        <span>PostgreSQL</span> {getStatusDot(status.postgresql)}
      </div>

      <div className="flex justify-between">
        <span>Colab 분석 서버</span> {getStatusDot(status.colab)}
      </div>
    </div>
  );
}
