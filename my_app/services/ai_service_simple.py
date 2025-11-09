"""
シンプルで安定したAIサービス - モロッコ観光ガイド
"""

import os
import json
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class MoroccoTourismGPT:
    """シンプルで安定したモロッコ観光専門GPTサービス"""
    
    def __init__(self):
        """初期化"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = "gpt-4o-mini"
        self.client = None
        
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
        
        # システムプロンプト
        self.system_prompt = """あなたはモロッコ観光専門のAIガイドです。

専門知識：
- モロッコの歴史、文化、伝統について詳しく説明
- 観光スポット、グルメ、ショッピング情報を提供
- 実用的な旅行アドバイス（交通、宿泊、予算など）

回答スタイル：
- 親しみやすく、わかりやすい日本語
- 具体的な情報を含む
- 安全性への配慮を含む

得意分野：
- マラケシュ、フェズ、カサブランカ、シャウエンなど主要都市
- サハラ砂漠、アトラス山脈などの自然
- タジン料理、ミントティーなどのグルメ
- スーク（市場）でのショッピング

常に旅行者の安全と楽しい体験を最優先に考えてアドバイスしてください。"""

    def _get_client(self):
        """OpenAIクライアントを取得（遅延初期化）"""
        if self.client is None:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                print("OpenAI client initialized successfully")
            except Exception as e:
                print(f"Failed to initialize OpenAI client: {e}")
                return None
        return self.client

    def get_morocco_guide_response(self, user_question: str, context: Optional[Dict] = None) -> Dict:
        """
        モロッコ観光に関する質問に対してGPTで回答を生成
        """
        # APIキーがない場合の代替レスポンス
        if not self.api_key:
            return self._get_fallback_response(user_question)
        
        try:
            client = self._get_client()
            if not client:
                return self._get_fallback_response(user_question)
            
            # プロンプト構築
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_question}
            ]
            
            # API呼び出し
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=800,
                temperature=0.7
            )
            
            return {
                'success': True,
                'response': response.choices[0].message.content,
                'model': self.model,
                'usage': {
                    'total_tokens': response.usage.total_tokens if response.usage else 0
                }
            }
            
        except Exception as e:
            print(f"AI response generation failed: {e}")
            return self._get_fallback_response(user_question)

    def _get_fallback_response(self, question: str) -> Dict:
        """API失敗時の代替レスポンス"""
        fallback_responses = {
            'マラケシュ': """マラケシュは「赤い街」と呼ばれるモロッコの古都です。

主要な観光スポット：
• ジャマ・エル・フナ広場 - 世界遺産の賑やかな広場
• バヒア宮殿 - 美しいイスラム建築
• マジョレル庭園 - 青色が印象的な庭園
• クトゥビーヤ・モスク - マラケシュのシンボル

おすすめの過ごし方：
• 朝早くスークを散策
• 夕方にジャマ・エル・フナ広場でパフォーマンス鑑賞
• 伝統的なリヤドに宿泊

注意点：
• 日中は非常に暑いため、早朝・夕方の観光がおすすめ
• スークでは価格交渉が基本
• 水分補給をこまめに行う""",
            
            'フェズ': """フェズはモロッコの文化首都として知られる古都です。

見どころ：
• フェズ・エル・バリ - 世界最大の迷路のような旧市街
• ブー・イナニア・マドラサ - 美しいイスラム神学校
• 革なめし工場 - 伝統的な革製品の製造現場
• カラウィーン・モスク - 世界最古の大学

体験できること：
• 伝統工芸品の制作見学
• 本格的なモロッコ料理
• 迷路のような街並み散策

アドバイス：
• 旧市街では道に迷いやすいのでガイド推奨
• 革なめし工場見学時はミントを持参""",
            
            'サハラ砂漠': """サハラ砂漠はモロッコ旅行のハイライトです。

主要な拠点：
• メルズーガ - エルグ・シェビ大砂丘の玄関口
• ザゴラ - 比較的アクセスしやすい砂漠エリア

体験できること：
• ラクダトレッキング
• 砂漠キャンプ
• 満天の星空観察
• 日の出・日の出鑑賞

準備するもの：
• 防寒着（夜は非常に寒い）
• 日焼け止め・帽子
• 大量の水
• 砂よけの服装

ベストシーズン：10月～4月の涼しい時期"""
        }
        
        # キーワードマッチングで適切なレスポンスを選択
        for keyword, response in fallback_responses.items():
            if keyword in question:
                return {
                    'success': True,
                    'response': response,
                    'model': 'fallback_system',
                    'usage': {'total_tokens': 0}
                }
        
        # デフォルトレスポンス
        return {
            'success': True,
            'response': """申し訳ございませんが、現在AI機能が一時的に利用できません。

モロッコ観光についての一般的な情報：

• ベストシーズン：10月～4月（涼しく過ごしやすい）
• 主要都市：マラケシュ、フェズ、カサブランカ、ラバト
• 必見スポット：ジャマ・エル・フナ広場、サハラ砂漠、シャウエン
• 名物料理：タジン、クスクス、ミントティー
• 通貨：モロッコ・ディルハム（MAD）

より詳しい情報については、後ほど改めてお試しください。""",
            'model': 'fallback_system',
            'usage': {'total_tokens': 0}
        }

    def get_quick_suggestions(self) -> List[str]:
        """おすすめ質問リスト"""
        return [
            "マラケシュでおすすめの観光スポットは？",
            "フェズの旧市街の見どころを教えて",
            "サハラ砂漠ツアーの料金と注意点は？",
            "モロッコ料理で絶対食べるべきものは？",
            "3日間でモロッコを回るプランを提案して",
            "シャウエンの青い街の写真スポットは？",
            "スークでの値段交渉のコツは？",
            "モロッコ旅行の予算はいくら必要？",
            "ベストシーズンはいつ？",
            "女性一人旅でも安全？"
        ]

    def test_connection(self) -> Dict:
        """API接続テスト"""
        if not self.api_key:
            return {
                'success': False,
                'error': 'API キーが設定されていません',
                'message': 'OpenAI API接続失敗'
            }
        
        try:
            client = self._get_client()
            if not client:
                return {
                    'success': False,
                    'error': 'クライアント初期化失敗',
                    'message': 'OpenAI API接続失敗'
                }
            
            # 簡単なテスト呼び出し
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "こんにちは"}],
                max_tokens=20
            )
            
            return {
                'success': True,
                'message': 'OpenAI API接続成功',
                'model': self.model,
                'response': response.choices[0].message.content
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'OpenAI API接続失敗'
            }


# グローバルインスタンス
morocco_gpt = None

def get_morocco_gpt():
    """GPTサービスのシングルトンインスタンスを取得"""
    global morocco_gpt
    if morocco_gpt is None:
        try:
            morocco_gpt = MoroccoTourismGPT()
        except Exception as e:
            print(f"Error initializing AI service: {e}")
            # ダミーオブジェクトでアプリのクラッシュを防ぐ
            class DummyGPT:
                def get_morocco_guide_response(self, question, context=None):
                    return {
                        'success': False,
                        'error': 'AI機能初期化エラー',
                        'response': 'AI機能は現在利用できません。'
                    }
                def get_quick_suggestions(self):
                    return ["AI機能は現在利用できません"]
                def test_connection(self):
                    return {'success': False, 'error': 'AI初期化失敗', 'message': 'AI機能利用不可'}
            morocco_gpt = DummyGPT()
    return morocco_gpt