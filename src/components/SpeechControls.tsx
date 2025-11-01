import React, { useState, useEffect } from 'react';
import { speakText, recognizeSpeech, isSpeechSynthesisSupported, isSpeechRecognitionSupported, stopSpeech, languageSettings, logAvailableVoices } from '../utils/speechUtils';

interface SpeechControlsProps {
  text: string;
  language: string;
  onSpeechResult?: (text: string) => void;
  className?: string;
}

const SpeechControls: React.FC<SpeechControlsProps> = ({
  text,
  language,
  onSpeechResult,
  className = ''
}) => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [speechSupported, setSpeechSupported] = useState(false);
  const [recognitionSupported, setRecognitionSupported] = useState(false);

  useEffect(() => {
    setSpeechSupported(isSpeechSynthesisSupported());
    setRecognitionSupported(isSpeechRecognitionSupported());
  }, []);

  const handleSpeak = async () => {
    if (!text.trim()) return;

    try {
      setError(null);
      setIsSpeaking(true);
      
      // デバッグ: 利用可能な音声を表示
      if (language === 'ar') {
        console.log('アラビア語音声再生を試行中...');
        logAvailableVoices();
      }
      
      const langSettings = languageSettings[language as keyof typeof languageSettings];
      if (!langSettings) {
        throw new Error('対応していない言語です');
      }

      console.log(`音声再生: "${text}" (言語: ${language}, コード: ${langSettings.code})`);
      
      await speakText(text, {
        lang: langSettings.code,
        rate: langSettings.rate,
        pitch: langSettings.pitch,
        volume: 1.0
      });
    } catch (err) {
      console.error('音声再生エラー:', err);
      setError(err instanceof Error ? err.message : '音声合成エラー');
    } finally {
      setIsSpeaking(false);
    }
  };

  const handleStopSpeaking = () => {
    stopSpeech();
    setIsSpeaking(false);
  };

  const handleListen = async () => {
    try {
      setError(null);
      setIsListening(true);
      
      const langSettings = languageSettings[language as keyof typeof languageSettings];
      if (!langSettings) {
        throw new Error('対応していない言語です');
      }

      const result = await recognizeSpeech({
        lang: langSettings.code,
        continuous: false,
        interimResults: false
      });

      if (result && onSpeechResult) {
        onSpeechResult(result);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : '音声認識エラー');
    } finally {
      setIsListening(false);
    }
  };

  const handleStopListening = () => {
    setIsListening(false);
  };

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* 音声読み上げボタン */}
      {speechSupported && (
        <div className="flex items-center space-x-1">
          {!isSpeaking ? (
            <button
              onClick={handleSpeak}
              disabled={!text.trim()}
              className="p-2 rounded-full bg-blue-500 hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white transition-colors"
              title="音声で読み上げ"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.617.816L4.88 14H2a1 1 0 01-1-1V7a1 1 0 011-1h2.88l3.503-2.816a1 1 0 011.617.816zM8 5.04L5.953 6.71A1 1 0 015.382 7H3v6h2.382a1 1 0 01.571.29L8 14.96V5.04z" clipRule="evenodd" />
                <path fillRule="evenodd" d="M12.707 4.293a1 1 0 010 1.414L11.414 7l1.293 1.293a1 1 0 01-1.414 1.414L10 8.414l-1.293 1.293a1 1 0 01-1.414-1.414L8.586 7 7.293 5.707a1 1 0 011.414-1.414L10 5.586l1.293-1.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
            </button>
          ) : (
            <button
              onClick={handleStopSpeaking}
              className="p-2 rounded-full bg-red-500 hover:bg-red-600 text-white transition-colors animate-pulse"
              title="読み上げ停止"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" />
              </svg>
            </button>
          )}
        </div>
      )}

      {/* 音声入力ボタン */}
      {recognitionSupported && onSpeechResult && (
        <div className="flex items-center space-x-1">
          {!isListening ? (
            <button
              onClick={handleListen}
              className="p-2 rounded-full bg-green-500 hover:bg-green-600 text-white transition-colors"
              title="音声で入力"
            >
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
              </svg>
            </button>
          ) : (
            <button
              onClick={handleStopListening}
              className="p-2 rounded-full bg-red-500 hover:bg-red-600 text-white transition-colors animate-pulse"
              title="録音停止"
            >
              <div className="w-4 h-4 flex items-center justify-center">
                <div className="w-2 h-2 bg-white rounded-full animate-ping"></div>
              </div>
            </button>
          )}
        </div>
      )}

      {/* エラー表示 */}
      {error && (
        <div className="text-xs text-red-500 bg-red-50 px-2 py-1 rounded max-w-xs">
          {error}
        </div>
      )}

      {/* 対応状況の表示 */}
      {!speechSupported && !recognitionSupported && (
        <div className="text-xs text-gray-500">
          音声機能は対応していません
        </div>
      )}
    </div>
  );
};

export default SpeechControls;