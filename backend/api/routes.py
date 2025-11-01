"""
メインAPIルート
"""

from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health_check():
    """ヘルスチェック"""
    return jsonify({
        'status': 'ok',
        'message': 'モロッコ観光ガイドAPI is running',
        'version': '1.0.0'
    })