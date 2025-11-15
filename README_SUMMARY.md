# 要約器（RAG）について

このリポジトリに追加された要約器の挙動と設定方法をまとめます。

## 概要
- 取得した RAG スニペットはプロンプトにそのまま入れるとトークン消費が大きいため、要約器で要旨に圧縮してから LLM に渡すようにしました。
- 要約器は以下の順で動作します：
  1. 環境変数 `OPENAI_API_KEY` が設定され、OpenAI クライアントが利用可能な場合は OpenAI に要約を依頼します。
  2. OpenAI が利用できない場合は軽量な抽出的要約にフォールバックします（各スニペットの先頭文をつなげる）。
- 要約結果には簡単な「参照元一覧」を付与して、出典参照を維持します。

## 有効化方法
- OpenAI による要約を使うには、環境変数 `OPENAI_API_KEY` を設定してください。
  - 例（PowerShell）:
    $env:OPENAI_API_KEY = "sk-..."

## Streamlit UI 設定
- Streamlit の AI ページで `Top K (retrieval)` と `Summary max chars` を調整可能にしました（コード内で `summarize_snippets` の `max_chars` とベクトル検索の `top_k` を制御します）。

## フォールバック
- OpenAI 呼び出しが失敗した場合はアプリは自動的に抽出的要約に切り替わります。

## 開発者向けメモ
- 要約器は `streamlit_app.py` の `summarize_snippets` 関数に実装されています。
- さらに品質を上げたい場合は BM25 ハイブリッドや要約の post-processing（冗長句削除等）を検討してください。
