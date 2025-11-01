"""
モロッコのリアルタイム情報取得サービス
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import time

class MoroccoRealtimeService:
    """モロッコのリアルタイム情報を取得するサービス"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 3600  # 1時間キャッシュ
        
    def _is_cache_valid(self, key: str) -> bool:
        """キャッシュが有効かチェック"""
        if key not in self.cache:
            return False
        
        cache_time = self.cache[key].get('timestamp', 0)
        return time.time() - cache_time < self.cache_duration
    
    def _get_cached_or_fetch(self, key: str, fetch_func) -> Optional[Dict]:
        """キャッシュから取得、または新しくフェッチ"""
        if self._is_cache_valid(key):
            return self.cache[key]['data']
        
        try:
            data = fetch_func()
            if data:
                self.cache[key] = {
                    'data': data,
                    'timestamp': time.time()
                }
                return data
        except Exception as e:
            print(f"Error fetching {key}: {e}")
            
        # キャッシュがあれば古くても返す
        if key in self.cache:
            return self.cache[key]['data']
        
        return None
    
    def get_weather_info(self, city: str = "Marrakech") -> Optional[Dict]:
        """指定都市の天気情報を取得"""
        def fetch_weather():
            # 模擬データ（実際のAPIキーがない場合）
            return {
                'city': city,
                'temperature': 22,
                'feels_like': 24,
                'humidity': 45,
                'description': '晴れ',
                'wind_speed': 3.2,
                'last_updated': datetime.now().isoformat(),
                'note': '模擬データ'
            }
        
        return self._get_cached_or_fetch(f"weather_{city}", fetch_weather)
    
    def get_exchange_rates(self) -> Optional[Dict]:
        """為替レート情報を取得"""
        def fetch_rates():
            try:
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    usd_to_mad = 10.2
                    jpy_to_usd = data['rates'].get('JPY', 150)
                    jpy_to_mad = usd_to_mad / jpy_to_usd * 100
                    
                    return {
                        'jpy_to_mad': round(jpy_to_mad, 2),
                        'usd_to_mad': usd_to_mad,
                        'eur_to_mad': round(usd_to_mad * 0.92, 2),
                        'last_updated': datetime.now().isoformat(),
                        'source': 'ExchangeRate-API'
                    }
            except:
                pass
            
            # フォールバック
            return {
                'jpy_to_mad': 0.067,
                'usd_to_mad': 10.2,
                'eur_to_mad': 11.1,
                'last_updated': datetime.now().isoformat(),
                'note': '概算レート'
            }
        
        return self._get_cached_or_fetch("exchange_rates", fetch_rates)
    
    def get_comprehensive_info(self, city: str = "Marrakech") -> Dict:
        """包括的なリアルタイム情報を取得"""
        return {
            'weather': self.get_weather_info(city),
            'exchange_rates': self.get_exchange_rates(),
            'generated_at': datetime.now().isoformat()
        }

# グローバルインスタンス
realtime_service = MoroccoRealtimeService()