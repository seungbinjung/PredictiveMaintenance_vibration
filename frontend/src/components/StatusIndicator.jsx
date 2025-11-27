import { useEffect, useState } from "react";

export default function StatusIndicator() {
  const [status, setStatus] = useState({});

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/system/status");
        const json = await res.json();
        setStatus(json);
      } catch (e) {
        console.log("Status fetch error:", e);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  const Item = ({ name, ok }) => (
    <div className="flex items-center gap-3 text-lg">
      <div
        className={`w-3 h-3 rounded-full ${
          ok ? "bg-green-400" : "bg-red-500"
        }`}
      ></div>
      {name}
    </div>
  );

  return (
    <div className="space-y-3">
      <Item name="FastAPI" ok={status.api} />
      <Item name="Redis" ok={status.redis} />
      <Item name="PostgreSQL" ok={status.db} />
      <Item name="Colab Server" ok={status.colab} />
    </div>
  );
}
