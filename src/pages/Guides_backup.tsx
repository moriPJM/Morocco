import React from 'react'
import { useTranslation } from 'react-i18next'

const Guides: React.FC = () => {
  const { t } = useTranslation()

  const cityGuides = [
    {
      id: 'cities',
      title: t('guides.citiesTitle'),
      icon: '🏛️',
      items: [
        {
          title: 'マラケシュ',
          description: '活気に満ちた赤い街。有名なジャマ・エル・フナ広場、美しいマジョレル庭園、迷路のようなメディナが魅力です。',
          image: 'https://images.unsplash.com/photo-1516706988947-d633b910e3bd?w=300&h=200&fit=crop',
          tips: ['ジャマ・エル・フナ広場は夕方頃が最も賑やか', 'マジョレル庭園は午前中の訪問がおすすめ']
        },
        {
          title: 'カサブランカ',
          description: 'モロッコ最大の経済都市。壮大なハッサン2世モスク、美しい海岸線コルニッシュ、アールデコ建築が見どころです。',
          image: 'https://images.unsplash.com/photo-1555993539-1732b0258235?w=300&h=200&fit=crop',
          tips: ['ハッサン2世モスクは金曜日の午後は見学不可', 'コルニッシュは夕日の時間帯が特に美しい']
        },
        {
          title: 'フェズ',
          description: '古都の魅力が残る文化の中心地。世界最大の迷路都市フェズ・エル・バリ、伝統的な革なめし工場、美しいマドラサが必見です。',
          image: 'https://images.unsplash.com/photo-1561129568-ed5bb6acea97?w=300&h=200&fit=crop',
          tips: ['革なめし工場は匂いが強いので、ミントを持参すると良い', 'フェズ・エル・バリは必ずガイドと一緒に']
        }
      ]
    },
    {
      id: 'culture',
      title: t('guides.cultureTitle'),
      icon: '🎭',
      items: [
        {
          title: '伝統工芸',
          description: 'モロッコの美しい手工芸品は世界的に有名です。陶器、絨毯、革製品、銀細工など、職人の技が光る作品をお楽しみください。',
          image: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=300&h=200&fit=crop'
        },
        {
          title: '音楽と踊り',
          description: 'ベルベル音楽、アンダルシア音楽、グナワ音楽など、多様な音楽文化が息づいています。',
          image: 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=300&h=200&fit=crop'
        }
      ]
    },
    {
      id: 'cuisine',
      title: t('guides.cuisineTitle'),
      icon: '🍽️',
      items: [
        {
          title: 'タジン',
          description: '円錐形の蓋が特徴的な土鍋料理。野菜、肉、魚など様々な具材を使った、モロッコの代表的な料理です。',
          image: 'https://images.unsplash.com/photo-1544736150-6f4a0b10d4e4?w=300&h=200&fit=crop'
        },
        {
          title: 'クスクス',
          description: '金曜日の伝統料理として親しまれている、セモリナ粉から作られる粒状のパスタです。',
          image: 'https://images.unsplash.com/photo-1573160103600-9663fbf3e55b?w=300&h=200&fit=crop'
        },
        {
          title: 'ミントティー',
          description: '緑茶にミントと砂糖を加えた、モロッコの国民的飲み物。おもてなしの心の象徴です。',
          image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=200&fit=crop'
        }
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {t('guides.title')}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            {t('guides.subtitle')}
          </p>
        </div>

        {/* ガイドセクション */}
        {cityGuides.map((section) => (
          <div key={section.id} className="mb-12 bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <span className="mr-3 text-3xl">{section.icon}</span>
              {section.title}
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {section.items.map((item, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-6 hover:shadow-lg transition-shadow">
                  <img 
                    src={item.image} 
                    alt={item.title}
                    className="w-full h-48 object-cover rounded-lg mb-4"
                  />
                  <h3 className="text-xl font-semibold text-morocco-red mb-3">
                    {item.title}
                  </h3>
                  <p className="text-gray-700 mb-4">
                    {item.description}
                  </p>
                  {item.tips && (
                    <div className="mt-4 p-3 bg-morocco-gold bg-opacity-20 rounded-lg">
                      <h4 className="font-semibold text-morocco-green mb-2">💡 観光のヒント</h4>
                      <ul className="text-sm text-gray-700 space-y-1">
                        {item.tips.map((tip, tipIndex) => (
                          <li key={tipIndex}>• {tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* 通貨情報 */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="mr-3 text-3xl">ℹ️</span>
            {t('guides.infoTitle')}
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="font-semibold mb-2">{t('guides.currencyTitle')}</h3>
              <p className="text-morocco-gold">{t('guides.currencyDesc')}</p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">{t('guides.languageTitle')}</h3>
              <p className="text-morocco-gold">{t('guides.languageDesc')}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Guides