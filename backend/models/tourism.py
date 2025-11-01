"""
観光スポットのデータモデル
"""

from backend.services.database import db
from datetime import datetime

class TourismSpot(db.Model):
    """観光スポットモデル"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200))
    name_ar = db.Column(db.String(200))
    description = db.Column(db.Text)
    description_en = db.Column(db.Text)
    category = db.Column(db.String(100))  # 歴史的建造物、自然、市場など
    city = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    rating = db.Column(db.Float, default=0.0)
    image_url = db.Column(db.String(500))
    best_time_to_visit = db.Column(db.String(100))
    entry_fee = db.Column(db.String(100))
    opening_hours = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TravelRoute(db.Model):
    """旅行ルートモデル"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration_days = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))  # Easy, Medium, Hard
    route_data = db.Column(db.JSON)  # スポットIDの配列
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserFavorite(db.Model):
    """ユーザーお気に入りモデル"""
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(100), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('tourism_spot.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)