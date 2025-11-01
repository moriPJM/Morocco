import React, { useState, useEffect, useRef } from 'react'
import { useTranslation } from 'react-i18next'

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

const AIGuide: React.FC = () => {
  const { t } = useTranslation()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // 初期メッセージ
  useEffect(() => {
    const welcomeMessage: Message = {
      id: '1',
      text: 'こんにちは！モロッコAIガイドです。モロッコの観光地、文化、料理、エチケットなど、何でもお気軽にお尋ねください。🇲🇦',
      isUser: false,
      timestamp: new Date()
    }
    setMessages([welcomeMessage])
  }, [])

  // メッセージの最下部にスクロール
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // AIガイドの応答ロジック
  const getAIResponse = (userInput: string): string => {
    const input = userInput.toLowerCase()

    // 観光地に関する質問
    if (input.includes('マラケシュ') || input.includes('marrakech')) {
      return `マラケシュは「赤い街」として知られる魅力的な都市です！🏛️

主な見どころ：
• ジャマ・エル・フナ広場 - 夜には食べ物の屋台や芸人で賑わいます
• マジョレル庭園 - イヴ・サンローランが愛した美しい青の庭園
• バヒア宮殿 - 19世紀の豪華な宮殿
• メディナ - 迷路のような旧市街でお買い物を楽しめます

ベストシーズンは10月〜4月です。他に何かお聞きしたいことはありますか？`
    }

    if (input.includes('カサブランカ') || input.includes('casablanca')) {
      return `カサブランカはモロッコ最大の経済都市です！🏙️

必見スポット：
• ハッサン2世モスク - 世界で3番目に大きなモスク
• コルニッシュ - 美しい海岸線の散歩道
• アールデコ建築群 - フランス植民地時代の美しい建築
• ハッバス地区 - 伝統的な雰囲気のあるエリア

映画「カサブランカ」の舞台としても有名ですね！`
    }

    if (input.includes('フェズ') || input.includes('fez')) {
      return `フェズは1000年以上の歴史を持つ古都です！🏺

見どころ：
• フェズ・エル・バリ - 世界最大の迷路都市
• 革なめし工場 - 伝統的な革製品の製造現場
• ブー・イナニア・マドラサ - 美しいイスラム建築
• 陶器工房 - 青と白の美しいフェズ陶器

迷子になりやすいので、ガイドと一緒に歩くことをお勧めします！`
    }

    // 料理に関する質問
    if (input.includes('タジン') || input.includes('料理') || input.includes('食べ物')) {
      return `モロッコ料理は香辛料の宝庫です！🍽️

代表的な料理：
• タジン - 円錐形の土鍋で作る蒸し料理
• クスクス - 金曜日の家族料理、野菜と肉のハーモニー
• ハリーラ - ラマダン明けに飲むスープ
• パスティーユ - 甘いパイ生地の中に鳩肉やチキン

ミントティーは必ず3杯飲むのがマナーですよ！🍵`
    }

    // エチケットに関する質問
    if (input.includes('マナー') || input.includes('エチケット') || input.includes('注意')) {
      return `モロッコでのマナーをお教えします！🤝

重要なポイント：
• 左手は不浄とされるため、右手で物を受け渡しする
• モスクでは肌の露出を避け、女性はスカーフを着用
• 写真撮影は必ず許可を取る
• 握手は同性同士のみ
• 靴を脱いで家に上がることが多い

「アッサラーム・アライクム」(平和があなたに)が基本の挨拶です。現地の文化を尊重することで、より深い体験ができますよ！`
    }

    // 買い物に関する質問
    if (input.includes('買い物') || input.includes('お土産') || input.includes('市場')) {
      return `モロッコでのお買い物は価格交渉が文化です！💰

おすすめお土産：
• アルガンオイル - モロッコ原産の美容オイル
• 革製品 - バッグや靴、ベルトなど
• 絨毯 - ベルベル絨毯は特に有名
• 陶器 - 青と白の美しいタイル
• 香辛料 - ラス・エル・ハヌートなど

スークでは最初の提示価格の1/3から交渉を始めましょう。楽しい駆け引きも旅の醍醐味です！`
    }

    // 天気・気候に関する質問
    if (input.includes('天気') || input.includes('気候') || input.includes('服装')) {
      return `モロッコの気候は地域によって異なります！🌤️

地域別気候：
• 沿岸部（カサブランカ）- 地中海性気候、温暖
• 内陸部（マラケシュ）- 乾燥した大陸性気候
• 山間部（アトラス山脈）- 冬は雪が降ることも
• 砂漠部（サハラ）- 昼夜の寒暖差が激しい

ベストシーズン：10月〜4月
夏は非常に暑いので、薄手の長袖と帽子をお忘れなく！`
    }

    // 交通に関する質問
    if (input.includes('交通') || input.includes('移動') || input.includes('電車')) {
      return `モロッコの交通手段をご紹介します！🚂

主な交通手段：
• ONCF - 高速鉄道アルボラクが便利（カサブランカ〜タンジェ）
• グランタクシー - 都市間移動に最適
• プチタクシー - 市内移動用の小型タクシー
• バス - CTM、スプラトゥールが大手会社
• レンタカー - 国際免許証が必要

タクシーはメーターを使ってもらうか、事前に料金交渉しましょう！`
    }

    // 言語に関する質問
    if (input.includes('言語') || input.includes('アラビア語') || input.includes('フランス語')) {
      return `モロッコは多言語国家です！🗣️

公用語：
• アラビア語（古典・モロッコ方言）
• ベルベル語（タマジット語）

広く使われる言語：
• フランス語 - 旧宗主国の影響で広く通用
• 英語 - 観光地では通じることが多い
• スペイン語 - 北部地域で使用

基本的な挨拶：
• こんにちは - アッサラーム・アライクム
• ありがとう - シュクラン
• はい - ナアム / ワハー`
    }

    // デフォルトの応答
    return `ご質問ありがとうございます！🙏

モロッコについて、以下のトピックでお答えできます：
• 観光地（マラケシュ、カサブランカ、フェズなど）
• 料理とグルメ
• 文化とエチケット
• お買い物とお土産
• 天気と気候
• 交通手段
• 言語について

具体的に何についてお知りになりたいですか？お気軽にお尋ねください！`
  }

  const handleSendMessage = () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsTyping(true)

    // AIの応答をシミュレート（少し遅延を入れて自然に）
    setTimeout(() => {
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: getAIResponse(inputText),
        isUser: false,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiResponse])
      setIsTyping(false)
    }, 1500)
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg h-96 flex flex-col">
      {/* ヘッダー */}
      <div className="bg-morocco-red text-white p-4 rounded-t-lg">
        <h3 className="font-semibold flex items-center">
          <span className="mr-2">🤖</span>
          モロッコAIガイド
        </h3>
        <p className="text-sm opacity-90">何でもお気軽にお尋ねください</p>
      </div>

      {/* メッセージエリア */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.isUser
                  ? 'bg-morocco-gold text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              <p className="whitespace-pre-line">{message.text}</p>
              <p className="text-xs opacity-70 mt-1">
                {message.timestamp.toLocaleTimeString('ja-JP', {
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* 入力エリア */}
      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="モロッコについて質問してください..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-morocco-red"
            disabled={isTyping}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isTyping}
            className="bg-morocco-red text-white px-4 py-2 rounded-lg hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            送信
          </button>
        </div>
      </div>
    </div>
  )
}

export default AIGuide