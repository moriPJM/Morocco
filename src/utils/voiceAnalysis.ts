// 強化された音声システム診断ユーティリティ

export interface VoiceAnalysis {
  totalVoices: number;
  arabicVoices: SpeechSynthesisVoice[];
  supportedLanguages: string[];
  browserInfo: {
    name: string;
    version: string;
    platform: string;
  };
  hasArabicSupport: boolean;
  recommendations: string[];
}

// ブラウザ情報を取得
export const getBrowserInfo = () => {
  const ua = navigator.userAgent;
  let browserName = 'Unknown';
  let version = 'Unknown';
  
  if (ua.includes('Chrome') && !ua.includes('Edg')) {
    browserName = 'Chrome';
    const match = ua.match(/Chrome\/(\d+)/);
    version = match ? match[1] : 'Unknown';
  } else if (ua.includes('Edg')) {
    browserName = 'Edge';
    const match = ua.match(/Edg\/(\d+)/);
    version = match ? match[1] : 'Unknown';
  } else if (ua.includes('Firefox')) {
    browserName = 'Firefox';
    const match = ua.match(/Firefox\/(\d+)/);
    version = match ? match[1] : 'Unknown';
  } else if (ua.includes('Safari') && !ua.includes('Chrome')) {
    browserName = 'Safari';
    const match = ua.match(/Version\/(\d+)/);
    version = match ? match[1] : 'Unknown';
  }
  
  return {
    name: browserName,
    version: version,
    platform: navigator.platform
  };
};

// 音声システムの包括的分析
export const analyzeVoiceSystem = async (): Promise<VoiceAnalysis> => {
  return new Promise((resolve) => {
    const performAnalysis = () => {
      const voices = window.speechSynthesis.getVoices();
      const arabicVoices = voices.filter(v => 
        v.lang.includes('ar') || 
        v.name.toLowerCase().includes('arab')
      );
      
      const supportedLanguages = [...new Set(voices.map(v => v.lang))];
      const browserInfo = getBrowserInfo();
      
      const recommendations: string[] = [];
      
      // ブラウザ別推奨事項
      if (browserInfo.name === 'Chrome' || browserInfo.name === 'Edge') {
        recommendations.push('✅ Chromium系ブラウザは音声合成に最適です');
      } else if (browserInfo.name === 'Firefox') {
        recommendations.push('⚠️ Firefoxは音声サポートが限定的です。ChromeまたはEdgeの使用を推奨');
      } else if (browserInfo.name === 'Safari') {
        recommendations.push('ℹ️ Safariの音声はmacOSシステム設定に依存します');
      }
      
      // アラビア語音声の状況
      if (arabicVoices.length === 0) {
        recommendations.push('❌ アラビア語音声が見つかりません');
        if (browserInfo.platform.includes('Win')) {
          recommendations.push('🔧 Windows: 設定 → 時刻と言語 → 音声でアラビア語音声を追加');
        } else if (browserInfo.platform.includes('Mac')) {
          recommendations.push('🔧 macOS: システム環境設定 → アクセシビリティ → 読み上げコンテンツ');
        }
      } else {
        recommendations.push(`✅ ${arabicVoices.length}個のアラビア語音声が利用可能`);
      }
      
      // 音声数の評価
      if (voices.length < 10) {
        recommendations.push('⚠️ 利用可能音声が少なすぎます。システム音声を追加してください');
      }
      
      resolve({
        totalVoices: voices.length,
        arabicVoices,
        supportedLanguages,
        browserInfo,
        hasArabicSupport: arabicVoices.length > 0,
        recommendations
      });
    };
    
    // 音声リストが空の場合は待機
    if (window.speechSynthesis.getVoices().length === 0) {
      console.log('音声リスト読み込み待機中...');
      window.speechSynthesis.onvoiceschanged = performAnalysis;
      // 5秒でタイムアウト
      setTimeout(performAnalysis, 5000);
    } else {
      performAnalysis();
    }
  });
};

// 強化されたアラビア語音声テスト
export const testArabicVoiceAdvanced = async (text: string = 'مرحبا'): Promise<{
  success: boolean;
  voiceUsed?: SpeechSynthesisVoice;
  error?: string;
  duration?: number;
}> => {
  return new Promise((resolve) => {
    const startTime = Date.now();
    
    if (!('speechSynthesis' in window)) {
      resolve({
        success: false,
        error: '音声合成APIがサポートされていません'
      });
      return;
    }
    
    const voices = window.speechSynthesis.getVoices();
    const arabicVoices = voices.filter(v => v.lang.includes('ar'));
    
    if (arabicVoices.length === 0) {
      resolve({
        success: false,
        error: 'アラビア語音声が利用できません'
      });
      return;
    }
    
    // 最適なアラビア語音声を選択
    let selectedVoice = arabicVoices.find(v => v.lang === 'ar-SA') || 
                       arabicVoices.find(v => v.lang.startsWith('ar-')) ||
                       arabicVoices[0];
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = selectedVoice;
    utterance.lang = selectedVoice.lang;
    utterance.rate = 0.8;
    utterance.volume = 1.0;
    
    utterance.onstart = () => {
      console.log(`▶️ アラビア語音声開始: ${selectedVoice.name}`);
    };
    
    utterance.onend = () => {
      const duration = Date.now() - startTime;
      console.log(`✅ アラビア語音声完了: ${duration}ms`);
      resolve({
        success: true,
        voiceUsed: selectedVoice,
        duration
      });
    };
    
    utterance.onerror = (event) => {
      console.error('❌ アラビア語音声エラー:', event.error);
      resolve({
        success: false,
        voiceUsed: selectedVoice,
        error: event.error
      });
    };
    
    try {
      window.speechSynthesis.speak(utterance);
    } catch (error) {
      resolve({
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー'
      });
    }
  });
};

// 音声の前処理でユーザーインタラクションを確保
export const initializeSpeechContext = (): Promise<boolean> => {
  return new Promise((resolve) => {
    if (!('speechSynthesis' in window)) {
      resolve(false);
      return;
    }
    
    // 非常に短い無音の音声を再生してコンテキストを初期化
    const utterance = new SpeechSynthesisUtterance('');
    utterance.volume = 0.01;
    utterance.rate = 10;
    
    utterance.onend = () => {
      console.log('🎤 音声コンテキスト初期化完了');
      resolve(true);
    };
    
    utterance.onerror = () => {
      console.log('⚠️ 音声コンテキスト初期化失敗');
      resolve(false);
    };
    
    try {
      window.speechSynthesis.speak(utterance);
    } catch {
      resolve(false);
    }
  });
};

// 複数の音声エンジンでテスト
export const testMultipleVoiceEngines = async (text: string) => {
  const voices = window.speechSynthesis.getVoices();
  const arabicVoices = voices.filter(v => v.lang.includes('ar'));
  
  const results = [];
  
  for (const voice of arabicVoices) {
    try {
      const result = await testArabicVoiceAdvanced(text);
      results.push({
        voice: voice.name,
        lang: voice.lang,
        ...result
      });
    } catch (error) {
      results.push({
        voice: voice.name,
        lang: voice.lang,
        success: false,
        error: error instanceof Error ? error.message : '不明なエラー'
      });
    }
  }
  
  return results;
};