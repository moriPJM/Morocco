import React from 'react'
import { useTranslation } from 'react-i18next'
import AIGuide from '../components/AIGuide'

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

🏗️ **建築の見どころ**
• アールデコ建築群 - 1920年代のフランス統治時代の遺産
• 新市街の近代建築
• ハバス地区の neo-モロッコ様式

✈️ **アクセス**: ムハンマド5世国際空港（市内から約45分）
🚄 **交通**: 高速鉄道アルボラクでラバトまで1時間`,
          image: '/images/casablanca-hassan-ii.jpg'
        },
        {
          title: 'フェズ',
          description: `1200年の歴史を持つモロッコの古都で、世界最大の迷路都市として知られています。

🏰 **フェズ・エル・バリ（旧市街）**
• 世界遺産登録の中世都市
• 9000以上の路地が入り組む世界最大の車が入れない都市
• カラウィン大学 - 世界最古の大学の一つ（859年創立）

🎨 **伝統工芸**
• 革なめし工場（タンネリー）- 1000年以上変わらない伝統技法
• 陶器工房 - 青と白の美しいフェズ陶器
• 金属細工 - 真鍮製品の職人街
• 絨毯織り - ベルベル絨毯とペルシャ絨毯

🕌 **宗教建築**
• ブー・イナニア・マドラサ - 14世紀の美しいイスラム神学校
• アッタリン・マドラサ - 精巧なタイル装飾
• カラウィン・モスク - 北アフリカ最大のモスク

🎯 **観光のコツ**
• 公認ガイドの利用を強く推奨（迷子防止）
• 革なめし工場見学時はミントを持参（臭い対策）
• スリと偽ガイドに注意
• 値段交渉は当然（最初の価格の1/3から開始）

📍 **周辺観光**
• メクネス - 古都の一つ（車で1時間）
• ヴォルビリス遺跡 - ローマ時代の遺跡`,
          image: '/images/fez-tannery.jpg'
        }
      ]
    },

    {
      id: 'history',
      title: '歴史・文化',
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
• アハワッシュ - 祭りの際の伝統的な歌と踊り
• ベンディール - 伝統的な太鼓を使った音楽

🌾 **生活様式**
• 遊牧生活の伝統 - サハラ砂漠のトゥアレグ族
• オアシス農業 - ナツメヤシを中心とした農法
• 季節移動 - 山間部での羊の放牧`
        },
        {
          title: 'イスラム文化',
          description: `モロッコ人の99%がイスラム教徒で、イスラム文化が社会の基盤となっています。

🕌 **宗教的実践**
• 1日5回の礼拝（サラート）- ファジュル、ズフル、アスル、マグリブ、イシャー
• 金曜日の集団礼拝（ジュムア）- モスクでの重要な社会活動
• ラマダン月の断食 - 共同体の連帯を深める聖なる月
• ハッジ（大巡礼）とウムラ（小巡礼）- メッカへの聖地巡礼

🏛️ **イスラム建築**
• ミナレット - 礼拝を呼びかける尖塔
• ミフラーブ - メッカの方向を示すニッチ
• 中庭（リヤド）- 内向きの建築様式
• 幾何学装飾 - アラベスクとカリグラフィー

📚 **学問の伝統**
• フェズのカラウィン大学 - 世界最古の大学（859年創立）
• 神学、法学、医学、天文学の研究拠点
• 写本文化 - 貴重な古典の保存と伝承
• アラビア語文学の発展

🎨 **芸術への影響**
• 偶像崇拝の禁止による抽象芸術の発達
• カリグラフィー（書道）の高度な発展
• 音楽における精神性の追求
• 建築における光と影の美学

⚖️ **社会制度**
• イスラム法（シャリーア）の影響
• 家族制度の重視
• 慈善（ザカート）の精神
• 商業倫理の発達`
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
          description: `モロッコ料理の代表格で、円錐形の蓋が特徴的な土鍋料理です。

🍲 **タジンの種類**
• チキンタジン with レモンとオリーブ - 最もポピュラーな組み合わせ
• ラムタジン with プルーンとアーモンド - 甘みと塩味の絶妙なバランス
• 野菜タジン - ベジタリアン向け、季節の野菜がたっぷり
• シーフードタジン - 沿岸都市の特産品

🔥 **調理の秘密**
• 円錐形の蓋により水分が循環し、素材の旨味を閉じ込める
• 弱火でじっくり蒸し煮することで、肉が驚くほど柔らかくなる
• スパイス（クミン、コリアンダー、シナモン等）の絶妙な調合

🌿 **使用される香辛料**
• ラス・エル・ハヌート - モロッコの万能スパイスミックス
• サフラン - 高級タジンに使用される黄金のスパイス
• ハリッサ - 辛味を加える赤唐辛子ペースト

💡 **食べ方のマナー**
• 右手でパンを使って食べる（左手は使わない）
• 中央から自分の前の部分のみを食べる
• 完食は作り手への最高の敬意`,
          image: '/images/tagine-dish.jpg'
        },
        {
          title: 'クスクス',
          description: `セモリナ粉から作られる粒状のパスタで、金曜日の家族団欒料理として親しまれています。

🥘 **クスクスの種類**
• ロイヤルクスクス - 牛肉、鶏肉、ソーセージの豪華版
• 野菜クスクス - ズッキーニ、人参、カボチャなど7種の野菜
• シーフードクスクス - 魚と海老の沿岸都市バージョン
• 甘いクスクス - デザートとして蜂蜜やナッツと共に

👨‍👩‍👧‍👦 **文化的意義**
• 金曜日（聖なる日）の昼食の伝統
• 家族が一つの大皿を囲んで食べる団欒の象徴
• 結婚式や祝祭日の特別料理
• 母から娘へ受け継がれる家庭の味

🥄 **調理プロセス**
1. クスクスを蒸し器で3回蒸す（ふっくら仕上げる秘訣）
2. 野菜と肉を別鍋で煮込む
3. スープと具材を美しく盛り付ける
4. ハリッサ（辛味ソース）を添える

🍯 **地域による違い**
• マラケシュ風 - やや甘めの味付け
• フェズ風 - スパイスを効かせた複雑な味
• カサブランカ風 - シーフード中心のモダンスタイル`,
          image: '/images/couscous-dish.jpg'
        },
        {
          title: 'ミントティー',
          description: `緑茶にミントと砂糖を加えた、モロッコの国民的飲み物で「モロッコの魂」とも呼ばれます。

🍃 **ミントティーの役割**
• おもてなしの象徴 - ゲストを迎える最初の一杯
• 商談の潤滑油 - スークでの価格交渉時に必ず登場
• 家族の絆 - 一日数回、家族で楽しむ憩いの時間
• 宗教的意味 - イスラム教で禁止されているアルコールの代わり

🫖 **正式な淹れ方**
1. 銀のティーポットに緑茶（中国茶）を入れる
2. 沸騰したお湯を注ぎ、茶葉を洗う（1回目は捨てる）
3. 新鮮なミントの葉をたっぷり加える
4. 角砂糖を大量に入れる（甘さは控えめでなく、しっかり甘く）
5. 高い位置からグラスに注ぐ（泡立てるため）

🥃 **飲み方の作法**
• 必ず3杯飲むのが礼儀（1杯目は苦い、2杯目は甘い、3杯目は優しい）
• 立って注ぐことで敬意を表す
• グラスは小さく、熱いまま飲む
• 断ることは失礼にあたる

⏰ **一日のリズム**
• 朝食後 - 一日の始まりに
• 昼食後 - 食事の消化を助ける
• 夕食後 - 家族団欒の時間
• 来客時 - いつでもすぐに準備される

💚 **健康効果**
• 消化促進 - ミントが胃腸の働きを助ける
• リラックス効果 - カフェインとミントの組み合わせ
• 抗酸化作用 - 緑茶のカテキン効果`,
          image: '/images/mint-tea.jpg'
        }
      ]
    },

    {
      id: 'practical',
      title: '旅行実用情報',
      icon: '🎒',
      items: [
        {
          title: '気候・服装',
          description: `モロッコは地域により大きく異なる気候を持ちます。適切な準備で快適な旅を。

🌡️ **地域別気候**
• 沿岸部（カサブランカ、ラバト）
  - 地中海性気候、年間通して温暖
  - 夏：25-30°C、冬：10-18°C
  - 湿度が高く、海風が涼しい

• 内陸部（マラケシュ、フェズ）
  - 大陸性気候、昼夜の寒暖差大
  - 夏：35-45°C、冬：5-20°C
  - 乾燥しており、夏は非常に暑い

• 山間部（アトラス山脈）
  - 高山気候、標高により変化
  - 夏でも涼しく、冬は雪が降る
  - 朝晩は冷え込み注意

• 砂漠部（サハラ砂漠）
  - 極度に乾燥、昼夜の寒暖差激大
  - 昼：40-50°C、夜：0-10°C

🧳 **服装の基本**
• 露出の少ない服装（宗教的配慮）
• 長袖シャツ・長ズボン推奨
• 女性は胸元、肩、足の露出を避ける
• モスク見学時は肌を完全に覆う

👕 **季節別服装ガイド**
春秋（3-5月、9-11月）：
• 長袖シャツ、薄手のセーター
• 軽いジャケット（朝晩用）
• 歩きやすい靴、帽子

夏（6-8月）：
• 薄手の長袖（日焼け・虫刺され防止）
• 麻やコットン素材推奨
• サングラス、日焼け止め必須
• 水分補給グッズ

冬（12-2月）：
• 厚手のジャケット、コート
• 重ね着できる服装
• マフラー、手袋（山間部）`
        },
        {
          title: '交通・移動',
          description: `モロッコの移動手段を理解して、効率的な旅行を計画しましょう。

🚄 **鉄道（ONCF）**
• アルボラク（高速鉄道）
  - カサブランカ⇔タンジェ（2時間10分）
  - 最高時速320km、フランスTGV技術
  - 1等・2等クラス、事前予約推奨

• 在来線
  - カサブランカ⇔マラケシュ（3時間）
  - カサブランカ⇔フェズ（4時間）
  - 快適で時間通り、冷房完備

🚌 **長距離バス**
• CTM（国営バス会社）
  - 全国ネットワーク、英語対応
  - 快適、時間通り、値段も手頃
  - オンライン予約可能

• スプラトゥール
  - 民間高級バス会社
  - より豪華な内装、軽食サービス
  - 主要都市間を運行

🚕 **タクシー**
• グランタクシー（都市間移動）
  - 6人乗り、相乗りが基本
  - 定員になるまで出発しない
  - 料金は事前交渉制

• プチタクシー（市内移動）
  - 3人乗り、メーター制
  - 市内のみ運行、安価
  - 必ずメーター使用を確認

✈️ **国内線**
• ロイヤルエアモロッコ
• ラム・エクスプレス
• 主要都市間を結ぶ

🚗 **レンタカー**
• 国際免許証必要
• 保険加入必須
• 山道や砂漠は4WD推奨`
        },
        {
          title: '宿泊・グルメ',
          description: `モロッコならではの宿泊施設と食事の楽しみ方をご紹介。

🏨 **宿泊施設の種類**
• リヤド（Riad）
  - 中庭付きの伝統的な邸宅ホテル
  - メディナ内、オーセンティックな体験
  - 予算：8,000円〜50,000円/泊
  - 事前予約必須、路地が複雑

• ダール（Dar）
  - より小規模な伝統家屋
  - 家庭的な雰囲気、安価
  - 予算：3,000円〜15,000円/泊

• 国際チェーンホテル
  - ヒルトン、マリオット等
  - 新市街、ビジネス向け
  - 予算：15,000円〜40,000円/泊

• カスバホテル
  - 砂漠や山間部の要塞ホテル
  - 絶景、サハラ砂漠体験
  - 予算：10,000円〜30,000円/泊

🍽️ **食事スタイル**
• 高級レストラン
  - リヤド内の美食レストラン
  - コース料理、ワイン提供
  - 予算：3,000円〜8,000円/人

• 庶民的レストラン
  - ローカル向け食堂
  - タジン、クスクス中心
  - 予算：500円〜1,500円/人

• 屋台・ファストフード
  - ジャマ・エル・フナ広場等
  - ハリーラスープ、ケバブ
  - 予算：200円〜800円/人

🥤 **飲み物事情**
• アルコール：イスラム教国だが観光地では入手可能
• ミントティー：どこでも飲める国民飲料
• フレッシュジュース：オレンジ、ザクロ等豊富
• 水：ミネラルウォーター推奨`
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
            <div className="space-y-8">
              {section.items.map((item, index) => (
                <div key={index} className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
                  {item.image ? (
                    <div className="md:flex">
                      <div className="md:w-1/3">
                        <img 
                          src={item.image} 
                          alt={item.title}
                          className="w-full h-64 md:h-full object-cover"
                        />
                      </div>
                      <div className="md:w-2/3 p-6">
                        <h3 className="text-2xl font-bold text-morocco-red mb-4">
                          {item.title}
                        </h3>
                        <div className="prose prose-sm max-w-none text-gray-700">
                          {item.description.split('\n\n').map((paragraph, pIndex) => {
                            // ヘッダー行（**で囲まれた部分）を検出
                            if (paragraph.includes('**')) {
                              const parts = paragraph.split('**');
                              return (
                                <div key={pIndex} className="mb-4">
                                  {parts.map((part, partIndex) => {
                                    if (partIndex % 2 === 1) {
                                      // **で囲まれた部分はヘッダーとして表示
                                      return (
                                        <h4 key={partIndex} className="font-bold text-morocco-red text-lg mb-2 flex items-center">
                                          {part}
                                        </h4>
                                      );
                                    } else if (part.trim()) {
                                      // 通常のテキスト
                                      return (
                                        <div key={partIndex} className="mb-2">
                                          {part.split('\n').map((line, lineIndex) => {
                                            if (line.trim().startsWith('•')) {
                                              // リスト項目
                                              return (
                                                <div key={lineIndex} className="ml-4 mb-1 flex items-start">
                                                  <span className="text-morocco-gold mr-2 mt-1">•</span>
                                                  <span>{line.trim().substring(1).trim()}</span>
                                                </div>
                                              );
                                            } else if (line.trim().startsWith('-')) {
                                              // サブリスト項目
                                              return (
                                                <div key={lineIndex} className="ml-8 mb-1 flex items-start">
                                                  <span className="text-gray-400 mr-2 mt-1">-</span>
                                                  <span className="text-sm">{line.trim().substring(1).trim()}</span>
                                                </div>
                                              );
                                            } else if (line.trim()) {
                                              // 通常の段落
                                              return (
                                                <p key={lineIndex} className="mb-2">
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
                            } else {
                              // 通常の段落
                              return (
                                <div key={pIndex} className="mb-4">
                                  {paragraph.split('\n').map((line, lineIndex) => {
                                    if (line.trim().startsWith('•')) {
                                      return (
                                        <div key={lineIndex} className="ml-4 mb-1 flex items-start">
                                          <span className="text-morocco-gold mr-2 mt-1">•</span>
                                          <span>{line.trim().substring(1).trim()}</span>
                                        </div>
                                      );
                                    } else if (line.trim().startsWith('-')) {
                                      return (
                                        <div key={lineIndex} className="ml-8 mb-1 flex items-start">
                                          <span className="text-gray-400 mr-2 mt-1">-</span>
                                          <span className="text-sm">{line.trim().substring(1).trim()}</span>
                                        </div>
                                      );
                                    } else if (line.trim()) {
                                      return (
                                        <p key={lineIndex} className="mb-2">
                                          {line.trim()}
                                        </p>
                                      );
                                    }
                                    return null;
                                  })}
                                </div>
                              );
                            }
                          })}
                        </div>
                      </div>
                    </div>
                  ) : (
                    // 画像がない場合のレイアウト
                    <div className="p-6">
                      <h3 className="text-2xl font-bold text-morocco-red mb-4">
                        {item.title}
                      </h3>
                      <div className="prose prose-sm max-w-none text-gray-700">
                        {item.description.split('\n\n').map((paragraph, pIndex) => {
                          // ヘッダー行（**で囲まれた部分）を検出
                          if (paragraph.includes('**')) {
                            const parts = paragraph.split('**');
                            return (
                              <div key={pIndex} className="mb-4">
                                {parts.map((part, partIndex) => {
                                  if (partIndex % 2 === 1) {
                                    // **で囲まれた部分はヘッダーとして表示
                                    return (
                                      <h4 key={partIndex} className="font-bold text-morocco-red text-lg mb-2 flex items-center">
                                        {part}
                                      </h4>
                                    );
                                  } else if (part.trim()) {
                                    // 通常のテキスト
                                    return (
                                      <div key={partIndex} className="mb-2">
                                        {part.split('\n').map((line, lineIndex) => {
                                          if (line.trim().startsWith('•')) {
                                            // リスト項目
                                            return (
                                              <div key={lineIndex} className="ml-4 mb-1 flex items-start">
                                                <span className="text-morocco-gold mr-2 mt-1">•</span>
                                                <span>{line.trim().substring(1).trim()}</span>
                                              </div>
                                            );
                                          } else if (line.trim().startsWith('-')) {
                                            // サブリスト項目
                                            return (
                                              <div key={lineIndex} className="ml-8 mb-1 flex items-start">
                                                <span className="text-gray-400 mr-2 mt-1">-</span>
                                                <span className="text-sm">{line.trim().substring(1).trim()}</span>
                                              </div>
                                            );
                                          } else if (line.trim()) {
                                            // 通常の段落
                                            return (
                                              <p key={lineIndex} className="mb-2">
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
                          } else {
                            // 通常の段落
                            return (
                              <div key={pIndex} className="mb-4">
                                {paragraph.split('\n').map((line, lineIndex) => {
                                  if (line.trim().startsWith('•')) {
                                    return (
                                      <div key={lineIndex} className="ml-4 mb-1 flex items-start">
                                        <span className="text-morocco-gold mr-2 mt-1">•</span>
                                        <span>{line.trim().substring(1).trim()}</span>
                                      </div>
                                    );
                                  } else if (line.trim().startsWith('-')) {
                                    return (
                                      <div key={lineIndex} className="ml-8 mb-1 flex items-start">
                                        <span className="text-gray-400 mr-2 mt-1">-</span>
                                        <span className="text-sm">{line.trim().substring(1).trim()}</span>
                                      </div>
                                    );
                                  } else if (line.trim()) {
                                    return (
                                      <p key={lineIndex} className="mb-2">
                                        {line.trim()}
                                      </p>
                                    );
                                  }
                                  return null;
                                })}
                              </div>
                            );
                          }
                        })}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* 文化的エチケット */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="mr-3 text-3xl">🤝</span>
            文化的エチケット・マナー
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🙏</span>挨拶とマナー
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• 握手は同性同士のみ、異性との握手は避ける</li>
                <li>• 「アッサラーム・アライクム」（平和があなたに）が一般的な挨拶</li>
                <li>• 左手は不浄とされるため、物の受け渡しは右手で</li>
                <li>• 年長者や地位の高い人を敬う文化</li>
                <li>• 靴を脱いで家に上がることが多い</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">👕</span>服装規定
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• モスクでは肌を露出しない服装必須</li>
                <li>• 女性はスカーフで髪を覆うことが推奨される</li>
                <li>• 短パンやタンクトップは公共の場では避ける</li>
                <li>• 保守的な地域では特に注意が必要</li>
                <li>• ビーチでは適度な露出は許容される</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🍵</span>食事のマナー
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• 食事前後の手洗いは大切な儀式</li>
                <li>• パンは神聖な食べ物、落とさないよう注意</li>
                <li>• ミントティーは3杯飲むのが礼儀</li>
                <li>• 食事中の左手使用は避ける</li>
                <li>• 豚肉・アルコールは宗教的にタブー</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🕌</span>宗教的配慮
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• 1日5回の祈りの時間を尊重する</li>
                <li>• 金曜日は聖なる日、モスクでの集団礼拝</li>
                <li>• ラマダン期間中は日中の飲食を控えめに</li>
                <li>• モスク内では静粛に、写真撮影は許可を得る</li>
                <li>• アザーン（礼拝の呼びかけ）中は敬意を示す</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">📷</span>写真撮影
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• 人物撮影は必ず許可を取る</li>
                <li>• 軍事施設・政府機関の撮影は禁止</li>
                <li>• 女性の撮影は特に慎重に</li>
                <li>• モスク内部は撮影禁止の場合が多い</li>
                <li>• 職人の作業風景撮影は小額のチップを</li>
              </ul>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">💰</span>商習慣・チップ
              </h3>
              <ul className="space-y-2 text-gray-700">
                <li>• スーク（市場）では価格交渉が文化</li>
                <li>• 最初の提示価格の1/3程度から交渉開始</li>
                <li>• レストランでは10-15%のチップが一般的</li>
                <li>• ホテルスタッフにも小額のチップを</li>
                <li>• ガイドには1日50-100ディルハム程度</li>
              </ul>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-morocco-green bg-opacity-10 rounded-lg border-l-4 border-morocco-green">
            <h3 className="font-semibold text-morocco-green mb-2">💡 旅行者へのアドバイス</h3>
            <p className="text-gray-700">
              モロッコの人々は非常にホスピタリティに富んでおり、外国人観光客を温かく迎えてくれます。
              文化的な違いを理解し、敬意を払うことで、より深いモロッコ体験ができるでしょう。
              不明な点があれば、現地の人に丁寧に尋ねることをお勧めします。
            </p>
          </div>
        </div>

        {/* AIガイド */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
            <span className="mr-3 text-3xl">🤖</span>
            AIガイドに質問する
          </h2>
          <div className="mb-4">
            <p className="text-gray-600 mb-4">
              モロッコ旅行の専門AIガイドが、観光地、文化、料理、エチケットなどの質問にお答えします。
              お気軽に何でもお尋ねください！
            </p>
          </div>
          <AIGuide />
        </div>

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