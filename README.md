# 🕌 モロッコ観光ガイド - Morocco Tourism Guide

Streamlitで作成されたインタラクティブなモロッコ観光ガイドアプリです。

## 🌟 特徴

- **インタラクティブマップ**: Foliumを使用した観光地マップ
- **観光地情報**: 12の主要観光地の詳細情報
- **AI観光ガイド**: OpenAI APIを使用したチャットボット機能
- **フィルタリング**: 都市やカテゴリによる絞り込み機能
- **レスポンシブデザイン**: モバイル対応

## 🗺️ 対象都市

- マラケシュ (Marrakech)
- カサブランカ (Casablanca)
- フェズ (Fez)
- メルズーガ (Merzouga)
- シャウエン (Chefchaouen)
- エッサウィラ (Essaouira)

## 🚀 デプロイ

このアプリはStreamlit Shareでデプロイされています。

### Streamlit Shareでのデプロイ手順

1. GitHubリポジトリにコードをプッシュ
2. Streamlit Shareにアクセス
3. リポジトリを選択
4. `streamlit_app.py`をメインファイルとして指定
5. デプロイ開始

## 🔧 ローカル実行

```bash
# 依存関係のインストール
pip install -r requirements.txt

# アプリケーション実行
streamlit run streamlit_app.py
```

## 📁 ファイル構成

```
morocco/
├── streamlit_app.py      # メインアプリケーション
├── requirements.txt      # 依存関係
├── .streamlit/
│   └── config.toml      # Streamlit設定
└── README.md            # このファイル
```

## 🛠️ 技術スタック

- **Frontend**: Streamlit
- **Map**: Folium + streamlit-folium
- **AI**: OpenAI API
- **Data**: Pandas
- **Deployment**: Streamlit Share

## 🔑 環境変数

AI機能を使用する場合は、以下の環境変数を設定してください：

```
OPENAI_API_KEY=your_openai_api_key_here
```

## 📊 観光地データ

アプリに含まれる観光地：

### マラケシュ
- ジャマ・エル・フナ広場
- クトゥビア・モスク
- バイア宮殿
- マジョレル庭園
- サーディアン朝の墳墓群

### カサブランカ
- ハッサン2世モスク
- リック・カフェ

### フェズ
- フェズ・エル・バリ
- カラウィーン大学

### その他
- エルグ・シェビ砂丘（メルズーガ）
- シャウエン旧市街
- エッサウィラ・メディナ

## 📝 ライセンス

MIT License

## 🤝 貢献

プルリクエストや Issue の作成を歓迎します！

---

Made with ❤️ and Streamlit