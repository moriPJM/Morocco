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
  const [isLoading, setIsLoading] = useState(false)
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

  // OpenAI APIを使用したAI応答の取得
  const getAIResponse = async (userInput: string): Promise<string> => {
    const apiKey = import.meta.env.VITE_OPENAI_API_KEY
    
    if (!apiKey) {
      return "申し訳ございませんが、AI機能を利用するにはAPIキーが必要です。"
    }

    try {
      const response = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo',
          messages: [
            {
              role: 'system',
              content: `あなたはモロッコ旅行の専門ガイドです。モロッコの観光地、文化、歴史、料理、言語、習慣、エチケット、交通、宿泊、買い物などについて、詳しく丁寧に日本語で回答してください。
              
              回答の特徴：
              - 親しみやすく、実用的な情報を提供
              - 具体的な場所名、料理名、文化的背景を含める
              - 安全な旅行のためのアドバイスも含める
              - 適切に絵文字を使用して読みやすくする
              - 日本人旅行者の視点で回答する`
            },
            {
              role: 'user',
              content: userInput
            }
          ],
          max_tokens: 500,
          temperature: 0.7
        })
      })

      const data = await response.json()
      
      if (data.error) {
        return `エラーが発生しました: ${data.error.message}`
      }
      
      return data.choices[0]?.message?.content || "申し訳ございませんが、回答を生成できませんでした。"
    } catch (error) {
      console.error('OpenAI API Error:', error)
      return "ネットワークエラーが発生しました。インターネット接続を確認してください。"
    }
  }

  // メッセージ送信処理
  const handleSendMessage = async () => {
    if (!inputText.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      const aiResponse = await getAIResponse(inputText)
      
      // タイピングエフェクトのシミュレーション
      setIsTyping(true)
      setTimeout(() => {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: aiResponse,
          isUser: false,
          timestamp: new Date()
        }
        setMessages(prev => [...prev, aiMessage])
        setIsTyping(false)
        setIsLoading(false)
      }, 1000)
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "申し訳ございませんが、エラーが発生しました。もう一度お試しください。",
        isUser: false,
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      setIsTyping(false)
      setIsLoading(false)
    }
  }
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