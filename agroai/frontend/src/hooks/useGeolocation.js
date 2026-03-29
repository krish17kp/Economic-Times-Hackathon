// Location: frontend/src/hooks/useGeolocation.js
import { useState, useCallback } from 'react'

export function useGeolocation() {
  const [location, setLocation] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const getLocation = useCallback(() => {
    if (!navigator.geolocation) {
      setError('GPS not supported')
      return
    }

    setLoading(true)
    setError(null)

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
        })
        setLoading(false)
      },
      (err) => {
        const messages = {
          1: 'Location permission denied. Please enter your pincode.',
          2: 'Location unavailable. Please enter your pincode.',
          3: 'Location timed out. Please enter your pincode.',
        }
        setError(messages[err.code] || 'An error occurred while getting location.')
        setLoading(false)
      }
    )
  }, [])

  return { location, error, loading, getLocation }
}
