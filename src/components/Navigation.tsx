import { useTranslation } from 'react-i18next'
import { Link, useLocation } from 'react-router-dom'

interface NavigationProps {
  currentLang: string
  onLanguageChange: (lang: string) => void
}

const Navigation = ({ currentLang, onLanguageChange }: NavigationProps) => {
  const { t } = useTranslation()
  const location = useLocation()

  const languages = [
    { code: 'ja', name: t('languages.japanese'), flag: '🇯🇵' },
    { code: 'en', name: t('languages.english'), flag: '🇬🇧' },
    { code: 'fr', name: t('languages.french'), flag: '🇫🇷' },
    { code: 'ar', name: t('languages.arabic'), flag: '🇲🇦' },
  ]

  const navItems = [
    { path: '/', key: 'home', icon: '🏠' },
    { path: '/translator', key: 'translator', icon: '🔤' },
    { path: '/guides', key: 'guides', icon: '📖' },
    { path: '/map', key: 'map', icon: '🗺️' },
    { path: '/favorites', key: 'favorites', icon: '❤️' },
    { path: '/voice-test', key: 'voicetest', icon: '🔊' },
  ]

  return (
    <nav className="bg-morocco-red shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center">
            <div className="text-white text-xl font-bold">
              🇲🇦 Morocco Guide
            </div>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              {navItems.map((item) => (
                <Link
                  key={item.key}
                  to={item.path}
                  className={`px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    location.pathname === item.path
                      ? 'bg-morocco-green text-white'
                      : 'text-white hover:bg-morocco-green hover:text-white'
                  }`}
                >
                  <span className="mr-2">{item.icon}</span>
                  {t(`navigation.${item.key}`)}
                </Link>
              ))}
            </div>
          </div>

          {/* Language Selector */}
          <div className="relative">
            <select
              value={currentLang}
              onChange={(e) => onLanguageChange(e.target.value)}
              className="bg-white text-gray-900 rounded-md px-3 py-1 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-morocco-gold"
            >
              {languages.map((lang) => (
                <option key={lang.code} value={lang.code}>
                  {lang.flag} {lang.name}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          {navItems.map((item) => (
            <Link
              key={item.key}
              to={item.path}
              className={`block px-3 py-2 rounded-md text-base font-medium transition-colors ${
                location.pathname === item.path
                  ? 'bg-morocco-green text-white'
                  : 'text-white hover:bg-morocco-green hover:text-white'
              }`}
            >
              <span className="mr-2">{item.icon}</span>
              {t(`navigation.${item.key}`)}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  )
}

export default Navigation