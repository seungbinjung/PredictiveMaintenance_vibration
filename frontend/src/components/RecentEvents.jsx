import { useEffect, useState } from "react";
import dayjs from "dayjs";
import useResultSSE from "../hooks/useResultSSE";

export default function RecentEvents() {
  const [events, setEvents] = useState([]);

  // 1) 기존: 초기 이벤트 로드 (DB에서 가져오는 부분)
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

  // 2) 새로운 SSE 구독 (백엔드 새 결과 push)
  const latestEvent = useResultSSE("http://127.0.0.1:8000/sse/results");

  // 3) latestEvent 값이 들어올 때마다 events 배열 앞에 추가
  useEffect(() => {
    if (!latestEvent) return;

    setEvents((prev) => {
      const updated = [latestEvent, ...prev];
      return updated.slice(0, 10); // 최대 10개 유지
    });
  }, [latestEvent]);

  // 4) 날짜 포맷
  const formatDate = (created_at) => {
    if (!created_at) return "-";

    return dayjs(created_at).format("YYYY-MM-DD HH:mm:ss");
  };

  // 5) 라벨 색상
  const getLabelColor = (label) => {
    if (label === "정상") return "text-green-400";
    if (label === "회전체불평형") return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="space-y-2">
      {events.map((event, idx) => (
        <div
          key={idx}
          className="flex justify-between p-3 border-b border-gray-700"
        >
          <span>{formatDate(event.created_at)}</span>
          <span className={getLabelColor(event.label)}>{event.label}</span>
        </div>
      ))}
    </div>
  );
}
