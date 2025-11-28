import { useEffect, useState } from "react";

export default function useResultSSE(url) {
  const [data, setData] = useState(null);

  useEffect(() => {
    let es = new EventSource(url);

    es.onmessage = (event) => {
      try {
        const json = JSON.parse(event.data);
        setData(json);  // full result object
      } catch (err) {
        console.error("Result SSE parse error:", err);
      }
    };

    es.onerror = () => {
      console.log("Result SSE disconnected. Reconnecting...");
      es.close();
      setTimeout(() => (es = new EventSource(url)), 1000);
    };

    return () => es.close();
  }, [url]);

  return data;
}

