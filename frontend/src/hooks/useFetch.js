export default async function useFetch(url) {
    try {
      const res = await fetch(url);
      return await res.json();
    } catch (e) {
      console.log("Fetch error:", e);
      return null;
    }
  }
  