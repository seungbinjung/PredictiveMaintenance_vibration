import { useEffect, useState } from "react";

export default function RecentEvents() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/results/recent");
        const json = await res.json();
        setEvents(json);
      } catch (e) {
        console.log("Fetch error:", e);
      }
    };

    load();
  }, []);

  return (
    <div className="space-y-2">
      {events.map((event, idx) => (
        <div
          key={idx}
          className="flex justify-between p-3 border-b border-gray-700"
        >
          <span>{new Date(event.created_at).toLocaleString()}</span>
          <span
            className={
              event.label === "2" ? "text-red-400" : "text-green-400"
            }
          >
            {event.label}
          </span>
        </div>
      ))}
    </div>
  );
}
