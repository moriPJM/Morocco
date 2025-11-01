import React, { useState, useEffect } from 'react';
import { getBrowserInfo } from '../utils/voiceAnalysis';

interface OSInstallGuide {
  os: string;
  title: string;
  icon: string;
  steps: string[];
  notes: string[];
}

const ArabicVoiceInstallGuide: React.FC = () => {
  const [browserInfo] = useState(getBrowserInfo());
  const [detectedOS, setDetectedOS] = useState<string>('unknown');

  useEffect(() => {
    const platform = navigator.platform.toLowerCase();
    const userAgent = navigator.userAgent.toLowerCase();
    
    let os = 'unknown';
    if (platform.includes('win') || userAgent.includes('windows')) {
      os = 'windows';
    } else if (platform.includes('mac') || userAgent.includes('mac')) {
      os = 'macos';
    } else if (userAgent.includes('linux')) {
      os = 'linux';
    }
    
    setDetectedOS(os);
  }, []);

  const installGuides: OSInstallGuide[] = [
    {
      os: 'windows',
      title: 'Windows 10/11',
      icon: '🪟',
      steps: [
        '1. 設定アプリを開く（Windowsキー + I）',
        '2. 「時刻と言語」を選択',
        '3. 「音声」をクリック',
        '4. 「音声を追加」をクリック',
        '5. アラビア語系言語を検索して選択：',
        '   • Arabic (Saudi Arabia) - 推奨',
        '   • Arabic (Egypt)',
        '   • Arabic (Morocco)',
        '6. ダウンロードが完了するまで待機',
        '7. ブラウザを再起動'
      ],
      notes: [
        '💡 Microsoft Speech Platformから追加音声をダウンロード可能',
        '💡 Edge/Chromeで最良の結果が得られます',
        '⚠️ 管理者権限が必要な場合があります'
      ]
    },
    {
      os: 'macos',
      title: 'macOS',
      icon: '🍎',
      steps: [
        '1. Appleメニュー → システム環境設定',
        '2. 「アクセシビリティ」を選択',
        '3. 「読み上げコンテンツ」をクリック',
        '4. 「システムの声」を選択',
        '5. 「カスタマイズ」をクリック',
        '6. アラビア語音声をチェック：',
        '   • Majed (Arabic)',
        '   • Maged (Arabic)',
        '7. ダウンロード完了まで待機',
        '8. Safariまたは他のブラウザを再起動'
      ],
      notes: [
        '💡 高品質な音声が利用可能',
        '💡 VoiceOverでも同じ音声が使用されます',
        '⚠️ ダウンロードサイズが大きい場合があります'
      ]
    },
    {
      os: 'linux',
      title: 'Linux',
      icon: '🐧',
      steps: [
        '1. ターミナルを開く',
        '2. espeak-dataパッケージをインストール：',
        '   sudo apt-get install espeak-data-ar',
        '3. または festival用音声をインストール：',
        '   sudo apt-get install festvox-ar-nah',
        '4. 音声エンジンを再起動：',
        '   sudo systemctl restart speech-dispatcher',
        '5. ブラウザを再起動'
      ],
      notes: [
        '💡 ディストリビューションによって手順が異なります',
        '💡 GNOME環境では設定アプリからも設定可能',
        '⚠️ 音声品質はWindows/macOSより劣る場合があります'
      ]
    }
  ];

  const renderGuide = (guide: OSInstallGuide, isDetected: boolean = false) => (
    <div key={guide.os} className={`p-6 rounded-lg border-2 ${
      isDetected ? 'bg-blue-50 border-blue-300' : 'bg-gray-50 border-gray-200'
    }`}>
      <div className="flex items-center gap-3 mb-4">
        <span className="text-2xl">{guide.icon}</span>
        <h3 className={`text-lg font-bold ${isDetected ? 'text-blue-800' : 'text-gray-800'}`}>
          {guide.title}
          {isDetected && <span className="ml-2 text-sm bg-blue-200 px-2 py-1 rounded">検出済み</span>}
        </h3>
      </div>
      
      <div className="mb-4">
        <h4 className="font-semibold text-gray-700 mb-2">📋 インストール手順：</h4>
        <ol className="text-sm text-gray-600 space-y-1">
          {guide.steps.map((step, index) => (
            <li key={index} className="leading-relaxed">
              {step}
            </li>
          ))}
        </ol>
      </div>
      
      <div>
        <h4 className="font-semibold text-gray-700 mb-2">💡 注意事項：</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          {guide.notes.map((note, index) => (
            <li key={index}>{note}</li>
          ))}
        </ul>
      </div>
    </div>
  );

  return (
    <div className="p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-xl font-bold mb-4 text-gray-800">
        🔧 アラビア語音声インストールガイド
      </h2>
      
      <div className="mb-6 p-4 bg-yellow-50 rounded-lg">
        <h3 className="font-semibold text-yellow-800 mb-2">🔍 システム情報</h3>
        <div className="text-sm text-yellow-700 space-y-1">
          <p><strong>ブラウザ:</strong> {browserInfo.name} {browserInfo.version}</p>
          <p><strong>プラットフォーム:</strong> {browserInfo.platform}</p>
          <p><strong>検出OS:</strong> {detectedOS}</p>
        </div>
      </div>

      <div className="space-y-6">
        {detectedOS !== 'unknown' && (
          <>
            <h3 className="text-lg font-semibold text-gray-800">
              🎯 お使いの環境向けガイド
            </h3>
            {installGuides
              .filter(guide => guide.os === detectedOS)
              .map(guide => renderGuide(guide, true))
            }
            
            <h3 className="text-lg font-semibold text-gray-800 mt-8">
              📚 その他のOS
            </h3>
          </>
        )}
        
        {installGuides
          .filter(guide => guide.os !== detectedOS)
          .map(guide => renderGuide(guide, false))
        }
      </div>
      
      <div className="mt-8 p-4 bg-green-50 rounded-lg">
        <h3 className="font-semibold text-green-800 mb-2">✅ インストール後の確認方法</h3>
        <ol className="text-sm text-green-700 space-y-1">
          <li>1. ブラウザを完全に再起動</li>
          <li>2. 音声テストページで「🔍 音声システム分析」を実行</li>
          <li>3. アラビア語音声が表示されることを確認</li>
          <li>4. 「🎵 強化アラビア語テスト」で実際に音声を試す</li>
        </ol>
      </div>
      
      <div className="mt-6 p-4 bg-red-50 rounded-lg">
        <h3 className="font-semibold text-red-800 mb-2">🚨 トラブルシューティング</h3>
        <ul className="text-sm text-red-700 space-y-1">
          <li>• インストール後もアラビア語音声が表示されない場合はPC再起動</li>
          <li>• Chrome/Edgeの使用を強く推奨（Firefoxは制限あり）</li>
          <li>• 会社PCの場合は管理者権限が必要</li>
          <li>• オフライン環境では音声ダウンロードに制限があります</li>
        </ul>
      </div>
    </div>
  );
};

export default ArabicVoiceInstallGuide;