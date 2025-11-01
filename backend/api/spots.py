"""
観光スポット関連API
"""

from flask import Blueprint, jsonify, request
from sqlalchemy import and_, or_, desc, case
from backend.models.tourism import TourismSpot, db

spots_bp = Blueprint('spots', __name__)

@spots_bp.route('/')
def get_spots():
    """観光スポット一覧取得"""
    try:
        # データベースから観光スポット一覧を取得
        spots = TourismSpot.query.all()
        
        spots_data = []
        for spot in spots:
            spots_data.append({
                'id': spot.id,
                'name': spot.name,
                'name_en': spot.name_en,
                'name_ar': spot.name_ar,
                'city': spot.city,
                'category': spot.category,
                'latitude': spot.latitude,
                'longitude': spot.longitude,
                'description': spot.description,
                'description_en': spot.description_en,
                'image_url': spot.image_url,
                'best_time_to_visit': spot.best_time_to_visit,
                'entry_fee': spot.entry_fee,
                'opening_hours': spot.opening_hours,
                'created_at': spot.created_at.isoformat() if spot.created_at else None
            })
        
        return jsonify({
            'success': True,
            'data': spots_data,
            'total': len(spots_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@spots_bp.route('/<int:spot_id>')
def get_spot_detail(spot_id):
    """観光スポット詳細取得"""
    try:
        spot = TourismSpot.query.get_or_404(spot_id)
        
        spot_data = {
            'id': spot.id,
            'name': spot.name,
            'name_en': spot.name_en,
            'name_ar': spot.name_ar,
            'city': spot.city,
            'category': spot.category,
            'latitude': spot.latitude,
            'longitude': spot.longitude,
            'description': spot.description,
            'description_en': spot.description_en,
            'image_url': spot.image_url,
            'best_time_to_visit': spot.best_time_to_visit,
            'entry_fee': spot.entry_fee,
            'opening_hours': spot.opening_hours,
            'created_at': spot.created_at.isoformat() if spot.created_at else None
        }
        
        return jsonify({
            'success': True,
            'data': spot_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404

@spots_bp.route('/search')
def search_spots():
    """観光スポット検索（強化版）"""
    try:
        print(f"[DEBUG] ===== NEW SEARCH REQUEST =====")
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        city = request.args.get('city', '').strip()
        
        print(f"[DEBUG] Raw parameters: {dict(request.args)}")
        print(f"[DEBUG] Processed parameters - query: '{query}', category: '{category}', city: '{city}'")
        
        # ベースクエリ
        spots_query = TourismSpot.query
        
        # 検索条件を追加
        if query:
            # 高度な検索：複数キーワード対応、重要度による重み付け
            keywords = [k.strip() for k in query.split() if k.strip()]
            search_conditions = []
            
            for keyword in keywords:
                # 各フィールドでの一致条件
                name_match = TourismSpot.name.ilike(f'%{keyword}%')
                city_match = TourismSpot.city.ilike(f'%{keyword}%')
                desc_match = TourismSpot.description.ilike(f'%{keyword}%')
                category_match = TourismSpot.category.ilike(f'%{keyword}%')
                
                # キーワードごとの条件を組み合わせ（OR）
                keyword_condition = or_(name_match, city_match, desc_match, category_match)
                search_conditions.append(keyword_condition)
            
            # すべてのキーワードでAND検索
            if search_conditions:
                spots_query = spots_query.filter(and_(*search_conditions))
        
        if category:
            print(f"[DEBUG] Filtering by category: '{category}'")
            # 部分一致検索に変更（例：「自然」で「自然・渓谷」「自然・山脈」なども含む）
            spots_query = spots_query.filter(TourismSpot.category.ilike(f'%{category}%'))
            
        if city:
            print(f"[DEBUG] Filtering by city: '{city}'")
            # 都市も部分一致検索に変更
            spots_query = spots_query.filter(TourismSpot.city.ilike(f'%{city}%'))
        
        # パラメータが何も指定されていない場合のみエラー
        if not query and not category and not city:
            return jsonify({
                'success': True,
                'data': [],
                'total': 0,
                'message': '検索条件を入力してください'
            })
        
        # 関連度順に並び替え（名前一致を優先）
        if query:
            # 名前での完全一致を最優先
            exact_name_match = TourismSpot.name.ilike(query)
            spots_query = spots_query.order_by(
                desc(case([(exact_name_match, 1)], else_=0)),
                TourismSpot.name
            )
        else:
            spots_query = spots_query.order_by(TourismSpot.name)
        
        # デバッグ：最終的なクエリ条件を表示
        print(f"[DEBUG] Query conditions - query: {bool(query)}, category: {bool(category)}, city: {bool(city)}")
        
        # 結果を取得（最大20件）
        spots = spots_query.limit(20).all()
        print(f"[DEBUG] Found {len(spots)} spots")
        
        # 検索結果の詳細情報
        spots_data = []
        for spot in spots:
            print(f"[DEBUG] Spot: {spot.name} - Category: {spot.category} - City: {spot.city}")
            spot_dict = {
                'id': spot.id,
                'name': spot.name,
                'name_en': spot.name_en,
                'city': spot.city,
                'category': spot.category,
                'latitude': spot.latitude,
                'longitude': spot.longitude,
                'description': spot.description,
                'image_url': spot.image_url,
                'best_time_to_visit': spot.best_time_to_visit,
                'entry_fee': spot.entry_fee,
                'opening_hours': spot.opening_hours
            }
            
            # 検索キーワードとの関連度を計算
            if query:
                relevance_score = calculate_relevance(spot, query)
                spot_dict['relevance_score'] = relevance_score
            
            spots_data.append(spot_dict)
        
        # 関連度順に再ソート
        if query:
            spots_data.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return jsonify({
            'success': True,
            'query': query,
            'category': category,
            'city': city,
            'data': spots_data,
            'total': len(spots_data),
            'message': f'{len(spots_data)}件の観光スポットが見つかりました'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '検索処理中にエラーが発生しました'
        }), 500

def calculate_relevance(spot, query):
    """検索関連度を計算"""
    score = 0
    query_lower = query.lower()
    keywords = [k.strip().lower() for k in query.split() if k.strip()]
    
    # 名前での一致（最高点）
    if spot.name and query_lower in spot.name.lower():
        score += 100
        # 完全一致ならさらに高得点
        if query_lower == spot.name.lower():
            score += 50
    
    # 都市での一致（高得点）
    if spot.city and query_lower in spot.city.lower():
        score += 50
    
    # カテゴリでの一致（中得点）
    if spot.category and query_lower in spot.category.lower():
        score += 30
    
    # 説明での一致（キーワードごとに加点）
    if spot.description:
        desc_lower = spot.description.lower()
        for keyword in keywords:
            if keyword in desc_lower:
                score += 10
    
    return score

@spots_bp.route('/categories')
def get_categories():
    """カテゴリー一覧取得"""
    try:
        categories = db.session.query(TourismSpot.category).distinct().all()
        category_list = [cat[0] for cat in categories if cat[0]]
        
        return jsonify({
            'success': True,
            'data': category_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@spots_bp.route('/cities')
def get_cities():
    """都市一覧取得"""
    try:
        cities = db.session.query(TourismSpot.city).distinct().all()
        city_list = [city[0] for city in cities if city[0]]
        
        return jsonify({
            'success': True,
            'data': city_list
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500