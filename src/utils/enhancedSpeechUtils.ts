// 強化されたアラビア語音声再生システム
import { analyzeVoiceSystem, initializeSpeechContext } from './voiceAnalysis';

export interface EnhancedSpeechOptions {
  lang: string;
  rate?: number;
  pitch?: number;
  volume?: number;
  maxRetries?: number;
  fallbackLangs?: string[];
  enableFallback?: boolean;
}

// 音声コンテキストの状態管理
class SpeechManager {
  private isInitialized = false;
  private voicesLoaded = false;
  private initPromise: Promise<boolean> | null = null;

  async initialize(): Promise<boolean> {
    if (this.initPromise) {
      return this.initPromise;
    }

    this.initPromise = this.performInitialization();
    return this.initPromise;
  }

  private async performInitialization(): Promise<boolean> {
    try {
      console.log('🎤 音声システム初期化開始');
      
      if (!('speechSynthesis' in window)) {
        console.error('❌ 音声合成APIサポートなし');
        return false;
      }

      // 音声リストの読み込み待機
      await this.waitForVoices();
      
      // 音声コンテキストの初期化
      const contextInitialized = await initializeSpeechContext();
      
      this.isInitialized = contextInitialized;
      console.log(`✅ 音声システム初期化完了: ${this.isInitialized}`);
      
      return this.isInitialized;
    } catch (error) {
      console.error('❌ 音声システム初期化エラー:', error);
      return false;
    }
  }

  private waitForVoices(): Promise<void> {
    return new Promise((resolve) => {
      const voices = window.speechSynthesis.getVoices();
      if (voices.length > 0) {
        this.voicesLoaded = true;
        resolve();
        return;
      }

      const checkVoices = () => {
        const newVoices = window.speechSynthesis.getVoices();
        if (newVoices.length > 0) {
          this.voicesLoaded = true;
          console.log(`📋 音声読み込み完了: ${newVoices.length}個`);
          resolve();
        }
      };

      window.speechSynthesis.onvoiceschanged = checkVoices;
      
      // 3秒でタイムアウト
      setTimeout(() => {
        console.warn('⚠️ 音声読み込みタイムアウト');
        resolve();
      }, 3000);
    });
  }

  isReady(): boolean {
    return this.isInitialized && this.voicesLoaded;
  }
}

const speechManager = new SpeechManager();

// 強化されたアラビア語音声再生関数
export const speakArabicEnhanced = async (
  text: string, 
  options: Partial<EnhancedSpeechOptions> = {}
): Promise<void> => {
  const config: EnhancedSpeechOptions = {
    lang: 'ar-SA',
    rate: 0.8,
    pitch: 1.0,
    volume: 1.0,
    maxRetries: 3,
    fallbackLangs: ['ar-EG', 'ar-MA', 'ar'],
    enableFallback: true,
    ...options
  };

  console.log(`🔊 アラビア語音声再生開始: "${text}"`);
  
  // 音声システムの初期化
  const initialized = await speechManager.initialize();
  if (!initialized) {
    throw new Error('音声システムの初期化に失敗しました');
  }

  // 音声システム分析
  const analysis = await analyzeVoiceSystem();
  console.log('📊 音声システム分析:', analysis);

  if (!analysis.hasArabicSupport) {
    if (config.enableFallback) {
      console.warn('⚠️ アラビア語音声なし - フォールバック実行');
      return speakWithFallback(text, config);
    } else {
      throw new Error('アラビア語音声がシステムにインストールされていません');
    }
  }

  // 最適な音声を選択
  const selectedVoice = selectBestArabicVoice(analysis.arabicVoices, config.lang);
  
  return new Promise((resolve, reject) => {
    let attempts = 0;
    
    const attemptSpeech = () => {
      attempts++;
      console.log(`🎯 音声再生試行 ${attempts}/${config.maxRetries}`);
      
      const utterance = new SpeechSynthesisUtterance(text);
      
      if (selectedVoice) {
        utterance.voice = selectedVoice;
        utterance.lang = selectedVoice.lang;
        console.log(`🎵 使用音声: ${selectedVoice.name} (${selectedVoice.lang})`);
      } else {
        utterance.lang = config.lang;
        console.log(`🎵 デフォルト言語: ${config.lang}`);
      }
      
      utterance.rate = config.rate!;
      utterance.pitch = config.pitch!;
      utterance.volume = config.volume!;

      utterance.onstart = () => {
        console.log('▶️ アラビア語音声再生開始');
      };

      utterance.onend = () => {
        console.log('✅ アラビア語音声再生完了');
        resolve();
      };

      utterance.onerror = (event) => {
        console.error(`❌ 音声エラー (試行${attempts}):`, event.error);
        
        if (attempts < config.maxRetries!) {
          // リトライ
          setTimeout(() => {
            window.speechSynthesis.cancel();
            attemptSpeech();
          }, 500);
        } else if (config.enableFallback) {
          // フォールバック実行
          speakWithFallback(text, config)
            .then(resolve)
            .catch(reject);
        } else {
          reject(new Error(`音声再生エラー: ${event.error}`));
        }
      };

      // 音声を停止してから再生
      window.speechSynthesis.cancel();
      
      // 少し待ってから再生（ブラウザの制限対応）
      setTimeout(() => {
        try {
          window.speechSynthesis.speak(utterance);
        } catch (error) {
          console.error('音声再生例外:', error);
          if (attempts < config.maxRetries!) {
            setTimeout(attemptSpeech, 1000);
          } else {
            reject(error);
          }
        }
      }, 100);
    };

    attemptSpeech();
  });
};

// 最適なアラビア語音声を選択
function selectBestArabicVoice(
  arabicVoices: SpeechSynthesisVoice[], 
  preferredLang: string
): SpeechSynthesisVoice | null {
  if (arabicVoices.length === 0) return null;

  // 1. 完全一致
  let voice = arabicVoices.find(v => v.lang === preferredLang);
  if (voice) return voice;

  // 2. 言語コードの前半一致
  const langPrefix = preferredLang.split('-')[0];
  voice = arabicVoices.find(v => v.lang.startsWith(langPrefix));
  if (voice) return voice;

  // 3. デフォルト音声
  voice = arabicVoices.find(v => v.default);
  if (voice) return voice;

  // 4. 最初の利用可能音声
  return arabicVoices[0];
}

// フォールバック音声再生
async function speakWithFallback(
  text: string, 
  config: EnhancedSpeechOptions
): Promise<void> {
  console.log('🔄 フォールバック音声再生開始');
  
  // 英語での読み上げ（多くのシステムで利用可能）
  const fallbackUtterance = new SpeechSynthesisUtterance(
    `Arabic text: ${text}`
  );
  fallbackUtterance.lang = 'en-US';
  fallbackUtterance.rate = config.rate!;
  fallbackUtterance.volume = config.volume!;

  return new Promise((resolve, reject) => {
    fallbackUtterance.onend = () => {
      console.log('✅ フォールバック音声完了');
      resolve();
    };
    
    fallbackUtterance.onerror = (event) => {
      console.error('❌ フォールバック音声エラー:', event.error);
      reject(new Error(`フォールバック音声エラー: ${event.error}`));
    };

    window.speechSynthesis.speak(fallbackUtterance);
  });
}

// 後方互換性のための既存関数の強化
export const speakArabic = async (
  text: string, 
  options?: Partial<EnhancedSpeechOptions>
): Promise<void> => {
  return speakArabicEnhanced(text, options);
};

export const speakMoroccanArabic = async (
  text: string, 
  options?: Partial<EnhancedSpeechOptions>
): Promise<void> => {
  return speakArabicEnhanced(text, {
    lang: 'ar-MA',
    ...options
  });
};

// システム診断関数
export const diagnoseSpeechSystem = async () => {
  console.log('🔍 音声システム診断開始');
  
  const analysis = await analyzeVoiceSystem();
  
  console.log('=== 音声システム診断結果 ===');
  console.log(`ブラウザ: ${analysis.browserInfo.name} ${analysis.browserInfo.version}`);
  console.log(`プラットフォーム: ${analysis.browserInfo.platform}`);
  console.log(`総音声数: ${analysis.totalVoices}`);
  console.log(`アラビア語音声数: ${analysis.arabicVoices.length}`);
  console.log('推奨事項:', analysis.recommendations);
  
  if (analysis.arabicVoices.length > 0) {
    console.log('利用可能アラビア語音声:');
    analysis.arabicVoices.forEach((voice, index) => {
      console.log(`  ${index + 1}. ${voice.name} (${voice.lang})`);
    });
  }
  
  return analysis;
};