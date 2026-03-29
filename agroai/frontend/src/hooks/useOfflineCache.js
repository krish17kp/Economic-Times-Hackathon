export function useOfflineCache() {
  const getCachedData = (key) => {
    const item = localStorage.getItem(key);
    if (!item) return null;
    try {
      return JSON.parse(item);
    } catch {
      return null;
    }
  };

  const setCachedData = (key, data) => {
    localStorage.setItem(key, JSON.stringify(data));
  };

  return { getCachedData, setCachedData };
}
