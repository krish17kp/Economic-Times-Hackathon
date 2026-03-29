// Location: frontend/src/context/AuthContext.jsx
import { createContext, useState, useEffect } from 'react'

export const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('agroai_token'))
  const [user, setUser] = useState(null)

  useEffect(() => {
    if (token) {
      // Decode JWT to get basic user info (no verification needed client-side)
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        setUser({ id: payload.sub, role: payload.role })
      } catch {
        setToken(null)
        localStorage.removeItem('agroai_token')
      }
    }
  }, [token])

  const login = (newToken, userData) => {
    setToken(newToken)
    setUser(userData)
    localStorage.setItem('agroai_token', newToken)
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('agroai_token')
  }

  return (
    <AuthContext.Provider value={{ token, user, login, logout, isLoggedIn: !!token }}>
      {children}
    </AuthContext.Provider>
  )
}
