import { useState, useCallback } from 'react';
import api from '../services/api';

export function useApi(method) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const response = await method(...args);
      setData(response.data);
      return response.data;
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [method]);

  return { data, loading, error, execute };
}
