import { useTranslation } from 'react-i18next'

const Home = () => {
  const { t } = useTranslation()

  const features = [
    {
      icon: '🔤',
      title: t('features.translator.title'),
      description: t('features.translator.description')
    },
    {
      icon: '📖',
      title: t('features.guides.title'),
      description: t('features.guides.description')
    },
    {
      icon: '🗺️',
      title: t('features.maps.title'),
      description: t('features.maps.description')
    },
    {
      icon: '❤️',
      title: t('features.favorites.title'),
      description: t('features.favorites.description')
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-morocco-sand to-morocco-blue">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl tracking-tight font-extrabold text-white sm:text-5xl md:text-6xl">
              <span className="block">{t('home.welcome')}</span>
              <span className="block text-morocco-gold">{t('home.subtitle')}</span>
            </h1>
            <p className="mt-3 max-w-md mx-auto text-base text-white sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
              {t('home.description')}
            </p>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-morocco-red font-semibold tracking-wide uppercase">{t('home.featuresTitle')}</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
              {t('home.featuresSubtitle')}
            </p>
          </div>

          <div className="mt-10">
            <div className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              {features.map((feature, index) => (
                <div key={index} className="relative">
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-morocco-red text-white text-2xl">
                    {feature.icon}
                  </div>
                  <div className="ml-16">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">{feature.title}</h3>
                    <p className="mt-2 text-base text-gray-500">{feature.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-morocco-green">
        <div className="max-w-2xl mx-auto text-center py-16 px-4 sm:py-20 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
            <span className="block">{t('home.ctaTitle')}</span>
            <span className="block">{t('home.ctaSubtitle')}</span>
          </h2>
          <p className="mt-4 text-lg leading-6 text-morocco-gold">
            {t('home.ctaDescription')}
          </p>
        </div>
      </div>
    </div>
  )
}

export default Home