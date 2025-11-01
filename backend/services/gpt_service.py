"""
OpenAI GPT統合サービス（強化版）
"""

import os
from openai import OpenAI
from typing import Optional, Dict, List
import json
from datetime import datetime
from backend.models.tourism import TourismSpot, db

class MoroccoTourismGPT:
    """モロッコ観光専用GPTサービス（強化版）"""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                print("✅ OpenAI GPT service initialized successfully")
            except Exception as e:
                print(f"❌ OpenAI initialization error: {e}")
                self.client = None
        else:
            print("⚠️ OpenAI API key not found in environment variables")
    
    def is_available(self) -> bool:
        """GPTサービスが利用可能かチェック"""
        if not self.api_key:
            print("⚠️ API key not found")
            return False
        if not self.client:
            print("⚠️ OpenAI client not initialized")
            return False
        
        # 簡単なAPIテスト
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("✅ GPT API test successful")
            return True
        except Exception as e:
            print(f"❌ GPT API test failed: {e}")
            return False
    
    def get_context_data(self) -> Dict:
        """データベースからコンテキスト情報を取得"""
        try:
            # 観光スポット情報
            spots = TourismSpot.query.limit(15).all()
            spots_data = []
            for spot in spots:
                spots_data.append({
                    'name': spot.name,
                    'city': spot.city,
                    'category': spot.category,
                    'description': spot.description[:150] if spot.description else '',
                    'best_time': spot.best_time_to_visit,
                    'entry_fee': spot.entry_fee
                })
            
            # 統計情報
            total_spots = TourismSpot.query.count()
            categories = db.session.query(TourismSpot.category).distinct().all()
            cities = db.session.query(TourismSpot.city).distinct().all()
            
            return {
                'spots': spots_data,
                'total_spots': total_spots,
                'categories': [cat[0] for cat in categories if cat[0]][:8],
                'cities': [city[0] for city in cities if city[0]][:8],
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Context data error: {e}")
            return {
                'spots': [],
                'total_spots': 0,
                'categories': [],
                'cities': [],
                'last_updated': datetime.now().isoformat()
            }
    
    def create_enhanced_system_prompt(self) -> str:
        """データベース情報を統合した高度なシステムプロンプト"""
        context = self.get_context_data()
        
        return f"""あなたは「ハッサン」という名前のプロのモロッコ観光ガイドです。20年以上の豊富な経験を持ち、日本人観光客を専門にサポートしています。

【データベース情報】
- 利用可能な観光スポット: {context['total_spots']}件
- 主要都市: {', '.join(context['cities'])}
- カテゴリー: {', '.join(context['categories'])}
- 最終更新: {context['last_updated'][:10]}

【主要観光スポット（一部）】
{json.dumps(context['spots'][:5], ensure_ascii=False, indent=2)}

【あなたの特徴】
- 20年以上モロッコ全土でガイドをしている現地の専門家
- 親しみやすく、親切で詳細な情報を提供する
- 実用的なアドバイス（料金、時間、アクセス方法など）を具体的に教える
- モロッコの文化と伝統を尊重し、旅行者に文化的配慮も教える
- 最新の2024年情報に基づいて回答する

【回答スタイル】
- 絵文字を適度に使って親しみやすく（🇲🇦 🕌 🐪 🍽️ など）
- 具体的な料金（ディルハム表記）、時間、場所を含める
- 安全面や文化的注意点も必ず含める
- データベースの観光スポット情報を活用する
- 季節や天候による違いも説明する
- 実際の体験談のような具体的なアドバイス

【専門分野】
- マラケシュ、フェズ、シャウエン、カサブランカなど主要都市
- サハラ砂漠ツアー（メルズーガ、ザゴラ）
- モロッコ料理とグルメスポット
- 伝統的なリヤド（宿泊施設）
- 交通手段（ONCF鉄道、CTMバス、プチタクシー）
- ベルベル文化とイスラム文化
- 買い物とお土産（価格交渉のコツ）
- 予算別の旅行プラン

【重要】データベースの情報を最大限活用し、実際に存在する観光スポットを中心に案内してください。日本人観光客の視点で、実際に役立つ情報を提供してください。"""

    def get_tourism_response(self, user_message: str) -> Optional[str]:
        """GPTを使用してモロッコ観光ガイドとしての応答を生成（強化版）"""
        
        if not self.is_available():
            return None
        
        try:
            # コンテキスト情報を追加
            context = self.get_context_data()
            enhanced_message = f"""
【ユーザーの質問】
{user_message}

【参考情報】
利用可能な観光スポット: {context['total_spots']}件
主要都市: {', '.join(context['cities'])}

この情報を活用して、具体的で実用的なアドバイスをお願いします。
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # より高性能で経済的なモデル
                messages=[
                    {"role": "system", "content": self.create_enhanced_system_prompt()},
                    {"role": "user", "content": enhanced_message}
                ],
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            # 応答の品質チェック
            if ai_response and len(ai_response.strip()) > 30:
                return ai_response.strip()
            else:
                return None
            
        except Exception as e:
            print(f"GPT API Error: {e}")
            return None
    
    def get_personalized_recommendation(self, city: str, interests: List[str] = None) -> Optional[str]:
        """個人化された観光推薦を生成"""
        if not self.is_available():
            return None
        
        try:
            # 該当都市のスポット情報を取得
            city_spots = TourismSpot.query.filter(
                TourismSpot.city.ilike(f'%{city}%')
            ).limit(8).all()
            
            spots_info = []
            for spot in city_spots:
                spots_info.append({
                    'name': spot.name,
                    'category': spot.category,
                    'description': spot.description[:100] if spot.description else '',
                    'entry_fee': spot.entry_fee,
                    'best_time': spot.best_time_to_visit
                })
            
            interests_str = ', '.join(interests) if interests else '一般的な観光'
            
            prompt = f"""
{city}での観光について、以下の条件で詳しい推薦をしてください：

【条件】
- 都市: {city}
- 興味: {interests_str}

【該当する観光スポット】
{json.dumps(spots_info, ensure_ascii=False, indent=2)}

以下を含めて回答してください：
- おすすめスポットの詳細説明
- 効率的な回り方のプラン
- ベストな時間帯と所要時間
- 具体的な料金と予算
- 文化的な注意点
- 地元民のような楽しみ方のコツ
"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": self.create_enhanced_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Personalized recommendation error: {e}")
            return None