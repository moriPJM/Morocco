import React, { useState, useEffect } from 'react';
import { logAvailableVoices, speakArabic, speakMoroccanArabic, speakText } from '../utils/speechUtils';

const VoiceDebugger: React.FC = () => {
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  const [selectedVoice, setSelectedVoice] = useState<string>('');
  const [testText, setTestText] = useState('مرحبا بكم في المغرب');
  const [isSpeaking, setIsSpeaking] = useState(false);

  useEffect(() => {
    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices();
      setVoices(availableVoices);
      logAvailableVoices();
    };

    // 音声リストが既に読み込まれている場合
    if (window.speechSynthesis.getVoices().length > 0) {
      loadVoices();
    } else {
      // 音声リストの読み込みを待つ
      window.speechSynthesis.onvoiceschanged = loadVoices;
    }
  }, []);

  const arabicVoices = voices.filter(voice => 
    voice.lang.includes('ar') || voice.name.toLowerCase().includes('arab')
  );

  const testArabicSpeech = async (method: 'standard' | 'arabic' | 'moroccan' | 'custom') => {
    setIsSpeaking(true);
    try {
      switch (method) {
        case 'standard':
          await speakText(testText, { lang: 'ar-SA', rate: 0.8 });
          break;
        case 'arabic':
          await speakArabic(testText);
          break;
        case 'moroccan':
          await speakMoroccanArabic(testText);
          break;
        case 'custom':
          if (selectedVoice) {
            const voice = voices.find(v => v.name === selectedVoice);
            const utterance = new SpeechSynthesisUtterance(testText);
            if (voice) utterance.voice = voice;
            utterance.rate = 0.8;
            window.speechSynthesis.speak(utterance);
          }
          break;
      }
    } catch (error) {
      console.error('音声テストエラー:', error);
    } finally {
      setIsSpeaking(false);
    }
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-gray-800">
        🔊 アラビア語音声デバッグツール
      </h2>
      
      {/* テストテキスト入力 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          テストテキスト（アラビア語）:
        </label>
        <input
          type="text"
          value={testText}
          onChange={(e) => setTestText(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
          placeholder="مرحبا بكم في المغرب"
          dir="rtl"
        />
      </div>

      {/* 利用可能な音声情報 */}
      <div className="mb-4">
        <h3 className="text-lg font-semibold mb-2">利用可能な音声情報:</h3>
        <div className="bg-gray-100 p-3 rounded text-sm">
          <p><strong>総音声数:</strong> {voices.length}</p>
          <p><strong>アラビア語音声数:</strong> {arabicVoices.length}</p>
          {arabicVoices.length > 0 && (
            <div className="mt-2">
              <p><strong>アラビア語音声一覧:</strong></p>
              <ul className="list-disc list-inside mt-1">
                {arabicVoices.map((voice, index) => (
                  <li key={index}>
                    {voice.name} ({voice.lang}) {voice.default ? '- デフォルト' : ''}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* 音声選択 */}
      {arabicVoices.length > 0 && (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            音声を選択:
          </label>
          <select
            value={selectedVoice}
            onChange={(e) => setSelectedVoice(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="">選択してください</option>
            {arabicVoices.map((voice, index) => (
              <option key={index} value={voice.name}>
                {voice.name} ({voice.lang})
              </option>
            ))}
          </select>
        </div>
      )}

      {/* テストボタン */}
      <div className="space-y-2">
        <h3 className="text-lg font-semibold">音声テスト:</h3>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => testArabicSpeech('standard')}
            disabled={isSpeaking}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            標準アラビア語 (ar-SA)
          </button>
          
          <button
            onClick={() => testArabicSpeech('arabic')}
            disabled={isSpeaking}
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 disabled:opacity-50"
          >
            speakArabic関数
          </button>
          
          <button
            onClick={() => testArabicSpeech('moroccan')}
            disabled={isSpeaking}
            className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 disabled:opacity-50"
          >
            モロッコアラビア語
          </button>
          
          {arabicVoices.length > 0 && (
            <button
              onClick={() => testArabicSpeech('custom')}
              disabled={isSpeaking || !selectedVoice}
              className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600 disabled:opacity-50"
            >
              選択した音声
            </button>
          )}
        </div>
      </div>

      {/* ブラウザ互換性情報 */}
      <div className="mt-4 p-3 bg-yellow-50 rounded">
        <h4 className="font-semibold text-yellow-800">ブラウザ互換性:</h4>
        <ul className="text-sm text-yellow-700 mt-1 space-y-1">
          <li>✅ Speech Synthesis API: {('speechSynthesis' in window) ? 'サポート' : '非サポート'}</li>
          <li>🌐 現在のブラウザ: {navigator.userAgent.includes('Chrome') ? 'Chrome' : 
                                navigator.userAgent.includes('Firefox') ? 'Firefox' : 
                                navigator.userAgent.includes('Safari') ? 'Safari' : 'その他'}</li>
          <li>💡 アラビア語音声は OS やブラウザによって利用可否が異なります</li>
          <li>💡 Windows: Microsoft Speech Platform で追加可能</li>
          <li>💡 macOS: システム環境設定 &gt; アクセシビリティ &gt; スピーチで追加可能</li>
        </ul>
      </div>

      {isSpeaking && (
        <div className="mt-4 p-3 bg-blue-50 rounded">
          <p className="text-blue-800">🔊 音声を再生中...</p>
        </div>
      )}
    </div>
  );
};

export default VoiceDebugger;