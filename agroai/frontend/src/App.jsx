// Location: frontend/src/App.jsx
import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { LanguageProvider } from './context/LanguageContext'
import { AuthProvider } from './context/AuthContext'
import Home from './pages/Home'
import Loader from './components/ui/Loader'

const Results = lazy(() => import('./pages/Results'))
const BuyerList = lazy(() => import('./pages/BuyerList'))
const ConversionGuide = lazy(() => import('./pages/ConversionGuide'))
const Assistant = lazy(() => import('./pages/Assistant'))
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
        <BrowserRouter>
          <Suspense fallback={<Loader />}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/results" element={<Results />} />
              <Route path="/buyers" element={<BuyerList />} />
              <Route path="/guide/:type" element={<ConversionGuide />} />
              <Route path="/assistant" element={<Assistant />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthProvider>
    </LanguageProvider>
  )
}
