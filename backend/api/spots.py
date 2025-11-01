"""
観光スポット関連API
"""

from flask import Blueprint, jsonify, request
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
                'rating': spot.rating,
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
            'rating': spot.rating,
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
    """観光スポット検索"""
    try:
        query = request.args.get('q', '').strip()
        category = request.args.get('category', '').strip()
        city = request.args.get('city', '').strip()
        
        # ベースクエリ
        spots_query = TourismSpot.query
        
        # 検索条件を追加
        if query:
            spots_query = spots_query.filter(
                TourismSpot.name.contains(query) |
                TourismSpot.description.contains(query) |
                TourismSpot.city.contains(query)
            )
        
        if category:
            spots_query = spots_query.filter(TourismSpot.category == category)
            
        if city:
            spots_query = spots_query.filter(TourismSpot.city == city)
        
        # 結果を取得
        spots = spots_query.all()
        
        spots_data = []
        for spot in spots:
            spots_data.append({
                'id': spot.id,
                'name': spot.name,
                'name_en': spot.name_en,
                'city': spot.city,
                'category': spot.category,
                'rating': spot.rating,
                'latitude': spot.latitude,
                'longitude': spot.longitude,
                'description': spot.description,
                'image_url': spot.image_url,
                'best_time_to_visit': spot.best_time_to_visit,
                'entry_fee': spot.entry_fee,
                'opening_hours': spot.opening_hours
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'category': category,
            'city': city,
            'data': spots_data,
            'total': len(spots_data)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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