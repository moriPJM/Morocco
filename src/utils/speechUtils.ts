// Web Speech API ユーティリティ関数

export interface SpeechOptions {
  lang: string;
  rate?: number;
  pitch?: number;
  volume?: number;
}

export interface RecognitionOptions {
  lang: string;
  continuous?: boolean;
  interimResults?: boolean;
}

// テキスト読み上げ機能
export const speakText = (text: string, options: SpeechOptions): Promise<void> => {
  return new Promise((resolve, reject) => {
    if (!('speechSynthesis' in window)) {
      reject(new Error('お使いのブラウザは音声合成に対応していません'));
      return;
    }

    // 既存の音声を停止
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = options.lang;
    utterance.rate = options.rate || 1;
    utterance.pitch = options.pitch || 1;
    utterance.volume = options.volume || 1;

    utterance.onend = () => {
      console.log(`音声再生完了: ${text} (言語: ${options.lang})`);
      resolve();
    };
    utterance.onerror = (event) => {
      console.error(`音声合成エラー: ${event.error} (言語: ${options.lang}, テキスト: ${text})`);
      reject(new Error(`音声合成エラー: ${event.error}`));
    };

    // 音声が開始されたときのログ
    utterance.onstart = () => {
      console.log(`音声再生開始: ${text} (言語: ${options.lang})`);
    };

    // 利用可能な音声を取得して設定
    const loadVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      console.log('利用可能な音声:', voices.map(v => `${v.name} (${v.lang})`));
      
      // アラビア語音声を探す
      let voice = voices.find(v => v.lang === options.lang);
      if (!voice) {
        // 完全一致しない場合は言語コードの最初の部分で検索
        voice = voices.find(v => v.lang.startsWith(options.lang.split('-')[0]));
      }
      
      if (voice) {
        utterance.voice = voice;
        console.log(`選択された音声: ${voice.name} (${voice.lang})`);
      } else {
        console.warn(`言語 ${options.lang} の音声が見つかりません`);
        // アラビア語の場合、利用可能なアラビア語系音声を探す
        if (options.lang.startsWith('ar')) {
          const arabicVoice = voices.find(v => v.lang.includes('ar'));
          if (arabicVoice) {
            utterance.voice = arabicVoice;
            console.log(`代替アラビア語音声を使用: ${arabicVoice.name} (${arabicVoice.lang})`);
          }
        }
      }

      // ブラウザによってはユーザーインタラクション直後でないと音声が再生されない
      try {
        window.speechSynthesis.speak(utterance);
        console.log('音声再生コマンド実行');
      } catch (error) {
        console.error('音声再生エラー:', error);
        reject(new Error('音声再生に失敗しました。ブラウザの音声設定を確認してください。'));
      }
    };

    // 音声リストが読み込まれていない場合は待機
    if (window.speechSynthesis.getVoices().length === 0) {
      console.log('音声リスト読み込み待機中...');
      window.speechSynthesis.onvoiceschanged = loadVoices;
      // 2秒でタイムアウト
      setTimeout(() => {
        if (window.speechSynthesis.getVoices().length === 0) {
          console.warn('音声リスト読み込みタイムアウト');
          // それでも試行
          loadVoices();
        }
      }, 2000);
    } else {
      loadVoices();
    }
  });
};

// 音声認識機能
export const recognizeSpeech = (options: RecognitionOptions): Promise<string> => {
  return new Promise((resolve, reject) => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      reject(new Error('お使いのブラウザは音声認識に対応していません'));
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    recognition.lang = options.lang;
    recognition.continuous = options.continuous || false;
    recognition.interimResults = options.interimResults || false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event: any) => {
      const result = event.results[event.results.length - 1];
      if (result.isFinal) {
        resolve(result[0].transcript);
      }
    };

    recognition.onerror = (event: any) => {
      reject(new Error(`音声認識エラー: ${event.error}`));
    };

    recognition.onend = () => {
      // 音声が認識されずに終了した場合
    };

    recognition.start();
  });
};

// 音声合成が利用可能かチェック
export const isSpeechSynthesisSupported = (): boolean => {
  return 'speechSynthesis' in window;
};

// 音声認識が利用可能かチェック
export const isSpeechRecognitionSupported = (): boolean => {
  return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
};

// 利用可能な音声一覧を取得
export const getAvailableVoices = (): SpeechSynthesisVoice[] => {
  if (!isSpeechSynthesisSupported()) return [];
  return window.speechSynthesis.getVoices();
};

// 音声合成を停止
export const stopSpeech = (): void => {
  if (isSpeechSynthesisSupported()) {
    window.speechSynthesis.cancel();
  }
};

// 言語コードと設定のマッピング
export const languageSettings = {
  'ja': { code: 'ja-JP', name: '日本語', rate: 1.0, pitch: 1.0 },
  'ar': { code: 'ar-SA', name: 'العربية', rate: 0.8, pitch: 1.0 },
  'ar-ma': { code: 'ar-MA', name: 'العربية المغربية', rate: 0.8, pitch: 1.0 }, // モロッコアラビア語
  'fr': { code: 'fr-FR', name: 'Français', rate: 1.0, pitch: 1.0 },
  'en': { code: 'en-US', name: 'English', rate: 1.0, pitch: 1.0 },
  'ber': { code: 'ar-MA', name: 'Tamazight', rate: 0.8, pitch: 1.1 } // Berberは代替としてモロッコアラビア語
};

// アラビア語専用の音声出力関数
export const speakArabic = (text: string, options?: Partial<SpeechOptions>): Promise<void> => {
  console.log(`アラビア語音声再生要求: "${text}"`);
  
  const arabicOptions: SpeechOptions = {
    lang: 'ar-SA',
    rate: 0.8,
    pitch: 1.0,
    volume: 1.0,
    ...options
  };
  
  // アラビア語のテキストクリーンアップ（発音記号除去）
  const cleanText = text.replace(/[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s]/g, '');
  console.log(`クリーンアップ後のテキスト: "${cleanText}"`);
  
  return speakText(cleanText || text, arabicOptions);
};

// モロッコアラビア語用の音声出力関数
export const speakMoroccanArabic = (text: string, options?: Partial<SpeechOptions>): Promise<void> => {
  console.log(`モロッコアラビア語音声再生要求: "${text}"`);
  
  const moroccanArabicOptions: SpeechOptions = {
    lang: 'ar-MA',
    rate: 0.8,
    pitch: 1.0,
    volume: 1.0,
    ...options
  };
  
  // アラビア語のテキストクリーンアップ
  const cleanText = text.replace(/[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s]/g, '');
  console.log(`クリーンアップ後のテキスト: "${cleanText}"`);
  
  // モロッコアラビア語が利用できない場合は標準アラビア語にフォールバック
  return speakText(cleanText || text, moroccanArabicOptions).catch(() => {
    console.log('モロッコアラビア語が利用できないため、標準アラビア語を使用');
    return speakText(cleanText || text, { ...moroccanArabicOptions, lang: 'ar-SA' });
  });
};

// 利用可能な音声一覧を表示するデバッグ関数
export const logAvailableVoices = (): void => {
  if (!isSpeechSynthesisSupported()) {
    console.log('音声合成はサポートされていません');
    return;
  }
  
  const loadAndLogVoices = () => {
    const voices = window.speechSynthesis.getVoices();
    console.log('=== 利用可能な音声一覧 ===');
    voices.forEach((voice, index) => {
      console.log(`${index + 1}. ${voice.name} (${voice.lang}) - ${voice.default ? 'デフォルト' : ''}`);
    });
    
    const arabicVoices = voices.filter(v => v.lang.includes('ar'));
    console.log('=== アラビア語系音声 ===');
    if (arabicVoices.length > 0) {
      arabicVoices.forEach((voice, index) => {
        console.log(`${index + 1}. ${voice.name} (${voice.lang})`);
      });
    } else {
      console.log('アラビア語音声が見つかりません');
    }
  };
  
  if (window.speechSynthesis.getVoices().length === 0) {
    window.speechSynthesis.onvoiceschanged = loadAndLogVoices;
  } else {
    loadAndLogVoices();
  }
};

// TypeScript定義の拡張
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}