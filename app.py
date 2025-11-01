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
from backend.services.database import init_db
import os

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
    print(" モロッコ観光ガイドアプリを起動中...")
    print("🌐 http://localhost:5000 でアクセスできます")
    app.run(debug=True, host='0.0.0.0', port=5000)