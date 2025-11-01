import { useRef } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { useTranslation } from 'react-i18next'
import 'leaflet/dist/leaflet.css'

const Map = () => {
  const { t } = useTranslation()
  const mapRef = useRef(null)

  const moroccanCities = [
    {
      name: t('map.cities.marrakech'),
      originalName: 'Marrakech',
      position: [31.6295, -7.9811],
      description: t('map.cities.marrakechDesc')
    },
    {
      name: t('map.cities.casablanca'),
      originalName: 'Casablanca',
      position: [33.5731, -7.5898],
      description: t('map.cities.casablancaDesc')
    },
    {
      name: t('map.cities.fez'),
      originalName: 'Fez',
      position: [34.0181, -5.0078],
      description: t('map.cities.fezDesc')
    },
    {
      name: t('map.cities.rabat'),
      originalName: 'Rabat',
      position: [34.0209, -6.8416],
      description: t('map.cities.rabatDesc')
    },
    {
      name: t('map.cities.chefchaouen'),
      originalName: 'Chefchaouen',
      position: [35.1711, -5.2636],
      description: t('map.cities.chefchaouenDesc')
    },
    {
      name: t('map.cities.essaouira'),
      originalName: 'Essaouira',
      position: [31.5125, -9.7749],
      description: t('map.cities.essaouiraDesc')
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <h1 className="text-2xl font-bold text-gray-900">🗺️ {t('map.title')}</h1>
          <p className="mt-1 text-gray-600">{t('map.subtitle')}</p>
        </div>
      </div>

      <div className="relative h-screen">
        <MapContainer
          center={[31.7917, -7.0926]}
          zoom={6}
          style={{ height: '100%', width: '100%' }}
          ref={mapRef}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {moroccanCities.map((city, index) => (
            <Marker key={index} position={city.position as [number, number]}>
              <Popup>
                <div className="text-center">
                  <h3 className="font-bold text-lg">{city.name}</h3>
                  <p className="text-sm text-gray-600 mt-1">{city.description}</p>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>

        {/* Legend */}
        <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-4 z-1000">
          <h3 className="font-bold mb-2">{t('map.legend')}</h3>
          <div className="space-y-2 text-sm">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-red-500 rounded-full mr-2"></div>
              <span>{t('map.majorCities')}</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-blue-500 rounded-full mr-2"></div>
              <span>{t('map.coastalCities')}</span>
            </div>
          </div>
        </div>
      </div>

      {/* City Information Panel */}
      <div className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">{t('map.featuredDestinations')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {moroccanCities.map((city, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-lg">{city.name}</h3>
                <p className="text-gray-600 text-sm mt-1">{city.description}</p>
                <div className="mt-2 text-xs text-gray-500">
                  📍 {city.position[0].toFixed(4)}, {city.position[1].toFixed(4)}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Map