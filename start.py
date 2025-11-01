#!/usr/bin/env python3
"""
Morocco Travel App - Python起動スクリプト
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Python バージョンチェック"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8以上が必要です")
        print(f"現在のバージョン: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """依存関係のインストール"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def build_frontend():
    """フロントエンドのビルド"""
    try:
        print("🏗️  Building frontend...")
        
        # npm installの確認
        if not os.path.exists("node_modules"):
            print("📦 Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True, capture_output=True, text=True)
        
        # React アプリのビルド
        subprocess.run(["npm", "run", "build"], check=True, capture_output=True, text=True)
        print("✅ Frontend built successfully")
        
    except subprocess.CalledProcessError as e:
        print("❌ Failed to build frontend")
        print(f"Error: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
        sys.exit(1)

def start_server():
    """サーバーの起動"""
    print("🚀 Starting Morocco Travel App...")
    print("📱 Access the app at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        # 環境変数設定
        os.environ['FLASK_ENV'] = 'development'
        
        # Flaskアプリの起動
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

def main():
    """メイン実行関数"""
    print("🇲🇦 Morocco Travel App - Python Setup")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    build_frontend()
    start_server()

if __name__ == "__main__":
    main()