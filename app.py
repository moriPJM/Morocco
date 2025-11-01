#!/usr/bin/env python3
"""
モロッコ観光ガイドアプリ - メインエントリーポイント
Morocco Tourism Guide App - Main Entry Point
"""

from flask import Flask, render_template, jsonify, request
from backend.api.routes import api_bp
from backend.api.spots import spots_bp
from backend.api.chat import chat_bp
from backend.api.maps import maps_bp
from backend.api.routes_api import routes_bp
from backend.services.database import init_db
from dotenv import load_dotenv
import os
import socket

# 環境変数を読み込み
load_dotenv()

def is_port_available(host, port):
    """ポートが使用可能かチェック"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result != 0
    except Exception:
        return False

def find_available_port(host, start_port=5000, max_port=5010):
    """使用可能なポートを検索"""
    for port in range(start_port, max_port + 1):
        if is_port_available(host, port):
            return port
    return None

def create_app():
    """アプリケーションファクトリー"""
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # 設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///morocco_guide.db')
    
    # データベース初期化
    init_db(app)
    
    # Blueprint登録
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(spots_bp, url_prefix='/api/spots')
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(maps_bp, url_prefix='/api/maps')
    app.register_blueprint(routes_bp, url_prefix='/api/routes')
    
    # メインルート
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/spots')
    def spots():
        return render_template('spots.html')
    
    @app.route('/routes')
    def routes():
        return render_template('routes.html')
    
    @app.route('/chat')
    def chat():
        return render_template('chat.html')
    
    @app.route('/favorites')
    def favorites():
        return render_template('favorites.html')
    
    @app.route('/info')
    def info():
        return render_template('info.html')
    
    @app.route('/settings')
    def settings():
        return render_template('settings.html')
    
    return app

if __name__ == "__main__":
    app = create_app()
    
    # サンプルデータの読み込み（開発環境のみ）
    with app.app_context():
        from data.sample_data import load_sample_data
        try:
            load_sample_data(app)
            print("✅ サンプルデータを読み込みました")
        except Exception as e:
            print(f"⚠️ サンプルデータ読み込みエラー: {e}")
    
    # サーバー設定
    host = '0.0.0.0'  # すべてのインターフェースでリッスン
    port = find_available_port('127.0.0.1')
    
    if port is None:
        print("❌ 使用可能なポートが見つかりません（5000-5010）")
        exit(1)
    
    print("🌐 モロッコ観光ガイドアプリを起動中...")
    print(f"🌐 http://localhost:{port} でアクセスできます")
    print(f"🔧 Starting Flask server on {host}:{port}...")
    
    try:
        app.run(debug=False, host=host, port=port, threaded=True, use_reloader=False)
    except Exception as e:
        print(f"❌ サーバー起動エラー: {e}")
        import traceback
        traceback.print_exc()