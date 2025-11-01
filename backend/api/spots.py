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
        # サンプルデータを返す（後でDBから取得に変更）
        sample_spots = [
            {
                'id': 1,
                'name': 'ジャマ・エル・フナ広場',
                'name_en': 'Jemaa el-Fnaa',
                'city': 'マラケシュ',
                'category': '広場・市場',
                'rating': 4.5,
                'latitude': 31.625901,
                'longitude': -7.989161,
                'description': 'マラケシュの中心部にある賑やかな広場。夜には屋台や大道芸人で溢れる'
            },
            {
                'id': 2,
                'name': 'サハラ砂漠',
                'name_en': 'Sahara Desert',
                'city': 'メルズーガ',
                'category': '自然',
                'rating': 4.8,
                'latitude': 31.0801,
                'longitude': -4.0133,
                'description': '世界最大の砂漠。ラクダツアーや星空観察が人気'
            },
            {
                'id': 3,
                'name': 'シャウエン',
                'name_en': 'Chefchaouen',
                'city': 'シャウエン',
                'category': '都市・建築',
                'rating': 4.7,
                'latitude': 35.1711,
                'longitude': -5.2636,
                'description': '青い街として有名な美しい山間の町'
            }
        ]
        
        return jsonify({
            'success': True,
            'data': sample_spots,
            'total': len(sample_spots)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@spots_bp.route('/<int:spot_id>')
def get_spot_detail(spot_id):
    """観光スポット詳細取得"""
    # サンプル詳細データ
    sample_detail = {
        'id': spot_id,
        'name': 'ジャマ・エル・フナ広場',
        'description': '詳細な説明がここに入ります...',
        'opening_hours': '24時間',
        'entry_fee': '無料',
        'best_time_to_visit': '夕方〜夜'
    }
    
    return jsonify({
        'success': True,
        'data': sample_detail
    })

@spots_bp.route('/search')
def search_spots():
    """観光スポット検索"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    return jsonify({
        'success': True,
        'query': query,
        'category': category,
        'data': []
    })