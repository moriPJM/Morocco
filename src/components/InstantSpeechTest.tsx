import React from 'react';

const InstantSpeechTest: React.FC = () => {
  const testInstantSpeech = () => {
    console.log('🔊 即座音声テスト開始');
    
    // 最もシンプルな音声テスト
    const utterance = new SpeechSynthesisUtterance('テスト');
    utterance.onstart = () => console.log('▶️ 音声開始');
    utterance.onend = () => console.log('✅ 音声終了');
    utterance.onerror = (e) => console.error('❌ 音声エラー:', e);
    
    window.speechSynthesis.speak(utterance);
  };

  const testArabicInstant = () => {
    console.log('🔊 アラビア語即座テスト開始');
    
    const utterance = new SpeechSynthesisUtterance('مرحبا');
    utterance.lang = 'ar-SA';
    utterance.rate = 0.8;
    utterance.onstart = () => console.log('▶️ アラビア語音声開始');
    utterance.onend = () => console.log('✅ アラビア語音声終了');
    utterance.onerror = (e) => console.error('❌ アラビア語音声エラー:', e);
    
    window.speechSynthesis.speak(utterance);
  };

  const stopAllSpeech = () => {
    console.log('⏹️ 全音声停止');
    window.speechSynthesis.cancel();
  };

  const checkBrowserSupport = () => {
    console.log('🔍 ブラウザサポート確認');
    console.log('speechSynthesis:', 'speechSynthesis' in window);
    console.log('User Agent:', navigator.userAgent);
    console.log('Language:', navigator.language);
    
    if ('speechSynthesis' in window) {
      console.log('音声合成API利用可能');
      const voices = window.speechSynthesis.getVoices();
      console.log(`音声数: ${voices.length}`);
      
      if (voices.length === 0) {
        console.log('音声リスト空 - 再読み込み試行');
        window.speechSynthesis.onvoiceschanged = () => {
          const newVoices = window.speechSynthesis.getVoices();
          console.log(`再読み込み後音声数: ${newVoices.length}`);
        };
      }
    } else {
      console.error('音声合成APIサポートなし');
    }
  };

  return (
    <div className="p-4 bg-blue-50 rounded-lg mb-6">
      <h3 className="text-lg font-bold mb-4 text-blue-800">🚀 即座音声テスト</h3>
      <div className="grid grid-cols-2 gap-2 mb-4">
        <button
          onClick={testInstantSpeech}
          className="px-3 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
        >
          日本語テスト
        </button>
        
        <button
          onClick={testArabicInstant}
          className="px-3 py-2 bg-green-500 text-white rounded hover:bg-green-600 text-sm"
        >
          アラビア語テスト
        </button>
        
        <button
          onClick={stopAllSpeech}
          className="px-3 py-2 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
        >
          停止
        </button>
        
        <button
          onClick={checkBrowserSupport}
          className="px-3 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 text-sm"
        >
          ブラウザ確認
        </button>
      </div>
      
      <p className="text-xs text-blue-600">
        💡 ボタンをクリックしてコンソール（F12）でログを確認してください
      </p>
    </div>
  );
};

export default InstantSpeechTest;