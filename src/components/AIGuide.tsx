import React, { useState, useEffect, useRef } from 'react'

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

const AIGuide: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // 初期メッセージ
  useEffect(() => {
    const welcomeMessage: Message = {
      id: '1',
      text: 'こんにちは！モロッコAIガイドです。OpenAI GPT-3.5を使用して、モロッコの観光地、文化、料理、エチケットなど、何でもお気軽にお尋ねください。🇲🇦',
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

  // Python バックエンドのAI APIを使用した応答の取得
  const getAIResponse = async (userInput: string): Promise<string> => {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userInput
        })
      })

      const data = await response.json()
      
      if (!response.ok) {
        return `エラーが発生しました: ${data.error || 'サーバーエラー'}`
      }
      
      return data.response || "申し訳ございませんが、回答を生成できませんでした。"
    } catch (error) {
      console.error('API Error:', error)
      return "ネットワークエラーが発生しました。サーバーとの接続を確認してください。"
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

  // Enterキーでメッセージ送信
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-lg">
      <div className="bg-morocco-red text-white p-4 rounded-t-lg">
        <h2 className="text-xl font-bold">🤖 モロッコAIガイド</h2>
        <p className="text-sm opacity-90">モロッコ旅行の専門ガイドです (Python + OpenAI GPT-3.5)</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                message.isUser
                  ? 'bg-morocco-green text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.text}</p>
              <p className="text-xs opacity-70 mt-1">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg max-w-xs">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="border-t p-4">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="モロッコについて何でもお聞きください..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-morocco-red"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputText.trim() || isLoading}
            className="bg-morocco-red text-white px-4 py-2 rounded-lg hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-morocco-red disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isLoading ? '📡' : '送信'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default AIGuide