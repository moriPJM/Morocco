"""
地図関連API
"""

from flask import Blueprint, jsonify, request

maps_bp = Blueprint('maps', __name__)

@maps_bp.route('/markers')
def get_map_markers():
    """地図マーカー情報取得"""
    markers = [
        {
            'id': 1,
            'name': 'ジャマ・エル・フナ広場',
            'lat': 31.625901,
            'lng': -7.989161,
            'category': 'square',
            'icon': 'square'
        },
        {
            'id': 2,
            'name': 'サハラ砂漠',
            'lat': 31.0801,
            'lng': -4.0133,
            'category': 'nature',
            'icon': 'mountain'
        },
        {
            'id': 3,
            'name': 'シャウエン',
            'lat': 35.1711,
            'lng': -5.2636,
            'category': 'city',
            'icon': 'building'
        }
    ]
    
    return jsonify({
        'success': True,
        'markers': markers
    })

@maps_bp.route('/route')
def get_route():
    """ルート情報取得"""
    start = request.args.get('start')
    end = request.args.get('end')
    
    return jsonify({
        'success': True,
        'start': start,
        'end': end,
        'route': {
            'distance': '340km',
            'duration': '4時間30分',
            'waypoints': []
        }
    })