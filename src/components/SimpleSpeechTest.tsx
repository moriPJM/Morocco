import React, { useState } from 'react';
import { speakArabic, speakMoroccanArabic, speakText, logAvailableVoices } from '../utils/speechUtils';

const SimpleSpeechTest: React.FC = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [lastError, setLastError] = useState<string>('');
  const [testResult, setTestResult] = useState<string>('');

  const testBasicSpeech = async () => {
    setIsPlaying(true);
    setLastError('');
    setTestResult('');
    
    try {
      console.log('🔊 基本音声テスト開始');
      
      // ブラウザサポートチェック
      if (!('speechSynthesis' in window)) {
        throw new Error('このブラウザは音声合成をサポートしていません');
      }
      
      console.log('✅ speechSynthesis API利用可能');
      
      // 音声リストを取得
      const voices = window.speechSynthesis.getVoices();
      console.log(`📋 利用可能音声数: ${voices.length}`);
      
      if (voices.length === 0) {
        // 音声リストが空の場合は少し待ってから再試行
        console.log('⏳ 音声リスト読み込み待機中...');
        await new Promise(resolve => {
          window.speechSynthesis.onvoiceschanged = () => {
            resolve(void 0);
          };
          // 3秒でタイムアウト
          setTimeout(resolve, 3000);
        });
        
        const voicesAfterWait = window.speechSynthesis.getVoices();
        console.log(`📋 再取得後音声数: ${voicesAfterWait.length}`);
      }
      
      // 簡単な日本語テスト
      console.log('🎯 日本語テスト開始');
      const utterance = new SpeechSynthesisUtterance('こんにちは');
      utterance.lang = 'ja-JP';
      utterance.rate = 1.0;
      utterance.volume = 1.0;
      
      utterance.onstart = () => {
        console.log('▶️ 音声再生開始');
        setTestResult('日本語音声再生中...');
      };
      
      utterance.onend = () => {
        console.log('✅ 日本語音声再生完了');
        setTestResult('日本語音声再生完了 - ブラウザ音声機能は正常');
        setIsPlaying(false);
      };
      
      utterance.onerror = (event) => {
        console.error('❌ 音声エラー:', event.error);
        setLastError(`音声エラー: ${event.error}`);
        setIsPlaying(false);
      };
      
      window.speechSynthesis.speak(utterance);
      
    } catch (error) {
      console.error('❌ テストエラー:', error);
      setLastError(error instanceof Error ? error.message : '不明なエラー');
      setIsPlaying(false);
    }
  };

  const testArabicSpeech = async () => {
    setIsPlaying(true);
    setLastError('');
    setTestResult('');
    
    try {
      console.log('🔊 アラビア語音声テスト開始');
      
      const arabicText = 'مرحبا';
      console.log(`🎯 テストテキスト: ${arabicText}`);
      
      setTestResult('アラビア語音声準備中...');
      
      await speakArabic(arabicText);
      
      setTestResult('アラビア語音声再生完了');
      setIsPlaying(false);
      
    } catch (error) {
      console.error('❌ アラビア語音声エラー:', error);
      setLastError(error instanceof Error ? error.message : '不明なエラー');
      setIsPlaying(false);
    }
  };

  const showVoicesInfo = () => {
    console.log('📋 音声情報表示開始');
    logAvailableVoices();
    
    const voices = window.speechSynthesis.getVoices();
    const arabicVoices = voices.filter(v => v.lang.includes('ar'));
    
    setTestResult(`総音声数: ${voices.length}, アラビア語音声: ${arabicVoices.length}`);
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-center">🔊 シンプル音声テスト</h2>
      
      <div className="space-y-4">
        <button
          onClick={testBasicSpeech}
          disabled={isPlaying}
          className="w-full px-4 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPlaying ? '再生中...' : '1. 基本音声テスト（日本語）'}
        </button>
        
        <button
          onClick={testArabicSpeech}
          disabled={isPlaying}
          className="w-full px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isPlaying ? '再生中...' : '2. アラビア語音声テスト'}
        </button>
        
        <button
          onClick={showVoicesInfo}
          disabled={isPlaying}
          className="w-full px-4 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          3. 利用可能音声を確認
        </button>
      </div>
      
      {testResult && (
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-800">テスト結果:</h3>
          <p className="text-blue-700">{testResult}</p>
        </div>
      )}
      
      {lastError && (
        <div className="mt-4 p-3 bg-red-50 rounded-lg">
          <h3 className="font-semibold text-red-800">エラー:</h3>
          <p className="text-red-700">{lastError}</p>
        </div>
      )}
      
      <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
        <h3 className="font-semibold text-yellow-800">💡 トラブルシューティング:</h3>
        <ul className="text-sm text-yellow-700 mt-2 space-y-1">
          <li>• ブラウザの音量がオンになっているか確認</li>
          <li>• ヘッドホンやスピーカーが接続されているか確認</li>
          <li>• ブラウザの設定で音声が許可されているか確認</li>
          <li>• 開発者ツール（F12）のコンソールで詳細ログを確認</li>
          <li>• Chrome/Edgeでは最も多くの音声がサポートされています</li>
        </ul>
      </div>
    </div>
  );
};

export default SimpleSpeechTest;