import { useState } from 'react'
import { useTranslation } from 'react-i18next'
import SpeechControls from '../components/SpeechControls'
import { speakText, languageSettings, speakArabic, speakMoroccanArabic } from '../utils/speechUtils'

const Translator = () => {
  const { t } = useTranslation()
  const [sourceText, setSourceText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [sourceLang, setSourceLang] = useState('ja')
  const [targetLang, setTargetLang] = useState('en')
  const [isTranslating, setIsTranslating] = useState(false)

  const languages = [
    { code: 'ja', name: t('languages.japanese'), flag: '🇯🇵' },
    { code: 'en', name: t('languages.english'), flag: '🇬🇧' },
    { code: 'fr', name: t('languages.french'), flag: '🇫🇷' },
    { code: 'ar', name: t('languages.arabic'), flag: '🇲🇦' },
    { code: 'ber', name: t('languages.berber'), flag: '🏔️' },
  ]

  // Simple mock translation function
  const translateText = async () => {
    if (!sourceText.trim()) return

    setIsTranslating(true)
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock translation - in a real app, you would call a translation API
    const mockTranslations: { [key: string]: { [key: string]: string } } = {
      'hello': {
        'ja': 'こんにちは',
        'ar': 'مرحبا',
        'fr': 'bonjour',
        'ber': 'azul',
        'en': 'hello'
      },
      'thank you': {
        'ja': 'ありがとう',
        'ar': 'شكراً لك',
        'fr': 'merci',
        'ber': 'tanmirt',
        'en': 'thank you'
      },
      'welcome to morocco': {
        'ja': 'モロッコへようこそ',
        'ar': 'مرحباً بكم في المغرب',
        'fr': 'bienvenue au maroc',
        'ber': 'anṛḥeb s lmeɣrib',
        'en': 'welcome to morocco'
      },
      'こんにちは': {
        'en': 'hello',
        'ar': 'مرحبا',
        'fr': 'bonjour',
        'ber': 'azul'
      },
      'ありがとう': {
        'en': 'thank you',
        'ar': 'شكراً لك',
        'fr': 'merci',
        'ber': 'tanmirt'
      },
      'モロッコへようこそ': {
        'en': 'welcome to morocco',
        'ar': 'مرحباً بكم في المغرب',
        'fr': 'bienvenue au maroc',
        'ber': 'anṛḥeb s lmeɣrib'
      },
      'どこですか？': {
        'en': 'where is',
        'ar': 'أين',
        'fr': 'où est',
        'ber': 'anda'
      },
      'いくらですか？': {
        'en': 'how much does it cost',
        'ar': 'كم الثمن',
        'fr': 'combien ça coûte',
        'ber': 'mnšḥal'
      },
      '助けて': {
        'en': 'help',
        'ar': 'مساعدة',
        'fr': 'aide',
        'ber': 'ɛawn'
      }
    }

    const lowercaseText = sourceText.toLowerCase()
    const translation = mockTranslations[lowercaseText]?.[targetLang] || 
                       `[翻訳: ${sourceText}]`
    
    setTranslatedText(translation)
    setIsTranslating(false)
  }

  const swapLanguages = () => {
    setSourceLang(targetLang)
    setTargetLang(sourceLang)
    setSourceText(translatedText)
    setTranslatedText(sourceText)
  }

  const speakPhrase = async (text: string, language: string) => {
    try {
      console.log(`フレーズ音声再生: "${text}" (言語: ${language})`);
      
      // アラビア語の場合は専用関数を使用
      if (language === 'ar') {
        console.log('アラビア語専用関数を使用');
        await speakArabic(text);
        return;
      }
      
      // モロッコアラビア語（ベルベル語代替）の場合
      if (language === 'ber') {
        console.log('モロッコアラビア語専用関数を使用');
        await speakMoroccanArabic(text);
        return;
      }
      
      // その他の言語は従来通り
      const langSettings = languageSettings[language as keyof typeof languageSettings];
      if (langSettings) {
        console.log(`標準音声関数を使用: ${langSettings.code}`);
        await speakText(text, {
          lang: langSettings.code,
          rate: langSettings.rate,
          pitch: langSettings.pitch,
          volume: 1.0
        });
      }
    } catch (error) {
      console.error('音声再生エラー:', error);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">{t('translator.title')}</h1>
          <p className="mt-2 text-gray-600">
            アラビア語、フランス語、ベルベル語、英語、日本語間で簡単に翻訳できます
          </p>
          <div className="mt-4 p-4 bg-blue-50 rounded-lg">
            <p className="text-sm text-blue-800">
              💡 <strong>使い方:</strong> 翻訳したいテキストを入力して「翻訳する」ボタンを押してください。
              よく使うフレーズは下のボタンから選択できます。
            </p>
            <p className="text-sm text-blue-700 mt-2">
              🎤 <strong>音声機能:</strong> 
              <span className="inline-flex items-center mx-1">
                <svg className="w-3 h-3 text-blue-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.816L4.88 14H2a1 1 0 01-1-1V7a1 1 0 011-1h2.88l3.503-2.816a1 1 0 011.617.816zM8 5.04L5.953 6.71A1 1 0 015.382 7H3v6h2.382a1 1 0 01.571.29L8 14.96V5.04z" clipRule="evenodd" />
                </svg>
                読み上げ
              </span>
              <span className="inline-flex items-center mx-1">
                <svg className="w-3 h-3 text-green-500 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                </svg>
                音声入力
              </span>
              で簡単に操作できます。
            </p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6">
          {/* Language Selection */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('translator.selectSource')}
              </label>
              <select
                value={sourceLang}
                onChange={(e) => setSourceLang(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-morocco-red focus:border-morocco-red"
              >
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <button
              onClick={swapLanguages}
              className="mx-4 p-2 text-morocco-red hover:bg-gray-100 rounded-full transition-colors"
              title={t('translator.swap')}
            >
              🔄
            </button>

            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {t('translator.selectTarget')}
              </label>
              <select
                value={targetLang}
                onChange={(e) => setTargetLang(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-morocco-red focus:border-morocco-red"
              >
                {languages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.flag} {lang.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Translation Interface */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-gray-700">
                  入力テキスト
                </label>
                <SpeechControls
                  text={sourceText}
                  language={sourceLang}
                  onSpeechResult={(text) => setSourceText(text)}
                  className="scale-90"
                />
              </div>
              <textarea
                value={sourceText}
                onChange={(e) => setSourceText(e.target.value)}
                placeholder={t('translator.enterText')}
                className="w-full h-40 p-4 border border-gray-300 rounded-md resize-none focus:ring-morocco-red focus:border-morocco-red"
                dir={sourceLang === 'ar' ? 'rtl' : 'ltr'}
              />
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-medium text-gray-700">
                  翻訳結果
                </label>
                <SpeechControls
                  text={translatedText}
                  language={targetLang}
                  className="scale-90"
                />
              </div>
              <textarea
                value={translatedText}
                readOnly
                placeholder="翻訳結果がここに表示されます..."
                className="w-full h-40 p-4 bg-gray-50 border border-gray-300 rounded-md resize-none"
                dir={targetLang === 'ar' ? 'rtl' : 'ltr'}
              />
            </div>
          </div>

          {/* Translate Button */}
          <div className="mt-6 text-center">
            <button
              onClick={translateText}
              disabled={!sourceText.trim() || isTranslating}
              className="px-8 py-3 bg-morocco-red text-white rounded-md hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isTranslating ? '翻訳中...' : t('translator.translate')}
            </button>
          </div>

          {/* Common Phrases by Situation */}
          <div className="mt-8">
            <h3 className="text-lg font-medium text-gray-900 mb-4">シチュエーション別フレーズ</h3>
            <p className="text-sm text-gray-600 mb-6">クリックして入力欄に挿入できます</p>
            
            {/* 基本的な挨拶 */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">👋</span>基本的な挨拶
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'hello', japanese: 'こんにちは', arabic: 'مرحبا (マルハバン)' },
                  { phrase: 'good morning', japanese: 'おはようございます', arabic: 'صباح الخير (サバーハ・ル・ハイル)' },
                  { phrase: 'good evening', japanese: 'こんばんは', arabic: 'مساء الخير (マサー・ル・ハイル)' },
                  { phrase: 'goodbye', japanese: 'さようなら', arabic: 'مع السلامة (マア・ッサラーマ)' },
                  { phrase: 'see you later', japanese: 'また後で', arabic: 'أراك لاحقا (アラーカ・ラーヒカン)' },
                  { phrase: 'nice to meet you', japanese: 'はじめまして', arabic: 'تشرفنا (タシャッラフナー)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 感謝とお詫び */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🙏</span>感謝とお詫び
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'thank you', japanese: 'ありがとう', arabic: 'شكرا (シュクラン)' },
                  { phrase: 'thank you very much', japanese: 'どうもありがとう', arabic: 'شكرا جزيلا (シュクラン・ジャジーラン)' },
                  { phrase: 'you are welcome', japanese: 'どういたしまして', arabic: 'عفوا (アフワン)' },
                  { phrase: 'excuse me', japanese: 'すみません', arabic: 'عذرا (ウズラン)' },
                  { phrase: 'I am sorry', japanese: '申し訳ありません', arabic: 'أنا آسف (アナー・アーシフ)' },
                  { phrase: 'no problem', japanese: '問題ありません', arabic: 'لا مشكلة (ラー・ムシュキラ)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 道案内・交通 */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🗺️</span>道案内・交通
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'where is', japanese: 'どこですか？', arabic: 'أين (アイン)' },
                  { phrase: 'how much does it cost', japanese: 'いくらですか？', arabic: 'كم الثمن (カム・アッタマン)' },
                  { phrase: 'can you help me', japanese: '手伝ってください', arabic: 'هل يمكنك مساعدتي (ハル・ユムキヌカ・ムサーアダティー)' },
                  { phrase: 'I am lost', japanese: '道に迷いました', arabic: 'لقد ضعت (ラカド・ダーアト)' },
                  { phrase: 'taxi', japanese: 'タクシー', arabic: 'تاكسي (タクシー)' },
                  { phrase: 'bus station', japanese: 'バス停', arabic: 'محطة الحافلات (マハッタ・アル・ハーフィラート)' },
                  { phrase: 'train station', japanese: '駅', arabic: 'محطة القطار (マハッタ・アル・キタール)' },
                  { phrase: 'airport', japanese: '空港', arabic: 'مطار (マタール)' },
                  { phrase: 'hotel', japanese: 'ホテル', arabic: 'فندق (ファンダク)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* レストラン・食事 */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🍽️</span>レストラン・食事
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'I would like', japanese: '〜をください', arabic: 'أريد (ウリード)' },
                  { phrase: 'menu please', japanese: 'メニューをお願いします', arabic: 'القائمة من فضلك (アル・カーイマ・ミン・ファドリク)' },
                  { phrase: 'water', japanese: '水', arabic: 'ماء (マー)' },
                  { phrase: 'tea', japanese: 'お茶', arabic: 'شاي (シャーイ)' },
                  { phrase: 'coffee', japanese: 'コーヒー', arabic: 'قهوة (カフワ)' },
                  { phrase: 'tagine', japanese: 'タジン', arabic: 'طاجين (タージン)' },
                  { phrase: 'couscous', japanese: 'クスクス', arabic: 'كسكس (クスクス)' },
                  { phrase: 'the bill please', japanese: 'お会計をお願いします', arabic: 'الفاتورة من فضلك (アル・ファートゥーラ・ミン・ファドリク)' },
                  { phrase: 'delicious', japanese: 'おいしい', arabic: 'لذيذ (ラジーズ)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* ショッピング */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🛒</span>ショッピング
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'how much', japanese: 'いくら？', arabic: 'بكم (ビカム)' },
                  { phrase: 'too expensive', japanese: '高すぎます', arabic: 'غالي جدا (ガーリー・ジッダン)' },
                  { phrase: 'can you lower the price', japanese: '値下げできますか？', arabic: 'هل يمكن تخفيض السعر (ハル・ユムキン・タクフィード・アッスィアル)' },
                  { phrase: 'I will buy', japanese: '買います', arabic: 'سأشتري (サアシュタリー)' },
                  { phrase: 'I am just looking', japanese: '見ているだけです', arabic: 'أنظر فقط (アンズル・ファカト)' },
                  { phrase: 'market', japanese: '市場', arabic: 'سوق (スーク)' },
                  { phrase: 'shop', japanese: '店', arabic: 'محل (マハル)' },
                  { phrase: 'souvenir', japanese: 'お土産', arabic: 'تذكار (タズカール)' },
                  { phrase: 'beautiful', japanese: '美しい', arabic: 'جميل (ジャミール)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 緊急時 */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🚨</span>緊急時
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'help', japanese: '助けて', arabic: 'مساعدة (ムサーアダ)' },
                  { phrase: 'police', japanese: '警察', arabic: 'شرطة (シュルタ)' },
                  { phrase: 'hospital', japanese: '病院', arabic: 'مستشفى (ムスタシュファー)' },
                  { phrase: 'doctor', japanese: '医者', arabic: 'طبيب (タビーブ)' },
                  { phrase: 'pharmacy', japanese: '薬局', arabic: 'صيدلية (サイダリーヤ)' },
                  { phrase: 'I need help', japanese: '助けが必要です', arabic: 'أحتاج مساعدة (アフタージュ・ムサーアダ)' },
                  { phrase: 'call the police', japanese: '警察を呼んで', arabic: 'اتصل بالشرطة (イッタスィル・ビッシュルタ)' },
                  { phrase: 'I am sick', japanese: '病気です', arabic: 'أنا مريض (アナー・マリード)' },
                  { phrase: 'emergency', japanese: '緊急事態', arabic: 'طوارئ (タワーリ)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* 数字と時間 */}
            <div className="mb-8">
              <h4 className="text-md font-semibold text-morocco-red mb-3 flex items-center">
                <span className="mr-2">🔢</span>数字と時間
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                {[
                  { phrase: 'one', japanese: '1', arabic: 'واحد (ワーヒド)' },
                  { phrase: 'two', japanese: '2', arabic: 'اثنان (イスナーン)' },
                  { phrase: 'three', japanese: '3', arabic: 'ثلاثة (サラーサ)' },
                  { phrase: 'four', japanese: '4', arabic: 'أربعة (アルバア)' },
                  { phrase: 'five', japanese: '5', arabic: 'خمسة (ハムサ)' },
                  { phrase: 'what time is it', japanese: '何時ですか？', arabic: 'كم الساعة (カム・アッサーア)' },
                  { phrase: 'today', japanese: '今日', arabic: 'اليوم (アル・ヤウム)' },
                  { phrase: 'tomorrow', japanese: '明日', arabic: 'غدا (ガダン)' },
                  { phrase: 'yesterday', japanese: '昨日', arabic: 'أمس (アムス)' }
                ].map((item) => (
                  <div
                    key={item.phrase}
                    className="p-3 bg-gray-50 hover:bg-gray-100 rounded-md transition-colors border border-gray-200 group"
                  >
                    <div className="flex justify-between items-start">
                      <button
                        onClick={() => setSourceText(item.japanese)}
                        className="flex-1 text-left"
                      >
                        <div className="font-medium text-gray-900">{item.japanese}</div>
                        <div className="text-xs text-gray-500 mt-1">{item.phrase}</div>
                        <div className="text-xs text-morocco-gold mt-1">{item.arabic}</div>
                      </button>
                      <div className="flex flex-col space-y-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button
                          onClick={() => speakPhrase(item.phrase, 'en')}
                          className="p-1 text-blue-500 hover:bg-blue-100 rounded text-xs"
                          title="英語で再生"
                        >
                          🔊
                        </button>
                        <button
                          onClick={() => speakPhrase(item.japanese, 'ja')}
                          className="p-1 text-green-500 hover:bg-green-100 rounded text-xs"
                          title="日本語で再生"
                        >
                          🎌
                        </button>
                        <button
                          onClick={() => speakPhrase(item.arabic.split(' (')[0], 'ar')}
                          className="p-1 text-orange-500 hover:bg-orange-100 rounded text-xs"
                          title="アラビア語で再生"
                        >
                          🕌
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Translator