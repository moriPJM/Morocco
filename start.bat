@echo off
echo 🇲🇦 Morocco Travel App - Starting...
echo.

REM Python バージョンチェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM 依存関係のインストール
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

REM npm の確認とフロントエンドビルド
where npm >nul 2>&1
if errorlevel 1 (
    echo ❌ npm not found. Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo 🏗️ Building frontend...
if not exist "node_modules" (
    echo 📦 Installing npm dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install npm dependencies
        pause
        exit /b 1
    )
)

npm run build
if errorlevel 1 (
    echo ❌ Failed to build frontend
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo 🚀 Starting Morocco Travel App...
echo 📱 Access the app at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Flaskサーバーの起動
set FLASK_ENV=development
python app.py

pause