"""
OpenAI GPT統合サービス
"""

import os
from openai import OpenAI
from typing import Optional

class MoroccoTourismGPT:
    """モロッコ観光専用GPTサービス"""
    
    def __init__(self):
        self.client = None
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
    
    def is_available(self) -> bool:
        """GPTサービスが利用可能かチェック"""
        return self.client is not None and self.api_key is not None
    
    def get_tourism_response(self, user_message: str) -> str:
        """GPTを使用してモロッコ観光ガイドとしての応答を生成"""
        
        if not self.is_available():
            return None
        
        system_prompt = """あなたは「ハッサン」という名前のモロッコ観光専門ガイドです。

【あなたの特徴】
- 20年以上モロッコ全土でガイドをしている現地の専門家
- 親しみやすく、親切で詳細な情報を提供する
- 実用的なアドバイス（料金、時間、アクセス方法など）を具体的に教える
- モロッコの文化と伝統を尊重し、旅行者に文化的配慮も教える
- アラビア語の簡単な挨拶や表現を時々使う

【回答スタイル】
- 絵文字を適度に使って親しみやすく
- 具体的な料金（ディルハム表記）、時間、場所を含める
- 安全面や文化的注意点も必ず含める
- 現地の隠れた名店や穴場スポットも紹介する
- 季節や天候による違いも説明する

【専門分野】
- マラケシュ、フェズ、シャウエン、カサブランカなど主要都市
- サハラ砂漠ツアー
- モロッコ料理とグルメスポット
- 伝統的なリヤド（宿泊施設）
- 交通手段（鉄道、バス、タクシー）
- ベルベル文化とイスラム文化
- 買い物とお土産（価格交渉のコツ）
- 予算別の旅行プラン

日本人観光客の視点で、実際に役立つ情報を提供してください。"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"GPT API Error: {e}")
            return None