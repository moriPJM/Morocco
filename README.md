# 🇲🇦 モロッコ観光ガイドアプリ

Flask + Bootstrap を使用したモロッコ観光ガイドWebアプリケーション

## 📋 機能

- **🏠 ホーム画面**: おすすめ観光地とカテゴリー別検索
- **📍 観光スポット**: 詳細情報、検索、フィルタリング
- **🗺️ 地図表示**: Google Maps統合（予定）
- **🤖 AI観光案内**: チャットベースの観光情報提供
- **❤️ お気に入り**: ユーザーのお気に入りスポット管理
- **🛣️ ルートプランナー**: おすすめ旅行ルート
- **ℹ️ 現地情報**: 通貨、気候、文化情報
- **⚙️ 設定**: 多言語対応（日本語/英語/フランス語）

## 🛠️ 技術スタック

### バックエンド
- **Flask**: Webフレームワーク
- **SQLAlchemy**: ORM
- **SQLite**: データベース（開発用）

### フロントエンド
- **Bootstrap 5**: UIフレームワーク
- **Font Awesome**: アイコン
- **Vanilla JavaScript**: インタラクション

### AI機能（予定）
- **OpenAI API**: チャット機能
- **LangChain**: RAG実装
- **ChromaDB**: ベクトルデータベース

## 🚀 セットアップ

### 1. 仮想環境の作成・有効化

```powershell
# 仮想環境作成（既に作成済み）
python -m venv .venv

# 仮想環境有効化
.\.venv\Scripts\Activate.ps1
```

### 2. 依存関係のインストール

```powershell
pip install -r requirements.txt
```

### 3. データベース初期化

```powershell
python -c "from app import create_app; from data.sample_data import load_sample_data; app = create_app(); load_sample_data(app)"
```

### 4. アプリケーション起動

```powershell
python app.py
```

アプリケーションが http://localhost:5000 で起動します。

## 📁 プロジェクト構造

```
morroco/
├── app.py                 # メインアプリケーション
├── requirements.txt       # 依存関係
├── .gitignore            # Git除外設定
├── README.md             # このファイル
├── backend/              # バックエンドコード
│   ├── api/              # APIエンドポイント
│   │   ├── routes.py     # メインルート
│   │   ├── spots.py      # 観光スポットAPI
│   │   ├── chat.py       # チャットAPI
│   │   └── maps.py       # 地図API
│   ├── models/           # データモデル
│   │   └── tourism.py    # 観光データモデル
│   └── services/         # サービス層
│       └── database.py   # DB設定
├── frontend/             # フロントエンド
│   ├── templates/        # HTMLテンプレート
│   │   ├── base.html     # ベーステンプレート
│   │   ├── index.html    # ホーム画面
│   │   ├── spots.html    # 観光スポット画面
│   │   └── chat.html     # チャット画面
│   └── static/           # 静的ファイル
│       ├── css/
│       │   └── style.css # メインスタイル
│       └── js/
│           └── app.js    # メインJavaScript
├── data/                 # データ関連
│   └── sample_data.py    # サンプルデータ
└── config/               # 設定ファイル
```

## 🔧 開発コマンド

```powershell
# 開発サーバー起動
python app.py

# データベースリセット
python data/sample_data.py

# 依存関係更新
pip freeze > requirements.txt

# テスト実行（今後実装）
python -m pytest

# 本番ビルド（今後実装）
python build.py
```

## 🌐 API エンドポイント

### 観光スポット
- `GET /api/spots/` - スポット一覧
- `GET /api/spots/<id>` - スポット詳細
- `GET /api/spots/search?q=<query>` - スポット検索

### チャット
- `POST /api/chat/message` - メッセージ送信
- `GET /api/chat/suggestions` - 提案取得

### 地図
- `GET /api/maps/markers` - マーカー情報
- `GET /api/maps/route` - ルート情報

### その他
- `GET /api/health` - ヘルスチェック

## 📋 今後の実装予定

- [ ] Google Maps API統合
- [ ] OpenAI ChatGPT API統合
- [ ] RAGシステム実装
- [ ] ユーザー認証
- [ ] レビュー・評価機能
- [ ] オフラインモード
- [ ] PWA対応
- [ ] 多言語対応完成
- [ ] 管理画面
- [ ] テストコード

## 🎨 カスタマイズ

### カラーテーマ
モロッコの国旗をイメージしたカラーパレットを使用：
- 赤: `#C41E3A` (Morocco Red)
- 緑: `#006233` (Morocco Green)  
- 金: `#FFD700` (Morocco Gold)

### API設定
環境変数で各種API設定が可能：
```powershell
$env:OPENAI_API_KEY="your-openai-key"
$env:GOOGLE_MAPS_API_KEY="your-maps-key"
$env:DATABASE_URL="sqlite:///morocco_guide.db"
```

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

質問や問題がある場合は、Issueを作成してください。

---

**Enjoy exploring Morocco! 🇲🇦**