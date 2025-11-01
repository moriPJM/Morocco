import { useState, Suspense, lazy } from 'react'
import { useTranslation } from 'react-i18next'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navigation from './components/Navigation'
import Home from './pages/Home'

// Lazy load heavy components
const Translator = lazy(() => import('./pages/Translator'))
const Guides = lazy(() => import('./pages/Guides'))
const Map = lazy(() => import('./pages/Map'))
const Favorites = lazy(() => import('./pages/Favorites'))
const VoiceTest = lazy(() => import('./pages/VoiceTest'))

// Loading fallback component
const PageLoadingSpinner = () => (
  <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-morocco-sand to-morocco-blue">
    <div className="text-center">
      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-morocco-red mx-auto mb-4"></div>
      <p className="text-xl text-gray-700">読み込み中...</p>
    </div>
  </div>
)

function App() {
  const { i18n } = useTranslation()
  const [currentLang, setCurrentLang] = useState(i18n.language)

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng)
    setCurrentLang(lng)
    document.documentElement.lang = lng
    document.documentElement.dir = lng === 'ar' ? 'rtl' : 'ltr'
  }

  return (
    <div className={`min-h-screen bg-gray-50 ${currentLang === 'ar' ? 'rtl' : 'ltr'}`}>
      <Router>
        <Navigation currentLang={currentLang} onLanguageChange={changeLanguage} />
        <main>
          <Suspense fallback={<PageLoadingSpinner />}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/translator" element={<Translator />} />
              <Route path="/guides" element={<Guides />} />
              <Route path="/map" element={<Map />} />
              <Route path="/favorites" element={<Favorites />} />
              <Route path="/voice-test" element={<VoiceTest />} />
            </Routes>
          </Suspense>
        </main>
      </Router>
    </div>
  )
}

export default App