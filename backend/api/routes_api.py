"""
旅行ルート関連API
"""

from flask import Blueprint, jsonify, request
from backend.models.tourism import TravelRoute, db

routes_bp = Blueprint('routes_api', __name__)

@routes_bp.route('/')
def get_routes():
    """旅行ルート一覧取得"""
    try:
        routes = TravelRoute.query.all()
        
        routes_data = []
        for route in routes:
            routes_data.append({
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'duration_days': route.duration_days,
                'difficulty': route.difficulty,
                'route_data': route.route_data,
                'created_at': route.created_at.isoformat() if route.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': routes_data,
            'total': len(routes_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routes_bp.route('/<int:route_id>')
def get_route_detail(route_id):
    """旅行ルート詳細取得"""
    try:
        route = TravelRoute.query.get_or_404(route_id)
        
        route_data = {
            'id': route.id,
            'name': route.name,
            'description': route.description,
            'duration_days': route.duration_days,
            'difficulty': route.difficulty,
            'route_data': route.route_data,
            'created_at': route.created_at.isoformat() if route.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': route_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@routes_bp.route('/categories')
def get_route_categories():
    """旅行ルートカテゴリー一覧取得"""
    try:
        # ルートデータからカテゴリーを抽出
        categories = [
            {'id': 'cultural', 'name': '文化・歴史', 'description': '古い都市や歴史的建造物を巡る文化的な旅'},
            {'id': 'adventure', 'name': '自然・アドベンチャー', 'description': 'サハラ砂漠やアトラス山脈での冒険的な旅'},
            {'id': 'classic', 'name': '王道・定番', 'description': '初回訪問におすすめの主要スポット巡り'},
            {'id': 'luxury', 'name': 'ラグジュアリー', 'description': '高級リヤドや特別体験を含む贅沢な旅'},
            {'id': 'gourmet', 'name': 'グルメ・料理', 'description': 'モロッコ料理や料理教室を楽しむ美食の旅'},
            {'id': 'relaxation', 'name': 'リラクゼーション', 'description': 'スパやビーチでゆったり過ごす癒しの旅'},
            {'id': 'photography', 'name': 'フォト・絶景', 'description': '美しい景色や建築を撮影する写真の旅'}
        ]
        
        return jsonify({
            'success': True,
            'data': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@routes_bp.route('/search')
def search_routes():
    """旅行ルート検索"""
    try:
        category = request.args.get('category', '').strip()
        duration = request.args.get('duration', '').strip()
        difficulty = request.args.get('difficulty', '').strip()
        
        # ベースクエリ
        routes_query = TravelRoute.query
        
        # 検索条件を追加
        if duration:
            if duration == '3':
                routes_query = routes_query.filter(TravelRoute.duration_days <= 4)
            elif duration == '7':
                routes_query = routes_query.filter(TravelRoute.duration_days.between(5, 9))
            elif duration == '10':
                routes_query = routes_query.filter(TravelRoute.duration_days >= 10)
        
        if difficulty:
            routes_query = routes_query.filter(TravelRoute.difficulty == difficulty)
        
        # 結果を取得
        routes = routes_query.all()
        
        # カテゴリーフィルタリング（route_dataに基づく）
        if category:
            filtered_routes = []
            for route in routes:
                route_category = determine_route_category(route)
                if route_category == category:
                    filtered_routes.append(route)
            routes = filtered_routes
        
        routes_data = []
        for route in routes:
            route_category = determine_route_category(route)
            routes_data.append({
                'id': route.id,
                'name': route.name,
                'description': route.description,
                'duration_days': route.duration_days,
                'difficulty': route.difficulty,
                'category': route_category,
                'route_data': route.route_data,
                'created_at': route.created_at.isoformat() if route.created_at else None
            })
        
        return jsonify({
            'success': True,
            'category': category,
            'duration': duration,
            'difficulty': difficulty,
            'data': routes_data,
            'total': len(routes_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def determine_route_category(route):
    """ルートのカテゴリーを判定"""
    name_lower = route.name.lower()
    description_lower = route.description.lower()
    
    if 'サハラ' in route.name or 'アドベンチャー' in route.name or 'トレッキング' in route.name:
        return 'adventure'
    elif '美食' in route.name or '料理' in route.name or 'グルメ' in route.name:
        return 'gourmet'
    elif '王道' in route.name or '周遊' in route.name:
        return 'classic'
    elif 'ベルベル' in route.name or '文化' in route.name or '歴史' in route.name:
        return 'cultural'
    elif 'ラグジュアリー' in route.name or '高級' in route.name:
        return 'luxury'
    elif 'リラック' in route.name or 'スパ' in route.name:
        return 'relaxation'
    elif 'フォト' in route.name or '絶景' in route.name:
        return 'photography'
    else:
        return 'classic'  # デフォルト