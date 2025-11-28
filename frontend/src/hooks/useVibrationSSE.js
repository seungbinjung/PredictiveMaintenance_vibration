import { useEffect, useState } from "react";

export default function useVibrationSSE(url) {
  const [value, setValue] = useState(null);

  useEffect(() => {
    let es = new EventSource(url);

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.value !== undefined) {
          setValue(data.value); // vibration only
        }
      } catch (err) {
        console.error("Vibration SSE parse error:", err);
      }
    };

    es.onerror = () => {
      console.log("SSE disconnected. Reconnecting...");
      es.close();
      setTimeout(() => (es = new EventSource(url)), 1000);
    };

    return () => es.close();
  }, [url]);

  return value;
}
