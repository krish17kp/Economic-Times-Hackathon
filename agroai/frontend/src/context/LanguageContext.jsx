// Location: frontend/src/context/LanguageContext.jsx
import { createContext, useState } from 'react'

export const LanguageContext = createContext()

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(
    localStorage.getItem('agroai_lang') || 'hi'  // Hindi default
  )

  const changeLang = (newLang) => {
    setLang(newLang)
    localStorage.setItem('agroai_lang', newLang)
  }

  return (
    <LanguageContext.Provider value={{ lang, setLang: changeLang }}>
      {children}
    </LanguageContext.Provider>
  )
}
