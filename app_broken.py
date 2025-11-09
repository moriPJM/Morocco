"""
モロッコ観光ガイドアプリのメインアプリケーション - AI機能搭載
"""

import os
import socket
from flask import Flask, render_template, jsonify, request, session
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

# ルート定義
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
        gpt_service = get_morocco_gpt()
        answer = gpt_service.get_answer(question)
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'AI応答エラー'
        }), 500
            
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

    @app.route('/api/spots')
    def get_spots():
        """観光地一覧の取得"""
        try:
            # 実際のデータベースまたは外部APIからデータを取得
            # 現在はサンプルデータを返す
            spots = [
                # マラケシュ地域（大幅拡充）
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
                    'id': 4, 'name': 'サアード朝の墓群', 'city': 'マラケシュ', 'category': '歴史建築',
                    'description': '16世紀サアード朝の王族墓地。精緻な装飾が施された霊廟',
                    'features': ['16世紀', 'サアード朝', '霊廟'], 'verified': True,
                    'lat': 31.621836, 'lng': -7.987617
                },
                {
                    'id': 5, 'name': 'マラケシュ・スーク', 'city': 'マラケシュ', 'category': '広場・市場',
                    'description': '北アフリカ最大級の市場。伝統工芸品や香辛料などが所狭しと並ぶ',
                    'features': ['伝統市場', '工芸品', '香辛料'], 'verified': True,
                    'lat': 31.627853, 'lng': -7.988735
                },
                {
                    'id': 6, 'name': 'マジョレル庭園', 'city': 'マラケシュ', 'category': '自然',
                    'description': 'イヴ・サンローランが愛した美しい庭園。鮮やかな青色が印象的',
                    'features': ['フランス式庭園', 'マジョレルブルー', '植物園'], 'verified': True,
                    'lat': 31.640693, 'lng': -8.003176
                },
                {
                    'id': 7, 'name': 'エル・バディ宮殿', 'city': 'マラケシュ', 'category': '歴史建築',
                    'description': '16世紀の遺跡宮殿。往時の栄華を偲ばせる壮大な廃墟',
                    'features': ['16世紀遺跡', '宮殿廃墟', '歴史的価値'], 'verified': True,
                    'lat': 31.618989, 'lng': -7.986234
                },
                {
                    'id': 8, 'name': 'ベン・ユースフ・マドラサ', 'city': 'マラケシュ', 'category': '宗教建築',
                    'description': '14世紀の神学校。美しいイスラム装飾とアーチが特徴',
                    'features': ['14世紀神学校', 'イスラム装飾', '学問の場'], 'verified': True,
                    'lat': 31.630556, 'lng': -7.988889
                },
                {
                    'id': 9, 'name': 'メナラ庭園', 'city': 'マラケシュ', 'category': '自然',
                    'description': '12世紀から続く歴史ある庭園。オリーブ畑と貯水池が美しい',
                    'features': ['12世紀庭園', 'オリーブ畑', '貯水池'], 'verified': True,
                    'lat': 31.600000, 'lng': -8.016667
                },
                {
                    'id': 10, 'name': 'アグダル庭園', 'city': 'マラケシュ', 'category': '自然',
                    'description': 'ユネスコ世界遺産の巨大な庭園。アトラス山脈の眺望が素晴らしい',
                    'features': ['世界遺産', '巨大庭園', 'アトラス山脈眺望'], 'verified': True, 'unesco': True,
                    'lat': 31.609722, 'lng': -7.968333
                },
                {
                    'id': 11, 'name': 'マラケシュ博物館', 'city': 'マラケシュ', 'category': '博物館',
                    'description': '19世紀の宮殿を利用した博物館。モロッコの芸術と文化を展示',
                    'features': ['19世紀宮殿', 'モロッコ芸術', '文化展示'], 'verified': True,
                    'lat': 31.629167, 'lng': -7.988611
                },
                {
                    'id': 12, 'name': 'ダール・シ・サイド博物館', 'city': 'マラケシュ', 'category': '博物館',
                    'description': '伝統的なリヤド建築の博物館。モロッコの工芸品を展示',
                    'features': ['リヤド建築', '伝統工芸', '装飾芸術'], 'verified': True,
                    'lat': 31.622778, 'lng': -7.984167
                },

                # カサブランカ地域（大幅拡充）
                {
                    'id': 13, 'name': 'ハッサン2世モスク', 'city': 'カサブランカ', 'category': '宗教建築',
                    'description': '世界で2番目に大きなモスク。海に面した壮大な建築',
                    'features': ['世界第2位', '海沿い', '現代建築'], 'verified': True,
                    'lat': 33.608416, 'lng': -7.632767
                },
                {
                    'id': 14, 'name': 'カサブランカ旧市街（メディナ）', 'city': 'カサブランカ', 'category': '都市・建築',
                    'description': 'フランス植民地時代の建築と伝統的なメディナが混在',
                    'features': ['植民地建築', 'アールデコ', '近代都市'], 'verified': True,
                    'lat': 33.589886, 'lng': -7.603869
                },
                {
                    'id': 15, 'name': 'ハッビース地区', 'city': 'カサブランカ', 'category': '都市・建築',
                    'description': '1930年代に建設された新しいメディナ。伝統と現代の融合',
                    'features': ['1930年代', '新メディナ', '計画都市'], 'verified': True,
                    'lat': 33.594167, 'lng': -7.616111
                },
                {
                    'id': 16, 'name': 'ムハンマド5世広場', 'city': 'カサブランカ', 'category': '広場・市場',
                    'description': '市の中心部にある主要広場。政府機関や重要建物に囲まれる',
                    'features': ['中心広場', '政府機関', '都市の心臓部'], 'verified': True,
                    'lat': 33.595833, 'lng': -7.620556
                },
                {
                    'id': 17, 'name': 'カサブランカ大聖堂', 'city': 'カサブランカ', 'category': '宗教建築',
                    'description': 'フランス統治時代に建てられたネオゴシック様式の大聖堂',
                    'features': ['ネオゴシック', 'フランス統治時代', 'カトリック大聖堂'], 'verified': True,
                    'lat': 33.596944, 'lng': -7.621111
                },
                {
                    'id': 18, 'name': 'リック・カフェ', 'city': 'カサブランカ', 'category': '文化施設',
                    'description': '映画「カサブランカ」にちなんだ有名なカフェ・レストラン',
                    'features': ['映画ゆかりの地', 'カフェ文化', 'ハリウッド'], 'verified': True,
                    'lat': 33.594722, 'lng': -7.611944
                },
                {
                    'id': 19, 'name': 'カサブランカ・ツインセンター', 'city': 'カサブランカ', 'category': '都市・建築',
                    'description': 'カサブランカのランドマーク的な高層ビル。現代モロッコの象徴',
                    'features': ['現代建築', 'ランドマーク', 'ビジネス中心地'], 'verified': True,
                    'lat': 33.584722, 'lng': -7.631944
                },
                {
                    'id': 20, 'name': 'アンファ地区', 'city': 'カサブランカ', 'category': '都市・建築',
                    'description': '高級住宅街。美しいヴィラと緑豊かな街並み',
                    'features': ['高級住宅街', 'ヴィラ建築', '緑豊か'], 'verified': True,
                    'lat': 33.575000, 'lng': -7.645833
                },
                {
                    'id': 21, 'name': 'コルニッシュ海岸', 'city': 'カサブランカ', 'category': '自然',
                    'description': '大西洋沿いの美しい海岸線。散歩やジョギングに最適',
                    'features': ['大西洋海岸', '散歩道', 'レクリエーション'], 'verified': True,
                    'lat': 33.555556, 'lng': -7.666667
                },

                # フェズ地域（大幅拡充）
                {
                    'id': 22, 'name': 'フェズ旧市街（フェズ・エル・バリ）', 'city': 'フェズ', 'category': '歴史建築',
                    'description': '世界最大の歩行者専用都市エリア。中世イスラム都市の完全な姿を保持',
                    'features': ['世界遺産', '中世都市', '迷路'], 'verified': True, 'unesco': True,
                    'lat': 34.063611, 'lng': -4.973056
                },
                {
                    'id': 23, 'name': 'ブー・イナニア・マドラサ', 'city': 'フェズ', 'category': '宗教建築',
                    'description': '14世紀に建造された神学校。モロッコで最も美しい建築の一つ',
                    'features': ['14世紀建造', '神学校', 'イスラム装飾'], 'verified': True,
                    'lat': 34.067500, 'lng': -4.977500
                },
                {
                    'id': 24, 'name': 'カラウィーン・モスク', 'city': 'フェズ', 'category': '宗教建築',
                    'description': '世界最古の大学としても知られる859年創設のモスク',
                    'features': ['859年創設', '世界最古大学', '学問の中心'], 'verified': True,
                    'lat': 34.065278, 'lng': -4.974167
                },
                {
                    'id': 25, 'name': 'フェズの皮なめし場', 'city': 'フェズ', 'category': '伝統工芸',
                    'description': '1000年以上続く伝統的な皮革加工。カラフルな染色槽が有名',
                    'features': ['1000年の伝統', '皮革加工', 'カラフル'], 'verified': True,
                    'lat': 34.070833, 'lng': -4.971944
                },
                {
                    'id': 26, 'name': 'ダール・バタ博物館', 'city': 'フェズ', 'category': '博物館',
                    'description': '19世紀の宮殿を利用したモロッコ伝統工芸博物館',
                    'features': ['19世紀宮殿', '伝統工芸', '博物館'], 'verified': True,
                    'lat': 34.063889, 'lng': -4.975000
                },
                {
                    'id': 27, 'name': 'アッタリン・マドラサ', 'city': 'フェズ', 'category': '宗教建築',
                    'description': '14世紀の神学校。精緻なゼリージュ装飾で有名',
                    'features': ['14世紀神学校', 'ゼリージュ装飾', '精緻な装飾'], 'verified': True,
                    'lat': 34.065556, 'lng': -4.974722
                },
                {
                    'id': 28, 'name': 'ネジャリン博物館', 'city': 'フェズ', 'category': '博物館',
                    'description': '木工芸に特化した博物館。17世紀のフォンドゥークを利用',
                    'features': ['木工芸専門', '17世紀フォンドゥーク', '職人技術'], 'verified': True,
                    'lat': 34.066944, 'lng': -4.976111
                },
                {
                    'id': 29, 'name': 'フェズ・エル・ジェディド', 'city': 'フェズ', 'category': '歴史建築',
                    'description': '13世紀に建設された「新しいフェズ」。王宮がある地区',
                    'features': ['13世紀建設', '王宮地区', '新フェズ'], 'verified': True,
                    'lat': 34.050000, 'lng': -4.983333
                },
                {
                    'id': 30, 'name': 'ボルジュ・ノール要塞', 'city': 'フェズ', 'category': '歴史建築',
                    'description': '16世紀の要塞。フェズの街を一望できる絶景ポイント',
                    'features': ['16世紀要塞', '絶景ポイント', '街全体眺望'], 'verified': True,
                    'lat': 34.071111, 'lng': -4.964444
                },
                {
                    'id': 31, 'name': 'ボルジュ・スッド要塞', 'city': 'フェズ', 'category': '歴史建築',
                    'description': '16世紀の南の要塞。現在は武器博物館として利用',
                    'features': ['16世紀要塞', '武器博物館', '軍事遺産'], 'verified': True,
                    'lat': 34.059722, 'lng': -4.964167
                },
                {
                    'id': 32, 'name': 'サヘリジ貯水池', 'city': 'フェズ', 'category': '歴史建築',
                    'description': '14世紀の巨大な貯水池。都市の水供給システムの歴史的遺産',
                    'features': ['14世紀建設', '巨大貯水池', '水利システム'], 'verified': True,
                    'lat': 34.075000, 'lng': -4.986111
                },

                # その他の主要観光地
                {
                    'id': 33, 'name': 'エルグ・シェビ砂丘', 'city': 'メルズーガ', 'category': '自然',
                    'description': 'サハラ砂漠の最も美しい砂丘群。ラクダツアーの拠点',
                    'features': ['サハラ砂漠', 'ラクダツアー', '星空観測'], 'verified': True,
                    'lat': 31.099974, 'lng': -4.013986
                },
                {
                    'id': 34, 'name': 'シャウエン旧市街', 'city': 'シャウエン', 'category': '都市・建築',
                    'description': '青い街として世界的に有名な美しい山間の町',
                    'features': ['青い建物', '山間の町', 'フォトスポット'], 'verified': True,
                    'lat': 35.168796, 'lng': -5.263882
                },
                {
                    'id': 35, 'name': 'エッサウィラ旧市街', 'city': 'エッサウィラ', 'category': '都市・建築',
                    'description': '大西洋に面した美しい港町。18世紀の城壁に囲まれた旧市街',
                    'features': ['世界遺産', '港町', '城壁'], 'verified': True, 'unesco': True,
                    'lat': 31.513048, 'lng': -9.759789
                }
            ]
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
            # 実際のデータベースから該当IDの詳細データを取得
            # 現在はサンプルデータを返す
            spot_details = {
                # マラケシュの観光地詳細
                1: {
                    'id': 1,
                    'name': 'ジャマ・エル・フナ広場',
                    'city': 'マラケシュ',
                    'category': '広場・市場',
                    'description': 'マラケシュの心臓部に位置する世界遺産の広場。日中は屋台や土産物店が並び、夜になると大道芸人やミュージシャンが集まり賑やかな雰囲気を楽しめます。',
                    'longDescription': 'ジャマ・エル・フナ広場は、モロッコのマラケシュにある世界遺産に登録された歴史的な広場です。11世紀に建設されたこの広場は、「死者の集会所」という意味を持ち、古くから重要な公共スペースとして機能してきました。昼間は様々な屋台や土産物店、伝統工芸品を売る商人たちで賑わい、夜になると音楽家、大道芸人、語り部などが集まって独特の文化的な空間を作り出します。この広場は、無形文化遺産としても登録されており、口承による物語の伝統「ハルカ」の聖地としても知られています。',
                    'features': ['世界遺産', '夜市', 'パフォーマー', '伝統工芸', '屋台料理', '無形文化遺産', 'ハルカ（物語の輪）'],
                    'verified': True,
                    'unesco': True,
                    'location': {
                        'lat': 31.625964,
                        'lng': -7.989250,
                        'address': 'Place Jemaa el-Fnaa, Marrakech 40000, Morocco'
                    },
                    'hours': {
                        'open': '24時間',
                        'note': '夜のパフォーマンスは日没後から深夜まで。最も活気があるのは19:00-23:00'
                    },
                    'access': {
                        'walking': 'マラケシュ駅から徒歩約20分、メディナの中心部',
                        'taxi': 'タクシーで市内中心部まで約10分（約20-30ディルハム）',
                        'bus': '市内バス6番、8番でJemaa el-Fnaa下車',
                        'car': '広場周辺には有料駐車場あり（1時間5ディルハム）'
                    },
                    'tips': [
                        '夜のパフォーマンスは必見ですが、貴重品の管理にご注意ください',
                        '屋台料理を楽しむ際は、信頼できる店舗を選びましょう',
                        '価格交渉は当たり前なので、遠慮せずに交渉してください',
                        '写真撮影は事前に許可を取り、チップを渡すのが礼儀です',
                        'ヘナタトゥーは一時的なものですが、アレルギーの確認を',
                        '夜は気温が下がるので、軽い羽織物を持参することをお勧めします'
                    ],
                    'nearbySpots': [
                        {'name': 'クトゥビア・モスク', 'distance': '200m', 'category': '宗教建築'},
                        {'name': 'マラケシュスーク', 'distance': '50m', 'category': '広場・市場'},
                        {'name': 'バヒア宮殿', 'distance': '1.2km', 'category': '歴史建築'}
                    ],
                    'bestTime': '夕方から夜にかけて（18:00-22:00）が最も活気があります。日中の暑さを避けて朝早く（7:00-9:00）の散策もおすすめ。',
                    'activities': '大道芸鑑賞、ヘナタトゥー体験、民族音楽・ダンス鑑賞、屋台グルメ巡り、伝統工芸品ショッピング、語り部の物語鑑賞',
                    'shopping': 'スパイス、アルガンオイル、ベルベル絨毯、革製品、陶器、銀製品、伝統衣装、モロッコランプ',
                    'photoSpots': '広場を見下ろすカフェのテラス席からの俯瞰撮影、夜のライトアップ、パフォーマーとの記念撮影',
                    'history': '11世紀のアルモラビッド朝時代に建設。「ジャマ・エル・フナ」は「死者の集会所」を意味し、かつては公開処刑場としても使用されていました。',
                    'culturalSignificance': 'モロッコの口承文化の中心地として、ユネスコ無形文化遺産に登録。ハルカ（物語の輪）の伝統が今も受け継がれています。',
                    'architecture': '広場自体は建築物ではありませんが、周囲を囲む伝統的なリヤド建築とモスクが調和した美しい景観を形成しています。'
                },
                2: {
                    'id': 2,
                    'name': 'クトゥビーヤ・モスク',
                    'city': 'マラケシュ',
                    'category': '宗教建築',
                    'description': 'マラケシュのシンボル的存在。12世紀に建造された美しいミナレット',
                    'longDescription': 'クトゥビーヤ・モスクは、1150年から1195年にかけて建設されたマラケシュで最も重要なモスクです。高さ77メートルのミナレットは、アルモハード朝の建築様式の傑作とされ、後のセビリアのヒラルダやラバトのハッサンの塔のモデルとなりました。「書店のモスク」という意味の名前は、かつてこの場所に多くの写本を扱う店があったことに由来します。ミナレットは遠く40km先からも見ることができ、砂漠の商人たちの道標としても機能していました。',
                    'features': ['12世紀建造', 'ミナレット', '歴史建築', 'アルモハード朝', 'イスラム芸術', '道標機能'],
                    'verified': True,
                    'location': {
                        'lat': 31.624307,
                        'lng': -7.993339,
                        'address': 'Kutubiyya Mosque, Marrakech, Morocco'
                    },
                    'hours': {
                        'open': '非ムスリムは外観のみ見学可能',
                        'note': '金曜日の祈りの時間（12:00-14:00）は避けることを推奨。夕日の時間帯（18:00-19:00）が撮影に最適。'
                    },
                    'access': {
                        'walking': 'ジャマ・エル・フナ広場から徒歩3分、非常にアクセス良好',
                        'taxi': '市内中心部からタクシーで5分',
                        'bus': '最寄りバス停「Koutoubia」から徒歩1分'
                    },
                    'tips': [
                        '非ムスリムは内部に入ることはできませんが、外観の美しさは必見です',
                        '夕日の時間帯は特に美しく、黄金色に輝くミナレットが撮影に最適です',
                        '祈りの時間を尊重し、静かに見学しましょう',
                        '近くのクトゥビーヤ庭園から全体を眺めることができます',
                        'ライトアップされた夜の姿も一見の価値があります',
                        '周辺の土産物店では、モスクをモチーフにした工芸品が購入できます'
                    ],
                    'nearbySpots': [
                        {'name': 'ジャマ・エル・フナ広場', 'distance': '200m', 'category': '広場・市場'},
                        {'name': 'クトゥビーヤ庭園', 'distance': '50m', 'category': '自然'},
                        {'name': 'マラケシュ・スーク', 'distance': '300m', 'category': '広場・市場'}
                    ],
                    'bestTime': '夕日の時間帯（17:30-18:30）と夜のライトアップ（19:00以降）が特におすすめ。',
                    'architecture': 'アルモハード様式の傑作。ミナレットは4面とも異なる装飾が施され、セビーク（乾燥煉瓦）とローズピンクの石で建設。',
                    'history': '1150年にアルモハード朝のアブド・アル＝ムーミンによって建設開始。2代目ミナレットとして現在の姿に。',
                    'culturalSignificance': 'イスラム建築の最高傑作の一つ。後のイベリア半島のイスラム建築に大きな影響を与えた。',
                    'photoSpots': 'クトゥビーヤ庭園からの全景、夕日バックのシルエット撮影、ライトアップされた夜景'
                },
                3: {
                    'id': 3,
                    'name': 'バヒア宮殿',
                    'city': 'マラケシュ',
                    'category': '歴史建築',
                    'description': '19世紀後期の豪華な宮殿。イスラム建築の装飾美を堪能できる',
                    'longDescription': 'バヒア宮殿は、19世紀後期にマラケシュの大宰相バ・アーマドによって建設された豪華な宮殿です。「美しい人」を意味するバヒアという名前は、彼の最愛の妃に捧げられたとされています。150の部屋と中庭、リヤドを持つこの宮殿は、モロッコ・アンダルシア建築の傑作とされ、精緻なゼリージュ（モザイクタイル）、彫刻、彩色天井などの装飾が見どころです。8ヘクタールの敷地に広がる宮殿は、当時のモロッコ貴族の豪華な生活様式を物語っています。',
                    'features': ['19世紀宮殿', 'イスラム装飾', '庭園', 'ゼリージュ', 'アンダルシア様式', '150の部屋', '8ヘクタール'],
                    'verified': True,
                    'location': {
                        'lat': 31.621522,
                        'lng': -7.983398,
                        'address': 'Palais Bahia, Marrakech, Morocco'
                    },
                    'hours': {
                        'open': '9:00-17:00（夏季は18:00まで）',
                        'note': '金曜日は13:00-14:30の祈りの時間は閉館。入場は閉館30分前まで。'
                    },
                    'access': {
                        'walking': 'ジャマ・エル・フナ広場から徒歩15分、メディナ南部',
                        'taxi': 'タクシーでBab Agnaou門まで、そこから徒歩5分',
                        'bus': '市内バス利用、最寄り停留所から徒歩10分',
                        'car': '近くに有料駐車場あり（1日20ディルハム）'
                    },
                    'tips': [
                        '入場料が必要です（70ディルハム、学生割引あり）',
                        '午前中の早い時間（9:00-11:00）は観光客が少なくおすすめ',
                        '装飾の細部をじっくり観察してください。職人の技術の高さに驚きます',
                        '中庭の光と影のコントラストが美しい写真スポットです',
                        '音声ガイド（英語・フランス語・アラビア語）の利用がおすすめ',
                        '庭園のオレンジの木とバラの香りも楽しめます'
                    ],
                    'nearbySpots': [
                        {'name': 'サアード朝の墓群', 'distance': '300m', 'category': '歴史建築'},
                        {'name': 'エル・バディ宮殿', 'distance': '400m', 'category': '歴史建築'},
                        {'name': 'ジャマ・エル・フナ広場', 'distance': '1.2km', 'category': '広場・市場'}
                    ],
                    'bestTime': '午前中の自然光が装飾を美しく照らします。春（3-5月）は庭園の花が咲き誇ります。',
                    'architecture': 'モロッコ・アンダルシア様式の傑作。ゼリージュ、タデラクト（漆喰）、木工細工の三位一体。',
                    'history': '1880年代、大宰相バ・アーマドが愛妃バヒアのために建設。フランス統治時代は総督府として使用。',
                    'culturalSignificance': '19世紀モロッコ宮廷文化の最高峰。イスラム芸術とアンダルシア文化の融合の象徴。',
                    'activities': '建築装飾鑑賞、庭園散策、写真撮影、音声ガイドツアー',
                    'photoSpots': '大中庭の噴水、ゼリージュの細工、彩色天井、アーチの連続、庭園のオレンジの木'
                },
                
                # カサブランカの観光地詳細を追加
                13: {
                    'id': 13,
                    'name': 'ハッサン2世モスク',
                    'city': 'カサブランカ',
                    'category': '宗教建築',
                    'description': '世界で2番目に大きなモスク。海に面した壮大な建築',
                    'longDescription': 'ハッサン2世モスクは1993年に完成した、世界で2番目に高いミナレット（高さ210m）を持つ壮大なモスクです。大西洋に面した立地で、一部は海の上に建設されています。2万5千人が同時に祈ることができ、さらに8万人が外の中庭で祈ることができる巨大な規模を誇ります。フランスの建築家ミシェル・ピンソーが設計し、モロッコの伝統的な建築技術と現代技術を融合させた傑作です。建設には世界中から集められた最高級の素材が使用され、3万人の職人と技術者が7年間かけて完成させました。',
                    'features': ['世界第2位', '海沿い', '現代建築', '巨大ミナレット', '最新技術', '国際的職人技術', '7年建設'],
                    'verified': True,
                    'location': {
                        'lat': 33.608416,
                        'lng': -7.632767,
                        'address': 'Hassan II Mosque, Casablanca, Morocco'
                    },
                    'hours': {
                        'open': 'ガイドツアー：9:00, 10:00, 11:00, 14:00, 15:00, 16:00',
                        'note': '金曜日は14:00からのみ。祈りの時間中は見学不可。土曜日は追加ツアーあり。'
                    },
                    'access': {
                        'tram': 'カサトラム1号線「Hassan II」駅下車、徒歩5分',
                        'taxi': 'カサブランカ市内中心部からタクシーで15分（約50ディルハム）',
                        'bus': '市内バス9番・10番利用可能',
                        'car': '専用駐車場完備（無料）'
                    },
                    'tips': [
                        '非ムスリムも内部見学可能（ガイドツアーのみ、120ディルハム）',
                        '海に面した壮大な外観は夕日の時間が最も美しい',
                        '入場券は事前にオンライン予約がおすすめ',
                        '服装規定：長袖・長ズボン、女性はヘッドスカーフ必要',
                        'ツアーは英語・フランス語・アラビア語で実施',
                        '内部撮影は制限があるため、ガイドの指示に従ってください'
                    ],
                    'nearbySpots': [
                        {'name': 'コルニッシュ海岸', 'distance': '1km', 'category': '自然'},
                        {'name': 'カサブランカ旧市街', 'distance': '3km', 'category': '都市・建築'},
                        {'name': 'ムハンマド5世広場', 'distance': '4km', 'category': '広場・市場'}
                    ],
                    'bestTime': '夕日の時間帯（17:00-18:30）の外観撮影。午前中のツアーは比較的空いています。',
                    'architecture': '現代イスラム建築の傑作。イタリア産大理石、チタン屋根、レーザー光線で方向を示すハイテク設備。',
                    'history': 'ハッサン2世国王の発案で1987年建設開始。国民の寄付により建設費を調達。',
                    'culturalSignificance': '現代モロッコのイスラム建築技術の粋。伝統と革新の融合の象徴。',
                    'activities': 'ガイドツアー参加、建築撮影、夕日鑑賞、近くのビーチ散策',
                    'shopping': 'モスク併設のギフトショップで宗教関連書籍、絵葉書、記念品',
                    'photoSpots': '海岸からの全景、ミナレットのアップ、夕日バックのシルエット、内部のシャンデリア'
                },

                # フェズの観光地詳細を追加
                22: {
                    'id': 22,
                    'name': 'フェズ旧市街（フェズ・エル・バリ）',
                    'city': 'フェズ',
                    'category': '歴史建築',
                    'description': '世界最大の歩行者専用都市エリア。中世イスラム都市の完全な姿を保持',
                    'longDescription': 'フェズ・エル・バリは、808年にイドリース朝によって建設された世界最古の中世都市の一つです。ユネスコ世界遺産に登録されており、9,400の小径と路地、30万人の住民を抱える世界最大の歩行者専用都市エリアです。1200年以上の歴史を持つこの迷路のような旧市街には、モスク、マドラサ（神学校）、宮殿、噴水、そして伝統的な住居が当時のまま保存されています。340のモスクと神学校、200のハンマム（公衆浴場）、数千の工房が現在も稼働しており、生きた中世都市として機能し続けています。',
                    'features': ['世界遺産', '中世都市', '迷路', '1200年の歴史', '伝統建築', '9400の路地', '30万住民'],
                    'verified': True,
                    'unesco': True,
                    'location': {
                        'lat': 34.063611,
                        'lng': -4.973056,
                        'address': 'Fes el-Bali, Fez, Morocco'
                    },
                    'hours': {
                        'open': '24時間（個別施設は異なる）',
                        'note': '金曜日の祈りの時間（12:00-14:00）は一部施設が閉鎖。夜間の一人歩きは避けることを推奨。'
                    },
                    'access': {
                        'walking': 'フェズ駅からタクシーでBab Boujeloud門まで15分、そこから徒歩',
                        'taxi': '主要な門（Bab Boujeloud, Bab Rcif）までタクシー利用（約30ディルハム）',
                        'bus': '市内バスでBab Boujeloud門へ（5ディルハム）',
                        'car': '門の外に有料駐車場あり（1日30ディルハム）'
                    },
                    'tips': [
                        '迷子になりやすいので、公認ガイドの利用を強く推奨します（1日500ディルハム）',
                        '歩きやすい靴での訪問が必要です。石畳で滑りやすい箇所もあります',
                        '商店での価格交渉は一般的です。最初の提示価格の1/3程度から交渉開始',
                        '写真撮影前に許可を取ることをお勧めします。特に人物撮影時',
                        '狭い路地では荷物を運ぶロバやラバに注意してください',
                        '現金を多めに準備。ほとんどの店でカードは使えません'
                    ],
                    'nearbySpots': [
                        {'name': 'ブー・イナニア・マドラサ', 'distance': '200m', 'category': '宗教建築'},
                        {'name': 'カラウィーン・モスク', 'distance': '300m', 'category': '宗教建築'},
                        {'name': 'フェズの皮なめし場', 'distance': '400m', 'category': '伝統工芸'}
                    ],
                    'bestTime': '午前中（8:00-12:00）は涼しく、工房の活動も活発。夕方（16:00-18:00）の散策も快適。',
                    'activities': 'ガイドツアー、伝統工芸見学、スーク散策、マドラサ見学、皮なめし場見学、ハンマム体験',
                    'shopping': '革製品、陶器、金属工芸品、絨毯、スパイス、アルガンオイル、伝統衣装、手工芸品',
                    'architecture': 'イスラム建築の宝庫。マリーン朝、サアド朝、アラウィー朝の各時代の建築様式が混在。',
                    'history': '808年にイドリース2世により建設。イスラム世界の重要な学問・商業中心地として栄えた。',
                    'culturalSignificance': '中世イスラム都市の完全な形を保持する唯一の都市。生きた文化遺産として機能。',
                    'photoSpots': 'Bab Boujeloud門、路地の迷路風景、工房での職人作業、モスクのミナレット群'
                }
            }

            # ID に該当する詳細データがあるかチェック
            if spot_id in spot_details:
                return jsonify(spot_details[spot_id])
            else:
                # 基本データから動的に詳細を生成
                basic_spot = next((spot for spot in spots if spot['id'] == spot_id), None)
                if basic_spot:
                    # より詳細な情報を自動生成
                    detailed_spot = {
                        'id': basic_spot['id'],
                        'name': basic_spot['name'],
                        'city': basic_spot['city'],
                        'category': basic_spot['category'],
                        'description': basic_spot['description'],
                        'longDescription': f"{basic_spot['description']} この場所は{basic_spot['city']}を代表する{basic_spot['category']}として多くの観光客に愛されています。",
                        'features': ['観光地', '文化体験', '見学可能'],
                        'verified': basic_spot.get('verified', False),
                        'location': basic_spot.get('location', {}),
                        'hours': {
                            'open': '営業時間については現地でご確認ください',
                            'note': '祝日や特別な日は営業時間が変更される場合があります'
                        },
                        'access': {
                            'note': '詳細なアクセス方法については現地の案内をご確認ください'
                        },
                        'tips': [
                            '訪問前に営業時間を確認することをお勧めします',
                            '現地の文化と習慣を尊重しましょう',
                            '写真撮影は許可を取ってから行いましょう'
                        ],
                        'bestTime': '訪問に最適な時間帯については現地情報をご確認ください',
                        'activities': '見学、写真撮影、文化体験'
                    }
                    return jsonify(detailed_spot)
                else:
                    return jsonify({
                        'error': '観光地が見つかりません',
                        'message': f'ID {spot_id} の観光地は存在しません'
                    }), 404
                        'taxi': '市内中心部からタクシーで5分',
                        'bus': '最寄りバス停「Koutoubia」'
                    },
                    'tips': [
                        '非ムスリムは内部に入ることはできません',
                        '夕日の時間帯は特に美しく撮影に最適です',
                        '祈りの時間を尊重し、静かに見学しましょう',
                        '近くの庭園から全体を眺めることができます'
                    ],
                    'nearbySpots': [
                        {'name': 'ジャマ・エル・フナ広場', 'distance': '200m', 'category': '広場・市場'},
                        {'name': 'クトゥビーヤ庭園', 'distance': '50m', 'category': '自然'},
                        {'name': 'マラケシュ・スーク', 'distance': '300m', 'category': '市場'}
                    ]
                },
                3: {
                    'id': 3,
                    'name': 'バヒア宮殿',
                    'city': 'マラケシュ',
                    'category': '歴史建築',
                    'description': '19世紀後期の豪華な宮殿。イスラム建築の装飾美を堪能できる',
                    'longDescription': 'バヒア宮殿は、19世紀後期にマラケシュの大宰相バ・アーマドによって建設された豪華な宮殿です。「美しい人」を意味するバヒアという名前は、彼の最愛の妃に捧げられたとされています。150の部屋と中庭、リヤドを持つこの宮殿は、モロッコ・アンダルシア建築の傑作とされ、精緻なゼリージュ（モザイクタイル）、彫刻、彩色天井などの装飾が見どころです。',
                    'features': ['19世紀宮殿', 'イスラム装飾', '庭園', 'ゼリージュ', 'アンダルシア様式'],
                    'verified': True,
                    'location': {
                        'lat': 31.621522,
                        'lng': -7.983398,
                        'address': 'Palais Bahia, Marrakech, Morocco'
                    },
                    'hours': {
                        'open': '9:00-17:00',
                        'note': '金曜日は13:00-14:30の祈りの時間は閉館'
                    },
                    'access': {
                        'walking': 'ジャマ・エル・フナ広場から徒歩15分',
                        'taxi': 'タクシーでBab Agnaou門まで、そこから徒歩5分',
                        'bus': '市内バス利用、最寄り停留所から徒歩10分'
                    },
                    'tips': [
                        '入場料が必要です（現地通貨でのお支払いを推奨）',
                        '午前中の早い時間は観光客が少なくおすすめ',
                        '装飾の細部をじっくり観察してください',
                        '中庭の光と影のコントラストが美しい写真スポットです'
                    ],
                    'nearbySpots': [
                        {'name': 'サアード朝の墓群', 'distance': '300m', 'category': '歴史建築'},
                        {'name': 'エル・バディ宮殿', 'distance': '400m', 'category': '歴史建築'},
                        {'name': 'ジャマ・エル・フナ広場', 'distance': '1.2km', 'category': '広場・市場'}
                    ]
                },
                
                # カサブランカの観光地詳細
                13: {
                    'id': 13,
                    'name': 'ハッサン2世モスク',
                    'city': 'カサブランカ',
                    'category': '宗教建築',
                    'description': '世界で2番目に大きなモスク。海に面した壮大な建築',
                    'longDescription': 'ハッサン2世モスクは1993年に完成した、世界で2番目に高いミナレット（高さ210m）を持つ壮大なモスクです。大西洋に面した立地で、一部は海の上に建設されています。2万5千人が同時に祈ることができ、さらに8万人が外の中庭で祈ることができる巨大な規模を誇ります。フランスの建築家ミシェル・ピンソーが設計し、モロッコの伝統的な建築技術と現代技術を融合させた傑作です。',
                    'features': ['世界第2位', '海沿い', '現代建築', '巨大ミナレット', '最新技術'],
                    'verified': True,
                    'location': {
                        'lat': 33.608416,
                        'lng': -7.632767,
                        'address': 'Hassan II Mosque, Casablanca, Morocco'
                    },
                    'hours': {
                        'open': 'ガイドツアー：9:00, 10:00, 11:00, 14:00, 15:00',
                        'note': '金曜日は14:00からのみ。祈りの時間中は見学不可'
                    },
                    'access': {
                        'tram': 'カサトラム1号線「Hassan II」駅下車',
                        'taxi': 'カサブランカ市内中心部からタクシーで15分',
                        'bus': '市内バス利用可能、複数路線が利用可能'
                    },
                    'tips': [
                        '非ムスリムも内部見学可能（ガイドツアーのみ）',
                        '海に面した壮大な外観は夕日の時間が最も美しい',
                        '入場券は事前購入を推奨します',
                        '服装規定があるので、控えめな服装で訪問してください'
                    ],
                    'nearbySpots': [
                        {'name': 'コルニッシュ海岸', 'distance': '1km', 'category': '自然'},
                        {'name': 'カサブランカ旧市街', 'distance': '3km', 'category': '都市・建築'},
                        {'name': 'ムハンマド5世広場', 'distance': '4km', 'category': '広場・市場'}
                    ]
                },

                # フェズの観光地詳細  
                22: {
                    'id': 22,
                    'name': 'フェズ旧市街（フェズ・エル・バリ）',
                    'city': 'フェズ',
                    'category': '歴史建築',
                    'description': '世界最大の歩行者専用都市エリア。中世イスラム都市の完全な姿を保持',
                    'longDescription': 'フェズ・エル・バリは、808年にイドリース朝によって建設された世界最古の中世都市の一つです。ユネスコ世界遺産に登録されており、9,400の小径と路地、30万人の住民を抱える世界最大の歩行者専用都市エリアです。1200年以上の歴史を持つこの迷路のような旧市街には、モスク、マドラサ（神学校）、宮殿、噴水、そして伝統的な住居が当時のまま保存されています。',
                    'features': ['世界遺産', '中世都市', '迷路', '1200年の歴史', '伝統建築'],
                    'verified': True,
                    'unesco': True,
                    'location': {
                        'lat': 34.063611,
                        'lng': -4.973056,
                        'address': 'Fes el-Bali, Fez, Morocco'
                    },
                    'hours': {
                        'open': '24時間（個別施設は異なる）',
                        'note': '金曜日の祈りの時間は一部施設が閉鎖'
                    },
                    'access': {
                        'walking': 'フェズ駅からタクシーでBab Boujeloud門まで、そこから徒歩',
                        'taxi': '主要な門（Bab Boujeloud, Bab Rcif）までタクシー利用',
                        'bus': '市内バスでBab Boujeloud門へ'
                    },
                    'tips': [
                        '迷子になりやすいので、ガイドの利用を推奨します',
                        '歩きやすい靴での訪問が必要です',
                        '商店での価格交渉は一般的です',
                        '写真撮影前に許可を取ることをお勧めします'
                    ],
                    'nearbySpots': [
                        {'name': 'ブー・イナニア・マドラサ', 'distance': '200m', 'category': '宗教建築'},
                        {'name': 'カラウィーン・モスク', 'distance': '300m', 'category': '宗教建築'},
                        {'name': 'フェズの皮なめし場', 'distance': '400m', 'category': '伝統工芸'}
                    ]
                }
            }
            
            if spot_id in spot_details:
                return jsonify(spot_details[spot_id])
            else:
                return jsonify({
                    'success': False,
                    'error': '観光地が見つかりません'
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
            # おすすめの観光地リストを返す
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
                    'id': 22,
                    'name': 'エルグ・シェビ砂丘',
                    'city': 'メルズーガ',
                    'category': '自然',
                    'description': 'サハラ砂漠の最も美しい砂丘群。ラクダツアーの拠点',
                    'verified': True
                },
                {
                    'id': 19,
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
    
    return app

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