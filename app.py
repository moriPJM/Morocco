from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import json
import requests
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)  # フロントエンドとの通信を許可

# OpenAI API設定
OPENAI_API_KEY = os.getenv('VITE_OPENAI_API_KEY')

@app.route('/')
def serve_react_app():
    """React アプリケーションのメインページを配信"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """静的ファイル（CSS、JS、画像など）を配信"""
    try:
        return send_from_directory(app.static_folder, path)
    except:
        # ファイルが見つからない場合はReactアプリのindex.htmlを返す（SPA対応）
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """OpenAI APIとの通信エンドポイント"""
    if not OPENAI_API_KEY:
        return jsonify({'error': 'OpenAI APIキーが設定されていません'}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'メッセージが空です'}), 400
        
        # OpenAI APIへのリクエスト
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {OPENAI_API_KEY}'
        }
        
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': '''あなたはモロッコ旅行の専門ガイドです。モロッコの観光地、文化、歴史、料理、言語、習慣、エチケット、交通、宿泊、買い物などについて、詳しく丁寧に日本語で回答してください。
                    
                    回答の特徴：
                    - 親しみやすく、実用的な情報を提供
                    - 具体的な場所名、料理名、文化的背景を含める
                    - 安全な旅行のためのアドバイスも含める
                    - 適切に絵文字を使用して読みやすくする
                    - 日本人旅行者の視点で回答する
                    - 回答は400文字程度に収める'''
                },
                {
                    'role': 'user',
                    'content': user_message
                }
            ],
            'max_tokens': 500,
            'temperature': 0.7
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({'error': f'OpenAI APIエラー: {response.status_code}'}), 500
        
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        
        return jsonify({'response': ai_response})
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'ネットワークエラー: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'サーバーエラー: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """サーバーの健康状態確認"""
    return jsonify({
        'status': 'healthy',
        'message': 'Morocco Travel App Python Server',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    # 開発環境での起動設定
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🇲🇦 Morocco Travel App starting on port {port}")
    print(f"📱 Access the app at: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)