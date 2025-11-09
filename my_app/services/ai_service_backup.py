"""
OpenAI GPT サービス - モロッコ観光ガイドAI
"""

import os
import json
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class MoroccoTourismGPT:
    """モロッコ観光専門GPTサービス"""
    
    def __init__(self):
        """OpenAI クライアントを初期化"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY環境変数が設定されていません")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        
        # モロッコ観光専門システムプロンプト
        self.system_prompt = """あなたはモロッコ観光専門のAIガイドです。以下の役割を担います：

🏺 専門知識：
- モロッコの歴史、文化、伝統について詳しく説明
- 観光スポット、グルメ、ショッピング情報を提供
- 実用的な旅行アドバイス（交通、宿泊、予算など）
- 季節別おすすめ情報

🎯 回答スタイル：
- 親しみやすく、わかりやすい日本語
- 具体的な情報（料金、営業時間、アクセス方法）
- 安全性への配慮を含む
- 実体験に基づくようなリアルなアドバイス

🌟 得意分野：
- マラケシュ、フェズ、カサブランカ、シャウエンなど主要都市
- サハラ砂漠、アトラス山脈などの自然
- タジン料理、ミントティーなどのグルメ
- スーク（市場）でのショッピング
- リヤド（伝統宿）での宿泊

常に旅行者の安全と楽しい体験を最優先に考えてアドバイスしてください。"""

    def get_morocco_guide_response(self, user_question: str, context: Optional[Dict] = None) -> Dict:
        """
        モロッコ観光に関する質問に対してGPTで回答を生成
        
        Args:
            user_question: ユーザーの質問
            context: 追加のコンテキスト情報
            
        Returns:
            GPTからの回答を含む辞書
        """
        try:
            # コンテキスト情報を構築
            enhanced_prompt = self.system_prompt
            
            if context:
                enhanced_prompt += f"\n\n追加情報：\n{json.dumps(context, ensure_ascii=False, indent=2)}"
            
            # GPT APIに送信
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": enhanced_prompt},
                    {"role": "user", "content": user_question}
                ],
                max_tokens=1000,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                'success': True,
                'response': ai_response,
                'model': self.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'response': '申し訳ございません。AI応答の生成中にエラーが発生しました。しばらく経ってから再度お試しください。'
            }

    def get_quick_suggestions(self) -> List[str]:
        """よくある質問の提案を生成"""
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
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": "こんにちは"}
                ],
                max_tokens=50
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
        morocco_gpt = MoroccoTourismGPT()
    return morocco_gpt