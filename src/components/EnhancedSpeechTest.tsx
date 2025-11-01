import React, { useState, useEffect } from 'react';
import { speakArabicEnhanced, diagnoseSpeechSystem } from '../utils/enhancedSpeechUtils';
import { analyzeVoiceSystem, VoiceAnalysis } from '../utils/voiceAnalysis';

const EnhancedSpeechTest: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [analysis, setAnalysis] = useState<VoiceAnalysis | null>(null);
  const [testResult, setTestResult] = useState<string>('');
  const [error, setError] = useState<string>('');

  useEffect(() => {
    // コンポーネント読み込み時に分析実行
    performAnalysis();
  }, []);

  const performAnalysis = async () => {
    setIsLoading(true);
    try {
      const result = await analyzeVoiceSystem();
      setAnalysis(result);
      console.log('音声システム分析完了:', result);
    } catch (error) {
      setError('分析エラー: ' + (error instanceof Error ? error.message : '不明なエラー'));
    } finally {
      setIsLoading(false);
    }
  };

  const testEnhancedArabic = async () => {
    setIsLoading(true);
    setError('');
    setTestResult('');
    
    try {
      await diagnoseSpeechSystem();
      setTestResult('音声システム診断完了 - 詳細はコンソールを確認');
      
      await speakArabicEnhanced('مرحباً بكم في المغرب', {
        enableFallback: true,
        maxRetries: 3
      });
      
      setTestResult('✅ 強化アラビア語音声再生成功！');
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '不明なエラー';
      setError('音声再生エラー: ' + errorMsg);
      console.error('音声テストエラー:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const testWithFallback = async () => {
    setIsLoading(true);
    setError('');
    setTestResult('');
    
    try {
      await speakArabicEnhanced('مرحبا', {
        enableFallback: true,
        maxRetries: 1
      });
      
      setTestResult('✅ フォールバック機能付き再生成功！');
    } catch (error) {
      const errorMsg = error instanceof Error ? error.message : '不明なエラー';
      setError('フォールバック再生エラー: ' + errorMsg);
    } finally {
      setIsLoading(false);
    }
  };

  const renderAnalysis = () => {
    if (!analysis) return null;

    return (
      <div className="space-y-4">
        <div className="p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-800 mb-2">🔍 システム分析結果</h3>
          <div className="text-sm text-blue-700 space-y-1">
            <p><strong>ブラウザ:</strong> {analysis.browserInfo.name} {analysis.browserInfo.version}</p>
            <p><strong>プラットフォーム:</strong> {analysis.browserInfo.platform}</p>
            <p><strong>総音声数:</strong> {analysis.totalVoices}</p>
            <p><strong>アラビア語音声:</strong> {analysis.arabicVoices.length}個</p>
            <p><strong>アラビア語サポート:</strong> {analysis.hasArabicSupport ? '✅ あり' : '❌ なし'}</p>
          </div>
        </div>

        {analysis.arabicVoices.length > 0 && (
          <div className="p-4 bg-green-50 rounded-lg">
            <h4 className="font-semibold text-green-800 mb-2">🎵 利用可能アラビア語音声</h4>
            <div className="text-sm text-green-700 space-y-1">
              {analysis.arabicVoices.map((voice, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span>{voice.name}</span>
                  <span className="text-xs bg-green-200 px-2 py-1 rounded">{voice.lang}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="p-4 bg-yellow-50 rounded-lg">
          <h4 className="font-semibold text-yellow-800 mb-2">💡 推奨事項</h4>
          <ul className="text-sm text-yellow-700 space-y-1">
            {analysis.recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      </div>
    );
  };

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-gray-800">
        🚀 強化されたアラビア語音声システム
      </h2>
      
      <div className="space-y-4 mb-6">
        <button
          onClick={performAnalysis}
          disabled={isLoading}
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          {isLoading ? '分析中...' : '🔍 音声システム分析'}
        </button>
        
        <button
          onClick={testEnhancedArabic}
          disabled={isLoading}
          className="w-full px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50"
        >
          {isLoading ? 'テスト中...' : '🎵 強化アラビア語テスト'}
        </button>
        
        <button
          onClick={testWithFallback}
          disabled={isLoading}
          className="w-full px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 disabled:opacity-50"
        >
          {isLoading ? 'テスト中...' : '🔄 フォールバック付きテスト'}
        </button>
      </div>

      {testResult && (
        <div className="mb-4 p-3 bg-green-50 rounded-lg">
          <p className="text-green-800">{testResult}</p>
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-50 rounded-lg">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {renderAnalysis()}

      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-semibold text-gray-800 mb-2">📝 新機能説明</h3>
        <ul className="text-sm text-gray-700 space-y-1">
          <li>• <strong>自動リトライ:</strong> 失敗時に最大3回まで自動で再試行</li>
          <li>• <strong>フォールバック:</strong> アラビア語音声がない場合の代替手段</li>
          <li>• <strong>音声初期化:</strong> ブラウザ制限を回避する事前初期化</li>
          <li>• <strong>詳細分析:</strong> システム状況の包括的診断</li>
          <li>• <strong>最適選択:</strong> 利用可能な最良のアラビア語音声を自動選択</li>
        </ul>
      </div>
    </div>
  );
};

export default EnhancedSpeechTest;