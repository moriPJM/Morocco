"""
モロッコ観光ガイドアプリのメインアプリケーション - AI機能搭載（クリーン版）
"""

import os
import socket
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from my_app.services.ai_service import get_morocco_gpt

# 環境変数を読み込み
load_dotenv()

# データベースインスタンス
db = SQLAlchemy()

def create_app():
    """Flaskアプリケーションファクトリ"""
    app = Flask(__name__, 
                template_folder='frontend/templates',
                static_folder='frontend/static')
    
    # CORS設定
    CORS(app)
    
    # アプリケーション設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///morocco_tourism.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # データベース初期化
    db.init_app(app)
    
    return app

# Flaskアプリケーション作成
app = create_app()

# =============================================================================
# ウェブページルート
# =============================================================================

@app.route('/')
def index():
    """ホームページ"""
    return render_template('index.html')

@app.route('/ai')
def ai_chat_page():
    """AIチャットページ"""
    return render_template('ai_chat.html')

@app.route('/spots')
def spots():
    """観光地一覧ページ"""
    return render_template('spots.html')

@app.route('/spots/<int:spot_id>')
def spot_detail(spot_id):
    """観光地詳細ページ"""
    return render_template('spot_detail.html', spot_id=spot_id)

@app.route('/map')
def map_page():
    """マップページ"""
    return render_template('map.html')

@app.route('/settings')
def settings():
    """設定ページ"""
    return render_template('settings.html')

# =============================================================================
# API エンドポイント
# =============================================================================

@app.route('/api/health')
def health_check():
    """ヘルスチェックエンドポイント"""
    return jsonify({
        'status': 'ok',
        'message': 'Morocco Tourism App is running!',
        'python_version': '3.11.9',
        'flask_version': '3.1.2',
        'ai_enabled': True
    })

@app.route('/api/ai/test')
def ai_test():
    """AI接続テスト"""
    try:
        gpt_service = get_morocco_gpt()
        result = gpt_service.test_connection()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'AI初期化エラー'
        }), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI チャットエンドポイント"""
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': '質問が提供されていません'
            }), 400
            
        question = data['question']
        context = data.get('context', None)
        
        gpt_service = get_morocco_gpt()
        result = gpt_service.get_morocco_guide_response(question, context)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'AI応答の生成中にエラーが発生しました。'
        }), 500

@app.route('/api/ai/suggestions')
def get_ai_suggestions():
    """おすすめ質問の取得"""
    try:
        gpt_service = get_morocco_gpt()
        suggestions = gpt_service.get_quick_suggestions()
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =============================================================================
# 観光地データ管理
# =============================================================================

def get_spots_data():
    """観光地データを取得"""
    return [
        # マラケシュ地域
        {
            'id': 1, 'name': 'ジャマ・エル・フナ広場', 'city': 'マラケシュ', 'category': '広場・市場',
            'description': 'マラケシュの心臓部に位置する世界遺産の広場。夜市や大道芸人のパフォーマンスで有名',
            'features': ['世界遺産', '夜市', 'パフォーマー'], 'verified': True, 'unesco': True,
            'lat': 31.625964, 'lng': -7.989250
        },
        {
            'id': 2, 'name': 'クトゥビーヤ・モスク', 'city': 'マラケシュ', 'category': '宗教建築',
            'description': 'マラケシュのシンボル的存在。12世紀に建造された美しいミナレット',
            'features': ['12世紀建造', 'ミナレット', '歴史建築'], 'verified': True,
            'lat': 31.624307, 'lng': -7.993339
        },
        {
            'id': 3, 'name': 'バヒア宮殿', 'city': 'マラケシュ', 'category': '歴史建築',
            'description': '19世紀後期の豪華な宮殿。イスラム建築の装飾美を堪能できる',
            'features': ['19世紀宮殿', 'イスラム装飾', '庭園'], 'verified': True,
            'lat': 31.621522, 'lng': -7.983398
        },
        {
            'id': 4, 'name': 'マジョレル庭園', 'city': 'マラケシュ', 'category': '自然',
            'description': 'イヴ・サンローランが愛した美しい庭園。鮮やかな青色が印象的',
            'features': ['フランス式庭園', 'マジョレルブルー', '植物園'], 'verified': True,
            'lat': 31.640693, 'lng': -8.003176
        },
        
        # カサブランカ地域
        {
            'id': 5, 'name': 'ハッサン2世モスク', 'city': 'カサブランカ', 'category': '宗教建築',
            'description': '世界で2番目に大きなモスク。海に面した壮大な建築',
            'features': ['世界第2位', '海沿い', '現代建築'], 'verified': True,
            'lat': 33.608416, 'lng': -7.632767
        },
        {
            'id': 6, 'name': 'カサブランカ旧市街', 'city': 'カサブランカ', 'category': '都市・建築',
            'description': 'フランス植民地時代の建築と伝統的なメディナが混在',
            'features': ['植民地建築', 'アールデコ', '近代都市'], 'verified': True,
            'lat': 33.589886, 'lng': -7.603869
        },
        
        # フェズ地域
        {
            'id': 7, 'name': 'フェズ旧市街', 'city': 'フェズ', 'category': '歴史建築',
            'description': '世界最大の歩行者専用都市エリア。中世イスラム都市の完全な姿を保持',
            'features': ['世界遺産', '中世都市', '迷路'], 'verified': True, 'unesco': True,
            'lat': 34.063611, 'lng': -4.973056
        },
        {
            'id': 8, 'name': 'カラウィーン・モスク', 'city': 'フェズ', 'category': '宗教建築',
            'description': '世界最古の大学としても知られる859年創設のモスク',
            'features': ['859年創設', '世界最古大学', '学問の中心'], 'verified': True,
            'lat': 34.065278, 'lng': -4.974167
        },
        
        # その他の主要観光地
        {
            'id': 9, 'name': 'エルグ・シェビ砂丘', 'city': 'メルズーガ', 'category': '自然',
            'description': 'サハラ砂漠の最も美しい砂丘群。ラクダツアーの拠点',
            'features': ['サハラ砂漠', 'ラクダツアー', '星空観測'], 'verified': True,
            'lat': 31.099974, 'lng': -4.013986
        },
        {
            'id': 10, 'name': 'シャウエン旧市街', 'city': 'シャウエン', 'category': '都市・建築',
            'description': '青い街として世界的に有名な美しい山間の町',
            'features': ['青い建物', '山間の町', 'フォトスポット'], 'verified': True,
            'lat': 35.168796, 'lng': -5.263882
        }
    ]

def get_spot_details():
    """観光地詳細データを取得"""
    return {
        1: {
            'id': 1,
            'name': 'ジャマ・エル・フナ広場',
            'city': 'マラケシュ',
            'category': '広場・市場',
            'description': 'マラケシュの心臓部に位置する世界遺産の広場。夜市や大道芸人のパフォーマンスで有名',
            'longDescription': 'ジャマ・エル・フナ広場は、モロッコのマラケシュにある世界遺産に登録された歴史的な広場です。11世紀に建設されたこの広場は、「死者の集会所」という意味を持ち、古くから重要な公共スペースとして機能してきました。',
            'features': ['世界遺産', '夜市', 'パフォーマー', '伝統工芸', '屋台料理'],
            'verified': True,
            'unesco': True,
            'location': {
                'lat': 31.625964,
                'lng': -7.989250,
                'address': 'Place Jemaa el-Fnaa, Marrakech 40000, Morocco'
            },
            'hours': {
                'open': '24時間',
                'note': '夜のパフォーマンスは日没後から深夜まで'
            },
            'tips': [
                '夜のパフォーマンスは必見ですが、貴重品の管理にご注意ください',
                '屋台料理を楽しむ際は、信頼できる店舗を選びましょう',
                '価格交渉は当たり前なので、遠慮せずに交渉してください'
            ]
        },
        2: {
            'id': 2,
            'name': 'クトゥビーヤ・モスク',
            'city': 'マラケシュ',
            'category': '宗教建築',
            'description': 'マラケシュのシンボル的存在。12世紀に建造された美しいミナレット',
            'longDescription': 'クトゥビーヤ・モスクは、1150年から1195年にかけて建設されたマラケシュで最も重要なモスクです。高さ77メートルのミナレットは、アルモハード朝の建築様式の傑作とされています。',
            'features': ['12世紀建造', 'ミナレット', '歴史建築', 'アルモハード朝'],
            'verified': True,
            'location': {
                'lat': 31.624307,
                'lng': -7.993339,
                'address': 'Kutubiyya Mosque, Marrakech, Morocco'
            },
            'hours': {
                'open': '非ムスリムは外観のみ見学可能',
                'note': '夕日の時間帯が撮影に最適'
            },
            'tips': [
                '非ムスリムは内部に入ることはできませんが、外観の美しさは必見です',
                '夕日の時間帯は特に美しく、黄金色に輝くミナレットが撮影に最適です',
                '祈りの時間を尊重し、静かに見学しましょう'
            ]
        }
    }

@app.route('/api/spots')
def get_spots():
    """観光地一覧の取得"""
    try:
        spots = get_spots_data()
        return jsonify(spots)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/spots/<int:spot_id>')
def get_spot_detail(spot_id):
    """特定観光地の詳細情報取得"""
    try:
        spot_details = get_spot_details()
        
        if spot_id in spot_details:
            return jsonify(spot_details[spot_id])
        else:
            # 基本データから詳細を生成
            spots = get_spots_data()
            basic_spot = next((spot for spot in spots if spot['id'] == spot_id), None)
            
            if basic_spot:
                detailed_spot = {
                    'id': basic_spot['id'],
                    'name': basic_spot['name'],
                    'city': basic_spot['city'],
                    'category': basic_spot['category'],
                    'description': basic_spot['description'],
                    'longDescription': f"{basic_spot['description']} この場所は{basic_spot['city']}を代表する{basic_spot['category']}として多くの観光客に愛されています。",
                    'features': basic_spot.get('features', ['観光地', '文化体験']),
                    'verified': basic_spot.get('verified', False),
                    'location': {
                        'lat': basic_spot.get('lat', 0),
                        'lng': basic_spot.get('lng', 0)
                    },
                    'hours': {
                        'open': '営業時間については現地でご確認ください',
                        'note': '祝日や特別な日は営業時間が変更される場合があります'
                    },
                    'tips': [
                        '訪問前に営業時間を確認することをお勧めします',
                        '現地の文化と習慣を尊重しましょう',
                        '写真撮影は許可を取ってから行いましょう'
                    ]
                }
                return jsonify(detailed_spot)
            else:
                return jsonify({
                    'error': '観光地が見つかりません',
                    'message': f'ID {spot_id} の観光地は存在しません'
                }), 404
                
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/spots/recommended')
def get_recommended_spots():
    """おすすめ観光地の取得"""
    try:
        recommended = [
            {
                'id': 1,
                'name': 'ジャマ・エル・フナ広場',
                'city': 'マラケシュ',
                'category': '広場・市場',
                'description': 'マラケシュの心臓部に位置する世界遺産の広場',
                'verified': True,
                'unesco': True
            },
            {
                'id': 9,
                'name': 'エルグ・シェビ砂丘',
                'city': 'メルズーガ',
                'category': '自然',
                'description': 'サハラ砂漠の最も美しい砂丘群。ラクダツアーの拠点',
                'verified': True
            },
            {
                'id': 10,
                'name': 'シャウエン旧市街',
                'city': 'シャウエン',
                'category': '都市・建築',
                'description': '青い街として世界的に有名な美しい山間の町',
                'verified': True
            }
        ]
        return jsonify(recommended)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# =============================================================================
# ユーティリティ関数
# =============================================================================

def find_available_port(start_port=5000, max_tries=10):
    """利用可能なポートを見つける"""
    for port in range(start_port, start_port + max_tries):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            result = sock.connect_ex(('127.0.0.1', port))
            if result != 0:  # ポートが利用可能
                return port
        except:
            pass
        finally:
            sock.close()
    return start_port

# =============================================================================
# アプリケーション起動
# =============================================================================

if __name__ == '__main__':
    app = create_app()
    
    # 利用可能なポートを検索
    port = find_available_port()
    
    print(f"🌟 モロッコ観光ガイドアプリを起動中...")
    print(f"🌐 アクセス URL: http://localhost:{port}")
    print(f"🐍 Python環境: 仮想環境 (.venv)")
    print(f"📦 パッケージ: インストール完了")
    print(f"⭐ 準備完了！")
    
    app.run(
        host='127.0.0.1',
        port=port,
        debug=True
    )