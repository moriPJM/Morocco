"""
モロッコ観光ガイドアプリのメインアプリケーション - AI機能搭載
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

@app.route('/spot/<int:spot_id>')
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

@app.route('/favicon.ico')
def favicon():
    """Faviconを提供"""
    return app.send_static_file('images/favicon.svg')

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

@app.route('/api/ai/suggestions')
def ai_suggestions():
    """おすすめ質問を取得"""
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
            'error': str(e),
            'suggestions': [
                "マラケシュでおすすめの観光スポットは？",
                "モロッコ料理で絶対食べるべきものは？",
                "サハラ砂漠ツアーについて教えて",
                "3日間でモロッコを回るプランを提案して",
                "モロッコ旅行の予算はいくら必要？"
            ]
        })

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
        result = gpt_service.get_morocco_guide_response(question)
        
        if result['success']:
            return jsonify({
                'success': True,
                'question': question,
                'response': result['response'],  # answerからresponseに変更
                'usage': result.get('usage'),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'AI応答エラー'),
                'response': result['response'],
                'timestamp': datetime.now().isoformat()
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'AI応答エラー'
        }), 500

# 観光地データ
SPOTS_DATA = [
    # マラケシュの観光地（12箇所）
    {
        'id': 1,
        'name': 'ジャマ・エル・フナ広場',
        'city': 'マラケシュ',
        'category': '広場・市場',
        'description': 'マラケシュの心臓部に位置する世界遺産の広場。日中は屋台や土産物店が並び、夜になると大道芸人やミュージシャンが集まり賑やかな雰囲気を楽しめます。',
        'verified': True,
        'location': {'lat': 31.625964, 'lng': -7.989250}
    },
    {
        'id': 2,
        'name': 'クトゥビーヤ・モスク',
        'city': 'マラケシュ',
        'category': '宗教建築',
        'description': 'マラケシュのシンボル的存在。12世紀に建造された美しいミナレット（高さ77m）で、街のどこからでも見ることができる目印です。',
        'verified': True,
        'location': {'lat': 31.624307, 'lng': -7.993339}
    },
    {
        'id': 3,
        'name': 'バヒア宮殿',
        'city': 'マラケシュ',
        'category': '歴史建築',
        'description': '19世紀後期の豪華な宮殿。イスラム建築の装飾美を堪能でき、精緻なゼリージュ（モザイクタイル）や美しい庭園が見どころです。',
        'verified': True,
        'location': {'lat': 31.621522, 'lng': -7.983398}
    },
    {
        'id': 4,
        'name': 'マラケシュ・スーク',
        'city': 'マラケシュ',
        'category': '広場・市場',
        'description': 'モロッコ最大級の伝統市場。革製品、絨毯、香辛料、工芸品など様々な商品が売られ、価格交渉も楽しめます。',
        'verified': True,
        'location': {'lat': 31.629472, 'lng': -7.989444}
    },
    {
        'id': 5,
        'name': 'サアード朝の墓群',
        'city': 'マラケシュ',
        'category': '歴史建築',
        'description': '16世紀サアード朝の王族の霊廟。精緻な装飾と美しい庭園で知られ、300年間封印されていた歴史的建造物です。',
        'verified': True,
        'location': {'lat': 31.620278, 'lng': -7.986389}
    },
    {
        'id': 6,
        'name': 'マジョレル庭園',
        'city': 'マラケシュ',
        'category': '自然',
        'description': 'フランス人画家ジャック・マジョレルが造った美しい庭園。後にイヴ・サンローランが所有し、今も多くの観光客に愛されています。',
        'verified': True,
        'location': {'lat': 31.641389, 'lng': -7.996111}
    },
    {
        'id': 7,
        'name': 'エル・バディ宮殿',
        'city': 'マラケシュ',
        'category': '歴史建築',
        'description': '16世紀サアード朝の壮大な宮殿跡。現在は廃墟となっていますが、当時の栄華を偲ばせる巨大な建造物です。',
        'verified': True,
        'location': {'lat': 31.620833, 'lng': -7.984167}
    },
    {
        'id': 8,
        'name': 'メナラ庭園',
        'city': 'マラケシュ',
        'category': '自然',
        'description': '12世紀に造られた広大な庭園。オリーブの木々と大きな貯水池があり、アトラス山脈を背景にした美しい景色が楽しめます。',
        'verified': True,
        'location': {'lat': 31.605556, 'lng': -8.017222}
    },
    {
        'id': 9,
        'name': 'ベン・ユーセフ・マドラサ',
        'city': 'マラケシュ',
        'category': '宗教建築',
        'description': '14世紀に建てられた神学校。美しいイスラム装飾と中庭で知られ、北アフリカ最大のマドラサの一つです。',
        'verified': True,
        'location': {'lat': 31.631944, 'lng': -7.988056}
    },
    {
        'id': 10,
        'name': 'マラケシュ博物館',
        'city': 'マラケシュ',
        'category': '博物館',
        'description': '19世紀の宮殿を改装した博物館。モロッコの伝統工芸品や現代美術作品を展示しています。',
        'verified': True,
        'location': {'lat': 31.631389, 'lng': -7.987500}
    },
    {
        'id': 11,
        'name': 'アグダル庭園',
        'city': 'マラケシュ',
        'category': '自然',
        'description': '12世紀に造られた王室庭園。オリーブやオレンジの木が植えられた広大な敷地で、週末のみ一般開放されています。',
        'verified': True,
        'location': {'lat': 31.605000, 'lng': -7.975000}
    },
    {
        'id': 12,
        'name': 'アトラス山脈の眺望ポイント',
        'city': 'マラケシュ',
        'category': '自然',
        'description': 'マラケシュから望むアトラス山脈の絶景ポイント。特に夕日の時間帯は山々が美しく染まり、息をのむような景色を楽しめます。',
        'verified': True,
        'location': {'lat': 31.580000, 'lng': -7.980000}
    },

    # カサブランカの観光地（9箇所）
    {
        'id': 13,
        'name': 'ハッサン2世モスク',
        'city': 'カサブランカ',
        'category': '宗教建築',
        'description': '世界で2番目に大きなモスク。海に面した壮大な建築で、非ムスリムも内部見学が可能です。',
        'verified': True,
        'location': {'lat': 33.608416, 'lng': -7.632767}
    },
    {
        'id': 14,
        'name': 'カサブランカ旧市街',
        'city': 'カサブランカ',
        'category': '都市・建築',
        'description': 'フランス統治時代の美しいアール・デコ建築が残る旧市街。カフェや買い物も楽しめます。',
        'verified': True,
        'location': {'lat': 33.589886, 'lng': -7.603869}
    },
    {
        'id': 15,
        'name': 'ムハンマド5世広場',
        'city': 'カサブランカ',
        'category': '広場・市場',
        'description': 'カサブランカの中心部にある大きな広場。周囲には重要な政府建物や商業施設が立ち並びます。',
        'verified': True,
        'location': {'lat': 33.596667, 'lng': -7.616667}
    },
    {
        'id': 16,
        'name': 'リック・カフェ',
        'city': 'カサブランカ',
        'category': '娯楽・体験',
        'description': '映画「カサブランカ」をテーマにしたレストラン・カフェ。映画の世界観を再現した内装が魅力です。',
        'verified': True,
        'location': {'lat': 33.594722, 'lng': -7.612222}
    },
    {
        'id': 17,
        'name': 'コルニッシュ海岸',
        'city': 'カサブランカ',
        'category': '自然',
        'description': '大西洋に面した美しい海岸線。散歩やジョギング、海水浴などが楽しめるリゾートエリアです。',
        'verified': True,
        'location': {'lat': 33.611111, 'lng': -7.650000}
    },
    {
        'id': 18,
        'name': 'セントラル・マーケット',
        'city': 'カサブランカ',
        'category': '広場・市場',
        'description': '地元の人々が利用する活気ある市場。新鮮な食材や日用品が豊富に揃います。',
        'verified': True,
        'location': {'lat': 33.592778, 'lng': -7.620556}
    },
    {
        'id': 19,
        'name': 'ツインセンター',
        'city': 'カサブランカ',
        'category': '都市・建築',
        'description': 'カサブランカのランドマークとなる近代的な高層ビル。ショッピングやビジネスの中心地です。',
        'verified': True,
        'location': {'lat': 33.583333, 'lng': -7.633333}
    },
    {
        'id': 20,
        'name': 'ノートルダム・ド・ルルド教会',
        'city': 'カサブランカ',
        'category': '宗教建築',
        'description': '1954年に建てられたカトリック教会。美しいステンドグラスと現代的な建築デザインが特徴です。',
        'verified': True,
        'location': {'lat': 33.589167, 'lng': -7.620833}
    },
    {
        'id': 21,
        'name': 'ムハンマド5世国際空港展望台',
        'city': 'カサブランカ',
        'category': '都市・建築',
        'description': '空港の展望台から市街地と離着陸する航空機を一望できるユニークな観光スポットです。',
        'verified': True,
        'location': {'lat': 33.366667, 'lng': -7.583333}
    },

    # フェズの観光地（11箇所）
    {
        'id': 22,
        'name': 'フェズ旧市街（フェズ・エル・バリ）',
        'city': 'フェズ',
        'category': '歴史建築',
        'description': '世界最大の歩行者専用都市エリア。中世イスラム都市の完全な姿を保持しているユネスコ世界遺産です。',
        'verified': True,
        'location': {'lat': 34.063611, 'lng': -4.973056}
    },
    {
        'id': 23,
        'name': 'フェズの皮なめし場',
        'city': 'フェズ',
        'category': '伝統工芸',
        'description': '1000年続く伝統的な皮革製造工程を見学できる場所。色とりどりの染色桶が印象的です。',
        'verified': True,
        'location': {'lat': 34.064722, 'lng': -4.970833}
    },
    {
        'id': 24,
        'name': 'カラウィーン・モスク',
        'city': 'フェズ',
        'category': '宗教建築',
        'description': '世界最古の大学としても知られる9世紀建立のモスク。イスラム教育の中心地として機能しています。',
        'verified': True,
        'location': {'lat': 34.064167, 'lng': -4.972500}
    },
    {
        'id': 25,
        'name': 'ブー・イナニア・マドラサ',
        'city': 'フェズ',
        'category': '宗教建築',
        'description': '14世紀に建てられた美しい神学校。精緻なイスラム装飾と大理石の中庭が見どころです。',
        'verified': True,
        'location': {'lat': 34.063889, 'lng': -4.972222}
    },
    {
        'id': 26,
        'name': 'ネジャリン・ファンドゥーク',
        'city': 'フェズ',
        'category': '歴史建築',
        'description': '18世紀の隊商宿を改装した木工芸博物館。フェズの伝統的な木工技術を学べます。',
        'verified': True,
        'location': {'lat': 34.064444, 'lng': -4.973611}
    },
    {
        'id': 27,
        'name': 'ダル・バタ博物館',
        'city': 'フェズ',
        'category': '博物館',
        'description': '19世紀の王宮を改装した博物館。モロッコの伝統工芸品や装飾美術を展示しています。',
        'verified': True,
        'location': {'lat': 34.063333, 'lng': -4.974167}
    },
    {
        'id': 28,
        'name': 'Bab Boujeloud（青い門）',
        'city': 'フェズ',
        'category': '歴史建築',
        'description': 'フェズ旧市街の正門として知られる美しいゲート。青と緑のタイルで装飾されています。',
        'verified': True,
        'location': {'lat': 34.062500, 'lng': -4.975000}
    },
    {
        'id': 29,
        'name': 'アッタリン・マドラサ',
        'city': 'フェズ',
        'category': '宗教建築',
        'description': '14世紀に建てられた神学校。美しいゼリージュ装飾と細密な彫刻で知られています。',
        'verified': True,
        'location': {'lat': 34.064722, 'lng': -4.973333}
    },
    {
        'id': 30,
        'name': 'フェズ新市街',
        'city': 'フェズ',
        'category': '都市・建築',
        'description': 'フランス統治時代に建設された新市街。現代的な街並みと旧市街のコントラストが興味深いエリアです。',
        'verified': True,
        'location': {'lat': 34.033333, 'lng': -5.000000}
    },
    {
        'id': 31,
        'name': 'メリニッド朝の墓群',
        'city': 'フェズ',
        'category': '歴史建築',
        'description': '13-15世紀のメリニッド朝の王族が眠る墓地。フェズ市街を一望できる丘の上に位置しています。',
        'verified': True,
        'location': {'lat': 34.070000, 'lng': -4.980000}
    },
    {
        'id': 32,
        'name': 'ジャルダン・ジャナン・スビル',
        'city': 'フェズ',
        'category': '自然',
        'description': '19世紀に造られた美しい庭園。フェズ旧市街の喧騒から離れた静かな憩いの場所です。',
        'verified': True,
        'location': {'lat': 34.055000, 'lng': -4.985000}
    },

    # その他の都市の観光地（3箇所）
    {
        'id': 33,
        'name': 'ウダイヤのカスバ',
        'city': 'ラバト',
        'category': '歴史建築',
        'description': 'ラバトの旧市街にある12世紀の要塞。大西洋を見下ろす絶景ポイントとしても人気です。',
        'verified': True,
        'location': {'lat': 34.038889, 'lng': -6.842222}
    },
    {
        'id': 34,
        'name': 'シャウエン旧市街',
        'city': 'シャウエン',
        'category': '都市・建築',
        'description': '青い街として有名な美しい山間の町。青と白で統一された建物群が幻想的な景観を作り出しています。',
        'verified': True,
        'location': {'lat': 35.169444, 'lng': -5.268056}
    },
    {
        'id': 35,
        'name': 'アイット・ベン・ハドゥ',
        'city': 'ワルザザート',
        'category': '歴史建築',
        'description': '世界遺産に登録された要塞化された村（クサル）。映画のロケ地としても有名な絶景スポットです。',
        'verified': True,
        'location': {'lat': 31.047222, 'lng': -7.129722}
    }
]

@app.route('/api/spots')
def get_spots():
    """観光地一覧を取得するAPIエンドポイント"""
    try:
        # フィルタリングパラメータを取得
        city = request.args.get('city')
        category = request.args.get('category')
        verified_only = request.args.get('verified', 'false').lower() == 'true'
        
        # データをフィルタリング
        filtered_spots = SPOTS_DATA.copy()

        if city:
            filtered_spots = [spot for spot in filtered_spots if spot['city'] == city]

        if category:
            filtered_spots = [spot for spot in filtered_spots if spot['category'] == category]

        if verified_only:
            filtered_spots = [spot for spot in filtered_spots if spot.get('verified', False)]

        return jsonify({
            'success': True,
            'data': filtered_spots,
            'total': len(filtered_spots),
            'filters_applied': {
                'city': city,
                'category': category,
                'verified_only': verified_only
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '観光地データ取得エラー'
        }), 500

@app.route('/api/spots/<int:spot_id>')
def get_spot_detail(spot_id):
    """観光地の詳細情報を取得するAPIエンドポイント"""
    try:
        # 詳細情報のデータベース（選択された観光地の詳細情報）
        spot_details = {
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
            }
        }

        # ID に該当する詳細データがあるかチェック
        if spot_id in spot_details:
            return jsonify(spot_details[spot_id])
        else:
            # 基本データから動的に詳細を生成
            basic_spot = next((spot for spot in SPOTS_DATA if spot['id'] == spot_id), None)
            if basic_spot:
                # より詳細な情報を自動生成
                detailed_spot = {
                    'id': basic_spot['id'],
                    'name': basic_spot['name'],
                    'city': basic_spot['city'],
                    'category': basic_spot['category'],
                    'description': basic_spot['description'],
                    'longDescription': f"{basic_spot['description']} この場所は{basic_spot['city']}を代表する{basic_spot['category']}として多くの観光客に愛されています。豊かな歴史と文化を持つこの地域では、伝統的な建築様式や現地の人々の生活様式を間近で体験することができます。訪問者は、この場所の独特な雰囲気と美しさに魅了され、モロッコの文化遺産の奥深さを感じることができるでしょう。",
                    'features': ['観光地', '文化体験', '見学可能', '歴史的価値', '写真撮影'],
                    'verified': basic_spot.get('verified', False),
                    'location': basic_spot.get('location', {}),
                    'hours': {
                        'open': '営業時間については現地でご確認ください',
                        'note': '祝日や特別な日は営業時間が変更される場合があります。金曜日の祈りの時間（12:00-14:00）にご注意ください。'
                    },
                    'access': {
                        'note': '詳細なアクセス方法については現地の案内をご確認ください。タクシーまたは公共交通機関の利用をお勧めします。',
                        'taxi': '市内中心部からタクシー利用可能',
                        'walking': '徒歩でのアクセスも可能な場合があります'
                    },
                    'tips': [
                        '訪問前に営業時間を確認することをお勧めします',
                        '現地の文化と習慣を尊重しましょう',
                        '写真撮影は許可を取ってから行いましょう',
                        '適切な服装での訪問をお勧めします',
                        '現金を準備しておくと便利です',
                        'ガイドの利用を検討してみてください'
                    ],
                    'bestTime': '訪問に最適な時間帯については現地情報をご確認ください。一般的に午前中は比較的観光客が少なくおすすめです。',
                    'activities': '見学、写真撮影、文化体験、建築鑑賞、歴史学習',
                    'architecture': 'モロッコの伝統的な建築様式を反映した美しい構造と装飾が特徴的です。',
                    'history': f'{basic_spot["city"]}の重要な歴史的場所として、長い間地域の文化と発展に貢献してきました。',
                    'culturalSignificance': 'モロッコの豊かな文化遺産を代表する重要な場所として、地域のアイデンティティと伝統を保持しています。'
                }
                return jsonify(detailed_spot)
            else:
                return jsonify({
                    'success': False,
                    'error': 'SPOT_NOT_FOUND',
                    'error_code': 404,
                    'message': '観光地が見つかりません',
                    'details': f'観光地ID {spot_id} は存在しません。有効なIDは1-{len(SPOTS_DATA)}です。',
                    'available_spots': len(SPOTS_DATA),
                    'suggestion': '観光地一覧(/api/spots)から有効なIDを確認してください。'
                }), 404

    except Exception as e:
        app.logger.error(f'Error fetching spot detail for ID {spot_id}: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': 'INTERNAL_SERVER_ERROR',
            'error_code': 500,
            'message': '観光地詳細取得エラー',
            'details': '内部サーバーエラーが発生しました。',
            'timestamp': datetime.now().isoformat(),
            'spot_id': spot_id
        }), 500

@app.route('/api/spots/recommended')
def get_recommended_spots():
    """おすすめ観光地を取得するAPIエンドポイント"""
    try:
        # 検証済みの観光地から上位を選択
        recommended = [spot for spot in SPOTS_DATA if spot.get('verified', False)][:6]

        return jsonify({
            'success': True,
            'data': recommended,
            'total': len(recommended)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'おすすめ観光地取得エラー'
        }), 500

@app.route('/api/cities')
def get_cities():
    """都市一覧を取得するAPIエンドポイント"""
    try:
        # すべての都市を重複なしで取得
        cities = list(set(spot['city'] for spot in SPOTS_DATA))
        cities.sort()  # アルファベット順にソート

        return jsonify({
            'success': True,
            'data': cities,
            'total': len(cities)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '都市一覧取得エラー'
        }), 500

@app.route('/api/categories')
def get_categories():
    """カテゴリ一覧を取得するAPIエンドポイント"""
    try:
        # すべてのカテゴリを重複なしで取得
        categories = list(set(spot['category'] for spot in SPOTS_DATA))
        categories.sort()  # アルファベット順にソート

        return jsonify({
            'success': True,
            'data': categories,
            'total': len(categories)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'カテゴリ一覧取得エラー'
        }), 500

# エラーハンドラー
@app.errorhandler(404)
def not_found_error(error):
    """404エラーハンドラー"""
    return render_template('error.html', 
                         error_code=404,
                         error_message="ページが見つかりません",
                         error_description="お探しのページは存在しないか、移動された可能性があります。"), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    return render_template('error.html',
                         error_code=500,
                         error_message="内部サーバーエラー",
                         error_description="サーバーで問題が発生しました。しばらくしてから再度お試しください。"), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """汎用エラーハンドラー"""
    app.logger.error(f'Unhandled exception: {e}', exc_info=True)
    return render_template('error.html',
                         error_code=500,
                         error_message="予期しないエラー",
                         error_description="申し訳ございません。予期しないエラーが発生しました。"), 500

def find_port():
    """利用可能なポートを見つける"""
    for port in range(5006, 5020):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    return 5006

if __name__ == '__main__':
    port = find_port()
    print(f"\n🚀 Morocco Tourism App starting on port {port}")
    print(f"📍 Local access: http://localhost:{port}")
    print("🤖 AI powered by OpenAI GPT-4o-mini")
    print(f"🏛️ Total tourist spots: {len(SPOTS_DATA)}")
    print("=" * 50)
    
    try:
        # 開発用設定でアプリを起動
        app.run(
            host='0.0.0.0',  # すべてのインターフェースでリッスン
            port=port,
            debug=True,
            use_reloader=False  # リローダーを無効化
        )
    except Exception as e:
        print(f"❌ アプリの起動に失敗しました: {e}")
        print(f"📋 ポート {port} が使用中の可能性があります")