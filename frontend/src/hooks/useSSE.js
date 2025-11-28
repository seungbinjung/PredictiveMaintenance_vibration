// frontend/src/hooks/useSSE.js
import { useEffect, useState } from "react";

export default function useSSE(url) {
  const [value, setValue] = useState(null);

  useEffect(() => {
    let es = new EventSource(url);

    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data?.value !== undefined) {
          setValue(data.value);
        }
      } catch (e) {
        console.error("SSE parse error:", e);
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
