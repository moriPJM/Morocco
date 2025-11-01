import { useState } from 'react'
import { useTranslation } from 'react-i18next'

interface FavoriteItem {
  id: string
  type: 'place' | 'phrase' | 'guide'
  title: string
  description: string
  content?: string
  location?: string
}

const Favorites = () => {
  const { t } = useTranslation()
  const [favorites, setFavorites] = useState<FavoriteItem[]>([
    {
      id: '1',
      type: 'place',
      title: t('favorites.sampleItems.place'),
      description: t('favorites.sampleItems.placeDesc'),
      location: 'マラケシュ'
    },
    {
      id: '2',
      type: 'phrase',
      title: t('favorites.sampleItems.phrase'),
      description: t('favorites.sampleItems.phraseDesc'),
      content: 'Marhaban bikum fi al-Maghrib'
    },
    {
      id: '3',
      type: 'guide',
      title: t('favorites.sampleItems.guide'),
      description: t('favorites.sampleItems.guideDesc'),
      content: t('favorites.sampleItems.guideContent')
    }
  ])

  const removeFavorite = (id: string) => {
    setFavorites(favorites.filter(item => item.id !== id))
  }

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'place':
        return '📍'
      case 'phrase':
        return '💬'
      case 'guide':
        return '📖'
      default:
        return '⭐'
    }
  }

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'place':
        return 'bg-blue-100 text-blue-800'
      case 'phrase':
        return 'bg-green-100 text-green-800'
      case 'guide':
        return 'bg-purple-100 text-purple-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">{t('favorites.title')}</h1>
          <p className="mt-2 text-gray-600">
            {t('favorites.subtitle')}
          </p>
        </div>

        {favorites.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm p-8 text-center">
            <div className="text-6xl mb-4">❤️</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">{t('favorites.noFavoritesTitle')}</h2>
            <p className="text-gray-600">
              {t('favorites.noFavoritesDesc')}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {favorites.map((item) => (
              <div key={item.id} className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <div className="text-3xl">{getTypeIcon(item.type)}</div>
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getTypeColor(item.type)}`}>
                          {item.type.charAt(0).toUpperCase() + item.type.slice(1)}
                        </span>
                      </div>
                      
                      <p className="text-gray-600 mb-2">{item.description}</p>
                      
                      {item.location && (
                        <div className="flex items-center text-sm text-gray-500 mb-2">
                          <span className="mr-1">📍</span>
                          {item.location}
                        </div>
                      )}
                      
                      {item.content && (
                        <div className="bg-gray-50 rounded-md p-3 text-sm text-gray-700">
                          {item.content}
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <button
                    onClick={() => removeFavorite(item.id)}
                    className="ml-4 p-2 text-gray-400 hover:text-red-500 transition-colors"
                    title={t('favorites.removeFromFavorites')}
                  >
                    ✕
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">{t('favorites.quickActions')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="text-2xl mb-2">🔍</div>
              <h3 className="font-medium">{t('favorites.explorePlaces')}</h3>
              <p className="text-sm text-gray-600">{t('favorites.explorePlacesDesc')}</p>
            </button>
            
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="text-2xl mb-2">💬</div>
              <h3 className="font-medium">{t('favorites.learnPhrases')}</h3>
              <p className="text-sm text-gray-600">{t('favorites.learnPhrasesDesc')}</p>
            </button>
            
            <button className="p-4 text-left border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
              <div className="text-2xl mb-2">📚</div>
              <h3 className="font-medium">{t('favorites.browseGuides')}</h3>
              <p className="text-sm text-gray-600">{t('favorites.browseGuidesDesc')}</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Favorites