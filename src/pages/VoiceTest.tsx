import React from 'react';
import VoiceDebugger from '../components/VoiceDebugger';
import SimpleSpeechTest from '../components/SimpleSpeechTest';
import InstantSpeechTest from '../components/InstantSpeechTest';
import EnhancedSpeechTest from '../components/EnhancedSpeechTest';
import ArabicVoiceInstallGuide from '../components/ArabicVoiceInstallGuide';

const VoiceTest: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">音声テストページ</h1>
          <p className="mt-2 text-gray-600">
            強化されたアラビア語音声機能のテストと診断
          </p>
        </div>
        
        {/* 強化されたシステム */}
        <div className="mb-8">
          <EnhancedSpeechTest />
        </div>
        
        {/* 即座テスト */}
        <InstantSpeechTest />
        
        {/* シンプルテスト */}
        <div className="mb-8">
          <SimpleSpeechTest />
        </div>
        
        {/* インストールガイド */}
        <div className="mb-8">
          <ArabicVoiceInstallGuide />
        </div>
        
        {/* 詳細デバッガー */}
        <VoiceDebugger />
        
        {/* 簡単なアラビア語フレーズテスト */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-bold mb-4">よく使うアラビア語フレーズ</h2>
          <div className="grid gap-4">
            {[
              { ar: 'مرحبا', ja: 'こんにちは', en: 'Hello' },
              { ar: 'شكراً لك', ja: 'ありがとう', en: 'Thank you' },
              { ar: 'مرحباً بكم في المغرب', ja: 'モロッコへようこそ', en: 'Welcome to Morocco' },
              { ar: 'كيف حالك؟', ja: 'お元気ですか？', en: 'How are you?' },
              { ar: 'أين المطعم؟', ja: 'レストランはどこですか？', en: 'Where is the restaurant?' },
              { ar: 'أحتاج مساعدة', ja: '助けが必要です', en: 'I need help' }
            ].map((phrase, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div className="flex-1">
                  <p className="text-lg font-arabic" dir="rtl">{phrase.ar}</p>
                  <p className="text-sm text-gray-600">{phrase.ja}</p>
                  <p className="text-xs text-gray-500">{phrase.en}</p>
                </div>
                <button 
                  onClick={() => {
                    const utterance = new SpeechSynthesisUtterance(phrase.ar);
                    utterance.lang = 'ar-SA';
                    utterance.rate = 0.8;
                    window.speechSynthesis.speak(utterance);
                  }}
                  className="ml-4 px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
                >
                  🔊 再生
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default VoiceTest;