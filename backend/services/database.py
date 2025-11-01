"""
データベース初期化とモデル定義
"""

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    """データベースを初期化"""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///morocco_guide.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        try:
            # サンプルデータの追加処理
            print("[OK] Database initialized successfully.")
        except Exception as e:
            print(f"[ERROR] Database initialization error: {e}")