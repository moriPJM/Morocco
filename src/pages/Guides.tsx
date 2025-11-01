import React from 'react'
import { useTranslation } from 'react-i18next'
import AIGuide from '../components/AIGuide'

const Guides: React.FC = () => {
  const { t } = useTranslation()

  // コンテンツを整形して表示する関数
  const renderFormattedContent = (content: string) => {
    return content.split('\n\n').map((paragraph, pIndex) => {
      // ヘッダー行（**で囲まれた部分）を検出
      if (paragraph.includes('**')) {
        const parts = paragraph.split('**');
        return (
          <div key={pIndex} className="mb-6">
            {parts.map((part, partIndex) => {
              if (partIndex % 2 === 1) {
                // **で囲まれた部分はヘッダーとして表示
                return (
                  <h4 key={partIndex} className="font-bold text-morocco-red text-xl mb-3 flex items-center">
                    {part}
                  </h4>
                );
              } else if (part.trim()) {
                // 通常のテキスト
                return (
                  <div key={partIndex} className="mb-3">
                    {part.split('\n').map((line, lineIndex) => {
                      if (line.trim().startsWith('•')) {
                        // リスト項目
                        return (
                          <div key={lineIndex} className="flex items-start mb-2 pl-4">
                            <span className="text-morocco-gold mr-3 mt-1">•</span>
                            <span className="text-gray-700 leading-relaxed">{line.trim().substring(1).trim()}</span>
                          </div>
                        );
                      } else if (line.trim()) {
                        // 通常の行
                        return (
                          <p key={lineIndex} className="text-gray-700 leading-relaxed mb-2">
                            {line.trim()}
                          </p>
                        );
                      }
                      return null;
                    })}
                  </div>
                );
              }
              return null;
            })}
          </div>
        );
      } else if (paragraph.trim()) {
        // 通常の段落
        return (
          <div key={pIndex} className="mb-4">
            {paragraph.split('\n').map((line, lineIndex) => {
              if (line.trim().startsWith('•')) {
                return (
                  <div key={lineIndex} className="flex items-start mb-2 pl-4">
                    <span className="text-morocco-gold mr-3 mt-1">•</span>
                    <span className="text-gray-700 leading-relaxed">{line.trim().substring(1).trim()}</span>
                  </div>
                );
              } else if (line.trim()) {
                return (
                  <p key={lineIndex} className="text-gray-700 leading-relaxed mb-2">
                    {line.trim()}
                  </p>
                );
              }
              return null;
            })}
          </div>
        );
      }
      return null;
    });
  };

  const cityGuides = [
    {
      id: 'cities',
      title: t('guides.citiesTitle'),
      icon: '🏛️',
      items: [
        {
          title: 'マラケシュ',
          description: `「赤い街」として知られるマラケシュは、モロッコ屈指の観光都市です。

🏛️ **主要観光地**
• ジャマ・エル・フナ広場 - 世界遺産に登録された活気溢れる中央広場
• マジョレル庭園 - イヴ・サンローランが愛した美しいコバルトブルーの庭園
• バヒア宮殿 - 19世紀の豪華絢爛な宮殿建築
• サアド朝の墓群 - 16世紀の美しい霊廟群
• クトゥビーヤ・モスク - マラケシュのシンボルとなる高さ77mのミナレット

🛍️ **ショッピング**
• メディナのスーク - 革製品、絨毯、陶器、香辛料の宝庫
• ゲリーズ - 新市街の高級ショッピングエリア

🍽️ **グルメ**
• ジャマ・エル・フナ広場の屋台料理
• 高級リヤドでの伝統モロッコ料理
• 屋上テラスからアトラス山脈を望む絶景レストラン

📅 **ベストシーズン**: 10月〜4月（夏は40度を超える猛暑）
💰 **予算**: 中級リヤド 1泊8,000〜15,000円`,
          image: '/images/marrakech-panorama.jpg'
        },
        {
          title: 'カサブランカ',
          description: `モロッコ最大の経済都市で、近代的な街並みとモロッコ伝統が融合した魅力的な都市です。

🕌 **主要観光地**
• ハッサン2世モスク - 世界で3番目に大きな壮大なモスク（海に面した絶景）
• オールドメディナ - 古い城壁に囲まれた伝統的な旧市街
• ムハンマド5世広場 - フランス植民地時代の美しい建築群
• リックスカフェ - 映画「カサブランカ」をテーマにした有名カフェ

🏖️ **コルニッシュ地区**
• アインディアブビーチ - 市内最大のビーチリゾート
• モロッコモール - アフリカ最大級のショッピングモール
• 高級ホテルとレストランが立ち並ぶ海岸通り

💰 **予算**: 中級ホテル 1泊6,000〜12,000円`,
          image: '/images/casablanca-hassan-ii.jpg'
        }
      ]
    },
    {
      id: 'history',
      title: t('guides.historyTitle'),
      icon: '📜',
      items: [
        {
          title: 'モロッコの歴史',
          description: `数千年の歴史を持つモロッコは、多様な文明が交差した魅力的な歴史を持ちます。

🏺 **古代から中世**
• ベルベル人の先住文化（紀元前数千年から）
• フェニキア・ローマ時代の影響（ヴォルビリス遺跡）
• イスラム征服（7世紀）とアラブ文化の流入
• アルモラビド朝（11-12世紀）- マラケシュ建設
• アルムワッヒド朝（12-13世紀）- クトゥビーヤモスク建設

👑 **王朝の変遷**
• マリーン朝（13-15世紀）- フェズの黄金時代
• サアド朝（16-17世紀）- サアド朝の墓群建設
• アラウィー朝（1666年〜現在）- 現王室の祖先

🏴‍☠️ **ヨーロッパとの関係**
• ポルトガル・スペインの沿岸部占領（15-16世紀）
• フランス保護領時代（1912-1956）
• スペイン保護領（北部・南部、1912-1956）
• 1956年独立達成

🤴 **現代モロッコ**
• ムハンマド5世 - 独立の父
• ハサン2世 - 近代化の推進者（1961-1999）
• ムハンマド6世 - 現国王（1999年〜）改革推進`
        },
        {
          title: 'ベルベル文化',
          description: `モロッコの先住民族ベルベル人（アマジグ人）の豊かな文化は、現代モロッコの基盤です。

🗣️ **言語**
• タマジット語（ベルベル語）- 2011年に公用語化
• ティフィナグ文字 - 古代から続く独自の文字体系
• 口承伝統 - 神話、詩、音楽の豊かな伝統

🎨 **芸術・工芸**
• ベルベル絨毯 - 地域ごとの独特な模様とシンボル
• 銀装身具 - 幾何学模様の美しいアクセサリー
• 陶器 - 素朴で実用的な日用品
• 刺繍 - 鮮やかな色彩の伝統的な服飾

🏠 **建築**
• カスバ（要塞化された村）- アトラス山脈に点在
• アイット・ベン・ハドゥ - 世界遺産の泥の城
• グラナリー（穀物倉庫）- 山間部の共同倉庫

🎵 **音楽とダンス**
• アハイドゥス - 山間部の集団舞踊
• アハワッシュ - 祭りの際の伝統的な歌と踊り`
        }
      ]
    },
    {
      id: 'food',
      title: t('guides.foodTitle'),
      icon: '🍽️',
      items: [
        {
          title: 'モロッコ料理の特徴',
          description: `アラブ、ベルベル、地中海、アンダルシアの影響を受けた豊かな味わい。

🌶️ **基本的な特徴**
• 香辛料を多用した風味豊かな料理
• 甘味と塩味の絶妙なバランス
• 新鮮な野菜と肉類の組み合わせ
• オリーブオイルとアルガンオイルの使用

🥘 **代表的な料理**
• タジン - 円錐形の蓋が特徴的な煮込み料理
• クスクス - 金曜日の国民料理、セモリナ粉の粒状パスタ
• パスティーヤ - 甘みのあるパイ生地に鳩肉やアーモンド
• ハリラ - トマトベースの栄養豊富なスープ

🍃 **主要な香辛料**
• ラス・エル・ハヌート - モロッコミックススパイス
• クミン、コリアンダー、シナモン
• サフラン - 世界最高級品の産地
• ハリッサ - 唐辛子ベースの辛味調味料

🍵 **飲み物**
• アタイ - ミントティー（国民的飲み物）
• アルガンオイル - 美容と健康に良い希少オイル
• フレッシュフルーツジュース`
        }
      ]
    },
    {
      id: 'culture',
      title: t('guides.cultureTitle'),
      icon: '🎭',
      items: [
        {
          title: '文化とエチケット',
          description: `モロッコはイスラム教国であり、宗教的・文化的な配慮が重要です。

🤝 **社会的エチケット**
• 挨拶は右手で行う（左手は不浄とされる）
• 年長者への敬意を示す
• 公共の場での大声や騒音は控える
• 同性間での握手は一般的、異性間は避ける

👗 **服装のマナー**
• 控えめで身体を覆う服装が好ましい
• モスクや宗教施設では長袖・長ズボン必須
• 女性は髪を隠すスカーフを持参推奨
• 海岸のリゾート地では比較的自由

🕌 **宗教的配慮**
• 1日5回の祈りの時間を尊重
• 金曜日は聖なる日（ジュムア）
• ラマダン期間中は日中の飲食に配慮
• モスク内では静粛に、撮影は許可を得る

💰 **商習慣**
• 価格交渉（ハガリング）は文化の一部
• 初回提示価格の30-50%程度が適正
• チップ文化あり（レストラン10-15%）
• 現金での支払いが主流`
        }
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-morocco-red/5 to-morocco-gold/5 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* ヘッダーセクション */}
        <div className="text-center mb-16 relative">
          <div className="absolute inset-0 bg-gradient-to-r from-morocco-red to-morocco-gold opacity-10 rounded-3xl"></div>
          <div className="relative py-12 px-8">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              🇲🇦 {t('guides.title')}
            </h1>
            <p className="text-2xl text-gray-700 max-w-4xl mx-auto leading-relaxed">
              {t('guides.subtitle')}
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <span className="inline-flex items-center px-4 py-2 bg-morocco-red/10 text-morocco-red rounded-full text-sm font-medium">
                📍 8つの都市ガイド
              </span>
              <span className="inline-flex items-center px-4 py-2 bg-morocco-gold/10 text-yellow-800 rounded-full text-sm font-medium">
                🏛️ 歴史・文化情報
              </span>
              <span className="inline-flex items-center px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-medium">
                💡 実用的なヒント
              </span>
            </div>
          </div>
        </div>

        {/* ナビゲーションメニュー */}
        <div className="mb-12">
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">📚 ガイドカテゴリー</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {cityGuides.map((section) => (
                <a
                  key={section.id}
                  href={`#${section.id}`}
                  className="group bg-gradient-to-br from-gray-50 to-white border border-gray-200 rounded-xl p-6 hover:shadow-lg hover:border-morocco-red/30 transition-all duration-300 transform hover:-translate-y-1"
                >
                  <div className="text-center">
                    <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-300">
                      {section.icon}
                    </div>
                    <h3 className="font-bold text-gray-900 group-hover:text-morocco-red transition-colors">
                      {section.title}
                    </h3>
                    <p className="text-sm text-gray-600 mt-2">
                      {section.items.length}項目
                    </p>
                  </div>
                </a>
              ))}
            </div>
          </div>
        </div>

        {/* AIガイドセクション */}
        <div className="mb-12">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl shadow-xl p-8 text-white">
            <div className="text-center mb-6">
              <h2 className="text-3xl font-bold mb-3">🤖 AIパーソナルガイド</h2>
              <p className="text-xl opacity-90">あなた専用のモロッコ旅行アシスタント</p>
            </div>
            <AIGuide />
          </div>
        </div>

        {/* ガイドセクション */}
        {cityGuides.map((section) => (
          <div key={section.id} id={section.id} className="mb-16">
            {/* セクションヘッダー */}
            <div className="text-center mb-10">
              <div className="inline-flex items-center bg-white rounded-full px-8 py-4 shadow-lg border border-gray-100">
                <span className="text-4xl mr-4">{section.icon}</span>
                <h2 className="text-3xl font-bold text-gray-900">{section.title}</h2>
              </div>
            </div>

            {/* セクションアイテム */}
            <div className="grid gap-8">
              {section.items.map((item, index) => (
                <div 
                  key={index} 
                  className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1"
                >
                  {(item as any).image ? (
                    /* 画像付きレイアウト */
                    <div className="lg:flex">
                      <div className="lg:w-2/5 relative">
                        <img 
                          src={(item as any).image} 
                          alt={item.title}
                          className="w-full h-80 lg:h-full object-cover"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent lg:hidden"></div>
                        <div className="absolute bottom-4 left-4 lg:hidden">
                          <h3 className="text-2xl font-bold text-white mb-2">{item.title}</h3>
                        </div>
                      </div>
                      <div className="lg:w-3/5 p-8">
                        <div className="hidden lg:block mb-6">
                          <h3 className="text-3xl font-bold text-morocco-red mb-2">{item.title}</h3>
                          <div className="w-20 h-1 bg-gradient-to-r from-morocco-red to-morocco-gold rounded"></div>
                        </div>
                        <div className="prose prose-lg max-w-none text-gray-700">
                          {renderFormattedContent(item.description)}
                        </div>
                      </div>
                    </div>
                  ) : (
                    /* テキストのみレイアウト */
                    <div className="p-8">
                      <div className="mb-6">
                        <h3 className="text-3xl font-bold text-morocco-red mb-3">{item.title}</h3>
                        <div className="w-20 h-1 bg-gradient-to-r from-morocco-red to-morocco-gold rounded"></div>
                      </div>
                      <div className="prose prose-lg max-w-none text-gray-700">
                        {renderFormattedContent(item.description)}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* フッター */}
        <div className="mt-20 text-center">
          <div className="bg-gradient-to-r from-morocco-red to-morocco-gold rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">🌟 素晴らしいモロッコ旅行を！</h3>
            <p className="text-lg opacity-90 max-w-2xl mx-auto">
              このガイドがあなたのモロッコ旅行を忘れられない体験にする手助けとなることを願っています。
              安全で楽しい旅をお過ごしください！
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Guides