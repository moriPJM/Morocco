#!/usr/bin/env python3
"""
Morocco Travel App - Python メインエントリーポイント
メインファイル: start.py
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time

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
        print("✅ Python dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install Python dependencies")
        print(f"Error: {e.stderr}")
        # 続行を試みる
        pass

def build_frontend():
    """フロントエンドのビルド"""
    try:
        print("🏗️  Building React frontend...")
        
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
        print("⚠️ Continuing with existing build...")
        
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js and npm")
        print("⚠️ Serving without frontend build...")

def start_server():
    """Pythonサーバーの起動（メインエントリーポイント）"""
    print("🚀 Starting Morocco Travel App (Python Backend)...")
    print("🇲🇦 Main Entry Point: start.py")
    print("📱 Frontend + Backend: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        # 環境変数設定
        os.environ['FLASK_ENV'] = 'development'
        os.environ['PYTHONPATH'] = os.getcwd()
        
        # ブラウザを自動で開く
        def open_browser():
            time.sleep(2)  # サーバー起動を待つ
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Flaskアプリの起動
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Installing missing dependencies...")
        install_dependencies()
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

def main():
    """メイン実行関数 - アプリケーションエントリーポイント"""
    print("🇲🇦 Morocco Travel App - Python Main Entry Point")
    print("=" * 60)
    print("📁 Main File Path: C:\\Users\\user\\Documents\\Morocco\\start.py")
    print("🔧 Backend: Python Flask")
    print("🖥️  Frontend: React + TypeScript")
    print("=" * 60)
    
    check_python_version()
    install_dependencies()
    build_frontend()
    start_server()

if __name__ == "__main__":
    main()