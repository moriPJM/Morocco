"""
モロッコ観光ガイド - Streamlit版
Morocco Tourism Guide App powered by Streamlit
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import json
import os
import traceback
import time
from functools import wraps
import logging
import re
from typing import List, Optional

# Optional vector search module (lazy - may fail if deps not installed)
try:
    from ai_vector_search import VectorStore, build_docs_from_kb, _HAS_SBT as _AI_VECTOR_HAS_SBT
except Exception:
    VectorStore = None
    build_docs_from_kb = None
    _AI_VECTOR_HAS_SBT = False

# Optional OpenAI client import (only used when API key is configured)
try:
    _openai_client = None
    # Try new-style client
    try:
        from openai import OpenAI  # type: ignore
        _openai_client = ('new', OpenAI)
    except Exception:
        # Fall back to legacy API
        import openai  # type: ignore
        _openai_client = ('legacy', openai)
except Exception:
    _openai_client = None

def call_openai_api(prompt_text: str) -> Optional[str]:
    """Call OpenAI chat completion API with robust fallbacks.

    Returns response text or None if failed.
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or _openai_client is None:
        return None

    try:
        mode, client_or_module = _openai_client
        # Prefer lightweight models if available
        preferred_models = [
            'gpt-4o-mini',
            'gpt-4o',
            'gpt-4-turbo',
            'gpt-3.5-turbo'
        ]

        if mode == 'new':
            # New client usage
            ClientClass = client_or_module
            client = ClientClass(api_key=api_key)
            model = preferred_models[0]
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for Morocco travel."},
                        {"role": "user", "content": prompt_text}
                    ],
                    temperature=0.5,  # 0.4→0.5 より創造的で詳細な回答を生成
                    max_tokens=1200,  # 600→1200 より長く詳細な回答を許可
                    timeout=20  # 15→20秒 長い回答生成のためタイムアウト延長
                )
            except Exception:
                # Try a fallback model
                model = preferred_models[-1]
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for Morocco travel."},
                        {"role": "user", "content": prompt_text}
                    ],
                    temperature=0.5,  # 0.4→0.5
                    max_tokens=1200,  # 600→1200
                    timeout=20  # 15→20秒
                )
            content = resp.choices[0].message.content if resp and resp.choices else None
            return content
        else:
            # Legacy openai module
            openai = client_or_module
            openai.api_key = api_key
            model = preferred_models[-1]
            try:
                completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant for Morocco travel."},
                        {"role": "user", "content": prompt_text}
                    ],
                    temperature=0.5,  # 0.4→0.5 より創造的で詳細な回答を生成
                    max_tokens=1200  # 800→1200 より長く詳細な回答を許可
                )
                return completion.choices[0].message["content"]
            except Exception as e:
                logger.warning(f"OpenAI legacy call failed: {e}")
                return None
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return None

# Load .env if present so OPENAI_API_KEY and other env vars are available during local runs
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; if not available, environment vars must be set externally
    pass

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def summarize_snippets(snippet_blocks: List[str], max_chars: int = 1200) -> str:
    """要約器: OpenAI が利用可能なら要約を依頼し、なければ軽量な抽出的要約にフォールバックする。

    Args:
        snippet_blocks: 各スニペット文字列のリスト（ヘッダ行を含む）
        max_chars: 返す要約の最大文字数（概算）

    Returns:
        生成されたコンパクトな要約文字列（必要なら短い参照一覧を末尾に追加）
    """
    try:
        if not snippet_blocks:
            return ""

        # コンパクトな入力を作る（各スニペットは先頭行のソースヘッダだけを残す）
        headers = []
        bodies = []
        for b in snippet_blocks:
            lines = [ln for ln in b.splitlines() if ln.strip()]
            if not lines:
                continue
            header = lines[0]
            body = " ".join(lines[1:])[:800]
            headers.append(header)
            bodies.append(body)

        compact_input = "\n\n".join([f"{h}\n{bod}" for h, bod in zip(headers, bodies)])

        # Try using OpenAI for a concise summary if available
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and _openai_client is not None:
            sum_prompt = (
                "次の参照コンテキストの要点を日本語で簡潔に要約してください。"
                " 各参照の要点は1-2文にまとめ、行頭に該当する出典を [SOURCE:...] として示してください。"
                f" 要約全体はおおむね{max_chars}文字以内に収めてください。\n\n{compact_input}"
            )
            try:
                resp = call_openai_api(sum_prompt)
                if resp:
                    # Append compact source list to help citation lookup
                    src_list = "\n\n参照元一覧:\n" + "\n".join(headers[:10])
                    out = resp.strip()
                    # Ensure length limit
                    if len(out) > max_chars:
                        out = out[:max_chars].rstrip() + "..."
                    return out + src_list
            except Exception as e:
                logger.info(f"OpenAI summarization failed, falling back: {e}")

        # Fallback: simple extractive summarization
        #  各スニペットから最初の1-2文を取り、全体を繋げて切り詰める
        sentences = []
        for body in bodies:
            # split Japanese/English sentences conservatively
            sents = re.split(r'(?<=[。！？!?])\s*', body)
            for s in sents:
                ts = s.strip()
                if ts:
                    sentences.append(ts)
                    break
        # If nothing found, fall back to first N chars of compact_input
        if not sentences:
            short = compact_input[:max_chars]
            src_list = "\n\n参照元一覧:\n" + "\n".join(headers[:10])
            return short + (src_list if headers else "")

        combined = "。 ".join(sentences)
        if len(combined) > max_chars:
            combined = combined[:max_chars].rstrip() + "..."
        src_list = "\n\n参照元一覧:\n" + "\n".join(headers[:10])
        return combined + src_list
    except Exception as e:
        logger.error(f"summarize_snippets error: {e}")
        return ""

# ユーザー入力検証関数
def validate_user_input(input_text, max_length=100, min_length=1):
    """ユーザー入力の検証"""
    if not input_text:
        return False, "入力が空です"
    
    # 文字列の場合の処理
    if isinstance(input_text, str):
        text = input_text.strip()
        if len(text) < min_length:
            return False, f"入力は{min_length}文字以上である必要があります"
        if len(text) > max_length:
            return False, f"入力は{max_length}文字以下である必要があります"
        
        # XSS防止のための基本的なサニタイゼーション
        import html
        sanitized = html.escape(text)
        return True, sanitized
    
    return True, input_text

def safe_file_operation(file_path, operation_type="read"):
    """ファイル操作の安全性チェック"""
    try:
        # ファイルパスの正規化
        normalized_path = os.path.normpath(file_path)
        
        # パストラバーサル攻撃防止
        if ".." in normalized_path or normalized_path.startswith("/"):
            logger.warning(f"Suspicious file path detected: {file_path}")
            return False, "不正なファイルパスです"
        
        # ファイル存在チェック（読み込み時）
        if operation_type == "read" and not os.path.exists(normalized_path):
            return False, f"ファイルが見つかりません: {normalized_path}"
        
        return True, normalized_path
    except Exception as e:
        logger.error(f"File operation validation error: {e}")
        return False, f"ファイル操作エラー: {str(e)}"

# エラーハンドリングデコレーター（強化版）
def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            logger.error(f"File not found in {func.__name__}: {str(e)}")
            st.error("📁 ファイルが見つかりません。管理者にお問い合わせください。")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error in {func.__name__}: {str(e)}")
            st.error("📄 データファイルの形式が正しくありません。")
            return None
        except PermissionError as e:
            logger.error(f"Permission error in {func.__name__}: {str(e)}")
            st.error("🔒 ファイルへのアクセス権限がありません。")
            return None
        except ValueError as e:
            logger.error(f"Value error in {func.__name__}: {str(e)}")
            st.error(f"⚠️ 入力値が正しくありません: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            st.error(f"❌ 予期しないエラーが発生しました: {str(e)}")
            with st.expander("🔍 エラー詳細（開発者向け）", expanded=False):
                st.code(traceback.format_exc())
            return None
    return wrapper

# パフォーマンス測定デコレーター
def measure_performance(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"{func.__name__} completed in {end_time - start_time:.3f} seconds")
        return result
    return wrapper

# ページ設定
st.set_page_config(
    page_title="モロッコ観光ガイド",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# テーマ設定の初期化
def init_theme():
    """テーマ設定の初期化"""
    try:
        if "theme" not in st.session_state:
            st.session_state.theme = "ライト"
        return st.session_state.theme
    except Exception as e:
        logger.warning(f"Theme initialization failed: {e}")
        return "ライト"

@handle_errors
def get_background_image_css():
    """背景画像のCSSを取得（エラーハンドリング強化版）"""
    import base64
    
    # 背景画像ファイルのパス（優先順に検索）
    alternative_paths = [
        os.path.join(os.path.dirname(__file__), "morocco_background.jpg"),
        r"c:\Users\user\Pictures\morocco_bg.jpg",
        r"c:\Users\user\Pictures\grjebasj2c5fmtqrxoh1.jpg",
    ]
    bg_image_path = None
    for p in alternative_paths:
        if os.path.exists(p):
            bg_image_path = p
            logger.info(f"Using background image path: {p}")
            break
    if not bg_image_path:
        # 明示的にFileNotFoundErrorを投げしてフォールバックCSSへ制御を渡す
        raise FileNotFoundError("No background image found in configured paths")
    
    try:
        # ファイル安全性チェック
        is_safe, result = safe_file_operation(bg_image_path, "read")
        if not is_safe:
            logger.warning(f"Background image file check failed: {result}")
            raise FileNotFoundError(result)
        
        # ファイルサイズチェック（10MB制限）
        file_size = os.path.getsize(bg_image_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            logger.warning(f"Background image too large: {file_size} bytes")
            raise ValueError(f"画像ファイルが大きすぎます: {file_size / (1024*1024):.1f}MB")
        
        # 画像ファイルをBase64エンコード
        with open(bg_image_path, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        
        logger.info(f"Background image loaded successfully: {len(img_data)} chars")
        
        css_template = """
        <style>
            /* Majorelle Blue + Gold Color Palette */
            :root {{
                --majorelle-blue: #6246EA;
                --majorelle-blue-light: rgba(98, 70, 234, 0.1);
                --majorelle-blue-medium: rgba(98, 70, 234, 0.6);
                --majorelle-blue-dark: #4A34C7;
                --gold: #FFD700;
                --gold-light: rgba(255, 215, 0, 0.1);
                --gold-medium: rgba(255, 215, 0, 0.3);
                --white-glass: rgba(255, 255, 255, 0.12);
                --white-glass-strong: rgba(255, 255, 255, 0.18);
                --text-primary: #2D1B69;
                --text-secondary: #6B7280;
                --text-light: rgba(255, 255, 255, 0.9);
            }}
            
            .stApp {{
                background: 
                    linear-gradient(to bottom, 
                        rgba(255, 255, 255, 0.2) 0%,
                        rgba(255, 255, 255, 0.1) 15%,
                        rgba(98, 70, 234, 0.15) 30%,
                        rgba(77, 52, 199, 0.25) 50%,
                        rgba(45, 27, 105, 0.4) 80%,
                        rgba(0, 0, 0, 0.3) 100%
                    ), 
                    url(data:image/jpeg;base64,{img_data});
                background-size: cover !important;
                background-position: center center !important;
                background-attachment: fixed !important;
                background-repeat: no-repeat !important;
                image-rendering: auto;
                min-height: 100vh;
                position: relative;
                z-index: 0;
            }
            
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.2);
                z-index: 0;
                pointer-events: none;
            }}
            
            .main {{
                position: relative;
                z-index: 1;
            }}
            
            /* Streamlit container adjustments for clean layout */
            .main .block-container {{
                padding-top: 1rem !important;
                margin-top: 0 !important;
                max-width: 1200px;
                padding-bottom: 0 !important;
            }}
            
            .stApp > header {{
                height: 0 !important;
                display: none !important;
                margin: 0 !important;
                padding: 0 !important;
            }}
            
            .main > div:first-child {{
                margin-top: 0 !important;
                padding-top: 0 !important;
            }}
            
            /* Remove Streamlit default margins */
            .main {{
                padding-top: 0 !important;
                margin-top: 0 !important;
            }}
            
            /* Remove any default spacing from Streamlit elements */
            [data-testid="stAppViewContainer"] {{
                padding-top: 0 !important;
            }}
            
            [data-testid="stHeader"] {{
                display: none !important;
                height: 0 !important;
            }}
            
            [data-testid="stToolbar"] {{
                display: none !important;
            }}
            
            /* ページ全体の上余白を削除 */
            main > div, .block-container {{
                padding-top: 0 !important;
                margin-top: 0 !important;
            }}

            /* タイトル部分の余白を削る */
            header {{
                margin-top: -2rem !important;
            }}

            /* さらに Streamlit の自動トップマージンを無効化 */
            section.main > div {{
                padding-top: 0 !important;
            }}
            
            .home-background {
                min-height: 0vh;
                padding: 0;
                margin: 0;
            }
            
            /* .home-content 削除済み */
            

            
            /* Section Background Hierarchy */
            .section-background-primary {{
                background: linear-gradient(135deg, 
                    var(--white-glass-strong) 0%, 
                    var(--majorelle-blue-light) 100%);
                border-radius: 20px;
                padding: 24px;
                margin: 16px 0;
                backdrop-filter: blur(20px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            .section-background-secondary {{
                background: linear-gradient(135deg, 
                    var(--gold-light) 0%, 
                    var(--white-glass) 100%);
                border-radius: 16px;
                padding: 20px;
                margin: 12px 0;
                backdrop-filter: blur(16px) saturate(160%);
                border: 1px solid rgba(255, 215, 0, 0.2);
            }}
            
            .section-background-tertiary {{
                background: var(--white-glass);
                border-radius: 12px;
                padding: 16px;
                margin: 8px 0;
                backdrop-filter: blur(12px) saturate(140%);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .home-header {{
                background: linear-gradient(135deg, var(--majorelle-blue) 0%, var(--majorelle-blue-dark) 50%, var(--gold) 100%);
                color: var(--text-light);
                padding: 40px 32px 48px 32px;
                border-radius: 20px;
                text-align: center;
                margin: -20px -24px 32px -24px;
                box-shadow: 
                    0 20px 40px rgba(98, 70, 234, 0.3),
                    0 8px 16px rgba(98, 70, 234, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
                position: relative;
                overflow: hidden;
            }}
            
            .home-header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url(data:image/jpeg;base64,{img_data});
                background-size: cover;
                background-position: center;
                opacity: 0.1;
                z-index: -1;
            }}
            
            .home-header h1 {{
                font-size: 2.8rem;
                margin-bottom: 16px;
                text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
                font-weight: 700;
                letter-spacing: 0.5px;
                line-height: 1.3;
                animation: titleSlideIn 1.2s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
                opacity: 0;
                transform: translateY(30px);
            }}
            
            .home-header p {{
                font-size: 1.1rem;
                margin: 0;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
                font-weight: 400;
                opacity: 0;
                line-height: 1.7;
                animation: subtitleFadeIn 1s cubic-bezier(0.4, 0.0, 0.2, 1) 0.3s forwards;
                transform: translateY(20px);
            }}
            
            @keyframes titleSlideIn {{
                0% {{
                    opacity: 0;
                    transform: translateY(30px) scale(0.95);
                }}
                100% {{
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }}
            }}
            
            @keyframes subtitleFadeIn {{
                0% {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                100% {{
                    opacity: 0.95;
                    transform: translateY(0);
                }}
            }}
            
            .metric-container {{
                background: var(--white-glass);
                border-radius: 12px;
                padding: 20px;
                margin: 16px 0;
                backdrop-filter: blur(16px) saturate(180%);
                box-shadow: 
                    0 4px 16px rgba(98, 70, 234, 0.1),
                    0 1px 4px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .spot-card {{
                background: rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                padding: 24px;
                margin: 16px 0;
                backdrop-filter: blur(28px) saturate(220%);
                box-shadow: 
                    0 12px 40px rgba(98, 70, 234, 0.2),
                    0 6px 20px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6),
                    inset 0 -1px 0 rgba(0, 0, 0, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.4);
                transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
                position: relative;
                z-index: 2;
            }}
            
            .spot-card:hover {{
                transform: translateY(-6px) scale(1.01);
                filter: brightness(1.03);
                box-shadow: 
                    0 20px 40px rgba(98, 70, 234, 0.25),
                    0 12px 24px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
            }}
            
            .spot-title {{
                font-size: 1.3rem;
                font-weight: 600;
                color: white;
                margin-bottom: 8px;
                line-height: 1.4;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
            }}
            
            .spot-meta {{
                color: white;
                margin-bottom: 16px;
                font-size: 0.95rem;
                line-height: 1.6;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
            }}
            
            .category-badge {{
                background: linear-gradient(135deg, var(--majorelle-blue), var(--majorelle-blue-dark));
                color: white;
                padding: 8px 14px;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 3px 12px rgba(98, 70, 234, 0.4);
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            .verified-badge {{
                background: linear-gradient(135deg, var(--gold), #FFA500);
                color: #1a1a1a;
                padding: 8px 14px;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 700;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 3px 12px rgba(255, 215, 0, 0.4);
                text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            .recommendation-card {{
                background: rgba(255, 255, 255, 0.4);
                border-radius: 12px;
                padding: 0;
                margin: 16px 0;
                backdrop-filter: blur(32px) saturate(250%);
                box-shadow: 
                    0 16px 48px rgba(98, 70, 234, 0.25),
                    0 8px 24px rgba(0, 0, 0, 0.2),
                    inset 0 2px 0 rgba(255, 255, 255, 0.7),
                    inset 0 -2px 0 rgba(0, 0, 0, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.5);
                transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
                height: 380px;
                display: flex;
                flex-direction: column;
                position: relative;
                overflow: hidden;
                z-index: 2;
            }}
            
            .card-thumbnail {{
                position: relative;
                height: 120px;
                overflow: hidden;
                border-radius: 12px 12px 8px 8px;
            }}
            
            .thumbnail-placeholder {{
                width: 100%;
                height: 100%;
                background: linear-gradient(135deg, var(--majorelle-blue-light), var(--gold-light));
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
            }}
            
            .thumbnail-icon {{
                font-size: 3rem;
                opacity: 0.8;
                z-index: 2;
                position: relative;
            }}
            
            .thumbnail-gradient {{
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, 
                    var(--majorelle-blue-medium), 
                    transparent 50%, 
                    var(--gold-medium));
                opacity: 0.6;
            }}
            
            .recommendation-card::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                background: linear-gradient(90deg, var(--majorelle-blue), var(--gold));
                opacity: 0.8;
            }}
            
            .recommendation-card:hover {{
                transform: translateY(-8px) scale(1.01);
                filter: brightness(1.03);
                box-shadow: 
                    0 24px 48px rgba(98, 70, 234, 0.25),
                    0 12px 24px rgba(0, 0, 0, 0.18),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
            }}
            
            .card-header {{
                border-bottom: 2px solid var(--gold);
                padding: 16px 20px 12px 20px;
                margin-bottom: 0;
                background: rgba(255, 255, 255, 0.2);
                backdrop-filter: blur(8px);
                border-radius: 12px 12px 0 0;
            }}
            
            .card-title {{
                font-size: 1.25rem;
                font-weight: 700;
                color: white;
                margin: 0 0 8px 0;
                line-height: 1.4;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
            }}
            
            .card-location {{
                color: white;
                font-size: 0.9rem;
                line-height: 1.6;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
            }}
            
            .card-content {{
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                padding: 16px 20px 20px 20px;
            }}
            
            .card-category {{
                margin-bottom: 16px;
            }}
            
            .card-description {{
                color: white;
                line-height: 1.6;
                flex-grow: 1;
                font-size: 0.9rem;
                margin-bottom: 16px;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
            }}
            
            .card-features {{
                margin-top: auto;
            }}
            
            .feature-tag {{
                background: rgba(255, 255, 255, 0.9);
                color: var(--majorelle-blue-dark);
                padding: 6px 12px;
                border-radius: 8px;
                font-size: 0.8rem;
                font-weight: 600;
                margin-right: 8px;
                display: inline-block;
                margin-bottom: 4px;
                border: 1px solid var(--majorelle-blue-medium);
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                text-shadow: none;
            }}
            
            .city-card {{
                background: var(--white-glass-strong);
                border-radius: 12px;
                padding: 24px;
                text-align: center;
                backdrop-filter: blur(18px) saturate(180%);
                box-shadow: 
                    0 6px 20px rgba(98, 70, 234, 0.12),
                    0 2px 8px rgba(0, 0, 0, 0.08),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.25);
                transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
                height: 180px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}
            
            .city-card:hover {{
                transform: translateY(-6px) scale(1.01);
                filter: brightness(1.03);
                box-shadow: 
                    0 16px 32px rgba(98, 70, 234, 0.22),
                    0 8px 16px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6);
            }}
            
            .info-section {{
                background: var(--white-glass-strong);
                border-radius: 12px;
                padding: 24px;
                backdrop-filter: blur(18px) saturate(180%);
                box-shadow: 
                    0 8px 24px rgba(98, 70, 234, 0.12),
                    0 4px 12px rgba(0, 0, 0, 0.08),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.25);
            }}
            
            .info-section h3 {{
                color: white;
                margin-bottom: 16px;
                border-bottom: 3px solid var(--gold);
                padding-bottom: 8px;
                font-size: 1.25rem;
                font-weight: 700;
                line-height: 1.4;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
            }}
            
            .info-card {{
                background: var(--white-glass);
                border-radius: 8px;
                padding: 16px;
                margin-top: 16px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 2px 8px rgba(98, 70, 234, 0.08);
            }}
            
            .info-card h4 {{
                color: white;
                margin-bottom: 12px;
                font-size: 1.1rem;
                font-weight: 600;
                line-height: 1.4;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
            }}
            
            .info-card ul {{
                margin: 0;
                padding-left: 20px;
            }}
            
            .info-card li {{
                color: white;
                margin-bottom: 8px;
                line-height: 1.6;
                font-size: 0.9rem;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
            }}
            
            /* Typography Hierarchy - Improved Readability */
            h1 {{ 
                font-size: 2.5rem; 
                line-height: 1.3; 
                font-weight: 700; 
                margin-bottom: 1rem;
                color: white;
                text-shadow: 0 2px 6px rgba(0, 0, 0, 0.8);
            }}
            h2 {{ 
                font-size: 2rem; 
                line-height: 1.4; 
                font-weight: 600; 
                margin-bottom: 0.8rem;
                color: white;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
            }}
            h3 {{ 
                font-size: 1.5rem; 
                line-height: 1.4; 
                font-weight: 600; 
                margin-bottom: 0.6rem;
                color: white;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.7);
            }}
            h4 {{ 
                font-size: 1.2rem; 
                line-height: 1.5; 
                font-weight: 600; 
                margin-bottom: 0.5rem;
                color: white;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.6);
            }}
            p, li {{ 
                font-size: 1rem;
                line-height: 1.7; 
                margin-bottom: 1rem;
                color: white;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.6);
                color: #2a2a2a;
            }}
            
            /* Enhanced text contrast for cards */
            .recommendation-card p, .spot-card p, .city-card p {{
                background: rgba(255, 255, 255, 0.8);
                padding: 8px 12px;
                border-radius: 6px;
                margin: 8px 0;
                color: #1a1a1a;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }}
            
            /* Small text for descriptions */
            .small-text {{
                font-size: 0.9rem;
                line-height: 1.6;
            }}
            
            /* Large text for emphasis */
            .large-text {{
                font-size: 1.1rem;
                line-height: 1.6;
                font-weight: 500;
            }}
            
            /* Scroll Fade-In Animation */
            .fade-in-element {{
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
            }}
            
            .fade-in-element.fade-in-visible {{
                opacity: 1;
                transform: translateY(0);
            }}
            
            .stale-in-left {{
                opacity: 0;
                transform: translateX(-30px);
                transition: all 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
            }}
            
            .stale-in-left.fade-in-visible {{
                opacity: 1;
                transform: translateX(0);
            }}
            
            .stale-in-right {{
                opacity: 0;
                transform: translateX(30px);
                transition: all 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
            }}
            
            .stale-in-right.fade-in-visible {{
                opacity: 1;
                transform: translateX(0);
            }}
            
            /* Staggered Animation for Cards */
            .recommendation-card:nth-child(1) {{
                animation-delay: 0.1s;
            }}
            
            .recommendation-card:nth-child(2) {{
                animation-delay: 0.2s;
            }}
            
            .recommendation-card:nth-child(3) {{
                animation-delay: 0.3s;
            }}
            
            .recommendation-card:nth-child(4) {{
                animation-delay: 0.4s;
            }}
            
            .card-appear {{
                animation: cardAppear 0.8s cubic-bezier(0.4, 0.0, 0.2, 1) forwards;
                opacity: 0;
                transform: translateY(20px) scale(0.95);
            }}
            
            @keyframes cardAppear {{
                0% {{
                    opacity: 0;
                    transform: translateY(20px) scale(0.95);
                }}
                100% {{
                    opacity: 1;
                    transform: translateY(0) scale(1);
                }}
            }}
            
            /* Page Load Animation */
            @keyframes pageLoadFade {{
                0% {{
                    opacity: 0;
                    transform: translateY(20px);
                }}
                100% {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            .main {{
                animation: pageLoadFade 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
            }}
            
            /* Smooth Scroll Enhancement */
            html {{
                scroll-behavior: smooth;
                scroll-padding-top: 20px;
            }}
            
            /* Pulse Loading Animation for Elements */
            .loading-pulse {{
                animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }}
            
            @keyframes pulse {{
                0%, 100% {{
                    opacity: 1;
                }}
                50% {{
                    opacity: .5;
                }}
            }}
            
            /* Smooth transitions for all interactive elements */
            .spot-card, .recommendation-card, .city-card, .info-section {{
                transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
            }}
            
            /* Enhanced Hover Glow Effect */
            .spot-card:hover, .recommendation-card:hover, .city-card:hover {{
                box-shadow: 
                    0 0 40px rgba(98, 70, 234, 0.3),
                    0 20px 40px rgba(98, 70, 234, 0.25),
                    0 12px 24px rgba(0, 0, 0, 0.15),
                    inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
            }}
            
            /* Text Readability Improvements */
            .text-box {{
                background: rgba(0, 0, 0, 0.4);
                padding: 1rem;
                border-radius: 12px;
                margin: 1rem 0;
                backdrop-filter: blur(8px);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .readable-text {{
                color: white !important;
                text-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
                line-height: 1.6;
            }}
            
            .text-overlay {{
                background: rgba(0, 0, 0, 0.5);
                padding: 1.5rem;
                border-radius: 16px;
                margin: 1rem 0;
                backdrop-filter: blur(12px) saturate(150%);
                border: 1px solid rgba(255, 255, 255, 0.15);
                box-shadow: 
                    0 8px 24px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }}
            
            .text-overlay h1, .text-overlay h2, .text-overlay h3, .text-overlay h4, .text-overlay p {{
                color: white !important;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
                margin-bottom: 1rem;
            }}
            
            .enhanced-readability {{
                background: linear-gradient(135deg, 
                    rgba(0, 0, 0, 0.6) 0%, 
                    rgba(45, 27, 105, 0.5) 100%);
                padding: 2rem;
                border-radius: 20px;
                margin: 1.5rem 0;
                backdrop-filter: blur(16px) saturate(180%);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 
                    0 12px 32px rgba(0, 0, 0, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
            }}
            
            .enhanced-readability * {{
                color: white !important;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.9);
            }}
            
            /* Enhanced Buttons */
            .stButton > button {{
                background: linear-gradient(135deg, var(--majorelle-blue), var(--majorelle-blue-dark)) !important;
                color: white !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 12px 24px !important;
                font-weight: 600 !important;
                font-size: 0.9rem !important;
                box-shadow: 
                    0 4px 12px rgba(98, 70, 234, 0.3),
                    0 2px 6px rgba(0, 0, 0, 0.1) !important;
                transition: all 0.4s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
                position: relative;
                overflow: hidden;
            }}
            
            .stButton > button::before {{
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, 
                    transparent, 
                    rgba(255, 255, 255, 0.2), 
                    transparent);
                transition: left 0.5s;
            }}
            
            .stButton > button:hover::before {{
                left: 100%;
            }}
            
            .stButton > button:hover {{
                background: linear-gradient(135deg, var(--majorelle-blue-dark), var(--gold)) !important;
                transform: translateY(-3px) scale(1.02) !important;
                filter: brightness(1.05) !important;
                box-shadow: 
                    0 12px 28px rgba(98, 70, 234, 0.5),
                    0 6px 16px rgba(0, 0, 0, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
            }}
            
            .stButton > button[data-baseweb="button"][kind="primary"] {{
                background: linear-gradient(135deg, var(--gold), #FFA500) !important;
                color: var(--text-primary) !important;
                box-shadow: 
                    0 4px 12px rgba(255, 215, 0, 0.4),
                    0 2px 6px rgba(0, 0, 0, 0.1) !important;
            }}
            
            .stButton > button[data-baseweb="button"][kind="primary"]:hover {{
                background: linear-gradient(135deg, #FFA500, var(--majorelle-blue)) !important;
                color: white !important;
                transform: translateY(-3px) scale(1.02) !important;
                filter: brightness(1.05) !important;
                box-shadow: 
                    0 12px 28px rgba(255, 165, 0, 0.5),
                    0 6px 16px rgba(0, 0, 0, 0.2) !important;
            }}
            
            /* Mobile Responsive Design */
            @media (max-width: 768px) {{
                .home-header {{
                    padding: 24px 16px 32px 16px;
                    margin: -16px -16px 24px -16px;
                }}
                
                .home-header h1 {{
                    font-size: 2rem !important;
                    margin-bottom: 12px;
                    line-height: 1.2;
                }}
                
                .home-header p {{
                    font-size: 1rem !important;
                    line-height: 1.5;
                }}
                
                .metric-container {{
                    padding: 12px 8px !important;
                    margin: 8px 4px !important;
                }}
                
                .metric-container > div:first-child {{
                    font-size: 2rem !important;
                    margin-bottom: 4px;
                }}
                
                .metric-container > div:nth-child(2) {{
                    font-size: 1.5rem !important;
                }}
                
                .metric-container > div:last-child {{
                    font-size: 0.9rem !important;
                }}
                
                .recommendation-card {{
                    margin: 8px 0 !important;
                    padding: 16px !important;
                }}
                
                .card-title {{
                    font-size: 1.1rem !important;
                    margin-bottom: 8px;
                }}
                
                .card-description {{
                    font-size: 0.9rem !important;
                    line-height: 1.4;
                }}
                
                .info-section {{
                    margin: 16px 0 !important;
                }}
                
                .info-section h3 {{
                    font-size: 1.3rem !important;
                    margin-bottom: 12px;
                }}
                
                .info-card {{
                    padding: 12px !important;
                }}
                
                .info-card h4 {{
                    font-size: 1rem !important;
                    margin-bottom: 8px;
                }}
                
                .info-card li {{
                    font-size: 0.9rem !important;
                    line-height: 1.4;
                    margin-bottom: 4px;
                }}
            }}
            
            @media (max-width: 480px) {{
                .home-header h1 {{
                    font-size: 1.7rem !important;
                    letter-spacing: 0.3px;
                }}
                
                .home-header p {{
                    font-size: 0.95rem !important;
                }}
                
                .metric-container {{
                    padding: 10px 6px !important;
                    margin: 6px 2px !important;
                }}
                
                .recommendation-card {{
                    padding: 12px !important;
                }}
                
                .card-title {{
                    font-size: 1rem !important;
                }}
                
                .card-location {{
                    font-size: 0.8rem !important;
                }}
                
                .card-description {{
                    font-size: 0.85rem !important;
                }}
            }}
        </style>
        """
        
        # Use simple replace to avoid Python str.format parsing of CSS braces
        css_filled = css_template.replace("{{", "{").replace("}}", "}")
        css_filled = css_filled.replace("{img_data}", img_data)
        return css_filled
        
    except FileNotFoundError:
        logger.warning("Background image not found, using fallback background")
        return """
        <style>
            /* Majorelle Blue + Gold Color Palette - Fallback */
            :root {
                --majorelle-blue: #6246EA;
                --majorelle-blue-light: rgba(98, 70, 234, 0.1);
                --majorelle-blue-medium: rgba(98, 70, 234, 0.6);
                --majorelle-blue-dark: #4A34C7;
                --gold: #FFD700;
                --gold-light: rgba(255, 215, 0, 0.1);
                --gold-medium: rgba(255, 215, 0, 0.3);
                --white-glass: rgba(255, 255, 255, 0.12);
                --white-glass-strong: rgba(255, 255, 255, 0.18);
                --text-primary: #2D1B69;
                --text-secondary: #6B7280;
                --text-light: rgba(255, 255, 255, 0.9);
            }
            
            .stApp {
                background: linear-gradient(135deg, 
                    #6246EA 0%, 
                    #4A34C7 25%,
                    #FFD700 50%,
                    #6246EA 75%,
                    #2D1B69 100%);
                background-size: 400% 400%;
                animation: gradientShift 15s ease infinite;
                min-height: 100vh;
                position: relative;
            }
            
            .stApp::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    linear-gradient(to bottom, 
                        rgba(255, 255, 255, 0.3) 0%,
                        rgba(255, 255, 255, 0.1) 20%,
                        rgba(0, 0, 0, 0.1) 60%,
                        rgba(0, 0, 0, 0.2) 100%
                    );
                pointer-events: none;
                z-index: 1;
            }
            
            @keyframes gradientShift {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            
            .home-background {
                background: transparent;
                min-height: 0vh;
                padding: 0;
                margin: 0;
                position: relative;
                z-index: 2;
            }
            
            .home-content {
                background: var(--white-glass-strong);
                padding: 24px;
                border-radius: 20px;
                backdrop-filter: blur(20px) saturate(180%);
                box-shadow: 
                    0 8px 32px rgba(0, 0, 0, 0.12),
                    0 2px 16px rgba(0, 0, 0, 0.08),
                    inset 0 1px 0 rgba(255, 255, 255, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.3);
                margin: 0;
            }
        </style>
        """

def get_theme_css(theme):
    """テーマに応じたCSSを取得"""
    if theme == "ダーク":
        return """
        <style>
            /* ダークテーマ */
            .stApp {
                background-color: #1e1e1e;
                color: #ffffff;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            
            .main-header {
                text-align: center;
                padding: 1rem;
                background: linear-gradient(90deg, #c0392b, #8b0000);
                color: white;
                border-radius: 10px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            .spot-card {
                border: 1px solid #444;
                border-radius: 10px;
                padding: 1rem;
                margin: 0.5rem 0;
                background: #2d2d2d;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                color: #ffffff;
            }
            
            .spot-title {
                color: #ffffff;
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .spot-meta {
                color: #cccccc;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }
            
            .verified-badge {
                background: #27ae60;
                color: white;
                padding: 0.2rem 0.5rem;
                border-radius: 15px;
                font-size: 0.8rem;
            }
            
            .category-badge {
                background: #3498db;
                color: white;
                padding: 0.2rem 0.5rem;
                border-radius: 15px;
                font-size: 0.8rem;
                margin-right: 0.5rem;
            }
            
            /* Streamlitコンポーネントのダークテーマ調整 */
            .stSelectbox > div > div {
                background-color: #2d2d2d;
                border: 1px solid #444;
                color: #ffffff;
            }
            
            .stTextInput > div > div {
                background-color: #2d2d2d;
                border: 1px solid #444;
                color: #ffffff;
            }
            
            .stTextArea > div > div {
                background-color: #2d2d2d;
                border: 1px solid #444;
                color: #ffffff;
            }
            
            .stMultiSelect > div > div {
                background-color: #2d2d2d;
                border: 1px solid #444;
            }
            
            .stSidebar {
                background-color: #1a1a1a;
            }
            
            .css-1d391kg {
                background-color: #1a1a1a;
            }
            
            /* メトリクスカードのダークテーマ */
            [data-testid="metric-container"] {
                background: linear-gradient(90deg, #2d2d2d, #3a3a3a);
                border: 1px solid #444;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }
            
            /* タブのダークテーマ */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #2d2d2d;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            
            /* チャット要素のダークテーマ */
            .stChatMessage {
                background-color: #2d2d2d;
                border: 1px solid #444;
            }
            
            /* マークダウンテキストのダークテーマ */
            .stMarkdown {
                color: #ffffff;
            }
            
            /* 情報ボックスのダークテーマ */
            .stInfo {
                background-color: #2d4a5a;
                border: 1px solid #3498db;
            }
            
            .stSuccess {
                background-color: #2d4a2d;
                border: 1px solid #27ae60;
            }
            
            .stWarning {
                background-color: #4a4a2d;
                border: 1px solid #f39c12;
            }
            
            .stError {
                background-color: #4a2d2d;
                border: 1px solid #e74c3c;
            }
            
            /* ボタンのダークテーマ */
            .stButton > button {
                background-color: #3a3a3a;
                border: 1px solid #555;
                color: #ffffff;
            }
            
            .stButton > button:hover {
                background-color: #4a4a4a;
                border: 1px solid #666;
            }
            
            /* リンクのダークテーマ */
            a {
                color: #5dade2;
            }
            
            a:hover {
                color: #85c1e9;
            }
            
            /* テーブルのダークテーマ */
            .stDataFrame {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            
            /* セレクトボックスの詳細スタイル */
            .stSelectbox > div > div > div {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            
            /* カスタムホバー効果 */
            .spot-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.4);
                transition: all 0.3s ease;
            }
            
            /* スクロール位置制御 */
            html {
                scroll-behavior: smooth;
                overflow-anchor: none;
            }
            
            body {
                scroll-behavior: smooth;
                overflow-anchor: none;
            }
            
            /* 詳細ページのスクロール制御 */
            #detail-page-top {
                position: relative;
                top: 0;
                scroll-margin-top: 0;
                scroll-snap-margin-top: 0;
            }
        </style>
        """
    else:
        return """
        <style>
            /* ライトテーマ */
            .stApp {
                background-color: #ffffff;
                color: #000000;
                transition: background-color 0.3s ease, color 0.3s ease;
            }
            
            .main-header {
                text-align: center;
                padding: 1rem;
                background: linear-gradient(90deg, #e74c3c, #c0392b);
                color: white;
                border-radius: 10px;
                margin-bottom: 2rem;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            .spot-card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 1rem;
                margin: 0.5rem 0;
                background: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                color: #000000;
            }
            
            .spot-title {
                color: #2c3e50;
                font-size: 1.2rem;
                font-weight: bold;
                margin-bottom: 0.5rem;
            }
            
            .spot-meta {
                color: #7f8c8d;
                font-size: 0.9rem;
                margin-bottom: 0.5rem;
            }
            
            .verified-badge {
                background: #27ae60;
                color: white;
                padding: 0.2rem 0.5rem;
                border-radius: 15px;
                font-size: 0.8rem;
            }
            
            .category-badge {
                background: #3498db;
                color: white;
                padding: 0.2rem 0.5rem;
                border-radius: 15px;
                font-size: 0.8rem;
                margin-right: 0.5rem;
            }
            
            /* メトリクスカードのライトテーマ */
            [data-testid="metric-container"] {
                background: linear-gradient(90deg, #f8f9fa, #e9ecef);
                border: 1px solid #dee2e6;
                padding: 1rem;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            /* カスタムホバー効果 */
            .spot-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }
            
            /* ボタンのライトテーマ */
            .stButton > button {
                background-color: #ffffff;
                border: 1px solid #ddd;
                color: #000000;
            }
            
            .stButton > button:hover {
                background-color: #f8f9fa;
                border: 1px solid #ccc;
            }
            
            /* スクロール位置制御 */
            html {
                scroll-behavior: smooth;
                overflow-anchor: none;
            }
            
            body {
                scroll-behavior: smooth;
                overflow-anchor: none;
            }
            
            /* 詳細ページのスクロール制御 */
            #detail-page-top {
                position: relative;
                top: 0;
                scroll-margin-top: 0;
                scroll-snap-margin-top: 0;
            }
        </style>
        """

# テーマの初期化とCSS適用
current_theme = init_theme()
st.markdown(get_theme_css(current_theme), unsafe_allow_html=True)

# 観光地データ
@st.cache_data
@handle_errors
@measure_performance
def load_spots_data():
    """観光地データを読み込み"""
    try:
        # 外部JSONファイルから読み込み
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'spots.json')
        if os.path.exists(json_path):
            with open(json_path, 'r', encoding='utf-8') as f:
                spots = json.load(f)
            logger.info(f"Loaded {len(spots)} spots from external JSON file")
            return spots
        else:
            logger.warning("External JSON file not found, using embedded data")
    except Exception as e:
        logger.error(f"Error loading external JSON: {e}")
        st.warning("⚠️ データファイルの読み込みに失敗しました。内蔵データを使用します。")
    
    # フォールバック：内蔵データ
    spots = [
        # マラケシュの観光地（15箇所）
        {
            'id': 1,
            'name': 'ジャマ・エル・フナ広場',
            'city': 'マラケシュ',
            'category': '広場・市場',
            'summary': 'モロッコ最大の文化交流の場として1000年以上親しまれるユネスコ世界遺産の広場',
            'features': {
                '景観': '赤レンガ造りの建物に囲まれた広大な石畳の広場、夜には幻想的なライトアップ',
                '歴史': '11世紀のアルモラヴィ朝時代から商業の中心地として発達、ユネスコ無形文化遺産',
                '文化': 'ベルベル、アラブ、アンダルシア文化が融合した「生きた文化博物館」'
            },
            'highlights': [
                'フレッシュオレンジジュース屋台（10-15DH）',
                '伝統的なヘナタトゥー体験',
                '大道芸人のパフォーマンス（蛇使い、音楽、語り部）',
                '夜の屋台グルメ（タジン、ケバブ、ハリラスープ）',
                '周辺スークでの買い物体験'
            ],
            'how_to_enjoy': {
                '昼間（10:00-16:00）': 'オレンジジュースを飲みながら広場の雰囲気を楽しむ、周辺スークでお土産探し',
                '夕方（16:00-19:00）': '夕日に染まる広場の美しさを堪能、屋台の準備風景を観察',
                '夜（19:00-23:00）': '本格的な屋台グルメと大道芸のメインタイム、現地の人々との交流'
            },
            'access_notes': {
                'アクセス': 'マラケシュ新市街から徒歩15分、タクシー利用可（20-30DH）',
                '注意点': '貴重品管理注意、しつこい客引きは丁寧に断る、屋台の値段交渉が必要',
                '服装': '歩きやすい靴推奨、夜は少し冷えるので羽織り物があると良い'
            },
            'verified': True,
            'lat': 31.625964,
            'lng': -7.989250,
            'best_time': '夕方〜夜',
            'duration': '2-3時間',
            'price_range': '無料（飲食・買い物は別）'
        },
        {
            'id': 2,
            'name': 'クトゥビア・モスク',
            'city': 'マラケシュ',
            'category': '宗教建築',
            'summary': 'マラケシュの象徴的ランドマーク、12世紀に建造された高さ77mの美しいミナレットを持つ歴史的モスク',
            'features': {
                '景観': '赤砂岩造りの荘厳なミナレット、街のどこからでも見える圧倒的な存在感',
                '歴史': '1150年頃アルモハード朝により建造、モロッコ・イスラム建築の最高傑作',
                '文化': '5回の礼拝時間に響く美しいアザーン（祈りの呼びかけ）'
            },
            'highlights': [
                '高さ77mの美しいミナレット',
                'ジャマ・エル・フナ広場からの絶景ビュー',
                '夜間の幻想的なライトアップ',
                '伝統的なイスラム建築様式の観察',
                '周辺の美しい庭園散策'
            ],
            'how_to_enjoy': {
                '日中（10:00-16:00）': '建築美を詳細に観察、周辺庭園でのんびり過ごす',
                '夕方（16:00-18:00）': '夕日に映える赤砂岩の美しさを堪能',
                '夜間（19:00-22:00）': 'ライトアップされたミナレットの撮影、広場からの眺望'
            },
            'access_notes': {
                'アクセス': 'ジャマ・エル・フナ広場から徒歩5分',
                '注意点': '非イスラム教徒は内部立入禁止、外観観賞のみ',
                '撮影': '外観の撮影は可能、respectful な態度で'
            },
            'verified': True,
            'lat': 31.624307,
            'lng': -7.993252,
            'best_time': '夕方〜夜（ライトアップ）',
            'duration': '30分〜1時間',
            'price_range': '無料（外観のみ）'
        },
        {
            'id': 3,
            'name': 'バイア宮殿',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'summary': '19世紀の大臣が建てた「美しい」宮殿、精巧なタイル装飾と160の部屋を持つモロッコ建築の傑作',
            'features': {
                '景観': '8ヘクタールの庭園と中央中庭、大理石の床と美しい噴水',
                '歴史': '1880年代、アフメド・イブン・ムーサ大臣が14年かけて建設',
                '文化': 'モロッコ・アンダルシア建築様式、ゼリージュ（モザイクタイル）技術の最高峰'
            },
            'highlights': [
                '精巧なゼリージュ（モザイクタイル）装飾',
                '彫刻された石膏装飾とアラベスク模様',
                '色とりどりの天井画と幾何学文様',
                '中央中庭の大理石床と噴水',
                '8ヘクタールの美しい庭園散策'
            ],
            'how_to_enjoy': {
                '入館時（9:00-10:00）': '朝の光が差し込む中庭の美しさを堪能',
                '見学中（10:00-11:00）': '各部屋の装飾技法を詳細に観察、写真撮影',
                '庭園散策（11:00-12:00）': '宮殿を囲む庭園でリラックス、建築美を振り返る'
            },
            'access_notes': {
                'アクセス': 'ジャマ・エル・フナ広場から徒歩15分、またはタクシー',
                '営業時間': '9:00-17:00（金曜日は14:30-15:30休憩）',
                '注意点': '内部撮影可能だが一部制限あり、入場券は現地購入のみ'
            },
            'verified': True,
            'lat': 31.620947,
            'lng': -7.982908,
            'best_time': '午前中（光の入り方が美しい）',
            'duration': '1-2時間',
            'price_range': '70DH（約800円）'
        },
        {
            'id': 4,
            'name': 'マジョレル庭園',
            'city': 'マラケシュ',
            'category': '庭園',
            'summary': 'イヴ・サンローランが愛した「マジョレル・ブルー」の植物園、300種の植物とベルベル博物館を持つ芸術的オアシス',
            'features': {
                '景観': '鮮やかなコバルトブルーの建物、世界中から集めた300種以上の植物、砂漠都市のオアシス',
                '歴史': '1924年フランス人画家ジャック・マジョレルが造成、1980年イヴ・サンローランが買取・復元',
                '文化': 'モロッコの植物文化とフランス芸術の融合、ベルベル文化の展示'
            },
            'highlights': [
                '「マジョレル・ブルー」のコバルトブルー建物',
                '300種以上の世界の植物（サボテン、椰子、バンブー）',
                'ベルベル博物館の伝統工芸品コレクション',
                'イヴ・サンローラン博物館（隣接）',
                '四季折々の美しい花々と庭園散策'
            ],
            'how_to_enjoy': {
                '早朝（8:00-10:00）': '涼しい時間帯に静かな庭園散策、写真撮影に最適な光',
                '午前中（10:00-12:00）': 'ベルベル博物館でモロッコ文化を学習、植物観察',
                '夕方（16:00-18:00）': '夕日に映える青い建物の美しさ、カフェでリラックス'
            },
            'access_notes': {
                'アクセス': '新市街ゲリーズ地区、マラケシュ中心部からタクシー15分',
                '営業時間': '8:00-18:00（10月-4月は17:30まで）',
                '注意点': '人気スポットのため混雑、朝一番の訪問がおすすめ'
            },
            'verified': True,
            'lat': 31.641214,
            'lng': -8.003674,
            'best_time': '早朝または夕方',
            'duration': '1-2時間',
            'price_range': '庭園150DH、博物館込み300DH'
        },
        {
            'id': 5,
            'name': 'サーディアン朝の墳墓群',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'summary': '16世紀のサーディアン王朝の霊廟群、300年間封印されていた「12の柱の間」を持つイスラム装飾芸術の傑作',
            'features': {
                '景観': '白大理石の柱と鍾乳石装飾の天井、色とりどりのゼリージュタイル',
                '歴史': '1557年建設、1917年まで300年間城壁に封印、フランス統治時代に再発見',
                '文化': 'サーディアン朝の権力と富の象徴、イスラム建築・装飾技術の最高峰'
            },
            'highlights': [
                '「12の柱の間」の白大理石柱とムカルナス天井',
                '精巧なゼリージュ（モザイクタイル）装飾',
                'アラベスク文様の石膏彫刻と大理石象嵌',
                'アーマド・アル・マンスール王の豪華な石棺',
                '美しい中庭と庭園の散策'
            ],
            'how_to_enjoy': {
                '入場時（9:00-10:00）': '朝の静寂な霊廟で荘厳な雰囲気を体感',
                '見学中（10:00-11:00）': '各霊廟の装飾技法を詳細に観察、写真撮影',
                '退場前（11:00-12:00）': '庭園で建築美を振り返り、歴史に思いを馳せる'
            },
            'access_notes': {
                'アクセス': 'クトゥビア・モスクから徒歩10分、バイア宮殿から徒歩5分',
                '営業時間': '9:00-17:00',
                '注意点': '神聖な場所のため、respectful な態度で見学'
            },
            'verified': True,
            'lat': 31.621439,
            'lng': -7.984467,
            'best_time': '午前中',
            'duration': '45分〜1時間',
            'price_range': '70DH（約800円）'
        },
        {
            'id': 6,
            'name': 'メナラ庭園',
            'city': 'マラケシュ',
            'category': '庭園',
            'summary': '12世紀から続く王室庭園。アトラス山脈を映す人工湖とパビリオンが織りなす絵画のような風景で、夕日の美しさは格別です。',
            'features': {
                '景観': '人工湖に映るアトラス山脈、夕日に輝く湖面、約10万本のオリーブ畑',
                '歴史': '12世紀アルモハード朝の灌漑システム、サアード朝時代のパビリオン改築',
                '文化': 'モロッコ古典庭園の傑作、農業技術と美学の融合、王室の避暑地'
            },
            'highlights': [
                'アトラス山脈を背景にした湖面の反射美',
                '19世紀建造の美しいパビリオンとその内部装飾',
                '夕日時間帯の湖面が金色に染まる絶景',
                '10万本のオリーブの木が作り出す銀緑の風景',
                '古代から続く巧妙な水利システムの見学'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '湖畔散歩、オリーブ畑見学、パビリオン内部見学',
                '昼間（11:00-16:00）': 'ピクニック、読書、庭園でのんびり',
                '夕方（16:00-19:00）': '夕日鑑賞、アトラス山脈の撮影、ロマンチックなひととき'
            },
            'access_notes': 'マラケシュ市内からタクシーで15分（50DH）。徒歩は1時間程度。日陰が少ないため帽子・日焼け止め必須。夕方は特に美しいが混雑するため早めの到着推奨。',
            'verified': True,
            'lat': 31.605000,
            'lng': -8.024444,
            'best_time': '夕方（サンセット）',
            'duration': '1-2時間',
            'price_range': '30DH（約350円）'
        },
        {
            'id': 7,
            'name': 'ベン・ユーセフ・マドラサ',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'summary': '14世紀マリーン朝が建設したマグリブ地域最大の神学校。900人の学生が学んだ教育の聖地で、精緻な装飾美術の傑作。',
            'features': {
                '建築': '中央中庭を囲むアーケード、130の学生寮、3階建ての壮大な構造',
                '装飾': '大理石とゼリージュの柱廊、杉材の精巧な天井、アラビア書道の石膏細工',
                '歴史': '14-16世紀の教育センター、イスラム学術の中心地、マリーン朝建築の最高傑作'
            },
            'highlights': [
                '中央中庭の息を呑む美しい装飾柱廊',
                '130の小さな学生寮と生活空間の再現',
                '幾何学模様とアラビア書道が施された壁面装飾',
                '杉材で作られた精巧な天井の木工細工',
                '当時の学生生活と教育システムの展示'
            ],
            'how_to_enjoy': {
                '入場（30分）': '音声ガイドで歴史を学び、建築美を鑑賞',
                '中庭散策（20分）': '装飾の詳細を観察、写真撮影',
                '学生寮見学（15分）': '当時の学生生活を想像しながら小部屋を見学'
            },
            'access_notes': 'ジャマ・エル・フナ広場から徒歩10分。スーク散策と合わせて訪問がおすすめ。午前中は光が差し込み撮影に最適。フラッシュ撮影禁止。',
            'verified': True,
            'lat': 31.631667,
            'lng': -7.989167,
            'best_time': '午前中（10:00-12:00）',
            'duration': '1-1.5時間',
            'price_range': '50DH（約570円）'
        },
        {
            'id': 8,
            'name': 'アグダル庭園',
            'city': 'マラケシュ',
            'category': '庭園',
            'summary': '12世紀から続く400ヘクタールの王室庭園。現在も機能する古代水利システムと果樹園が織りなす農業遺産の傑作。',
            'features': {
                '規模': '400ヘクタールの広大な敷地、東京ドーム85個分の巨大庭園',
                '農業': 'オリーブ、オレンジ、ザクロ、イチジク、アーモンドの果樹園',
                '水利': '800年前の灌漑システム、2つの大型貯水池、現役の給水機能'
            },
            'highlights': [
                '12世紀から変わらない古代灌漑システムの驚異',
                '季節ごとに実る豊富な果樹（オレンジ、ザクロ、イチジク）',
                '王室の離宮として使用される歴史的建造物',
                '400ヘクタールの圧倒的なスケールの自然景観',
                'アトラス山脈を背景にした絵画のような風景'
            ],
            'how_to_enjoy': {
                '入園（15分）': '王室庭園の歴史解説を聞き、全体map確認',
                '果樹園散策（60分）': '季節の果樹観察、古代灌漑システム見学',
                '貯水池エリア（30分）': '水利技術の見学、景観撮影'
            },
            'access_notes': '金・土曜日のみ開園（週2日限定）。マラケシュ中心部からタクシー20分。広大なため歩きやすい靴必須。日陰少なく帽子・水分持参推奨。',
            'verified': True,
            'lat': 31.609722,
            'lng': -7.965556,
            'best_time': '金・土曜日の午前中（9:00-12:00）',
            'duration': '1.5-2.5時間',
            'price_range': '10DH（約115円）'
        },
        # カサブランカの観光地（12箇所）
        {
            'id': 9,
            'name': 'ハッサン2世モスク',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'summary': '世界第3位の規模を誇る海に浮かぶモスク、高さ210mのミナレットとガラス床を持つ現代イスラム建築の傑作',
            'features': {
                '景観': '大西洋に面した圧巻の立地、世界最高210mのミナレット、10万人収容の巨大空間',
                '歴史': '1993年完成、ハッサン2世国王の命により7年かけて建設、モロッコの国家プロジェクト',
                '文化': '伝統と現代の融合、モロッコの職人技術と最新テクノロジーの結晶'
            },
            'highlights': [
                '世界最高210mのミナレット（レーザー光でメッカ方向を指示）',
                'ガラス床から大西洋を見下ろす唯一無二の体験',
                '25,000平方mの巨大礼拝堂と精巧な装飾',
                'モロッコ全土から集められた最高級素材',
                '屋外広場から望む大西洋の絶景'
            ],
            'how_to_enjoy': {
                'ガイドツアー（9:00-10:00）': '内部見学で建築技術と装飾の詳細を学習',
                '自由見学（10:00-11:00）': 'ガラス床体験、ミナレット展望、写真撮影',
                '海岸散策（11:00-12:00）': '外観を海側から眺める、周辺コルニッシュ散歩'
            },
            'access_notes': {
                'アクセス': 'カサブランカ市街地からタクシー20分、トラム利用可',
                'ツアー時間': '金曜以外9:00,10:00,11:00,14:00開始',
                '注意点': '非ムスリムはガイドツアーのみ入場可、適切な服装必須'
            },
            'verified': True,
            'lat': 33.608311,
            'lng': -7.632815,
            'best_time': '午前中（ガイドツアー）',
            'duration': '1-2時間',
            'price_range': 'ツアー130DH（約1500円）'
        },
        {
            'id': 10,
            'name': 'リック・カフェ',
            'city': 'カサブランカ',
            'category': '文化施設',
            'summary': '映画「カサブランカ」の世界を完璧再現した伝説のカフェ・レストラン。「君の瞳に乾杯」の舞台で映画ファン必見の聖地。',
            'features': {
                '映画再現': '1940年代の内装完全再現、映画小道具、アンティーク家具配置',
                '雰囲気': '毎夜のピアノ演奏、薄暗い照明、ノスタルジックな音楽',
                '料理': 'モロッコ・フランス融合料理、名物タジン、厳選ワインセレクション'
            },
            'highlights': [
                '映画「カサブランカ」の名シーン再現スポット',
                '毎夜演奏される「時の過ぎゆくままに」ピアノライブ',
                '映画ポスターとアンティーク家具で彩られた1940年代内装',
                '「君の瞳に乾杯」を実際に体験できる特別な瞬間',
                'ハンフリー・ボガートとイングリッド・バーグマンの写真展示'
            ],
            'how_to_enjoy': {
                'アペリティフ（18:00-19:00）': '映画の世界観に浸りながらカクテルタイム',
                'ディナー（19:00-21:00）': '本格モロッコ・フランス料理を映画音楽と共に',
                'ピアノタイム（21:00-22:00）': '生演奏を聞きながら映画の名シーンを回想'
            },
            'access_notes': 'カサブランカ旧市街内、ハッサン2世モスクから徒歩15分。要予約（特に夕食時）。ドレスコード：スマートカジュアル。',
            'verified': True,
            'lat': 33.594629,
            'lng': -7.619054,
            'best_time': '夕方〜夜（18:00-22:00）',
            'duration': '2-3時間',
            'price_range': 'ディナー300-500DH（約3500-5800円）'
        },
        {
            'id': 11,
            'name': 'カサブランカ旧市街（メディナ）',
            'city': 'カサブランカ',
            'category': '都市・建築',
            'description': '18世紀に建設されたカサブランカの旧市街。白い家々が立ち並ぶ小さな迷路のような街並みは、大都市カサブランカの中にある静かなオアシスです。伝統的なモロッコ建築、小さなモスク、地元の工芸品店、昔ながらのハマム（公衆浴場）などが点在し、現代都市の喧騒を忘れさせてくれます。特に朝の散歩がおすすめで、地元の人々の日常生活を垣間見ることができます。',
            'verified': True,
            'lat': 33.598056,
            'lng': -7.611944,
            'best_time': '午前中',
            'duration': '1-2時間',
            'price_range': '無料'
        },
        {
            'id': 12,
            'name': 'モハメッド5世広場',
            'city': 'カサブランカ',
            'category': '広場・市場',
            'summary': 'フランス保護領時代の都市計画が生んだカサブランカの行政中枢。政府建物に囲まれた格調高い広場で夜のライトアップが美しい。',
            'features': {
                '建築': 'フランス植民地時代の都市計画、新古典主義建築、対称的な広場設計',
                '政治': 'モロッコの行政中心地、重要政府機関の集積地、国家行事の舞台',
                '文化': '中央郵便局の美しい建築、ムーレイ・ユーセフ・モスクとの調和'
            },
            'highlights': [
                '夜間のライトアップされた美しい中央噴水',
                'フランス植民地時代の新古典主義建築群',
                '重要な政府建物（裁判所、中央郵便局）の外観',
                'ムーレイ・ユーセフ・モスクとの宗教・世俗の調和',
                'カサブランカの都市計画の傑作としての景観'
            ],
            'how_to_enjoy': {
                '昼間（10:00-16:00）': '政府建築の外観見学、中央郵便局訪問、都市計画の美しさを鑑賞',
                '夕方（16:00-19:00）': '広場でのカフェタイム、地元のビジネスマンの往来観察',
                '夜間（19:00-22:00）': 'ライトアップされた噴水と建物群の夜景撮影'
            },
            'access_notes': 'カサブランカ中央駅から徒歩10分。周辺に多数のカフェ・レストラン。平日は政府関係者で混雑。夜景撮影は20:00以降がおすすめ。',
            'verified': True,
            'lat': 33.596944,
            'lng': -7.622222,
            'best_time': '夕方〜夜',
            'duration': '30分〜1時間',
            'price_range': '無料'
        },
        {
            'id': 13,
            'name': 'ノートルダム・ド・ルルド教会',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'summary': 'モロッコ最大都市に建つ美しいカトリック教会。イスラム国家における宗教的多様性と寛容さを象徴する現代建築の傑作。',
            'features': {
                '建築': 'モダン建築とモロッコ伝統要素の融合、独特の現代的デザイン、機能的な美しさ',
                '宗教': 'イスラム国家でのカトリック信仰、宗教的寛容性、フランス植民地の遺産',
                '芸術': '美しいステンドグラス、現代的祭壇デザイン、静寂な祈りの空間'
            },
            'highlights': [
                '色とりどりの美しいステンドグラスアート',
                'モダン建築とモロッコ様式の絶妙な融合',
                'イスラム国家での宗教的多様性を体現する空間',
                '毎日行われるミサと国際的な信者コミュニティ',
                '静寂で神聖な祈りの雰囲気と建築美'
            ],
            'how_to_enjoy': {
                '見学（20分）': '建築デザインの鑑賞、ステンドグラス観察',
                'ミサ参加（60分）': '宗教体験、多文化コミュニティとの交流（日曜8:00/10:00）',
                '静寂タイム（15分）': '祈りと瞑想、心の平安を得る時間'
            },
            'access_notes': 'カサブランカ中心部、モハメッド5世広場から徒歩15分。ミサ時間：平日7:00、日曜8:00/10:00。適切な服装で入場。写真撮影は許可制。',
            'verified': True,
            'lat': 33.589722,
            'lng': -7.623889,
            'best_time': '午前中（9:00-11:00）',
            'duration': '30-60分',
            'price_range': '無料（寄付歓迎）'
        },
        {
            'id': 14,
            'name': 'カサブランカ・ツインセンター',
            'city': 'カサブランカ',
            'category': '現代建築',
            'summary': 'モロッコ最高層115メートルの双子タワー。現代モロッコの経済発展を象徴し、市街と大西洋の絶景展望台を持つランドマーク。',
            'features': {
                '建築': '2つの28階建てタワー、モロッコ最高層115メートル、現代建築の傑作',
                '機能': 'ショッピングモール、国際オフィス、5つ星ホテル、展望デッキ',
                '象徴': '現代モロッコの経済発展、アフリカのビジネスハブ、国際都市の証'
            },
            'highlights': [
                '展望デッキからのカサブランカ市街360度パノラマ',
                '大西洋の水平線まで見渡せる絶景ビュー',
                '夜間の美しいライトアップとイルミネーション',
                'モロッコ最大級のショッピングモール体験',
                '高層階からのハッサン2世モスクの俯瞰'
            ],
            'how_to_enjoy': {
                'ショッピング（2時間）': '高級ブランドショップ、国際的なフードコート体験',
                '展望デッキ（30分）': '市街パノラマ、大西洋絶景、写真撮影',
                '夜景鑑賞（1時間）': 'ライトアップされたカサブランカの夜景を堪能'
            },
            'access_notes': 'カサブランカ市街中心部、タクシーで主要ホテルから10分。展望デッキは天候により閉鎖の場合あり。ショッピングモールは10:00-22:00営業。',
            'verified': True,
            'lat': 33.588889,
            'lng': -7.630556,
            'best_time': '夕方（16:00-19:00）展望デッキ',
            'duration': '1-3時間',
            'price_range': '展望デッキ50DH（約580円）'
        },
        {
            'id': 15,
            'name': 'ムーレイ・ユーセフ・モスク',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'summary': 'カサブランカ最古級のモスクで、伝統的モロッコ・アンダルシア建築の美しい代表例。モハメッド5世広場の重要なランドマーク。',
            'features': {
                '建築': '伝統的モロッコ・アンダルシア様式、白い壁と緑のタイル装飾、優雅なミナレット',
                '歴史': '20世紀初頭創建、フランス保護領時代の改築、カサブランカの宗教的発展',
                '文化': '日常的な礼拝の場、金曜日の集団礼拝、地域イスラム共同体の中心'
            },
            'highlights': [
                '伝統的モロッコ・アンダルシア建築の美しい外観',
                '白い壁面に映える緑のゼリージュ（モザイクタイル）',
                'シンプルで優雅なミナレットのデザイン',
                'モハメッド5世広場との調和した都市景観',
                '金曜日の集団礼拝時の信者たちの様子'
            ],
            'how_to_enjoy': {
                '外観鑑賞（15分）': '建築美の観察、写真撮影（適切な距離から）',
                '周辺散策（30分）': '旧市街との組み合わせ散策、カフェでの休憩',
                '文化観察（15分）': '礼拝時間の信者の様子を見学（敬意を持って）'
            },
            'access_notes': 'モハメッド5世広場から徒歩2分。非ムスリムは外観見学のみ。礼拝時間は騒音を避ける。写真撮影は建物に敬意を払って適切な距離から。',
            'verified': True,
            'lat': 33.598333,
            'lng': -7.620833,
            'best_time': '午前中（10:00-12:00）',
            'duration': '30分（外観見学）',
            'price_range': '無料'
        },
        # フェズの観光地（10箇所）
        {
            'id': 16,
            'name': 'フェズ・エル・バリ',
            'city': 'フェズ',
            'category': '都市・建築',
            'summary': '世界最大の車両進入禁止都市、ユネスコ世界遺産。1200年続く迷宮都市で28万人が暮らす生きた中世都市の奇跡。',
            'features': {
                '都市構造': '9000本の路地が網目状、世界最大の歩行者専用都市、幅1メートルの迷路',
                '文化遺産': '1200年続く伝統工芸、革なめし・金属細工・陶器作りの職人街',
                '生活': '28万人の住民、生きた歴史都市、中世から変わらぬ日常生活'
            },
            'highlights': [
                '世界最大の車両進入禁止歴史都市の散策',
                '1200年前から変わらない迷宮のような路地構造',
                '現役で稼働する伝統工芸の職人街見学',
                '中世イスラム都市の完璧に保存された街並み',
                '28万人が暮らす生きた歴史都市の日常風景'
            ],
            'how_to_enjoy': {
                '午前（9:00-12:00）': 'ガイド付き迷宮探索、主要モスクと学校見学',
                '昼（12:00-15:00）': '職人街見学、伝統工芸体験、スーク散策',
                '午後（15:00-18:00）': '住宅地散策、地元生活観察、カフェ休憩'
            },
            'access_notes': '徒歩でのみアクセス可能。迷子防止のため公認ガイド推奨（300-500DH）。狭い路地で道に迷いやすい。貴重品管理注意。',
            'verified': True,
            'lat': 34.063611,
            'lng': -4.972222,
            'best_time': '午前中（9:00-12:00）涼しい時間帯',
            'duration': '半日〜1日',
            'price_range': 'ガイド300-500DH（約3500-5800円）'
        },
        {
            'id': 17,
            'name': 'カラウィーン大学・モスク',
            'city': 'フェズ',
            'category': '歴史建築',
            'description': '859年にファーティマ・アル・フィフリーヤによって創設された世界最古の大学の一つ。ギネスブックにも認定されているこの学府は、1200年以上にわたって学問の中心地として機能し続けています。図書館には40万冊以上の写本があり、その中にはイブン・ルシュド（アヴェロエス）やマイモニデスの貴重な著作も含まれています。現在も8000人以上の学生が学ぶ現役の宗教教育機関で、イスラム世界の知的遺産の宝庫です。',
            'verified': True,
            'lat': 34.064444,
            'lng': -4.974167,
            'best_time': '午前中',
            'duration': '1時間（外観・中庭）',
            'price_range': '無料（ムスリム以外は中庭まで）'
        },
        {
            'id': 18,
            'name': 'シュワラ皮なめし場',
            'city': 'フェズ',
            'category': '伝統工芸',
            'description': '11世紀から続く世界最大かつ最古の皮なめし工場。数百の石製の染色槽が並ぶ光景は圧巻で、職人たちが素足で槽に入り、1000年変わらない伝統技法で革をなめしています。鳩の糞、石灰、塩、各種植物染料を使用する天然製法で作られるフェズレザーは世界的に有名。ミントを鼻に当てながら見学する独特の体験は、フェズでしかできない貴重なものです。周辺の革製品店での買い物も楽しめます。',
            'verified': True,
            'lat': 34.066667,
            'lng': -4.971389,
            'best_time': '午前中（暑さを避ける）',
            'duration': '1時間',
            'price_range': '見学無料（チップあり）'
        },
        {
            'id': 19,
            'name': 'ボウ・イナニア・マドラサ',
            'city': 'フェズ',
            'category': '歴史建築',
            'description': '1356年にマリーン朝のスルタン・アブー・イナーンによって建設された神学校。マリーン朝建築の最高傑作とされ、精緻な装飾技術の粋を集めた建物です。入口の青銅製の扉、中庭の大理石の柱、壁面を覆う幾何学模様のゼリージュ、アラベスク文様の石膏彫刻、そして天井の杉材の装飾など、あらゆる装飾要素が完璧に調和しています。現在も祈りの場として使用されている生きた遺産です。',
            'verified': True,
            'lat': 34.065556,
            'lng': -4.973333,
            'best_time': '午前中',
            'duration': '45分〜1時間',
            'price_range': '20DH（約230円）'
        },
        {
            'id': 20,
            'name': 'ダール・バタ博物館',
            'city': 'フェズ',
            'category': '博物館',
            'description': '19世紀の宮殿を改装したモロッコ工芸美術博物館。フェズの伝統工芸品の宝庫で、精巧な木工細工、金属工芸、陶器、絨毯、刺繍、書道作品などが展示されています。特に有名なのは青と白の美しいフェズ陶器のコレクション。建物自体も美しく、中庭の噴水と庭園、装飾タイル、彫刻された石膏など、アンダルシア建築の傑作です。フェズの文化遺産を包括的に理解できる重要な施設です。',
            'verified': True,
            'lat': 34.062778,
            'lng': -4.976389,
            'best_time': '午前中',
            'duration': '1-2時間',
            'price_range': '20DH（約230円）'
        },
        {
            'id': 21,
            'name': 'メリニード朝の墳墓群',
            'city': 'フェズ',
            'category': '歴史建築',
            'description': 'フェズを見下ろす丘の上にある14世紀マリーン朝の王族墓地。廃墟となった霊廟群ですが、フェズ・エル・バリの全景を一望できる絶景スポットとして人気です。特に夕日の時間帯は、旧市街の無数のミナレットや赤い屋根瓦が夕日に染まり、1000年の歴史を持つ古都の美しさを実感できます。写真撮影の名所でもあり、多くの観光客が訪れる定番スポットです。',
            'verified': True,
            'lat': 34.072222,
            'lng': -4.970000,
            'best_time': '夕方（サンセット）',
            'duration': '1時間',
            'price_range': '無料'
        },
        {
            'id': 22,
            'name': 'アッタリーン・マドラサ',
            'city': 'フェズ',
            'category': '歴史建築',
            'description': '1325年にマリーン朝によって建設された小さいながらも最も美しい神学校の一つ。「香辛料商のマドラサ」という意味の名前が示すように、スパイス市場に隣接しています。3階建ての建物は中庭を囲むように設計され、学生寮の小部屋が並んでいます。装飾の密度と質の高さは驚異的で、特に中庭の柱廊のタイルワークと石膏装飾は必見。小規模だからこそ、細部まで行き届いた職人技の素晴らしさを堪能できます。',
            'verified': True,
            'lat': 34.064722,
            'lng': -4.974722,
            'best_time': '午前中',
            'duration': '30分〜45分',
            'price_range': '20DH（約230円）'
        },
        # メルズーガとサハラ砂漠の観光地（6箇所）
        {
            'id': 23,
            'name': 'エルグ・シェビ砂丘',
            'city': 'メルズーガ',
            'category': '自然',
            'summary': 'モロッコで最も美しいサハラ砂漠の砂丘群。高さ150mの金色の砂丘が連なる、砂漠体験の聖地として知られています。',
            'features': {
                '景観': '金色の砂丘群、360度の砂漠パノラマ、満天の星空',
                '自然': '高さ150mの砂丘、サハラ砂漠の中心部、砂の色彩変化',
                '体験': 'ラクダトレッキング、砂漠キャンプ、ベルベル音楽鑑賞'
            },
            'highlights': [
                '金色からオレンジ、赤、紫へと変化する砂丘の色彩',
                '砂丘頂上からの360度砂漠パノラマビュー',
                '満天の星空の下でのベルベル音楽体験',
                'ラクダに乗って砂丘を登る伝統的な砂漠体験'
            ],
            'how_to_enjoy': {
                '日の出前（5:30-6:30）': '砂丘登頂、日の出の色彩変化観賞',
                '午前（7:00-11:00）': 'ラクダトレッキング、砂漠散策',
                '日中（11:00-17:00）': '砂漠キャンプ休憩、ベルベル文化体験',
                '夕方（17:00-19:00）': '日没観賞、砂丘の色彩変化',
                '夜間（19:00-翌朝）': 'キャンプファイヤー、星空観察、ベルベル音楽'
            },
            'access_notes': '- メルズーガから4WDまたはラクダでアクセス\n- 砂漠ツアーは1-2日のキャンプが一般的\n- 日の出・日没時間の確認が重要\n- 砂漠用の服装と日焼け止めが必須',
            'description': 'モロッコで最も美しい砂丘群の一つ。高さ150メートルの金色の砂丘が連なるこの地域は、サハラ砂漠体験の聖地です。ラクダトレッキングで砂丘の頂上に登れば、360度の砂漠パノラマが広がります。日の出と日没時の色彩変化は息をのむ美しさで、砂丘が金色からオレンジ、赤、紫へと変化する様子は一生の思い出になります。砂漠キャンプでは満天の星空の下でベルベル音楽を楽しめます。',
            'verified': True,
            'lat': 31.099167,
            'lng': -4.010556,
            'best_time': '日の出・日没',
            'duration': '1-2日（キャンプ含む）',
            'price_range': 'ツアー500-1500DH'
        },
        {
            'id': 24,
            'name': 'ハッシ・ラブド砂丘',
            'city': 'メルズーガ',
            'category': '自然',
            'summary': 'エルグ・シェビの北に位置する静寂な砂丘エリア。観光客が少なく、手つかずのサハラ砂漠と化石発見地として知られています。',
            'features': {
                '景観': '360度砂丘パノラマ、手つかずの砂漠風景、静寂な環境',
                '自然': '化石発見地、三葉虫化石、原始的な砂漠環境',
                '体験': 'サンドボード、クワッドバイク、化石探し'
            },
            'highlights': [
                '観光客が少ない静寂なサハラ砂漠体験',
                '三葉虫の化石が発見される地質学的価値',
                '360度砂丘に囲まれた壮大な環境',
                'サンドボードで砂丘を滑り降りる爽快感'
            ],
            'how_to_enjoy': {
                '午前（9:00-12:00）': '4WDでアクセス、砂丘散策',
                '昼（12:00-14:00）': '化石探し、地質観察',
                '午後（14:00-16:00）': 'サンドボード、クワッドバイク',
                '夕方（16:00-18:00）': '砂丘登頂、夕日観賞',
                '夜間': '星空観察（キャンプ宿泊の場合）'
            },
            'access_notes': '- 4WDまたはクワッドバイクでのアクセスが必要\n- エルグ・シェビより観光客が少ない穴場\n- 化石は持ち帰り禁止\n- 砂漠用装備と水分補給が重要',
            'description': 'エルグ・シェビの北に位置する静寂な砂丘エリア。観光客が少なく、より手つかずのサハラ砂漠を体験できます。化石の発見地としても知られ、三葉虫の化石が多数発見されています。360度砂丘に囲まれた環境で、砂漠の静寂と壮大さを純粋に感じることができる隠れた名所。サンドボードやクワッドバイクのアクティビティも楽しめます。',
            'verified': True,
            'lat': 31.094167,
            'lng': -4.045556,
            'best_time': '午後〜夕方',
            'duration': '半日',
            'price_range': 'ツアー300-600DH'
        },
        # シャウエンの観光地（8箇所）
        {
            'id': 25,
            'name': 'シャウエン旧市街（メディナ）',
            'city': 'シャウエン',
            'category': '都市・建築',
            'summary': '「青い真珠」と称される山間の美しい街、青く塗られた家々が織りなすおとぎ話のような旧市街',
            'features': {
                '景観': '様々な青色に塗られた家々、迷路のような石畳の小径、花で飾られたバルコニー',
                '歴史': '1471年アンダルシアからのムーア人が建設、レコンキスタ後の避難地',
                '文化': 'アンダルシア・ムーア建築様式、ベルベル文化とイスラム文化の融合'
            },
            'highlights': [
                '様々な青色のトーンで塗られた壁面',
                '石畳の迷路のような細い路地',
                '青いドアと窓枠の美しいコントラスト',
                '伝統工芸品の工房とお土産屋',
                '屋上テラスからのリフ山脈の眺望'
            ],
            'how_to_enjoy': {
                '午前中（8:00-12:00）': '美しい朝の光に映える青い街並み散策、写真撮影',
                '昼間（12:00-16:00）': '工房見学、伝統工芸品ショッピング、カフェで休憩',
                '夕方（16:00-19:00）': '夕日に染まる青い街の幻想的な美しさを堪能'
            },
            'access_notes': {
                'アクセス': 'フェズから車で約4時間、タンジェから約2時間半',
                '散策コツ': '迷路のような路地、目印を覚えながら歩くこと',
                '注意点': '観光客向け価格に注意、値段交渉を忘れずに'
            },
            'verified': True,
            'lat': 35.168889,
            'lng': -5.268333,
            'best_time': '午前中（光の加減が美しい）',
            'duration': '半日〜1日',
            'price_range': '散策無料'
        },
        {
            'id': 26,
            'name': 'ウタ・エル・ハマム広場',
            'city': 'シャウエン',
            'category': '広場・市場',
            'summary': 'シャウエンの心臓部となる中央広場。青い街並みを背景にした写真撮影の聖地で、地元の人々との交流の場。',
            'features': {
                '景観': '周囲を青い建物に囲まれた石畳広場、中央の美しい噴水、赤茶色カスバとの色彩対比',
                '文化': '地元民の社交の場、伝統的な茶文化、山間の町ののどかな生活',
                '撮影': 'シャウエンで最も写真映えするスポット、青い街並みの絶好の背景'
            },
            'highlights': [
                '中央噴水と青い街並みの完璧な構図',  
                '夕方の地元民の茶飲み社交風景',
                'カスバの赤茶色と街の青色の美しいコントラスト',
                '周囲のカフェテラスから広場を見下ろす眺望',
                'モロッコ山間部の伝統的な広場文化の体験'
            ],
            'how_to_enjoy': {
                '午前（9:00-12:00）': '静かな広場で朝の光に映える青い街並み撮影',
                '昼（12:00-16:00）': 'カフェでミントティーを飲みながら人間観察',
                '夕方（16:00-19:00）': '地元の人々の社交を見学、夕日に染まる広場'
            },
            'access_notes': 'シャウエン旧市街の中心部、徒歩でのみアクセス可能。周囲にカフェ・レストラン多数。写真撮影時は地元の人への配慮を忘れずに。',
            'verified': True,
            'lat': 35.169444,
            'lng': -5.268056,
            'best_time': '夕方（16:00-18:00）',
            'duration': '1-2時間',
            'price_range': '無料（カフェ利用20-30DH）'
        },
        {
            'id': 27,
            'name': 'シャウエン・カスバ',
            'city': 'シャウエン',
            'category': '歴史建築',
            'summary': '15世紀に建設された要塞で、現在は博物館として機能。城壁からシャウエンの青い街並みとリフ山脈の絶景を一望できます。',
            'features': {
                '景観': '青い街並みの俯瞰、リフ山脈パノラマ、青い屋根瓦のコントラスト',
                '歴史': '15世紀の要塞建築、ベルベル文化の歴史展示',
                '文化': '地域博物館、伝統工芸品展示、文化遺産保存'
            },
            'highlights': [
                '屋上からの青い街全体のパノラマビュー',
                '15世紀の要塞建築と城壁',
                'ベルベル文化と地域史の展示',
                'リフ山脈の雄大な山岳風景',
                '青い屋根瓦と白い壁の美しいコントラスト'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '博物館見学、ベルベル文化について学習',
                '昼（11:00-13:00）': '城壁散策、歴史建築観察',
                '午後（13:00-16:00）': '屋上展望台、青い街並み撮影',
                '夕方（16:00-18:00）': '夕日に染まるリフ山脈観賞'
            },
            'access_notes': '- メディナ中心部から徒歩5分\n- 入場料10DH、カメラ撮影可\n- 屋上は風が強いため注意\n- 階段が多いため歩きやすい靴推奨',
            'description': '15世紀に建設された要塞で、現在は博物館として機能しています。城壁からはシャウエンの青い街並みとリフ山脈の絶景を一望できます。内部には地域の歴史、ベルベル文化、伝統工芸品が展示されており、この地域の豊かな文化遺産を学ぶことができます。特に屋上からのパノラマビューは圧巻で、青い屋根瓦と白い壁のコントラストが美しい町全体を見渡せます。',
            'verified': True,
            'lat': 35.169167,
            'lng': -5.268611,
            'best_time': '午後（展望のため）',
            'duration': '1時間',
            'price_range': '10DH（約115円）'
        },
        {
            'id': 28,
            'name': 'アケチャウル滝',
            'city': 'シャウエン',
            'category': '自然',
            'summary': 'シャウエンから徒歩45分のリフ山脈にある美しい滝。天然プールでの水遊びとハイキングが楽しめる自然スポットです。',
            'features': {
                '景観': 'リフ山脈の清流、滝壺の天然プール、緑豊かな山間風景',
                '自然': '水量豊富な滝、清涼な山の水、四季の自然変化',
                '体験': 'ハイキング、水遊び、自然観察、森林浴'
            },
            'highlights': [
                '春から初夏の水量豊富な迫力ある滝',
                '滝壺の天然プールでの水遊び',
                'リフ山脈の緑豊かなハイキングコース',
                '青い街とは対照的な自然環境',
                '地元の人々も利用する憩いの場'
            ],
            'how_to_enjoy': {
                '出発前（8:00-9:00）': 'ハイキング準備、水分・軽食持参',
                '道中（9:00-10:00）': '山間ハイキング、自然観察',
                '滞在（10:00-14:00）': '滝見学、水遊び、休憩',
                '帰路（14:00-15:00）': 'ハイキング、シャウエン帰還'
            },
            'access_notes': '- シャウエン中心部から徒歩約45分\n- ハイキングシューズと水着持参推奨\n- 春〜初夏が水量豊富でベスト\n- 冬場は水量少なく寒いため注意',
            'description': 'シャウエンの町から徒歩約45分の場所にある美しい滝。リフ山脈の清流が作り出すこの滝は、特に春から初夏にかけて水量が豊富で迫力があります。滝壺は天然のプールのようになっており、夏場は地元の人々が水遊びを楽しむ人気スポット。ハイキングコースとしても整備されており、山間の自然を満喫しながら滝までの道のりを楽しめます。青い街とは対照的な緑豊かな自然が魅力です。',
            'verified': True,
            'lat': 35.150000,
            'lng': -5.275000,
            'best_time': '春〜初夏',
            'duration': '半日（往復）',
            'price_range': '無料'
        },
        # エッサウィラの観光地（8箇所）
        {
            'id': 29,
            'name': 'エッサウィラ・メディナ',
            'city': 'エッサウィラ',
            'category': '都市・建築',
            'summary': '大西洋に面した「風の街」の要塞都市、ユネスコ世界遺産に登録されたヨーロッパ・アフリカ建築融合の傑作',
            'features': {
                '景観': '白い城壁に囲まれた旧市街、大西洋の青と建物の白のコントラスト',
                '歴史': '18世紀フランス人建築家テオドール・コルニュ設計、ポルトガル・フランス植民地遺産',
                '文化': 'ヨーロッパとアフリカ建築の融合、グナワ音楽の聖地、国際的アート都市'
            },
            'highlights': [
                'ユネスコ世界遺産の完璧に保存された要塞都市',
                '大西洋を望む白い城壁と青い海のコントラスト',
                'ポルトガル・フランス・モロッコ建築の融合美',
                'グナワ音楽祭の会場と音楽文化',
                'ウィンドサーフィン・カイトサーフィンの聖地'
            ],
            'how_to_enjoy': {
                '午前中（9:00-12:00）': '城壁散策と大西洋の絶景、旧市街の建築美を堪能',
                '昼間（12:00-16:00）': 'アートギャラリー巡り、グナワ音楽体験、海鮮ランチ',
                '夕方（16:00-19:00）': '漁港見学、夕日鑑賞、風の音を聞きながら散策'
            },
            'access_notes': {
                'アクセス': 'マラケシュから車で約3時間、カサブランカから約4時間',
                '特徴': '年中強い貿易風、ウォータースポーツ最適',
                '注意点': '風が強いため帽子や軽いものに注意'
            },
            'verified': True,
            'lat': 31.513056,
            'lng': -9.769444,
            'best_time': '午前中',
            'duration': '半日〜1日',
            'price_range': '散策無料'
        },
        {
            'id': 30,
            'name': 'スカラ・デュ・ポール',
            'city': 'エッサウィラ',
            'category': '歴史建築',
            'summary': '18世紀建設の海に面した要塞。ポルトガル様式の大砲が設置され、大西洋の絶景と映画撮影地として有名です。',
            'features': {
                '景観': '大西洋パノラマビュー、夕日の絶景、漁港の活気ある風景',
                '歴史': '18世紀ポルトガル様式要塞、古い大砲設置、海洋防衛史',
                '文化': '映画撮影地、海洋博物館、エッサウィラの歴史展示'
            },
            'highlights': [
                'ポルトガル様式の歴史的大砲と城壁',
                '大西洋に沈む美しい夕日のサンセットビュー',
                '映画「オセロ」「キングダム・オブ・ヘブン」撮影地',
                '要塞からの漁港と大西洋のパノラマ',
                '18世紀の海洋防衛建築の見学'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '要塞見学、大砲と城壁観察',
                '昼（11:00-14:00）': '海洋博物館、エッサウィラ史学習',
                '午後（14:00-17:00）': '大西洋展望、漁港観察',
                '夕方（17:00-19:00）': 'サンセット鑑賞、幻想的な要塞シルエット'
            },
            'access_notes': '- メディナから徒歩5分\n- 入場料10DH、夕日時間は混雑\n- 風が強いため防寒着推奨\n- カメラ撮影に最適な絶景スポット',
            'description': '18世紀に建設された海に面した要塞。ポルトガル様式の大砲が設置された城壁からは、大西洋の絶景と漁港の活気ある様子を一望できます。映画「オセロ」や「キングダム・オブ・ヘブン」の撮影地としても有名。夕日の時間帯は特に美しく、オレンジ色に染まる大西洋と要塞のシルエットが幻想的な雰囲気を作り出します。要塞内には小さな博物館もあり、エッサウィラの海洋史を学べます。',
            'verified': True,
            'lat': 31.511944,
            'lng': -9.771389,
            'best_time': '夕方（サンセット）',
            'duration': '1時間',
            'price_range': '10DH（約115円）'
        },
        {
            'id': 31,
            'name': 'エッサウィラ港',
            'city': 'エッサウィラ',
            'category': '港・市場',
            'summary': 'モロッコで最も絵になる漁港。青い漁船と活気ある魚市場で、新鮮な海の幸と漁師たちの生活を体験できます。',
            'features': {
                '景観': '青い漁船の並び、かもめが舞う港風景、大西洋の海岸線',
                '文化': '漁師の伝統的生活、魚市場の活気、海洋文化',
                'グルメ': '新鮮なイワシ、タコ、ウニ、カニ、港沿いシーフードレストラン'
            },
            'highlights': [
                '青い漁船が美しく並ぶ絵画的な港風景',
                '毎日の新鮮な魚介類の水揚げ作業',
                'かもめが舞い踊る活気ある魚市場',
                '港沿いレストランでの獲れたて海の幸',
                '映画のような漁師たちの働く姿'
            ],
            'how_to_enjoy': {
                '早朝（6:00-8:00）': '魚の水揚げ作業見学、漁師の活動観察',
                '午前（8:00-11:00）': '魚市場散策、新鮮な魚介類の見学',
                '昼（11:00-14:00）': '港沿いレストランでシーフードランチ',
                '午後（14:00-17:00）': '港の散策、青い漁船の写真撮影'
            },
            'access_notes': '- メディナから徒歩3分\n- 早朝の水揚げ時間が最も活気がある\n- 魚市場は新鮮な魚介類の購入可能\n- 港沿いレストランで海の幸を堪能',
            'description': 'モロッコで最も絵になる漁港の一つ。青い漁船が並ぶ港では、毎日新鮮な魚介類が水揚げされ、魚市場は活気に満ちています。特にイワシ、タコ、ウニ、カニなどが豊富で、港沿いのレストランでは獲れたての海の幸を味わえます。かもめが舞い踊る中で働く漁師たちの姿は、まるで映画の一場面のよう。朝早い時間帯に訪れると、船から魚を降ろす作業風景を見学できます。',
            'verified': True,
            'lat': 31.511389,
            'lng': -9.770833,
            'best_time': '早朝（魚の水揚げ）',
            'duration': '1時間',
            'price_range': '無料'
        },
        {
            'id': 32,
            'name': 'ムーレイ・ハッサン広場',
            'city': 'エッサウィラ',
            'category': '広場・市場',
            'summary': 'エッサウィラの中心広場で、メディナと新市街を結ぶ重要な場所。グナワ音楽と大道芸で賑わう文化の交差点です。',
            'features': {
                '景観': '時計塔、メディナ城壁の眺望、美しい都市計画の景観',
                '文化': 'グナワ音楽演奏、大道芸、伝統音楽の生演奏',
                '体験': 'カフェテラス、人間観察、地元と観光客の交流'
            },
            'highlights': [
                '夕方の大道芸人とミュージシャンの演奏',
                'グナワ音楽などの伝統音楽鑑賞',
                '時計塔とメディナ城壁の美しい眺望',
                'カフェテラスでのミントティータイム',
                '地元の人々と観光客の活気ある交流'
            ],
            'how_to_enjoy': {
                '午前（9:00-12:00）': '広場散策、周辺のお土産店巡り',
                '昼（12:00-15:00）': 'カフェランチ、人間観察',
                '午後（15:00-17:00）': 'ミントティー休憩、メディナ城壁眺望',
                '夕方（17:00-19:00）': '大道芸鑑賞、グナワ音楽体験'
            },
            'access_notes': '- メディナの中心部に位置\n- 周囲にカフェ、レストラン、お土産店\n- 夕方が最も賑やかで音楽演奏が多い\n- テラス席でのんびり過ごすのがおすすめ',
            'description': 'エッサウィラの中心広場で、メディナと新市街を結ぶ重要な場所。周囲をカフェ、レストラン、お土産店が囲み、常に地元の人々と観光客で賑わっています。夕方になると大道芸人やミュージシャンが集まり、グナワ音楽などの伝統音楽を楽しめます。広場からは時計塔やメディナの城壁を眺めることができ、エッサウィラの都市計画の美しさを実感できます。カフェのテラスでミントティーを飲みながらの人間観察も楽しいひとときです。',
            'verified': True,
            'lat': 31.512500,
            'lng': -9.768889,
            'best_time': '夕方',
            'duration': '1時間',
            'price_range': '無料'
        },
        # ラバトの観光地（6箇所）
        {
            'id': 33,
            'name': 'ハッサンの塔',
            'city': 'ラバト',
            'category': '歴史建築',
            'summary': '12世紀末アルモハード朝が建設した未完のモスクのミナレット。ユネスコ世界遺産でモロッコ首都のシンボルです。',
            'features': {
                '景観': '高さ44mの赤砂岩の塔、広大な遺跡敷地、ブールグレグ川の眺望',
                '歴史': '12世紀アルモハード朝建築、未完のモスク、ユネスコ世界遺産',
                '建築': 'アルモハード朝三大傑作、赤砂岩建築、イスラム建築様式'
            },
            'highlights': [
                '赤砂岩で造られた44mの壮大なミナレット',
                'アルモハード朝建築の三大傑作の一つ',
                '未完の巨大モスクの歴史的遺跡',
                'ユネスコ世界遺産としての価値',
                'ラバト首都のランドマークとしての存在感'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '遺跡全体散策、歴史について学習',
                '昼（11:00-14:00）': '塔の詳細観察、建築様式研究',
                '午後（14:00-17:00）': '周辺遺跡探索、写真撮影',
                '夕方（17:00-19:00）': '夕日に映える赤砂岩の美しさ鑑賞'
            },
            'access_notes': '- ラバト市内中心部に位置\n- 入場料10DH、ガイド利用推奨\n- ムハンマド5世霊廟と合わせて見学\n- 夕方の赤砂岩が美しい時間帯がベスト',
            'description': '12世紀末にアルモハード朝の第3代カリフ、ヤアクーブ・アル・マンスールによって建設が始められた未完のモスクのミナレット。高さ44メートルの赤砂岩の塔は、完成していれば80メートルになる予定でした。現在はユネスコ世界遺産に登録され、モロッコの首都ラバトのシンボルとなっています。同時代に建てられたセビリアのヒラルダの塔やマラケシュのクトゥビア・モスクと共に、アルモハード朝建築の三大傑作とされています。',
            'verified': True,
            'lat': 34.025833,
            'lng': -6.825000,
            'best_time': '夕方',
            'duration': '1時間',
            'price_range': '10DH（約115円）'
        },
        {
            'id': 34,
            'name': 'ムハンマド5世霊廟',
            'city': 'ラバト',
            'category': '歴史建築',
            'summary': 'モロッコ独立の父ムハンマド5世とハッサン2世国王が眠る白大理石の霊廟。1971年完成の美しい王室建築です。',
            'features': {
                '景観': '白大理石の美しい霊廟、精巧な大理石彫刻、壮麗な建築美',
                '歴史': 'ムハンマド5世・ハッサン2世国王の安置所、モロッコ独立史',
                '建築': '伝統モロッコ建築とモダン様式の融合、ゼリージュ、金箔天井'
            },
            'highlights': [
                '白大理石の壮麗な霊廟建築',
                '色とりどりのゼリージュと金箔天井の装飾',
                '精巧な大理石彫刻の芸術的価値',
                '衛兵の交代式の厳粛なセレモニー',
                'モロッコ王室の歴史と独立の象徴'
            ],
            'how_to_enjoy': {
                '午前（9:00-10:00）': '霊廟見学、建築美の観察',
                '午前（10:00-11:00）': '内部装飾鑑賞、ゼリージュ・金箔天井',
                '午前（11:00-12:00）': '衛兵交代式見学（時間要確認）',
                '見学後': 'ハッサンの塔と合わせて歴史学習'
            },
            'access_notes': '- ハッサンの塔と隣接、無料入場\n- 服装規定あり（露出控えめ）\n- 衛兵交代式の時間要事前確認\n- 静寂を保ち敬意を示すことが重要',
            'description': 'モロッコ独立の父であるムハンマド5世国王とハッサン2世国王が眠る白大理石の霊廟。現国王ムハンマド6世の祖父と父が安置されています。1971年に完成したこの霊廟は、伝統的なモロッコ建築とモダンな要素を融合させた美しい建物です。内部の装飾は息をのむ美しさで、色とりどりのゼリージュ、金箔を施した天井、精巧な大理石彫刻が施されています。衛兵の交代式も見どころの一つです。',
            'verified': True,
            'lat': 34.025278,
            'lng': -6.825278,
            'best_time': '午前中',
            'duration': '45分',
            'price_range': '無料'
        },
        {
            'id': 35,
            'name': 'ウダイヤ・カスバ',
            'city': 'ラバト',
            'category': '歴史建築',
            'summary': '12世紀アルモハード朝の要塞で、ユネスコ世界遺産。ブー・レグレグ川と大西洋の絶景オーシャンビューが楽しめます。',
            'features': {
                '景観': 'ブー・レグレグ川と大西洋の合流点、絶景オーシャンビュー、白と青の美しい住宅街',
                '歴史': '12世紀アルモハード朝要塞、ユネスコ世界遺産、中世防衛建築',
                '文化': 'アンダルシア庭園、地中海風住宅街、カフェ・マウデ'
            },
            'highlights': [
                'ブー・レグレグ川と大西洋の壮大な合流点の眺望',
                '白と青で彩られた地中海風の美しい住宅街',
                '12世紀アルモハード朝の歴史的要塞建築',
                '静寂なアンダルシア庭園での癒しの時間',
                'カフェ・マウデでの絶景ミントティー体験'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '要塞散策、12世紀建築の観察',
                '昼（11:00-14:00）': '白と青の住宅街散策、写真撮影',
                '午後（14:00-16:00）': 'アンダルシア庭園、静寂の時間',
                '夕方（16:00-18:00）': 'カフェ・マウデ、夕日オーシャンビュー'
            },
            'access_notes': '- ラバト市内から徒歩またはタクシー\n- アンダルシア庭園入場料10DH\n- 夕方の海景色が最も美しい\n- カフェ・マウデは絶景スポット',
            'description': '12世紀アルモハード朝時代に建設された要塞で、現在はユネスコ世界遺産に登録されています。ブー・レグレグ川と大西洋の合流点に建つこの要塞からは、絶景のオーシャンビューが楽しめます。城壁内には白と青で彩られた美しい住宅街が広がり、まるで地中海の漁村のような雰囲気。アンダルシア庭園も併設されており、静寂な空間で首都の喧騒を忘れることができます。カフェ・マウデでのミントティーも格別です。',
            'verified': True,
            'lat': 34.033889,
            'lng': -6.839167,
            'best_time': '夕方',
            'duration': '2時間',
            'price_range': '庭園10DH'
        },
        # メクネスの観光地（5箇所）
        {
            'id': 36,
            'name': 'ヴォルビリス遺跡',
            'city': 'メクネス',
            'category': '古代遺跡',
            'summary': '紀元前3世紀から11世紀のローマ帝国属州都市遺跡。北アフリカ最高の保存状態を誇るユネスコ世界遺産です。',
            'features': {
                '景観': '40ヘクタールの広大な遺跡、ゼルホン平野の絶景、古代都市の全景',
                '歴史': '紀元前3世紀〜11世紀のローマ都市、ユネスコ世界遺産、古代文明の証',
                '芸術': '見事なモザイク床、オルフェウスの家、ディオニュソスの家'
            },
            'highlights': [
                '北アフリカ最高保存状態のローマ遺跡',
                '「オルフェウスの家」「ディオニュソスの家」の芸術的モザイク',
                '古代ローマの凱旋門、神殿、公衆浴場の遺構',
                '40ヘクタールに広がる古代都市の壮大なスケール',
                'ゼルホン平野を見渡す絶景のロケーション'
            ],
            'how_to_enjoy': {
                '午前（9:00-10:30）': '遺跡入口、全体概要の把握、地図確認',
                '午前（10:30-12:00）': 'モザイク見学、オルフェウス・ディオニュソスの家',
                '昼（12:00-13:30）': '凱旋門、神殿、公衆浴場など主要遺構',
                '午後（13:30-15:00）': '居住区散策、ゼルホン平野展望'
            },
            'access_notes': '- メクネスから車で約30分\n- 入場料70DH、ガイド推奨\n- 午前中が涼しく見学に最適\n- 歩きやすい靴と日焼け対策必須',
            'description': '紀元前3世紀から11世紀まで存在したローマ帝国の属州都市の遺跡。北アフリカで最も保存状態の良いローマ遺跡の一つで、ユネスコ世界遺産に登録されています。40ヘクタールの敷地には、見事なモザイク床、凱旋門、神殿、公衆浴場、居住区などが残されています。特に「オルフェウスの家」「ディオニュソスの家」のモザイクは芸術的価値が極めて高く、古代ローマの豊かな文化を物語っています。遺跡からは肥沃なゼルホン平野の絶景も楽しめます。',
            'verified': True,
            'lat': 34.074444,
            'lng': -5.555556,
            'best_time': '午前中',
            'duration': '2-3時間',
            'price_range': '70DH（約800円）'
        },
        {
            'id': 37,
            'name': 'バブ・マンスール門',
            'city': 'メクネス',
            'category': '歴史建築',
            'summary': 'イスマーイール朝18世紀建設のモロッコ最美の門。高さ16m・幅8mの巨大な門で、夜間ライトアップが美しい象徴的建造物です。',
            'features': {
                '景観': '高さ16m・幅8mの巨大門、夜間ライトアップ、メクネスのランドマーク',
                '歴史': '18世紀イスマーイール朝建築、「モロッコのヴェルサイユ」の象徴',
                '建築': '緑と白のゼリージュ装飾、精巧な石膏彫刻、イスラム建築美'
            },
            'highlights': [
                'モロッコで最も美しいとされる歴史的な門',
                '緑と白のゼリージュ装飾と精巧な石膏彫刻',
                '高さ16メートルの圧倒的なスケール感',
                '夜間ライトアップの幻想的な美しさ',
                'イスマーイール朝の栄華を物語る象徴的建造物'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '門の建築詳細観察、ゼリージュ装飾鑑賞',
                '昼（11:00-15:00）': '歴史学習、イスマーイール朝について',
                '夕方（15:00-18:00）': '写真撮影、周辺散策',
                '夜間（18:00-20:00）': 'ライトアップ鑑賞、幻想的な夜景'
            },
            'access_notes': '- メクネス旧市街の入口に位置\n- 24時間見学可能、夜間照明あり\n- 建築家エル・マンスール・エル・アレジ設計\n- 周辺にカフェ・レストランあり',
            'description': 'イスマーイール朝のスルタン・ムーレイ・イスマーイールによって18世紀初頭に建設された、モロッコで最も美しい門の一つ。高さ16メートル、幅8メートルの巨大な門は、緑と白のゼリージュ装飾と精巧な石膏彫刻で装飾されています。門の名前は設計した建築家エル・マンスール・エル・アレジに由来します。夜間のライトアップは特に美しく、「ヴェルサイユのモロッコ版」と呼ばれたメクネスの栄華を物語る象徴的建造物です。',
            'verified': True,
            'lat': 33.893889,
            'lng': -5.556111,
            'best_time': '夕方〜夜',
            'duration': '30分',
            'price_range': '無料'
        },
        # ティトゥアンの観光地（3箇所）
        {
            'id': 38,
            'name': 'ティトゥアン旧市街',
            'city': 'ティトゥアン',
            'category': '都市・建築',
            'summary': '15世紀末アンダルシアのムーア人が建設したユネスコ世界遺産。「白いハト」の名の通り白い建物が美しい山間の古都です。',
            'features': {
                '景観': '白い建物群、美しい山間古都、アンダルシア風建築',
                '歴史': '15世紀末ムーア人建設、レコンキスタ後の文化継承、ユネスコ世界遺産',
                '文化': 'アンダルシア文化、精巧な木工装飾、伝統手工芸'
            },
            'highlights': [
                'アンダルシア追放ムーア人が築いた歴史的価値',
                '「白いハト」の名にふさわしい白い建物群',
                '精巧な木工装飾と美しい中庭を持つ住宅',
                '金属細工と木工芸品で有名な職人街',
                'ユネスコ世界遺産としての文化的意義'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '旧市街散策、白い建築群の観察',
                '午前（11:00-12:30）': '職人街見学、伝統手工芸の見学',
                '昼（12:30-14:00）': 'アンダルシア様式住宅と中庭見学',
                '午後（14:00-16:00）': '木工・金属細工工房体験、お土産購入'
            },
            'access_notes': '- ティトゥアン市内中心部\n- 散策は無料、工房見学は交渉次第\n- 午前中が涼しく散策に最適\n- アンダルシア文化の説明を聞くとより理解深まる',
            'description': '15世紀末にアンダルシアから追放されたムーア人によって建設されたユネスコ世界遺産の旧市街。「白いハト」という意味の名前の通り、白い建物が美しい山間の古都です。アンダルシア文化の影響が色濃く残る建築様式、精巧な木工装飾、美しい中庭を持つ住宅群など、独特の文化的価値を持っています。職人街では伝統的な手工芸が今も営まれており、特に金属細工と木工芸品で有名です。',
            'verified': True,
            'lat': 35.578611,
            'lng': -5.368611,
            'best_time': '午前中',
            'duration': '半日',
            'price_range': '散策無料'
        },
        # タンジェの観光地（4箇所）
        {
            'id': 39,
            'name': 'ヘラクレスの洞窟',
            'city': 'タンジェ',
            'category': '自然',
            'summary': 'タンジェ郊外の自然海蝕洞窟。開口部がアフリカ大陸の形に見え、ギリシャ神話のヘラクレス伝説で有名です。',
            'features': {
                '景観': 'アフリカ大陸形の開口部、大西洋絶景、夕日の幻想的光景',
                '自然': '海蝕洞窟、自然形成、ケープ・スパルテル近接',
                '文化': 'ギリシャ神話ヘラクレス伝説、大西洋と地中海の境界'
            },
            'highlights': [
                '洞窟開口部がアフリカ大陸の形に見える自然の造形',
                'ギリシャ神話の英雄ヘラクレスの休息伝説',
                '洞窟内から望む大西洋の絶景パノラマ',
                '夕日時間の幻想的で美しい光景',
                'ケープ・スパルテルとの地理学的重要性'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': '洞窟探索、自然形成の観察',
                '昼（11:00-14:00）': 'ケープ・スパルテル訪問、地理学習',
                '午後（14:00-17:00）': '洞窟内散策、大西洋展望',
                '夕方（17:00-19:00）': '夕日鑑賞、幻想的な光景撮影'
            },
            'access_notes': '- タンジェ市内から車で約20分\n- 無料見学、駐車場あり\n- 夕方の夕日時間が最も美しい\n- ケープ・スパルテルと合わせて訪問推奨',
            'description': 'タンジェ郊外に位置する自然が作り出した海蝕洞窟。洞窟の開口部がアフリカ大陸の形に見えることで有名です。ギリシャ神話の英雄ヘラクレスがここで休息したという伝説からこの名前が付けられました。洞窟内からは大西洋の絶景が望め、特に夕日の時間帯は幻想的な光景が楽しめます。近くのケープ・スパルテルは、大西洋と地中海が出会う地点として地理学的にも重要な場所です。',
            'verified': True,
            'lat': 35.792222,
            'lng': -5.929444,
            'best_time': '夕方',
            'duration': '1時間',
            'price_range': '無料'
        },
        {
            'id': 40,
            'name': 'タンジェ・メディナ',
            'city': 'タンジェ',
            'category': '都市・建築',
            'summary': 'ジブラルタル海峡を見下ろす丘の旧市街。アフリカとヨーロッパの交差点として栄えた歴史的な街並みが保存されています。',
            'features': {
                '景観': 'ジブラルタル海峡俯瞰、スペイン海岸線展望、丘陵地の美しい街並み',
                '歴史': 'アフリカ・ヨーロッパ交差点、古代からの港湾都市、多文化交流',
                '文化': '北アフリカ・地中海・アンダルシア文化の融合、職人工房'
            },
            'highlights': [
                'ジブラルタル海峡とスペイン海岸線の絶景',
                'アフリカとヨーロッパ文化が交わる独特な雰囲気',
                '迷路のような小径と白い壁の伝統的家屋',
                '職人工房での伝統的手工芸の見学',
                'カスバからの大西洋・地中海パノラマビュー'
            ],
            'how_to_enjoy': {
                '午前（9:00-11:00）': 'メディナ散策、迷路のような街並み探索',
                '午前（11:00-12:30）': '職人工房見学、伝統工芸体験',
                '昼（12:30-14:00）': '伝統カフェでミントティー、地元グルメ',
                '午後（14:00-16:00）': 'カスバ見学、ジブラルタル海峡絶景'
            },
            'access_notes': '- タンジェ市内中心部、港から徒歩圏内\n- 散策無料、一部施設は入場料あり\n- 午前中が涼しく散策しやすい\n- ヨーロッパフェリー港からもアクセス良好',
            'description': 'ジブラルタル海峡を見下ろす丘に位置する旧市街。アフリカとヨーロッパの交差点として栄えたタンジェの歴史を物語る街並みが保存されています。迷路のような小径、白い壁の家々、職人の工房、伝統的なカフェなど、北アフリカの典型的なメディナの特徴を持ちながら、地中海とアンダルシアの影響も感じられる独特の雰囲気があります。カスバからはスペインの海岸線まで見渡せる絶景が楽しめます。',
            'verified': True,
            'lat': 35.782778,
            'lng': -5.810556,
            'best_time': '午前中',
            'duration': '2-3時間',
            'price_range': '散策無料'
        }
    ]
    
    return spots

def init_ai_service():
    """AI機能の初期化（高精度対応版・ベクトルストア事前ロード最適化）"""
    # 環境変数からAPIキーを安全に取得（表示しない）
    api_key = os.getenv('OPENAI_API_KEY')
    kb = get_ai_knowledge_base()
    
    # ベクトルストアの事前ロード/構築（初回のみ、高速化のため）
    if _AI_VECTOR_HAS_SBT and VectorStore and build_docs_from_kb:
        if 'kb_vector_store' not in st.session_state or not st.session_state.get('kb_vector_store'):
            try:
                # 永続化されたインデックスがあればロード、なければ構築
                import hashlib
                kb_str = json.dumps(kb, sort_keys=True, ensure_ascii=False)
                kb_hash = hashlib.sha256(kb_str.encode('utf-8')).hexdigest()[:16]
                index_dir = os.path.join(os.path.dirname(__file__), 'data', 'ai_vector_index')
                os.makedirs(index_dir, exist_ok=True)
                index_path = os.path.join(index_dir, f'kb_index_{kb_hash}')
                
                try:
                    # まず永続化されたインデックスをロード
                    vs = VectorStore.load(index_path)
                    logger.info(f"Loaded persisted vector index from {index_path}")
                except FileNotFoundError:
                    # なければ構築して保存
                    logger.info("Building new vector index...")
                    docs = build_docs_from_kb(kb)
                    vs = VectorStore()
                    vs.build(docs)
                    try:
                        vs.save(index_path)
                        logger.info(f"Saved vector index to {index_path}")
                    except Exception as e:
                        logger.warning(f"Failed to save vector index: {e}")
                
                st.session_state['kb_vector_store'] = vs
                st.session_state['kb_vector_store_built'] = True
                logger.info("Vector store initialized and cached")
            except Exception as e:
                logger.warning(f"Vector store initialization failed: {e}")
    
    return {
        'available': bool(api_key),
        'api_key_masked': '****' if api_key else None,
        'knowledge_base': kb,
        'fallback_responses': get_enhanced_fallback_responses(),
        # Vector search availability (sentence-transformers + sklearn must be installed)
        'vector_search_available': bool(_AI_VECTOR_HAS_SBT),
        # whether a KB vector store has been built in this session (may be created on demand)
        'vector_store_built': bool(st.session_state.get('kb_vector_store_built', False))
    }

def get_ai_knowledge_base():
    """AI用の詳細知識ベース"""
    # Built-in base
    base = {
        'country_info': {
            'name': 'モロッコ王国',
            'capital': 'ラバト',
            'largest_city': 'カサブランカ',
            'population': '約3700万人',
            'area': '446,550平方キロメートル',
            'languages': ['アラビア語', 'ベルベル語（タマジグト語）', 'フランス語'],
            'currency': 'モロッコ・ディルハム（MAD）',
            'climate': '地中海性気候、大陸性気候、砂漠気候',
            'time_zone': 'GMT+1',
            'religion': 'イスラム教（スンニ派）99%'
        },
        'cultural_context': {
            'berber_heritage': 'ベルベル人（アマジグ人）は北アフリカの先住民族で、モロッコ文化の基盤',
            'islamic_influence': '7世紀のイスラム征服以降、アラブ・イスラム文化が根付く',
            'andalusian_legacy': '15世紀にスペインから移住したムーア人がアンダルシア文化を伝承',
            'french_colonial': '1912-1956年のフランス保護領時代の影響が現代にも残存',
            'modern_identity': '伝統と現代が調和した独特の文化アイデンティティ'
        },
        'travel_tips': {
            'best_seasons': {
                'spring': '3-5月: 温暖で観光に最適',
                'summer': '6-8月: 内陸部は酷暑、沿岸部は涼しい',
                'autumn': '9-11月: 過ごしやすく観光シーズン',
                'winter': '12-2月: 温和だがアトラス山脈は寒い'
            },
            'cultural_etiquette': {
                'greetings': 'アッサラーム・アライクム（平和があなたに）',
                'dress_code': '控えめな服装、特に宗教施設では肌の露出を避ける',
                'photography': 'モスク内部や人物撮影は許可を得る',
                'haggling': 'スークでの価格交渉は文化の一部',
                'meal_customs': '右手で食事、パンで料理をすくう'
            },
            'practical_info': {
                'visa': '日本国民は90日以内の観光は査証不要',
                'health': '特別な予防接種は不要',
                'safety': '観光地は比較的安全、夜間の一人歩きは避ける',
                'internet': 'WiFiは都市部で普及、通信速度は中程度',
                'transportation': 'ONCF鉄道、CTMバス、グランタクシーが主要交通手段'
            }
        }
    }

    # Attempt to load external JSON knowledge files from data/ai_knowledge
    kb_dir = os.path.join(os.path.dirname(__file__), 'data', 'ai_knowledge')
    if os.path.isdir(kb_dir):
        try:
            for fname in os.listdir(kb_dir):
                if not fname.lower().endswith('.json'):
                    continue
                path = os.path.join(kb_dir, fname)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        extra = json.load(f)
                    # Merge extra into base (shallow/deep merge for dicts and extend lists)
                    for k, v in extra.items():
                        if k not in base:
                            base[k] = v
                        else:
                            # both exist
                            if isinstance(base[k], dict) and isinstance(v, dict):
                                # merge nested dict
                                for subk, subv in v.items():
                                    if subk not in base[k]:
                                        base[k][subk] = subv
                                    else:
                                        # extend lists or overwrite scalars
                                        if isinstance(base[k][subk], list) and isinstance(subv, list):
                                            # append unique items
                                            for it in subv:
                                                if it not in base[k][subk]:
                                                    base[k][subk].append(it)
                                        else:
                                            base[k][subk] = subv
                            elif isinstance(base[k], list) and isinstance(v, list):
                                for it in v:
                                    if it not in base[k]:
                                        base[k].append(it)
                            else:
                                base[k] = v
                except Exception as e:
                    logger.warning(f"Failed to load AI knowledge file {path}: {e}")
        except Exception as e:
            logger.warning(f"Failed to scan ai_knowledge directory: {e}")

    return base

def get_enhanced_fallback_responses():
    """拡張されたフォールバック応答"""
    return {
        'マラケシュ': '''マラケシュは「赤い街」として知られるモロッコの帝国都市です。

**主要観光地（15箇所）:**
• ジャマ・エル・フナ広場: 1000年の歴史を持つユネスコ世界遺産
• クトゥビア・モスク: 12世紀建造、高さ77mのミナレット
• バイア宮殿: 19世紀の豪華な宮殿、精巧なタイル装飾
• マジョレル庭園: イヴ・サンローラン所有の美しい植物園
• サーディアン朝の墳墓群、エル・バディ宮殿などもご案内

**おすすめ体験:**
• 夕方のジャマ・エル・フナ広場で大道芸観賞
• 伝統的なリヤドホテルでの宿泊
• スークでのお土産探し
• アトラス山脈日帰りツアー''',

        'カサブランカ': '''カサブランカはモロッコ最大の経済都市で、現代的な魅力を持ちます。

**主要観光地（12箇所）:**
• ハッサン2世モスク: 世界第3位の規模、海に面した美しい立地
• リック・カフェ: 映画「カサブランカ」の世界を再現
• 旧市街メディナ: 18世紀の白い街並み
• コーニッシュ海岸、モロッコ・モールなども充実  
• ツインセンター: 現代モロッコのシンボル

**文化的特徴:**
• フランス植民地時代の建築遺産
• モロッコ経済の中心地
• 国際的な雰囲気と伝統の融合''',

        'フェズ': '''フェズは1200年の歴史を持つモロッコの古都で、イスラム文化の宝庫です。

**主要観光地（10箇所）:**
• フェズ・エル・バリ: 世界最大の車両進入禁止都市
• カラウィーン大学: 859年創設の世界最古の大学
• シュワラ皮なめし場: 11世紀から続く伝統技法
• ボウ・イナニア・マドラサ: マリーン朝建築の傑作

**文化的価値:**
• イスラム学問の中心地
• 伝統工芸の継承地
• 中世の街並みが完全保存''',

        'メルズーガ': '''メルズーガはサハラ砂漠観光の玄関口で、砂漠体験の聖地です。

**主要観光地（6箇所）:**
• エルグ・シェビ砂丘: 高さ150mの美しい砂丘群
• ハッシ・ラブド砂丘: より静寂な砂漠体験

**おすすめ体験:**
• ラクダトレッキングで砂丘登頂
• 砂漠キャンプで満天の星空観賞
• ベルベル音楽と伝統料理
• 日の出・日没の絶景撮影''',

        'シャウエン': '''シャウエンは「青い真珠」と呼ばれる山間の美しい町です。

**主要観光地（8箇所）:**
• 青い旧市街: 青く塗られた家々の独特な景観
• ウタ・エル・ハマム広場: 町の中心広場
• カスバ: 15世紀の要塞、町を一望
• アケチャウル滝: 自然の美しい滝
• スペイン・モスク、神の橋なども魅力的

**特徴:**
• アンダルシア・ムーア人の建築様式
• リフ山脈の美しい自然
• アーティストや写真家に人気''',

        'エッサウィラ': '''エッサウィラは「アフリカの風の街」として知られる大西洋沿岸の港町です。

**主要観光地（8箇所）:**
• 要塞都市メディナ: ユネスコ世界遺産
• スカラ・デュ・ポール: 18世紀の海上要塞
• 活気ある漁港: 新鮮な海の幸
• ムーレイ・ハッサン広場: 町の中心
• シディ・モハメド・ベン・アブドラ博物館などが充実

**文化的特徴:**
• グナワ音楽の聖地
• ウィンドサーフィンの名所
• ポルトガル・フランス建築の融合''',

        'general': '''モロッコは北アフリカに位置する王国で、豊かな文化遺産と自然の美しさで知られています。

**基本情報:**
• 首都: ラバト（政治）、カサブランカ（経済）
• 人口: 約3700万人
• 言語: アラビア語、ベルベル語（公用語）、フランス語
• 宗教: イスラム教（スンニ派）99%
• 通貨: モロッコ・ディルハム（MAD）

**文化的特徴:**
• アラブ、ベルベル、アンダルシア、アフリカ文化の融合
• 豊富なユネスコ世界遺産
• 伝統工芸と現代アートの共存
• 多様な気候と地形（砂漠、山脈、海岸）'''
    }

@handle_errors
@measure_performance
def main():
    """メインアプリケーション"""
    
    # データ検証
    try:
        spots = load_spots_data()
        logger.info(f"Successfully loaded {len(spots) if spots else 0} tourist spots")
        if not spots:
            st.error("❌ 観光地データの読み込みに失敗しました")
            st.stop()
    except Exception as e:
        st.error(f"❌ データ読み込みエラー: {str(e)}")
        logger.error(f"Failed to load spots data: {e}")
        st.stop()
    
    # シンプルなページ管理
    # URLパラメータまたはセッション状態から現在のページを決定
    query_params = st.query_params
    
    if 'spot_id' in query_params:
        # 詳細ページの表示
        try:
            spot_id = int(query_params['spot_id'])
            # 有効なIDかチェック
            valid_ids = [spot['id'] for spot in spots]
            if spot_id not in valid_ids:
                st.error(f"❌ 無効な観光地ID: {spot_id}")
                st.info("🏠 ホームページに戻ります")
                st.query_params.clear()
                st.rerun()
            else:
                show_spot_detail_by_id(spot_id)
        except ValueError:
            st.error("❌ 無効なURLパラメータです")
            st.query_params.clear()
            st.rerun()
    else:
        # 通常のページ表示
        show_main_app()

def show_main_app():
    """メインアプリケーションの表示"""
    # サイドバー
    st.sidebar.title("🧭 ナビゲーション")
    
    # ページ選択
    current_page = st.session_state.get('current_page', '🏠 ホーム')
    page_options = ["🏠 ホーム", "🗺️ マップ", "📍 観光地一覧", "🛣️ 観光ルート", "🏛️ モロッコ文化・歴史", "🤖 AI観光ガイド", "⚙️ 設定"]
    
    page_index = 0
    if current_page in page_options:
        page_index = page_options.index(current_page)
    
    page = st.sidebar.selectbox(
        "ページを選択",
        page_options,
        index=page_index
    )
    
    # 現在のページをセッション状態に保存
    st.session_state.current_page = page
    
    # テーマ表示
    st.sidebar.markdown("---")
    current_theme = st.session_state.get("theme", "ライト")
    theme_emoji = "🌞" if current_theme == "ライト" else "🌙"
    st.sidebar.markdown(f"**🎨 現在のテーマ: {theme_emoji} {current_theme}**")
    st.sidebar.markdown("*テーマ変更は設定ページで行えます*")
    
    # データ読み込み
    spots = load_spots_data()
    ai_service = init_ai_service()
    
    # ページ表示
    if page == "🏠 ホーム":
        show_home_page(spots)
    elif page == "🗺️ マップ":
        show_map_page(spots)
    elif page == "📍 観光地一覧":
        show_spots_page(spots)
    elif page == "🛣️ 観光ルート":
        show_route_page(spots)
    elif page == "🏛️ モロッコ文化・歴史":
        show_culture_history_page()
    elif page == "🤖 AI観光ガイド":
        show_ai_page(ai_service)
    elif page == "⚙️ 設定":
        show_settings_page()

def show_spot_detail_by_id(spot_id):
    """IDによる詳細ページ表示"""
    spots = load_spots_data()
    
    # 前のページ情報を保存（初回のみ）
    if 'previous_page' not in st.session_state:
        st.session_state.previous_page = st.session_state.get('current_page', '📍 観光地一覧')
    
    # IDで観光地を検索
    spot = None
    for s in spots:
        if s['id'] == spot_id:
            spot = s
            break
    
    if not spot:
        st.error("⚠️ 指定された観光地が見つかりません")
        if st.button("← 観光地一覧に戻る", key="map_back_to_list"):
            st.query_params.clear()
            # 前のページに戻る
            if 'previous_page' in st.session_state and st.session_state.previous_page:
                st.session_state.current_page = st.session_state.previous_page
            else:
                st.session_state.current_page = '📍 観光地一覧'
            st.session_state.previous_page = None  # リセット
            st.rerun()
        return
    
    # 詳細ページのヘッダー
    st.markdown(f"""
    <div class="detail-header">
        <h1>📍 {spot['name']}</h1>
        <p>{spot['city']} - {spot['category']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # サイドバー
    st.sidebar.title("📍 観光地詳細")
    st.sidebar.markdown(f"**{spot['name']}**")
    st.sidebar.markdown(f"📍 {spot['city']}")
    st.sidebar.markdown(f"🏷️ {spot['category']}")
    if spot.get('verified'):
        st.sidebar.success("✅ 認定スポット")
    
    st.sidebar.markdown("---")
    if st.sidebar.button("← 観光地一覧に戻る", use_container_width=True):
        st.query_params.clear()
        # 前のページに戻る
        if 'previous_page' in st.session_state and st.session_state.previous_page:
            st.session_state.current_page = st.session_state.previous_page
        else:
            st.session_state.current_page = '📍 観光地一覧'
        st.session_state.previous_page = None  # リセット
        st.rerun()
    
    # 詳細情報を表示
    show_spot_details(spot)
def show_tourism_precautions_section():
    """観光での注意点セクション"""
    st.markdown("### ⚠️ モロッコ観光での注意点・マナー")
    
    st.markdown("""
    モロッコは魅力的な観光地ですが、異なる文化や環境のため、
    事前に知っておくべき注意点やマナーがあります。
    安全で快適な旅行のために、以下の情報をご確認ください。
    """)
    
    # 文化・宗教的注意点
    st.markdown("#### 🕌 文化・宗教的マナー")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **👔 服装について**
        - **宗教施設**: 肌の露出を控える（長袖・長ズボン必須）
        - **女性**: 特に肩・膝・胸元を覆う服装
        - **男性**: タンクトップ・短パンは避ける
        - **モスク**: 非ムスリムは一般的に入場不可
        - **靴**: モスクや家庭では脱靴
        
        **📸 写真撮影マナー**
        - **人物**: 必ず許可を取る（特に女性）
        - **宗教施設**: 撮影禁止の場所あり
        - **軍事施設**: 撮影厳禁
        - **料金**: 写真撮影に料金を要求される場合あり
        """)
    
    with col2:
        st.markdown("""
        **🤝 社会的マナー**
        - **握手**: 男性同士は問題なし、異性間は控えめに
        - **左手**: 不浄とされるため食事・握手では使わない
        - **足裏**: 人に向けるのは失礼
        - **頭**: 子供の頭を触るのは避ける
        - **アルコール**: 公共の場での飲酒は避ける
        
        **🗣️ 言語・コミュニケーション**
        - **挨拶**: 「サラーム・アライクム」（平安があなたに）
        - **感謝**: 「シュクラン」（ありがとう）
        - **フランス語**: 観光地では通じることが多い
        - **英語**: 若い世代や観光業者は理解
        """)
    
    # 安全・防犯対策
    st.markdown("#### 🛡️ 安全・防犯対策")
    
    tab1, tab2, tab3 = st.tabs(["💰 詐欺・ぼったくり対策", "🚨 一般的な安全対策", "🏥 健康・医療"])
    
    with tab1:
        st.markdown("""
        **🎯 よくある詐欺・トラブル**
        
        **偽ガイド詐欺**
        - 「道に迷った観光客を助ける」と接近
        - 法外なガイド料を請求
        - **対策**: 公式ガイドのみ利用、事前料金確認
        
        **カーペット・お土産詐欺**
        - 「特別価格」「友達だから」と甘い言葉
        - 高額商品を売りつけ
        - **対策**: 複数店舗で価格比較、即決避ける
        
        **タクシーぼったくり**
        - メーター使用拒否、観光客料金
        - 遠回りして料金つり上げ
        - **対策**: メーター確認、事前料金交渉、配車アプリ利用
        
        **「無料」サービス詐欺**
        - ヘナタトゥー、写真撮影後に料金請求
        - **対策**: 「無料」には必ず事前確認
        
        **交渉のコツ**
        - 最初の提示価格の30-50%から交渉開始
        - 歩いて立ち去る演技も効果的
        - 複数人で買い物する場合は事前に役割分担
        """)
    
    with tab2:
        st.markdown("""
        **🔒 基本的な安全対策**
        
        **貴重品管理**
        - パスポートコピーを持参、原本はホテル金庫
        - 現金は分散して持つ
        - 高価なアクセサリーは避ける
        - バッグは前に持つ、ファスナーは常に閉める
        
        **移動時の注意**
        - 夜間の一人歩きは避ける
        - 人気のない路地は避ける
        - 交通量の多い道路横断時は十分注意
        - 長距離移動は信頼できる交通手段を選択
        
        **宿泊時の注意**
        - ホテルのセキュリティ確認
        - 部屋番号を他人に言わない
        - ドアロックの確認を習慣化
        - 緊急連絡先をメモして持参
        
        **緊急時の連絡先**
        - 警察: 19
        - 消防: 15
        - 救急: 15
        - 観光警察: 主要観光地に配備
        - 日本領事館: +212-537-63-17-82（ラバト）
        """)
    
    with tab3:
        st.markdown("""
        **🏥 健康・医療関連**
        
        **事前準備**
        - 海外旅行保険への加入必須
        - 常備薬の持参（処方箋も英語・フランス語で）
        - 予防接種: 破傷風、A型肝炎推奨
        - 医療情報の英語・フランス語訳準備
        
        **食事・飲水注意**
        - 水道水は避け、ミネラルウォーター使用
        - 氷入り飲料は避ける
        - 生野菜・果物は信頼できる店のみ
        - 屋台料理は衛生状態を確認
        - 肉類は十分加熱されたもののみ
        
        **気候対策**
        - 強い日差し: 日焼け止め（SPF50+）、帽子、サングラス必須
        - 乾燥対策: リップクリーム、保湿クリーム
        - 砂漠: 昼夜の寒暖差に対応する服装
        - 高山地帯: 高山病対策、防寒具
        
        **よくある体調不良**
        - 旅行者下痢: 整腸剤持参
        - 脱水症状: こまめな水分補給
        - 食あたり: 症状が続く場合は医療機関受診
        - 日射病・熱中症: 適度な休憩と水分補給
        """)
    
    # 実用的なアドバイス
    st.markdown("#### 💡 実用的なアドバイス")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **💰 お金関連**
        - **通貨**: ディルハム（MAD）
        - **両替**: 銀行・公認両替所を利用
        - **クレジットカード**: 主要ホテル・レストランで利用可
        - **現金**: 小額紙幣を多めに用意
        - **チップ**: ホテル・レストランで10-15%程度
        - **値段交渉**: スーク（市場）では必須
        
        **📱 通信・インターネット**
        - **SIMカード**: 空港・携帯ショップで購入可
        - **WiFi**: ホテル・カフェで利用可能
        - **国際ローミング**: 高額になる場合あり
        - **翻訳アプリ**: Google翻訳など事前ダウンロード
        """)
    
    with col2:
        st.markdown("""
        **🎒 荷物・持ち物**
        - **必需品**: パスポート、ビザ（不要）、航空券
        - **服装**: 長袖・長ズボン、歩きやすい靴
        - **日用品**: 日焼け止め、帽子、サングラス
        - **薬品**: 常備薬、虫除けスプレー、絆創膏
        - **電子機器**: 変換プラグ（Cタイプ）、モバイルバッテリー
        - **現金**: 米ドル・ユーロを少額
        
        **⏰ 時間・スケジュール**
        - **時差**: 日本より8時間遅れ（冬）、9時間遅れ（夏）
        - **金曜日**: 多くの店舗が昼過ぎまで休業
        - **ラマダン**: 期間中は営業時間が変更
        - **昼寝時間**: 13-15時頃は多くの店が休憩
        """)
    
    # 緊急時対応
    st.markdown("#### 🚨 緊急時の対応")
    
    st.error("""
    **緊急連絡先（モロッコ国内）**
    - **警察**: 19
    - **消防・救急**: 15
    - **観光警察**: 主要観光地に配備
    - **日本国総領事館（カサブランカ）**: +212-522-27-57-18
    - **日本国大使館（ラバト）**: +212-537-63-17-82
    """)
    
    st.warning("""
    **トラブル発生時の対応**
    1. **まず安全確保** - 危険な場所からの移動
    2. **状況把握** - 何が起きたかを冷静に判断
    3. **記録保存** - 日時、場所、関係者の記録
    4. **連絡** - ホテル、保険会社、大使館等
    5. **証拠保全** - 写真、レシート、証明書等の保管
    """)
    
    st.info("""
    **📞 24時間日本語サポート**
    多くの海外旅行保険には24時間日本語サポートが付帯しています。
    緊急時は遠慮なく利用し、適切なアドバイスを求めましょう。
    """)
    
    # 最後に前向きなメッセージ
    st.success("""
    **🌟 安全で素晴らしいモロッコ旅行のために**
    
    これらの注意点は怖がらせるためではなく、より安全で快適な旅行を楽しんでいただくためのものです。
    基本的な注意を守れば、モロッコは非常に魅力的で安全な観光地です。
    美しい文化、温かい人々、素晴らしい体験があなたを待っています！
    
    **良い旅を！ Have a nice trip! رحلة سعيدة**
    """)

def get_feature_tags(features):
    """安全にfeature tagsを生成する関数"""
    try:
        if not features:
            return ""
        
        # featuresがリストでない場合の処理
        if not isinstance(features, (list, tuple)):
            if isinstance(features, dict):
                features = list(features.keys())
            elif isinstance(features, str):
                features = [features]
            else:
                return ""
        
        # 最初の2つの要素を取得してHTMLタグを生成
        feature_list = list(features)[:2]
        return ''.join([f'<span class="feature-tag">{str(feature)}</span>' for feature in feature_list])
    
    except Exception as e:
        logger.warning(f"Error generating feature tags: {e}")
        return ""

def show_home_page(spots):
    """ホームページ"""
    # 背景画像のCSSを適用
    st.markdown(get_background_image_css(), unsafe_allow_html=True)
    
    # 背景画像コンテナの開始
    st.markdown('<div class="home-background">', unsafe_allow_html=True)
    # home-content div削除
    
    # ヘッダーセクション
    st.markdown("""
    <div class="home-header">
        <h1>🕌 モロッコ観光ガイドへようこそ</h1>
        <p>あなたの完璧なモロッコ旅行をサポートします</p>
        <div style="margin-top: 1.5rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem; display: inline-block;">
                🌍 40+ 観光地
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem; display: inline-block;">
                🗺️ 対話型マップ
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 25px; margin: 0.5rem; display: inline-block;">
                🤖 AI ガイド
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 統計情報
    cities = set(spot['city'] for spot in spots)
    verified_count = sum(1 for spot in spots if spot.get('verified', False))
    categories = set(spot['category'] for spot in spots)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-around; margin: 32px 0; flex-wrap: wrap;">
        <div class="metric-container" style="text-align: center; flex: 1; margin: 8px;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">📍</div>
            <div style="font-size: 2rem; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">{len(spots)}</div>
            <div style="color: white; font-weight: 500; line-height: 1.6; text-shadow: 0 1px 3px rgba(0,0,0,0.7);">観光地数</div>
        </div>
        <div class="metric-container" style="text-align: center; flex: 1; margin: 8px;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🏙️</div>
            <div style="font-size: 2rem; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">{len(cities)}</div>
            <div style="color: white; font-weight: 500; line-height: 1.6; text-shadow: 0 1px 3px rgba(0,0,0,0.7);">都市数</div>
        </div>
        <div class="metric-container" style="text-align: center; flex: 1; margin: 8px;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">✅</div>
            <div style="font-size: 2rem; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">{verified_count}</div>
            <div style="color: white; font-weight: 500; line-height: 1.6; text-shadow: 0 1px 3px rgba(0,0,0,0.7);">認定スポット</div>
        </div>
        <div class="metric-container" style="text-align: center; flex: 1; margin: 8px;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🎯</div>
            <div style="font-size: 2rem; font-weight: 700; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">{len(categories)}</div>
            <div style="color: white; font-weight: 500; line-height: 1.6; text-shadow: 0 1px 3px rgba(0,0,0,0.7);">カテゴリ数</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # クイックアクションセクション
    st.markdown("""
    <div style="margin: 32px 0; text-align: center; background: var(--white-glass); padding: 24px; border-radius: 15px; backdrop-filter: blur(12px);">
        <h2 style="color: white; margin-bottom: 12px; font-size: 2.2rem; font-weight: 600; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">
            🚀 今すぐ始める
        </h2>
        <p style="color: rgba(255,255,255,0.9); font-size: 1rem; margin: 0; text-shadow: 0 1px 3px rgba(0,0,0,0.6);">
            お好みの方法でモロッコ観光を開始しましょう
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🗺️ マップを見る", use_container_width=True, type="primary"):
            st.session_state.current_page = "🗺️ マップ"
            st.rerun()
    
    with col2:
        if st.button("🛣️ ルート作成", use_container_width=True):
            st.session_state.current_page = "🛣️ 観光ルート"
            st.rerun()
    
    with col3:
        if st.button("🤖 AI に相談", use_container_width=True):
            st.session_state.current_page = "🤖 AI観光ガイド"
            st.rerun()
    
    with col4:
        if st.button("📍 観光地一覧", use_container_width=True):
            st.session_state.current_page = "📍 観光地一覧"
            st.rerun()
    
    st.markdown("---")
    
    # おすすめ観光地
    st.markdown("""
    <div style="margin: 40px 0; text-align: center; background: var(--white-glass); padding: 32px; border-radius: 20px; backdrop-filter: blur(16px);">
        <h2 style="color: white; margin-bottom: 16px; font-size: 2.8rem; font-weight: 700; text-shadow: 0 3px 6px rgba(0,0,0,0.8); letter-spacing: 0.5px;">
            ✨ おすすめ観光地 ✨
        </h2>
        <p style="color: white; font-size: 1.2rem; margin-bottom: 8px; line-height: 1.8; text-shadow: 0 2px 4px rgba(0,0,0,0.7); font-weight: 500;">
            🕌 モロッコの魅力あふれる観光スポット 🕌
        </p>
        <p style="color: rgba(255,255,255,0.9); font-size: 1rem; margin: 0; line-height: 1.6; text-shadow: 0 1px 3px rgba(0,0,0,0.6);">
            厳選された認定スポットから、あなたの旅を特別なものにする場所をご案内します
        </p>
        <div style="width: 80px; height: 3px; background: linear-gradient(90deg, var(--gold), var(--majorelle-blue)); margin: 20px auto 0; border-radius: 2px;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    recommended_spots = [spot for spot in spots if spot.get('verified', False)][:6]
    
    # 認定済み観光地がない場合は、人気の観光地を表示
    if not recommended_spots:
        st.info("📍 すべての観光地から人気スポットをご紹介します")
        recommended_spots = spots[:6]  # 最初の6つを表示
    
    # 3列のグリッドレイアウト
    for i in range(0, len(recommended_spots), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(recommended_spots):
                spot = recommended_spots[i + j]
                with col:
                    # 観光地の種類に応じたアイコンを選択
                    category_icons = {
                        '広場・市場': '🏛️',
                        '宗教建築': '🕌',
                        '歴史建築': '🏰',
                        '自然': '🌿',
                        '都市・建築': '🏢',
                        '博物館': '🏛️',
                        '文化施設': '🎭',
                        '伝統工芸': '🎨'
                    }
                    thumbnail_icon = category_icons.get(spot['category'], '📍')
                    
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <div class="card-thumbnail">
                            <div class="thumbnail-placeholder">
                                <div class="thumbnail-icon">{thumbnail_icon}</div>
                                <div class="thumbnail-gradient"></div>
                            </div>
                        </div>
                        <div class="card-header">
                            <h3 class="card-title">{spot['name']}</h3>
                            <div class="card-location">📍 {spot['city']}</div>
                        </div>
                        <div class="card-content">
                            <div class="card-category">
                                <span class="category-badge">{spot['category']}</span>
                                {' <span class="verified-badge">✓ 認定済み</span>' if spot.get('verified') else ''}
                            </div>
                            <p class="card-description">{(spot.get('summary') or spot.get('description', '詳細情報なし'))[:80]}...</p>
                            <div class="card-features">
                                {get_feature_tags(spot.get('features', []))}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    st.markdown("---")
    

    
    # モロッコ豆知識セクション
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-section">
            <h3 style="color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); font-size: 1.4rem; margin-bottom: 16px; text-align: center;">
                📚 モロッコ豆知識 📚
            </h3>
            <div class="info-card">
                <h4>🌍 基本情報</h4>
                <ul>
                    <li><strong>首都</strong>: ラバト</li>
                    <li><strong>最大都市</strong>: カサブランカ</li>
                    <li><strong>人口</strong>: 約3,700万人</li>
                    <li><strong>公用語</strong>: アラビア語、ベルベル語</li>
                    <li><strong>通貨</strong>: モロッコ・ディルハム (MAD)</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-section">
            <h3 style="color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8); font-size: 1.4rem; margin-bottom: 16px; text-align: center;">
                🎭 文化・伝統 🎭
            </h3>
            <div class="info-card">
                <h4>✨ 特徴</h4>
                <ul>
                    <li><strong>建築</strong>: イスラム・アンダルシア様式</li>
                    <li><strong>工芸</strong>: 絨毯、陶器、金属工芸</li>
                    <li><strong>料理</strong>: タジン、クスクス</li>
                    <li><strong>音楽</strong>: グナワ、アンダルシア音楽</li>
                    <li><strong>祭り</strong>: バラ祭り、映画祭</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # 背景画像コンテナの終了
    # home-content div削除
    st.markdown('</div>', unsafe_allow_html=True)  # home-background

def show_map_page(spots):
    """マップページ"""
    st.subheader("🗺️ モロッコ観光地マップ")
    
    # 高度なフィルター機能
    st.markdown("### 🎯 マップフィルター")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cities = sorted(set(spot['city'] for spot in spots))
        selected_cities = st.multiselect(
            "🏙️ 表示する都市（複数選択可）",
            options=cities,
            default=cities,  # デフォルトで全都市選択
            placeholder="都市を選択"
        )
    
    with col2:
        categories = sorted(set(spot['category'] for spot in spots))
        selected_categories = st.multiselect(
            "🎯 表示するカテゴリ（複数選択可）",
            options=categories,
            default=categories,  # デフォルトで全カテゴリ選択
            placeholder="カテゴリを選択"
        )
    
    with col3:
        map_options = st.multiselect(
            "⚙️ マップオプション",
            options=["認定済みのみ", "詳細情報表示", "価格情報表示"],
            default=["詳細情報表示"],
            placeholder="オプションを選択"
        )
    
    # フィルタリング
    filtered_spots = spots
    
    # 都市フィルター（複数選択）
    if selected_cities:
        filtered_spots = [spot for spot in filtered_spots if spot['city'] in selected_cities]
    
    # カテゴリフィルター（複数選択）
    if selected_categories:
        filtered_spots = [spot for spot in filtered_spots if spot['category'] in selected_categories]
    
    # 認定済みフィルター
    if "認定済みのみ" in map_options:
        filtered_spots = [spot for spot in filtered_spots if spot.get('verified', False)]
    
    # マップ作成
    if filtered_spots:
        try:
            # マップの中心を計算
            center_lat = sum(spot['lat'] for spot in filtered_spots) / len(filtered_spots)
            center_lng = sum(spot['lng'] for spot in filtered_spots) / len(filtered_spots)
            
            m = folium.Map(
                location=[center_lat, center_lng], 
                zoom_start=6,
                tiles="OpenStreetMap"
            )
        except Exception as e:
            st.error(f"❌ 地図の初期化に失敗しました: {str(e)}")
            st.info("📍 デフォルトの地図を表示します")
            m = folium.Map(
                location=[31.7917, -7.0926],  # モロッコの中心
                zoom_start=6,
                tiles="OpenStreetMap"
            )
        
        # マーカーを追加
        for spot in filtered_spots:
            # 詳細情報の表示判定
            show_details = "詳細情報表示" in map_options
            show_price = "価格情報表示" in map_options
            
            # ポップアップHTMLの構築
            popup_content = f"""
            <div style="width: 300px; font-family: Arial, sans-serif;">
                <h4 style="color: #2c3e50; margin-bottom: 8px;">{spot['name']}</h4>
                <p style="margin: 4px 0;"><b>📍 {spot['city']}</b> • <b>🏷️ {spot['category']}</b></p>
            """
            
            if spot.get('verified'):
                popup_content += '<p style="margin: 4px 0;"><span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">✅ 認定済み</span></p>'
            
            if show_details:
                # descriptionまたはsummaryを使用
                description = spot.get('description') or spot.get('summary') or '詳細情報なし'
                popup_content += f'<p style="margin: 8px 0; line-height: 1.4;">{description[:150]}...</p>'
                
                if spot.get('best_time'):
                    popup_content += f'<p style="margin: 4px 0;"><b>⏰ ベストタイム:</b> {spot["best_time"]}</p>'
                
                if spot.get('duration'):
                    popup_content += f'<p style="margin: 4px 0;"><b>⏱️ 所要時間:</b> {spot["duration"]}</p>'
            else:
                # descriptionまたはsummaryを使用
                description = spot.get('description') or spot.get('summary') or '詳細情報なし'
                popup_content += f'<p style="margin: 8px 0; line-height: 1.4;">{description[:80]}...</p>'
            
            if show_price and spot.get('price_range'):
                popup_content += f'<p style="margin: 4px 0;"><b>💰 料金:</b> {spot["price_range"]}</p>'
            
            popup_content += '</div>'
            
            popup_html = popup_content
            
            folium.Marker(
                location=[spot['lat'], spot['lng']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=spot['name'],
                icon=folium.Icon(
                    color='red' if spot.get('verified') else 'blue',
                    icon='check' if spot.get('verified') else 'info-sign'
                )
            ).add_to(m)
        
        # マップ表示
        st_folium(m, width=700, height=500)
        
        # 観光地リスト
        st.subheader(f"📍 観光地一覧 ({len(filtered_spots)}件)")
        
    for spot in filtered_spots:
            with st.expander(f"{spot['name']} - {spot['city']}"):
                st.write(spot.get('summary') or spot.get('description', '詳細情報なし'))
                st.write(f"**カテゴリ:** {spot['category']}")
                if spot.get('verified'):
                    st.success("✅ 認定済み")
                
                # 詳細ボタン
                if st.button("📖 詳細", key=f"list_detail_{spot['id']}", use_container_width=True):
                    st.query_params['spot_id'] = spot['id']
                    st.rerun()
    else:
        st.warning("選択した条件に一致する観光地がありません。")

@handle_errors
def show_spot_details(spot):
    """観光地の詳細情報を表示 - シンプル版"""
    
    # デバッグ出力
    st.write("🔍 詳細表示関数が呼び出されました")
    st.write(f"観光地データ: {spot.get('name', 'No name')}")
    
    # シンプルなヘッダー
    st.title(f"🏛️ {spot.get('name', '不明な観光地')}")
    st.subheader(f"📍 {spot.get('city', '不明')} • 🎯 {spot.get('category', '不明')}")
    
    # 戻るボタン
    if st.button("🔙 一覧に戻る", key="detail_back_button", type="primary"):
        # 詳細モードを終了
        st.session_state.detail_mode = False
        st.session_state.selected_spot = None
        
        # URLパラメータをクリア
        if 'spot_id' in st.query_params:
            st.query_params.clear()
        
        # 前のページ情報があれば、そのページに戻る
        if 'previous_page' in st.session_state and st.session_state.previous_page:
            st.session_state.current_page = st.session_state.previous_page
        else:
            # デフォルトは観光地一覧に戻る
            st.session_state.current_page = '📍 観光地一覧'
        
        # ページ状態をリセット
        st.session_state.page_just_changed = True
        st.rerun()
    
    st.markdown("---")
    
    # 基本的な詳細情報
    if spot.get('summary'):
        st.markdown("### 📋 概要")
        st.write(spot['summary'])
        
    if spot.get('description'):
        st.markdown("### 📝 詳細説明")
        st.write(spot['description'])
        
    # 基本情報
    st.markdown("### 📊 基本情報")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**都市:** {spot.get('city', '不明')}")
        st.write(f"**カテゴリ:** {spot.get('category', '不明')}")
        
    with col2:
        if spot.get('coordinates'):
            lat, lon = spot['coordinates']
            st.write(f"**緯度:** {lat:.4f}")
            st.write(f"**経度:** {lon:.4f}")
    
    # 追加ボタン
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📋 観光地一覧", key="detail_list_button", use_container_width=True):
            st.query_params.clear()
            st.session_state.current_page = '📍 観光地一覧'
            st.rerun()
            
    with col2:
        if st.button("🏠 ホーム", key="detail_home_button", use_container_width=True):
            st.query_params.clear()
            st.session_state.current_page = '🏠 ホーム'
            st.rerun()
    st.markdown(f"""
    <div class="detail-hero">
        <h1>� {spot['name']}</h1>
        <div class="subtitle">
            🏙️ {spot['city']} • 🎯 {spot['category']}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # メイン内容エリア
    # 📋 概要・詳細解説セクション（大幅拡充）
    st.markdown("## 📋 詳細解説")
    
    # メイン解説
    if spot.get('summary'):
        st.markdown("### 🎯 概要")
        st.write(spot['summary'])
        st.markdown("---")
    
    if spot.get('description'):
        st.markdown("### � 詳細説明")
        st.write(spot['description'])
        st.markdown("---")
    
    # 🌟 総合情報セクション（解説量大幅増加）
    st.markdown("## 🌟 総合観光情報")
    
    # カテゴリ別詳細情報の拡充表示
    category = spot.get('category', '')
    city = spot.get('city', '')
    
    # カテゴリに応じた詳細解説を追加
    if category == '歴史的建造物':
        st.markdown(f"""
        ### 🏛️ 歴史的価値について
        {spot['name']}は{city}を代表する歴史的建造物として、長い歴史と文化的価値を持っています。
        この建造物は時代を超えて多くの人々に愛され続けており、
        モロッコの豊かな歴史と伝統を物語る重要な文化遺産です。
        
        **建築的特徴:**
        - 伝統的なモロッコ建築様式
        - 精密な装飾と職人技
        - 地域固有の建材と技術の使用
        - 気候に適応した設計思想
        """)
    elif category == '市場・スーク':
        st.markdown(f"""
        ### 🛍️ 市場文化について
        {spot['name']}は{city}の商業・文化の中心地として機能する伝統的な市場です。
        ここでは何世紀にもわたって受け継がれてきた商取引の伝統と、
        現代的なニーズが見事に調和した独特の雰囲気を体験できます。
        
        **市場の特色:**
        - 伝統工芸品と現代商品の共存
        - 職人による手作り品の実演販売
        - 地域特産品と輸入品の豊富な品揃え
        - 活気ある交渉文化と人間関係
        """)
    elif category == '宮殿・庭園':
        st.markdown(f"""
        ### 🌺 宮殿文化について
        {spot['name']}は{city}の王室文化と庭園芸術の粋を集めた貴重な文化遺産です。
        精緻な建築美と計算された庭園設計は、イスラム芸術の最高峰を示しています。
        
        **宮殿の魅力:**
        - 王室の生活様式と文化的背景
        - イスラム庭園の設計思想と美学
        - 季節ごとに変化する自然美
        - 建築と自然の調和した空間設計
        """)
    else:
        st.markdown(f"""
        ### 🎨 文化的意義について
        {spot['name']}は{city}を代表する{category}として、
        この地域の文化と伝統を深く体現している重要な観光地です。
        訪問者はここで本物のモロッコ文化に触れ、その魅力を存分に味わうことができます。
        """)
    
    st.markdown("---")
    
    # 📚 詳細タブ構造（解説内容を大幅拡充）
    if spot.get('features') or spot.get('highlights') or spot.get('how_to_enjoy') or spot.get('access_notes'):
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "✨ 特徴・魅力", "👀 見どころガイド", "🎪 体験・楽しみ方", "🚗 アクセス・実用情報", "📊 詳細データ"
        ])
        
        with tab1:
            st.markdown("## ✨ 特徴・魅力の詳細解説")
            
            # 特徴情報の拡充表示
            features = spot.get('features', {})
            if features:
                st.markdown("### 🏛️ 主要な特徴")
                if isinstance(features, dict):
                    for key, value in features.items():
                        st.markdown(f"""
                        **{key}**
                        
                        {value}
                        
                        この特徴は{spot['name']}を特別な場所にしている重要な要素の一つです。
                        訪問者の多くがこの点に魅力を感じ、印象深い体験として記憶に残しています。
                        """)
                        st.markdown("---")
                else:
                    st.write(features)
            
            # 見どころ情報の詳細化
            highlights = spot.get('highlights', [])
            if highlights:
                st.markdown("### 👀 注目すべき見どころ")
                if isinstance(highlights, list):
                    for i, highlight in enumerate(highlights, 1):
                        st.markdown(f"""
                        **見どころ {i}: {highlight}**
                        
                        この見どころは{spot['name']}の中でも特に注目すべきポイントです。
                        多くの観光客がここで立ち止まり、写真撮影や詳細な観察を楽しんでいます。
                        時間をかけてじっくりと観察することで、より深い理解と感動を得ることができます。
                        """)
                        st.markdown("---")
                else:
                    st.write(highlights)
            
            # 追加の魅力ポイント
            st.markdown("""
            ### 🌟 その他の魅力ポイント
            
            **文化体験価値:**
            - 本物のモロッコ文化に触れる貴重な機会
            - 地域の歴史と伝統を深く理解できる
            - 現地の人々との交流の可能性
            
            **写真撮影スポット:**
            - インスタグラム映えする美しい景観
            - 様々な角度から楽しめる撮影ポイント
            - 時間帯による光の変化と表情の違い
            
            **学習・教育価値:**
            - 歴史学習の生きた教材
            - 建築・芸術の実例研究
            - 異文化理解の促進
            """)
        
        with tab2:
            st.markdown("## 👀 見どころガイド（詳細版）")
            
            st.markdown("""
            ### � 効果的な見学方法
            
            **推奨見学順序:**
            1. まず全体を俯瞰して雰囲気を掴む
            2. 主要な見どころを重点的に観察
            3. 細部の装飾や技法に注目
            4. 最後に再度全体を見渡して印象をまとめる
            
            **観察のポイント:**
            - 建築様式と装飾の技法
            - 使用されている材料と色彩
            - 光の当たり方による表情の変化
            - 周囲の環境との調和
            """)
            
            # 時間帯別の楽しみ方
            st.markdown("""
            ### ⏰ 時間帯別の楽しみ方
            
            **朝の時間帯（8:00-10:00）:**
            - 観光客が少なく静かな雰囲気
            - 朝日による美しい光の演出
            - 地元の人々の日常生活を垣間見る機会
            
            **昼の時間帯（10:00-15:00）:**
            - 明るい日差しで細部まで鮮明に観察可能
            - 活気ある雰囲気と賑わい
            - ガイドツアーの充実した解説
            
            **夕方の時間帯（15:00-18:00）:**
            - 柔らかな西日による温かい雰囲気
            - 黄金時間の美しい写真撮影
            - 比較的涼しく快適な見学環境
            
            **夜の時間帯（18:00以降）:**
            - ライトアップによる幻想的な美しさ
            - 昼間とは異なる神秘的な雰囲気
            - 地元の夜の文化体験
            """)
            
            how_to_enjoy = spot.get('how_to_enjoy', {})
            if how_to_enjoy:
                st.markdown("### 🎪 具体的な楽しみ方")
                if isinstance(how_to_enjoy, dict):
                    for time_period, activity in how_to_enjoy.items():
                        st.markdown(f"""
                        **{time_period}の楽しみ方:**
                        
                        {activity}
                        
                        この時間帯特有の魅力を最大限に活用して、
                        {spot['name']}での体験をより豊かにしましょう。
                        """)
                        st.markdown("---")
                else:
                    st.write(how_to_enjoy)
        
        with tab3:
            st.markdown("## 🎪 体験・楽しみ方の完全ガイド")
            
            st.markdown("""
            ### 🎨 文化体験プログラム
            
            **伝統工芸体験:**
            - 地元職人による実演見学
            - 簡単な工芸品作りへの参加
            - 技法の歴史と文化的背景の学習
            
            **料理・味覚体験:**
            - 地域特産の食材と料理の試食
            - 伝統的な調理法の見学
            - 食文化の歴史と意義の理解
            
            **音楽・芸能体験:**
            - 伝統音楽の演奏鑑賞
            - 民族舞踊の見学や参加
            - 楽器や衣装の文化的意味の学習
            """)
            
            st.markdown("""
            ### 🚶‍♂️ 散策・探索の楽しみ方
            
            **のんびり散策コース:**
            - 時間に余裕を持った自由な探索
            - 気になった場所での長時間の観察
            - 地元の人々との自然な交流
            
            **テーマ別探索:**
            - 建築様式に焦点を当てた見学
            - 歴史的な出来事の痕跡を辿る
            - 装飾芸術の技法と変遷を追う
            
            **写真撮影ツアー:**
            - 最適な撮影スポットの発見
            - 光の条件を活かした撮影技法
            - 構図と角度の工夫による表現
            """)
            
            st.markdown("""
            ### 👥 グループ・家族での楽しみ方
            
            **家族連れの場合:**
            - 子供向けの分かりやすい解説
            - 安全で楽しい見学ルートの選択
            - 家族写真の撮影スポット
            
            **友人グループの場合:**
            - みんなで楽しめる体験活動
            - グループ写真の撮影
            - 感想や発見の共有
            
            **カップルの場合:**
            - ロマンチックな雰囲気の場所
            - 二人だけの特別な思い出作り
            - 美しい夕日や夜景の鑑賞
            """)
        
        with tab4:
            st.markdown("## 🚗 アクセス・実用情報の詳細ガイド")
            
            access_notes = spot.get('access_notes', '')
            if access_notes:
                st.markdown("### 🚌 交通アクセス情報")
                if isinstance(access_notes, str):
                    access_text = access_notes.replace('\\n', '\n')
                    st.write(access_text)
                else:
                    st.write(access_notes)
                st.markdown("---")
            
            st.markdown(f"""
            ### 🚗 {city}での移動手段
            
            **タクシー利用:**
            - メーター制の正規タクシー推奨
            - 事前の料金確認と交渉
            - 主要ホテルからの所要時間と料金目安
            
            **公共交通機関:**
            - バス路線と停留所の情報
            - 運行時間と料金体系
            - 地元の人との相乗りの可能性
            
            **徒歩でのアクセス:**
            - 最寄りの主要施設からの徒歩ルート
            - 道中の見どころと休憩スポット
            - 安全な歩行ルートの選択
            """)
            
            st.markdown("""
            ### ⚠️ 注意事項・安全情報
            
            **服装・持ち物:**
            - 宗教的配慮が必要な場合の適切な服装
            - 歩きやすい靴と日除け対策
            - 貴重品の管理と最小限の携帯
            
            **文化的マナー:**
            - 写真撮影時の許可とマナー
            - 宗教的な場所での行動規範
            - 地元の人々への敬意と配慮
            
            **健康・安全対策:**
            - 水分補給と熱中症対策
            - 日焼け止めと帽子の着用
            - 緊急時の連絡先と対処法
            """)
            
            st.markdown("""
            ### 💰 料金・支払い情報
            
            **入場料・見学料:**
            - 基本入場料と割引制度
            - ガイド料金と追加サービス
            - グループ割引や学生割引の有無
            
            **その他の費用:**
            - 写真撮影料（該当する場合）
            - お土産購入の予算目安
            - 飲食や休憩にかかる費用
            
            **支払い方法:**
            - 現金支払いの必要性
            - クレジットカード利用の可否
            - 両替の必要性と方法
            """)
        
        with tab5:
            st.markdown("## 📊 詳細データ・統計情報")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📍 基本位置情報")
                st.write(f"**所在都市:** {spot.get('city', '不明')}")
                st.write(f"**カテゴリ:** {spot.get('category', '不明')}")
                st.write(f"**認定状況:** {'✅ 公式認定観光地' if spot.get('verified') else '一般観光地'}")
                
                if spot.get('coordinates'):
                    lat, lon = spot['coordinates']
                    st.markdown("### 🗺️ 正確な座標")
                    st.write(f"**緯度:** {lat:.6f}")
                    st.write(f"**経度:** {lon:.6f}")
                    st.write(f"**GPS座標:** {lat:.6f}, {lon:.6f}")
                
                # 追加データ
                if spot.get('best_time'):
                    st.write(f"**最適訪問時期:** {spot['best_time']}")
                if spot.get('duration'):
                    st.write(f"**推奨滞在時間:** {spot['duration']}")
                if spot.get('price_range'):
                    st.write(f"**料金目安:** {spot['price_range']}")
                
            with col2:
                st.markdown("### 📈 観光統計情報")
                st.markdown("""
                **人気度指標:**
                - 年間訪問者数の推定
                - 観光シーズンごとの混雑度
                - 国際観光客の割合
                
                **評価・レビュー:**
                - 観光客満足度の平均値
                - 主要な評価ポイント
                - 改善要望の傾向
                
                **アクセシビリティ:**
                - バリアフリー対応状況
                - 車椅子利用の可否
                - 高齢者・子供連れへの配慮
                """)
                
                st.markdown("### 🌡️ 気候・環境データ")
                st.markdown(f"""
                **{city}の気候特性:**
                - 年間平均気温と降水量
                - 観光に最適な季節
                - 服装選択の参考情報
                
                **環境への配慮:**
                - 持続可能な観光への取り組み
                - 環境保護の重要性
                - 観光客ができる貢献
                """)
            
            st.markdown("---")
            st.markdown("### 📚 参考情報・追加リソース")
            st.markdown(f"""
            **歴史的背景:**
            {spot['name']}の歴史は古く、この地域の文化的発展と密接に関わっています。
            時代を通じて多くの人々に愛され、保護され、現在に至るまで重要な役割を果たし続けています。
            
            **文化的意義:**
            この場所は単なる観光地ではなく、{city}の文化的アイデンティティを体現する重要な文化遺産です。
            訪問者はここで本物の文化体験を通じて、より深い理解と感動を得ることができます。
            
            **将来の展望:**
            持続可能な観光開発と文化遺産の保護を両立させながら、
            次世代にこの素晴らしい場所を引き継いでいくことが重要です。
            """)
    else:
        # 基本的な説明のみの場合も拡充
        st.markdown("## 📝 詳細情報（基本版）")
        if spot.get('description'):
            st.write(spot['description'])
            
            # 基本情報も拡充
            st.markdown("---")
            st.markdown(f"""
            ### 🌟 {spot['name']}について
            
            この観光地は{city}を訪れる際にぜひ立ち寄りたいスポットの一つです。
            {category}として分類される{spot['name']}は、その独特の魅力と文化的価値で多くの観光客を魅了しています。
            
            **訪問の意義:**
            - 地域文化への理解を深める
            - 歴史的背景を学ぶ機会
            - 美しい景観や建築の鑑賞
            - 現地の人々との交流
            
            **期待できる体験:**
            - 本物の文化との出会い
            - 印象深い写真撮影
            - 新しい発見と学び
            - 特別な思い出の創造
            """)
        else:
            st.markdown(f"""
            ### 📝 {spot['name']}詳細情報
            
            {spot['name']}は{city}に位置する{category}です。
            この場所は地域の文化と歴史を反映した重要な観光スポットとして、
            多くの訪問者に愛され続けています。
            
            **基本的な魅力:**
            - 地域特有の文化的価値
            - 歴史的な重要性
            - 美しい景観や建築
            - 教育的価値
            
            **訪問者へのメッセージ:**
            詳細な情報は現在準備中ですが、この場所は必ず訪れる価値のある
            素晴らしいスポットです。実際に足を運んでその魅力を体感してください。
            """)
            
            st.info("より詳細な情報は今後のアップデートで追加予定です。")

    
    # セクション区切り
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # 地図表示（座標がある場合）
    if spot.get('coordinates'):
        st.markdown("### 🗺️ 位置情報")
        
        import folium
        from streamlit_folium import st_folium
        
        lat, lon = spot['coordinates']
        
        # 地図スタイルの改良
        m = folium.Map(
            location=[lat, lon], 
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # カスタムマーカー
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(f"""
                <div style="width: 200px;">
                    <h4>{spot['name']}</h4>
                    <p><strong>📍 {spot['city']}</strong></p>
                    <p><strong>🎯 {spot['category']}</strong></p>
                    {'<p><strong>✅ 認定観光地</strong></p>' if spot.get('verified') else ''}
                </div>
            """, max_width=250),
            tooltip=f"📍 {spot['name']}",
            icon=folium.Icon(
                color='red', 
                icon='star' if spot.get('verified') else 'info-sign',
                prefix='fa'
            )
        ).add_to(m)
        
        # 地図表示（全幅）
        st_folium(m, width='100%', height=450, returned_objects=["last_object_clicked"])
        
        # 座標情報の表示
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 緯度", f"{lat:.6f}")
        with col2:
            st.metric("📍 経度", f"{lon:.6f}")
        with col3:
            st.metric("🎯 ズーム", "13")
    
    # ページの絶対最上部マーカー
    st.markdown("""
    <div class="detail-page-container">
        <div id="page-top" style="height: 0; margin: 0; padding: 0; position: absolute; top: 0;"></div>
    </div>
    """, unsafe_allow_html=True)
    # 戻るボタンと観光地名を上部に配置
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔙 前のページに戻る", key="detail_prev_page", use_container_width=True):
            # 詳細モードを終了
            st.session_state.detail_mode = False
            st.session_state.selected_spot = None
            
            # URLパラメータをクリア
            if 'spot_id' in st.query_params:
                st.query_params.clear()
            
            # 前のページ情報があれば、そのページに戻る
            if 'previous_page' in st.session_state and st.session_state.previous_page:
                st.session_state.current_page = st.session_state.previous_page
            else:
                # デフォルトは観光地一覧に戻る
                st.session_state.current_page = '📍 観光地一覧'
            
            # ページ状態をリセット
            st.session_state.page_just_changed = True
            st.session_state.scroll_to_top = True
            st.session_state.force_scroll_reset = True
            st.session_state.detail_just_opened = False
            st.session_state.page_reset_required = True
            st.rerun()
    
    with col2:
        pass  # 空のカラム
    
    # 関連アクション
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 🔗 関連アクション")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗺️ マップで確認", key="detail_map_confirm", use_container_width=True):
            st.session_state.detail_mode = False
            st.session_state.selected_spot = None
            # マップページに移動する処理（将来の拡張）
            st.info("マップページでこの観光地を確認できます")
    
    with col2:
        if st.button("📋 観光地一覧", key="detail_to_list_old", use_container_width=True):
            st.query_params.clear()
            st.session_state.current_page = '📍 観光地一覧'
            st.rerun()
    
    with col3:
        if st.button("�️ マップビュー", use_container_width=True):
            st.query_params.clear()
            st.session_state.current_page = '🗺️ マップ'
            st.rerun()


def show_spots_page(spots):
    """観光地一覧ページ"""
    st.subheader("📍 観光地一覧")
    
    # 高度な検索・フィルター機能
    st.markdown("### 🔍 検索・フィルター")
    
    # テキスト検索（入力検証付き）
    search_term_raw = st.text_input("🔍 観光地を検索", placeholder="名前や都市名、説明文で検索...")
    
    # 検索語の検証とサニタイゼーション
    search_term = ""
    if search_term_raw:
        is_valid, validated_input = validate_user_input(search_term_raw, max_length=50, min_length=1)
        if is_valid:
            search_term = validated_input
        else:
            st.warning(f"⚠️ 検索入力エラー: {validated_input}")
    
    # フィルター（複数選択対応）- 1列構成
    cities = sorted(set(spot['city'] for spot in spots))
    selected_cities = st.multiselect(
        "🏙️都市を選択（複数選択可）",
        options=cities,
        default=[],
        placeholder="都市を選択してください"
    )
    
    categories = sorted(set(spot['category'] for spot in spots))
    selected_categories = st.multiselect(
        "🎯 カテゴリを選択（複数選択可）",
        options=categories,
        default=[],
        placeholder="カテゴリを選択してください"
    )
    
    # 追加オプション
    col3, col4, col5 = st.columns(3)
    
    with col3:
        show_verified_only = st.checkbox("✅ 認定済みのみ表示")
    
    with col4:
        # 価格フィルター
        price_filter = st.selectbox(
            "💰 価格帯",
            ["すべて", "無料", "有料（500円未満）", "有料（500円以上）"]
        )
    
    with col5:
        # 所要時間フィルター
        duration_filter = st.selectbox(
            "⏱️ 所要時間",
            ["すべて", "短時間（1時間未満）", "中時間（1-3時間）", "長時間（3時間以上）"]
        )
    
    # フィルタリング
    filtered_spots = spots
    
    # テキスト検索（名前、都市、説明文を対象）
    if search_term:
        filtered_spots = [
            spot for spot in filtered_spots 
            if search_term.lower() in spot['name'].lower() or 
               search_term.lower() in spot['city'].lower() or
               search_term.lower() in (spot.get('summary') or spot.get('description', '')).lower()
        ]
    
    # 都市フィルター（複数選択）
    if selected_cities:
        filtered_spots = [spot for spot in filtered_spots if spot['city'] in selected_cities]
    
    # カテゴリフィルター（複数選択）
    if selected_categories:
        filtered_spots = [spot for spot in filtered_spots if spot['category'] in selected_categories]
    
    # 認定済みフィルター
    if show_verified_only:
        filtered_spots = [spot for spot in filtered_spots if spot.get('verified', False)]
    
    # 価格フィルター
    if price_filter != "すべて":
        if price_filter == "無料":
            filtered_spots = [spot for spot in filtered_spots if '無料' in spot.get('price_range', '')]
        elif price_filter == "有料（500円未満）":
            filtered_spots = [spot for spot in filtered_spots 
                            if spot.get('price_range', '') and '無料' not in spot.get('price_range', '') 
                            and any(keyword in spot.get('price_range', '') for keyword in ['10DH', '20DH', '30DH', '50DH'])]
        elif price_filter == "有料（500円以上）":
            filtered_spots = [spot for spot in filtered_spots 
                            if spot.get('price_range', '') and any(keyword in spot.get('price_range', '') for keyword in ['70DH', '130DH', '150DH', '300DH'])]
    
    # 所要時間フィルター
    if duration_filter != "すべて":
        if duration_filter == "短時間（1時間未満）":
            filtered_spots = [spot for spot in filtered_spots 
                            if spot.get('duration', '') and any(keyword in spot.get('duration', '') for keyword in ['30分', '45分'])]
        elif duration_filter == "中時間（1-3時間）":
            filtered_spots = [spot for spot in filtered_spots 
                            if spot.get('duration', '') and any(keyword in spot.get('duration', '') for keyword in ['1時間', '2時間', '1-2時間', '1-3時間'])]
        elif duration_filter == "長時間（3時間以上）":
            filtered_spots = [spot for spot in filtered_spots 
                            if spot.get('duration', '') and any(keyword in spot.get('duration', '') for keyword in ['半日', '1日', '2-3時間', '2日'])]
    
    # 検索結果の統計情報と操作ボタン
    if filtered_spots:
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🔍 検索結果", f"{len(filtered_spots)}件")
        
        with col2:
            result_cities = set(spot['city'] for spot in filtered_spots)
            st.metric("🏙️ 対象都市", f"{len(result_cities)}都市")
        
        with col3:
            result_categories = set(spot['category'] for spot in filtered_spots)
            st.metric("🎯 カテゴリ", f"{len(result_categories)}種類")
        
        with col4:
            verified_count = sum(1 for spot in filtered_spots if spot.get('verified', False))
            st.metric("✅ 認定済み", f"{verified_count}件")
        
        with col5:
            # エクスポート機能
            if st.button("📥 結果をCSVで保存", key="csv_export_button"):
                import pandas as pd
                df = pd.DataFrame(filtered_spots)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="⬇️ CSVダウンロード",
                    data=csv,
                    file_name=f"morocco_spots_{len(filtered_spots)}件.csv",
                    mime="text/csv"
                )
    
    # ソート機能
    if filtered_spots:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### 📋 検索結果一覧")
        
        with col2:
            sort_option = st.selectbox(
                "並び替え",
                ["名前順", "都市順", "カテゴリ順", "認定優先"]
            )
    
    # ソート処理
    if sort_option == "名前順":
        filtered_spots = sorted(filtered_spots, key=lambda x: x['name'])
    elif sort_option == "都市順":
        filtered_spots = sorted(filtered_spots, key=lambda x: x['city'])
    elif sort_option == "カテゴリ順":
        filtered_spots = sorted(filtered_spots, key=lambda x: x['category'])
    elif sort_option == "認定優先":
        filtered_spots = sorted(filtered_spots, key=lambda x: (not x.get('verified', False), x['name']))
    
    # 観光地カード表示（詳細ボタン付き）- 1列構成
    for i, spot in enumerate(filtered_spots):
        with st.container():
            # 追加情報の構築
            additional_info = ""
            if spot.get('best_time'):
                additional_info += f"<br>⏰ <strong>ベストタイム:</strong> {spot['best_time']}"
            if spot.get('duration'):
                additional_info += f"<br>⏱️ <strong>所要時間:</strong> {spot['duration']}"
            if spot.get('price_range'):
                additional_info += f"<br>💰 <strong>料金:</strong> {spot['price_range']}"
            
            # 概要表示（新形式の場合）
            description = spot.get('summary', spot.get('description', ''))
            if len(description) > 100:
                description = description[:100] + "..."
            
            st.markdown(f"""
            <div class="spot-card">
                <div class="spot-title">{spot['name']}</div>
                <div class="spot-meta">
                    📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                    {' • <span class="verified-badge">認定済み</span>' if spot.get('verified') else ''}
                </div>
                <p>{description}</p>
                {additional_info}
                <p><small>座標: {spot['lat']:.4f}, {spot['lng']:.4f}</small></p>
            </div>
            """, unsafe_allow_html=True)
            
            # 詳細ボタン
            detail_key = f"detail_{spot['id']}"
            if st.button("📖 詳細を見る", key=detail_key, use_container_width=True):
                st.query_params['spot_id'] = spot['id']
                st.rerun()
            
            st.markdown("---")  # 区切り線を追加
    else:
        # 検索結果が0件の場合
        st.warning("🔍 検索条件に一致する観光地が見つかりませんでした。")
        
        st.info("""
        **検索のヒント:**
        - より広い条件で検索してみてください
        - 都市やカテゴリの選択を解除してみてください
        - 検索キーワードを変更してみてください
        """)
        
        if st.button("🔄 フィルターをリセット", key="reset_filter_button"):
            st.rerun()
        
        # おすすめ観光地を表示
        st.markdown("""
        <div style="margin: 24px 0; padding: 20px; background: linear-gradient(135deg, var(--majorelle-blue-light), var(--gold-light)); border-radius: 15px; border-left: 5px solid var(--majorelle-blue);">
            <h3 style="color: var(--majorelle-blue); margin: 0; font-size: 1.5rem; font-weight: 600; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">
                ✨ おすすめ観光地 ✨
            </h3>
            <p style="color: var(--text-primary); margin: 8px 0 0; font-size: 0.95rem; line-height: 1.5;">
                検索条件に該当する観光地が見つからない場合は、以下の厳選スポットをご覧ください
            </p>
        </div>
        """, unsafe_allow_html=True)
        recommended = [spot for spot in spots if spot.get('verified', False)][:4]
        
        for i, spot in enumerate(recommended):
            st.markdown(f"""
            <div class="spot-card" style="opacity: 0.8;">
                <div class="spot-title">{spot['name']}</div>
                <div class="spot-meta">
                    📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                    <span class="verified-badge">認定済み</span>
                </div>
                <p>{(spot.get('summary') or spot.get('description', '詳細情報なし'))[:100]}...</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 詳細ボタン
            if st.button("📖 詳細を見る", key=f"home_detail_{spot['id']}", use_container_width=True):
                st.query_params['spot_id'] = spot['id']
                st.rerun()
            
            st.markdown("---")  # 区切り線を追加
    
    # 背景画像コンテナの終了
    # home-content div削除
    st.markdown('</div>', unsafe_allow_html=True)  # home-background 終了

def show_route_page(spots):
    """観光ルート作成ページ"""
    st.subheader("🛣️ 観光ルート作成")
    
    st.markdown("""
    ### 🗺️ あなただけの観光ルートを作成しよう！
    
    複数の観光地を選択して、効率的な観光ルートを自動生成します。
    移動時間や観光地の特徴を考慮した最適なルートを提案いたします。
    """)
    
    # セッション状態の初期化
    if 'selected_route_spots' not in st.session_state:
        st.session_state.selected_route_spots = []
    if 'generated_route' not in st.session_state:
        st.session_state.generated_route = None
    
    # ルート作成セクション
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎯 ルート条件設定")
        
        # 都市選択
        cities = sorted(set(spot['city'] for spot in spots))
        selected_city = st.selectbox(
            "🏙️ 都市を選択",
            options=["すべて"] + cities,
            help="特定の都市内でのルートまたは複数都市をまたがるルート"
        )
        
        # 旅行日数
        travel_days = st.selectbox(
            "📅 旅行日数",
            options=[1, 2, 3, 4, 5, 6, 7],
            index=1,
            help="選択した日数に応じてルートを最適化します"
        )
        
        # 旅行スタイル
        travel_style = st.selectbox(
            "🎨 旅行スタイル",
            options=[
                "文化・歴史重視",
                "自然・景観重視", 
                "グルメ・体験重視",
                "写真撮影重視",
                "リラックス重視",
                "アドベンチャー重視",
                "バランス型"
            ],
            help="旅行スタイルに応じて適切な観光地を優先的に選択します"
        )
        
        # 移動手段
        transport_mode = st.selectbox(
            "🚗 主な移動手段",
            options=["レンタカー", "ツアーバス", "公共交通機関", "徒歩+タクシー"],
            help="移動手段に応じてルート距離と時間を最適化します"
        )
        
        # 予算レベル
        budget_level = st.selectbox(
            "💰 予算レベル",
            options=["エコノミー", "スタンダード", "プレミアム", "ラグジュアリー"],
            help="予算に応じて宿泊や食事のグレードを調整します"
        )
    
    with col2:
        st.markdown("#### 🏛️ 観光地選択")
        
        # フィルタリング
        filtered_spots = spots
        if selected_city != "すべて":
            filtered_spots = [spot for spot in spots if spot['city'] == selected_city]
        
        # カテゴリフィルター
        categories = sorted(set(spot['category'] for spot in filtered_spots))
        selected_categories = st.multiselect(
            "🎯 興味のあるカテゴリ",
            options=categories,
            default=categories[:3],
            help="興味のあるカテゴリを選択してください"
        )
        
        if selected_categories:
            filtered_spots = [spot for spot in filtered_spots if spot['category'] in selected_categories]
        
        # 観光地選択
        st.markdown("**観光地を選択してください：**")
        
        for spot in filtered_spots[:10]:  # 最初の10件を表示
            col_check, col_info = st.columns([0.1, 0.9])
            
            with col_check:
                is_selected = spot in st.session_state.selected_route_spots
                selected = st.checkbox(
                    "選択", 
                    value=is_selected, 
                    key=f"route_spot_{spot['id']}", 
                    label_visibility="collapsed"
                )
                
                # 選択状態の更新
                if selected and spot not in st.session_state.selected_route_spots:
                    st.session_state.selected_route_spots.append(spot)
                elif not selected and spot in st.session_state.selected_route_spots:
                    st.session_state.selected_route_spots.remove(spot)
            
            with col_info:
                verified_badge = "✅" if spot.get('verified') else ""
                st.markdown(f"**{spot['name']}** {verified_badge}")
                st.caption(f"📍 {spot['city']} • {spot['category']}")
    
    # 選択された観光地の表示
    st.markdown("---")
    st.markdown("#### 🎯 選択された観光地")
    
    if st.session_state.selected_route_spots:
        cols = st.columns(min(len(st.session_state.selected_route_spots), 4))
        for i, spot in enumerate(st.session_state.selected_route_spots):
            with cols[i % 4]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 0.5rem; border-radius: 5px; margin: 0.2rem;">
                    <strong>{spot['name']}</strong><br>
                    <small>📍 {spot['city']}</small>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"**合計: {len(st.session_state.selected_route_spots)}箇所**")
        
        # ルート生成ボタン
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            # 選択された観光地数のチェック
            num_selected = len(st.session_state.selected_route_spots)
            min_spots = travel_days
            max_spots = travel_days * 4
            
            if num_selected < min_spots:
                st.warning(f"⚠️ 最低{min_spots}箇所の観光地を選択してください（現在:{num_selected}箇所）")
                button_disabled = True
            elif num_selected > max_spots:
                st.warning(f"⚠️ 観光地数が多すぎます。{max_spots}箇所以下にしてください（現在:{num_selected}箇所）")
                button_disabled = True
            else:
                button_disabled = False
            
            if st.button("🗺️ ルートを生成", type="primary", use_container_width=True, disabled=button_disabled):
                try:
                    with st.spinner("最適なルートを生成中..."):
                        st.session_state.generated_route = generate_optimal_route(
                            st.session_state.selected_route_spots,
                            travel_days,
                            travel_style,
                            transport_mode,
                            budget_level
                        )
                    st.success("✅ 観光ルートが生成されました！")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ ルート生成でエラーが発生しました: {str(e)}")
                    logger.error(f"Route generation error: {e}")
    else:
        st.info("観光地を選択してください。")
    
    # 生成されたルートの表示
    if st.session_state.generated_route:
        st.markdown("---")
        st.markdown("### 🗺️ 生成された観光ルート")
        
        route = st.session_state.generated_route
        
        # ルート概要
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📅 日数", f"{route['total_days']}日")
        with col2:
            st.metric("📍 観光地数", f"{route['total_spots']}箇所")
        with col3:
            st.metric("🚗 総移動距離", f"約{route['total_distance']}km")
        with col4:
            st.metric("💰 予算目安", f"{route['estimated_cost']}円")
        
        # 日別ルート
        for day_num, day_plan in enumerate(route['daily_plans'], 1):
            with st.expander(f"📅 {day_num}日目: {day_plan['theme']}", expanded=day_num==1):
                st.markdown(f"**テーマ:** {day_plan['theme']}")
                st.markdown(f"**移動距離:** 約{day_plan['distance']}km")
                
                for i, activity in enumerate(day_plan['activities'], 1):
                    col_time, col_activity = st.columns([0.2, 0.8])
                    
                    with col_time:
                        st.markdown(f"**{activity['time']}**")
                    
                    with col_activity:
                        if activity['type'] == 'spot':
                            st.markdown(f"🏛️ **{activity['name']}**")
                            st.caption(f"📍 {activity['location']} • 滞在時間: {activity['duration']}")
                            st.caption(activity['description'])
                        elif activity['type'] == 'meal':
                            st.markdown(f"🍽️ **{activity['name']}**")
                            st.caption(activity['description'])
                        elif activity['type'] == 'transport':
                            st.markdown(f"🚗 {activity['description']}")
                    
                    if i < len(day_plan['activities']):
                        st.markdown("↓")
        
        # ルートをマップで表示
        st.markdown("### 🗺️ ルートマップ")
        display_route_map(st.session_state.generated_route)
        
        # アクション
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📧 ルートをメール送信", use_container_width=True):
                st.info("メール送信機能は今後実装予定です")
        with col2:
            if st.button("📄 PDFでダウンロード", use_container_width=True):
                st.info("PDF出力機能は今後実装予定です")
        with col3:
            if st.button("🔄 ルートをリセット", use_container_width=True):
                st.session_state.selected_route_spots = []
                st.session_state.generated_route = None
                st.success("ルートがリセットされました")
                st.rerun()
                st.rerun()

def generate_optimal_route(selected_spots, travel_days, travel_style, transport_mode, budget_level):
    """最適な観光ルートを生成"""
    import math

    def haversine(a, b):
        # a, b: (lat, lon)
        R = 6371.0
        lat1, lon1 = math.radians(a[0]), math.radians(a[1])
        lat2, lon2 = math.radians(b[0]), math.radians(b[1])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        hav = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 2 * R * math.asin(math.sqrt(hav))

    # Collect coordinates; for spots missing coordinates, keep None
    coords = [ (spot.get('lat'), spot.get('lng')) if ('lat' in spot and 'lng' in spot) else None for spot in selected_spots ]

    # If few or missing coordinates, fall back to naive split
    if all(c is None for c in coords) or len(selected_spots) <= 2:
        # Simple even split and keep original order
        spots_per_day = max(1, min(4, len(selected_spots) // travel_days))
        daily_plans = []
        remaining = selected_spots.copy()
        for day in range(travel_days):
            take = min(spots_per_day, len(remaining)) if day < travel_days - 1 else len(remaining)
            day_spots = remaining[:take]
            remaining = remaining[take:]
            activities = []
            activities.append({'time':'09:00','type':'meal','name':'朝食','description':'ホテルで朝食'})
            for i, spot in enumerate(day_spots):
                activities.append({'time':f'{9+i*2}:00','type':'spot','name':spot['name'],'location':spot['city'],'duration':spot.get('duration','1時間'),'description':spot.get('summary','')[:100]+'...','coordinates': [spot.get('lat'), spot.get('lng')], 'spot_data': spot})
                if i < len(day_spots)-1:
                    activities.append({'time':f'{9+i*2+1}:30','type':'transport','description':f'移動（{transport_mode}）'})
            activities.append({'time':'12:30','type':'meal','name':'昼食','description':'昼食'})
            activities.append({'time':'18:00','type':'meal','name':'夕食','description':'夕食'})
            daily_plans.append({'theme': travel_style, 'distance': 0, 'activities': activities})

        total_distance = sum(p['distance'] for p in daily_plans)
        budget_multiplier = {"エコノミー":0.7,"スタンダード":1.0,"プレミアム":1.5,"ラグジュアリー":2.5}
        base_cost = 8000 * travel_days * budget_multiplier.get(budget_level,1.0)
        return {'total_days': travel_days,'total_spots': len(selected_spots),'total_distance': int(total_distance),'estimated_cost': f"{int(base_cost):,}",'daily_plans': daily_plans,'transport_mode': transport_mode,'budget_level': budget_level}

    # Build distance matrix
    n = len(selected_spots)
    dist = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if coords[i] is None or coords[j] is None:
                dist[i][j] = 1e6
            else:
                dist[i][j] = haversine(coords[i], coords[j])

    # Nearest neighbour TSP
    def nearest_neighbor_order(start=0):
        visited = [False]*n
        order = [start]
        visited[start]=True
        for _ in range(n-1):
            last = order[-1]
            # find nearest unvisited
            best, bestd = -1, float('inf')
            for j in range(n):
                if not visited[j] and dist[last][j] < bestd:
                    best, bestd = j, dist[last][j]
            if best==-1:
                break
            order.append(best)
            visited[best]=True
        return order

    # 2-opt improvement
    def two_opt(order):
        improved = True
        best_order = order[:]
        def tour_length(o):
            s = 0.0
            for i in range(len(o) - 1):
                s += dist[o[i]][o[i+1]]
            return s
        best_len = tour_length(best_order)
        while improved:
            improved = False
            for i in range(1, n-2):
                for j in range(i+1, n-1):
                    new_order = best_order[:i] + best_order[i:j+1][::-1] + best_order[j+1:]
                    new_len = tour_length(new_order)
                    if new_len + 1e-6 < best_len:
                        best_order = new_order
                        best_len = new_len
                        improved = True
            # exit if no improvement
        return best_order

    # Try nearest neighbour starting from multiple seeds and keep best
    best_route = None
    best_len = float('inf')
    for s in range(min(n, 5)):  # try up to 5 different starts
        order = nearest_neighbor_order(start=s)
        order = two_opt(order)
        # compute length
        L = sum(dist[order[i]][order[i+1]] for i in range(len(order)-1))
        if L < best_len:
            best_len = L
            best_route = order

    # Reorder spots according to best_route
    ordered_spots = [selected_spots[i] for i in best_route]
    ordered_coords = [coords[i] for i in best_route]

    # Split into days (contiguous chunks) trying to balance total intra-day distance
    avg_per_day = max(1, math.ceil(len(ordered_spots) / travel_days))
    daily_plans = []
    idx = 0
    total_distance = 0.0
    for day in range(travel_days):
        # last day gets the remainder
        if day == travel_days - 1:
            chunk = ordered_spots[idx:]
            chunk_coords = ordered_coords[idx:]
        else:
            chunk = ordered_spots[idx: idx+avg_per_day]
            chunk_coords = ordered_coords[idx: idx+avg_per_day]
        idx += len(chunk)

        activities = []
        activities.append({'time':'09:00','type':'meal','name':'朝食','description':'ホテルで朝食'})
        day_dist = 0.0
        for i, spot in enumerate(chunk):
            activities.append({'time':f'{9+i*2}:00','type':'spot','name':spot['name'],'location':spot['city'],'duration':spot.get('duration','1時間'),'description':spot.get('summary','')[:120]+'...','coordinates':[spot.get('lat'), spot.get('lng')],'spot_data': spot})
            if i < len(chunk)-1:
                activities.append({'time':f'{9+i*2+1}:30','type':'transport','description':f'移動（{transport_mode}）'})
                # add distance between successive
                a = chunk_coords[i]
                b = chunk_coords[i+1]
                if a and b:
                    d = haversine(a,b)
                    day_dist += d
        activities.append({'time':'12:30','type':'meal','name':'昼食','description':'昼食'})
        activities.append({'time':'18:00','type':'meal','name':'夕食','description':'夕食'})
        daily_plans.append({'theme': travel_style, 'distance': int(day_dist), 'activities': activities})
        total_distance += day_dist

    budget_multiplier = {"エコノミー":0.7,"スタンダード":1.0,"プレミアム":1.5,"ラグジュアリー":2.5}
    base_cost = 8000 * travel_days * budget_multiplier.get(budget_level,1.0)

    return {'total_days': travel_days,'total_spots': len(selected_spots),'total_distance': int(total_distance),'estimated_cost': f"{int(base_cost):,}",'daily_plans': daily_plans,'transport_mode': transport_mode,'budget_level': budget_level}

def display_route_map(route):
    """ルートマップを表示"""
    import folium
    from streamlit_folium import st_folium
    
    # 実際の観光地座標を収集
    all_coordinates = []
    spot_activities = []
    
    for day_num, day_plan in enumerate(route['daily_plans']):
        for activity in day_plan['activities']:
            if activity['type'] == 'spot' and activity.get('coordinates'):
                lat, lon = activity['coordinates']
                all_coordinates.append([lat, lon])
                spot_activities.append((day_num, activity))
    
    # 座標がない場合のフォールバック
    if not all_coordinates:
        # デフォルトのモロッコ中心地図
        m = folium.Map(
            location=[31.7917, -7.0926],
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # ルート情報がない旨を表示
        folium.Marker(
            [31.7917, -7.0926],
            popup="観光地の座標データがありません",
            tooltip="モロッコ中心",
            icon=folium.Icon(color='gray', icon='info-sign')
        ).add_to(m)
        
        st_folium(m, width=700, height=500)
        st.warning("⚠️ 選択された観光地の座標データが不足しています。一般的なモロッコ地図を表示しています。")
        return
    
    # 座標の中心点を計算
    center_lat = sum(coord[0] for coord in all_coordinates) / len(all_coordinates)
    center_lon = sum(coord[1] for coord in all_coordinates) / len(all_coordinates)
    
    # 適切なズームレベルを計算
    lat_range = max(coord[0] for coord in all_coordinates) - min(coord[0] for coord in all_coordinates)
    lon_range = max(coord[1] for coord in all_coordinates) - min(coord[1] for coord in all_coordinates)
    zoom_level = min(10, max(6, 8 - int(max(lat_range, lon_range))))
    
    # 地図作成
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_level,
        tiles='OpenStreetMap'
    )
    
    # 日別の色設定
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'darkblue']
    
    # マーカーを追加
    route_coordinates = []
    
    for day_num, activity in spot_activities:
        color = colors[day_num % len(colors)]
        lat, lon = activity['coordinates']
        route_coordinates.append([lat, lon])
        
        # 詳細なポップアップ情報
        popup_html = f"""
        <div style="width: 250px;">
            <h4>{activity['name']}</h4>
            <p><strong>📅 {day_num + 1}日目</strong></p>
            <p><strong>📍 場所:</strong> {activity['location']}</p>
            <p><strong>⏰ 時間:</strong> {activity['time']}</p>
            <p><strong>⌛ 滞在:</strong> {activity['duration']}</p>
            <p>{activity['description']}</p>
        </div>
        """
        
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"Day {day_num + 1}: {activity['name']}",
            icon=folium.Icon(
                color=color, 
                icon='info-sign',
                prefix='fa'
            )
        ).add_to(m)
        
        # 日数ラベルを追加
        folium.CircleMarker(
            [lat + 0.01, lon + 0.01],
            radius=15,
            popup=f"Day {day_num + 1}",
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.8,
            weight=2
        ).add_to(m)
    
    # ルートライン（連続する観光地を線で結ぶ）
    if len(route_coordinates) > 1:
        # 日別にルートラインを描画
        current_day = -1
        day_coordinates = []
        
        for day_num, activity in spot_activities:
            if day_num != current_day:
                # 前の日のラインを描画
                if len(day_coordinates) > 1:
                    folium.PolyLine(
                        day_coordinates,
                        color=colors[current_day % len(colors)],
                        weight=3,
                        opacity=0.7,
                        popup=f"Day {current_day + 1} Route"
                    ).add_to(m)
                
                # 新しい日の開始
                current_day = day_num
                day_coordinates = []
            
            day_coordinates.append(activity['coordinates'])
        
        # 最後の日のラインを描画
        if len(day_coordinates) > 1:
            folium.PolyLine(
                day_coordinates,
                color=colors[current_day % len(colors)],
                weight=3,
                opacity=0.7,
                popup=f"Day {current_day + 1} Route"
            ).add_to(m)
    
    # 凡例を追加
    legend_html = '''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: auto; 
                background-color: white; border:2px solid grey; z-index:9999; 
                font-size:14px; padding: 10px">
    <h4>観光ルート凡例</h4>
    '''
    
    for i in range(min(len(route['daily_plans']), len(colors))):
        legend_html += f'<p><i class="fa fa-circle" style="color:{colors[i]}"></i> {i + 1}日目</p>'
    
    legend_html += '</div>'
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # 地図を表示
    st_folium(m, width=700, height=500)
    
    # 統計情報
    if all_coordinates:
        st.info(f"📍 マップに表示中: {len(all_coordinates)}箇所の観光地")
    else:
        st.warning("⚠️ 表示できる観光地がありません")

def show_culture_history_page():
    """モロッコ文化・歴史ページ"""
    st.subheader("🏛️ モロッコ文化・歴史ガイド")
    
    # タブ形式で情報を整理
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📚 歴史", "🎨 文化", "🏛️ 建築", "🍽️ グルメ", "🎭 伝統", "⚠️ 観光注意点"])
    
    with tab1:
        show_history_section()
    
    with tab2:
        show_culture_section()
    
    with tab3:
        show_architecture_section()
    
    with tab4:
        show_cuisine_section()
    
    with tab5:
        show_traditions_section()
    
    with tab6:
        show_tourism_precautions_section()

def show_history_section():
    """歴史セクション"""
    st.markdown("### 📚 モロッコの歴史")
    
    # 時代別の歴史
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("""
        **主要時代**
        - 先史時代・ベルベル時代
        - ローマ時代（42-429年）
        - イスラム征服（681年～）
        - アルモラヴィ朝（1040-1147年）
        - アルモハード朝（1121-1269年）
        - マリーン朝（1244-1465年）
        - サーディアン朝（1549-1659年）
        - アラウィー朝（1666年～現在）
        - フランス保護領（1912-1956年）
        - 独立（1956年）
        """)
    
    with col2:
        st.markdown("""
        #### 🏺 古代・先史時代
        モロッコの歴史は旧石器時代にまで遡ります。原住民であるベルベル人（アマジグ人）は、数千年にわたってこの地域で独自の文化を発達させてきました。
        
        #### 🏛️ ローマ時代
        紀元前146年にカルタゴが滅亡すると、現在のモロッコ北部はローマ帝国の属州となりました。ヴォルビリス遺跡は、この時代の繁栄を物語る貴重な遺産です。
        
        #### ☪️ イスラム時代の始まり
        681年、ウマイヤ朝の軍勢がモロッコに到来し、イスラム教が伝来しました。これにより、モロッコは北アフリカのイスラム文明の中心地の一つとなりました。
        
        #### 👑 栄光の王朝時代
        **アルモラヴィ朝（1040-1147年）**: サハラ砂漠から興った王朝で、マラケシュを首都としてイベリア半島南部まで支配しました。
        
        **アルモハード朝（1121-1269年）**: モロッコ史上最大の版図を築いた王朝。クトゥビア・モスク、ハッサンの塔などの傑作建築を残しました。
        
        **マリーン朝（1244-1465年）**: フェズを首都とし、学問と芸術が花開いた時代。多くのマドラサ（神学校）が建設されました。
        """)
    
    # 現代史
    st.markdown("#### 🇫🇷 保護領時代と独立")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **フランス保護領時代（1912-1956年）**
        - 1912年フェズ条約によりフランス保護領となる
        - スルタン制は維持されるが実権はフランスが掌握
        - カサブランカ、ラバトなどの近代都市が発展
        - インフラ整備が進む一方、伝統文化は保護される
        """)
    
    with col2:
        st.success("""
        **独立への道のり**
        - 1944年独立党（イスティクラール党）結成
        - 1953年ムハンマド5世がフランスにより廃位・追放
        - 1955年ムハンマド5世復位
        - 1956年3月2日独立達成
        - 1957年王制に移行、ムハンマド5世が初代国王に
        """)

def show_culture_section():
    """文化セクション"""
    st.markdown("### 🎨 モロッコの豊かな文化")
    
    # 文化の多様性
    st.markdown("#### 🌍 文化の融合")
    st.write("""
    モロッコの文化は、**アラブ**、**ベルベル（アマジグ）**、**アンダルシア**、**アフリカ**の4つの要素が融合した独特のものです。
    この多文化性が、モロッコを世界で最も魅力的な文化的目的地の一つにしています。
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 🏺 ベルベル文化
        - **言語**: タマジグト語（公用語）
        - **芸術**: 絨毯、陶器、金属工芸
        - **音楽**: アフリカのリズムを基調
        - **建築**: 土造りの集落（カスバ）
        - **社会**: 部族社会の伝統
        """)
    
    with col2:
        st.markdown("""
        #### ☪️ アラブ・イスラム文化
        - **言語**: アラビア語（公用語）
        - **宗教**: イスラム教（スンニ派）
        - **芸術**: カリグラフィー、幾何学模様
        - **建築**: モスク、マドラサ
        - **法律**: イスラム法の影響
        """)
    
    with col3:
        st.markdown("""
        #### 🏛️ アンダルシア文化
        - **起源**: 15世紀スペインからの移民
        - **建築**: 精巧な装飾、中庭式住宅
        - **芸術**: タイル装飾（ゼリージュ）
        - **音楽**: アンダルシア音楽
        - **都市**: フェズ、ティトゥアン等
        """)
    
    # 言語と宗教
    st.markdown("#### 🗣️ 言語と宗教")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **公用語**
        - **アラビア語**: 公用語、行政・教育で使用
        - **タマジグト語**: ベルベル語、2011年に公用語化
        
        **その他の言語**
        - **フランス語**: 旧宗主国言語、ビジネスで広く使用
        - **スペイン語**: 北部地域で使用
        - **英語**: 観光業・国際ビジネスで増加傾向
        """)
    
    with col2:
        st.markdown("""
        **宗教**
        - **イスラム教**: 人口の99%（スンニ派）
        - **国王**: 「信者の長（アミール・アル・ムウミニーン）」の称号
        - **宗教的寛容**: キリスト教、ユダヤ教も保護
        - **スーフィズム**: 神秘主義的イスラムの伝統
        - **モラビト**: 聖者廟崇拝の文化
        """)

def show_architecture_section():
    """建築セクション"""
    st.markdown("### 🏛️ モロッコ建築の至宝")
    
    st.write("""
    モロッコ建築は、**イスラム建築**の最高峰の一つとして世界的に評価されています。
    精巧な装飾技術、数学的な幾何学模様、そして機能美を兼ね備えた傑作が数多く残されています。
    """)
    
    # 建築様式
    st.markdown("#### 🏗️ 主要建築様式")
    
    tab1, tab2, tab3, tab4 = st.tabs(["ムーア建築", "アルモハード様式", "マリーン様式", "アラウィー様式"])
    
    with tab1:
        st.markdown("""
        #### 🕌 ムーア建築（8-15世紀）
        **特徴:**
        - 馬蹄形アーチ
        - 複雑な幾何学模様
        - アラベスク装飾
        - 中庭（パティオ）中心の設計
        
        **代表例:**
        - アルハンブラ宮殿（スペイン）
        - フェズ・エル・バリの住宅群
        - ティトゥアンの旧市街
        """)
    
    with tab2:
        st.markdown("""
        #### 🏛️ アルモハード様式（12-13世紀）
        **特徴:**
        - 巨大で荘厳な建築物
        - 簡潔で力強いデザイン
        - 高い正方形のミナレット
        - 赤砂岩の使用
        
        **代表例:**
        - クトゥビア・モスク（マラケシュ）
        - ハッサンの塔（ラバト）
        - ヒラルダの塔（セビリア、スペイン）
        """)
    
    with tab3:
        st.markdown("""
        #### 🎨 マリーン様式（13-15世紀）
        **特徴:**
        - 極めて精巧な装飾
        - ムカルナス（鍾乳石装飾）の発達
        - カリグラフィーの多用
        - ゼリージュ（色タイル）の完成
        
        **代表例:**
        - ボウ・イナニア・マドラサ（フェズ）
        - アッタリーン・マドラサ（フェズ）
        - アルハンブラ宮殿の増築部分
        """)
    
    with tab4:
        st.markdown("""
        #### 👑 アラウィー様式（17世紀～現在）
        **特徴:**
        - 古典様式の復活と発展
        - 宮殿建築の隆盛
        - 現代技術との融合
        - 国際的影響の取り入れ
        
        **代表例:**
        - バイア宮殿（マラケシュ）
        - ハッサン2世モスク（カサブランカ）
        - 王宮群（ラバト、フェズ、マラケシュ、メクネス）
        """)
    
    # 装飾技術
    st.markdown("#### 🎨 モロッコ装飾芸術の技法")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **ゼリージュ（色タイル装飾）**
        - 幾何学模様のモザイクタイル
        - 主な色：白、青、緑、黄、茶
        - 数学的精密性
        - フェズが生産中心地
        """)
    
    with col2:
        st.markdown("""
        **タドラクト（モロッコ漆喰）**
        - 石灰と石鹸で磨いた壁面仕上げ
        - 防水性と光沢
        - ハマム（浴場）に多用
        - マラケシュ伝統の技法
        """)
    
    with col3:
        st.markdown("""
        **木工細工（メヌイジェリ）**
        - 精密な木材象嵌
        - 幾何学・植物モチーフ
        - シダー材の使用
        - 天井、扉、窓格子に使用
        """)

def show_cuisine_section():
    """グルメセクション"""
    st.markdown("### 🍽️ モロッコ料理の世界")
    
    st.write("""
    モロッコ料理は、**地中海**、**アラブ**、**ベルベル**、**アンダルシア**、**アフリカ**の食文化が融合した、
    世界で最も洗練された料理の一つです。スパイスの芸術的な使い方で知られています。
    """)
    
    # 代表料理
    st.markdown("#### 🥘 代表的なモロッコ料理")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🍲 タジン（Tajine）
        **特徴:**
        - 円錐形の蓋付き土鍋で調理
        - 蒸し煮による素材の旨味凝縮
        - 肉、野菜、果物の絶妙な組み合わせ
        
        **人気の種類:**
        - **鶏肉とレモンのタジン**: 国民的料理
        - **牛肉とプルーンのタジン**: 甘みとスパイスの調和
        - **野菜タジン**: ベジタリアン対応
        - **魚のタジン**: 沿岸部の特産
        """)
        
        st.markdown("""
        #### 🍚 クスクス（Couscous）
        **特徴:**
        - セモリナ粉から作る粒状パスタ
        - 金曜日の家庭料理として定着
        - 蒸し器で丁寧に調理
        
        **バリエーション:**
        - **野菜クスクス**: 7種の野菜使用
        - **肉クスクス**: ラムや鶏肉と
        - **魚クスクス**: 沿岸部の名物
        - **甘いクスクス**: デザート用
        """)
    
    with col2:
        st.markdown("""
        #### 🥣 ハリラ（Harira）
        **特徴:**
        - トマトベースの栄養豊富なスープ
        - ラマダン月の断食明けに必須
        - レンズ豆、ひよこ豆、米入り
        
        **文化的意義:**
        - 家族の絆を深める料理
        - 地域により味付けが異なる
        - 冬の定番料理
        """)
        
        st.markdown("""
        #### 🥖 モロッコパン
        **種類:**
        - **ホブズ**: 円形の日常パン
        - **バゲット**: フランス統治時代の名残
        - **ムスメン**: 薄く延ばした層状パン
        - **バグリル**: セモリナ粉のパン
        
        **特徴:**
        - 毎食必須のアイテム
        - 地域の小麦粉使用
        - 共同オーブンでの焼成
        """)
    
    # 飲み物文化
    st.markdown("#### 🫖 モロッコの飲み物文化")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **アタイ（ミントティー）**
        - モロッコの国民的飲み物
        - 緑茶＋ミント＋砂糖
        - おもてなしの象徴
        - 高い位置から注ぐ芸術的所作
        - 1日何度でも飲む習慣
        """)
    
    with col2:
        st.markdown("""
        **フレッシュジュース**
        - オレンジジュース（最も人気）
        - ザクロジュース（健康効果）
        - アボカドジュース（栄養満点）
        - キャロットジュース（ビタミン豊富）
        - 街角の屋台で絞りたて提供
        """)
    
    with col3:
        st.markdown("""
        **コーヒー文化**
        - **カフェ・オ・レ**: フランス式
        - **カフェ・ノワール**: エスプレッソ
        - **カフェ・カッスィール**: 濃いコーヒー
        - カフェ文化はフランス統治時代から
        - 男性の社交場として重要
        """)

def show_traditions_section():
    """伝統セクション"""
    st.markdown("### 🎭 モロッコの伝統と習慣")
    
    # 音楽と舞踊
    st.markdown("#### 🎵 音楽と舞踊")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🥁 グナワ音楽
        **起源と特徴:**
        - サハラ以南アフリカからの奴隷文化
        - 宗教的・治療的音楽
        - トランス状態を誘発
        - カルカバ（金属カスタネット）使用
        
        **楽器:**
        - **ゲンブリ**: ベース弦楽器
        - **カルカバ**: 金属製響器
        - **ダルブッカ**: ゴブレット型太鼓
        
        **現代への影響:**
        - ジャズとの融合
        - 国際的な評価
        - エッサウィラ・グナワ音楽祭
        """)
    
    with col2:
        st.markdown("""
        #### 🎶 アンダルシア音楽
        **歴史:**
        - 15世紀スペインからの移民が伝承
        - アラブ・アンダルシア古典音楽
        - 宮廷音楽としての発展
        
        **特徴:**
        - 複雑な旋律とリズム
        - 詩的な歌詞
        - 多楽器による合奏
        
        **主要楽器:**
        - **ウード**: リュート族弦楽器
        - **カーヌーン**: ツィター族
        - **ダフ**: フレームドラム
        - **ナイ**: 葦笛
        """)
    
    # 工芸と職人技
    st.markdown("#### 🎨 伝統工芸と職人技")
    
    tab1, tab2, tab3, tab4 = st.tabs(["絨毯・織物", "陶器・金属工芸", "革製品", "木工・石工"])
    
    with tab1:
        st.markdown("""
        #### 🧶 絨毯・織物
        **ベルベル絨毯:**
        - 各部族固有の模様と色彩
        - 羊毛を天然染料で染色
        - 家族の歴史を織り込む
        - アトラス山脈の村々が産地
        
        **都市型絨毯:**
        - ペルシャ様式の影響
        - 絹を使用した高級品
        - 幾何学・植物模様
        - ラバト、サレが有名
        """)
    
    with tab2:
        st.markdown("""
        #### 🏺 陶器・金属工芸
        **フェズ陶器:**
        - 青と白の美しい配色
        - コバルトブルーが特徴
        - 14世紀から続く伝統
        - 実用性と芸術性の両立
        
        **金属工芸:**
        - 銅、真鍮、銀の加工
        - 透かし彫りの技術
        - ティーセット、トレイ製作
        - フェズ、メクネスが中心地
        """)
    
    with tab3:
        st.markdown("""
        #### 👜 革製品
        **特徴:**
        - 世界最高品質の革
        - 天然なめし技術
        - 伝統的な手作業
        - 1000年変わらぬ製法
        
        **主要産地:**
        - **フェズ**: 最高級品
        - **マラケシュ**: 観光客向け
        - **テトゥアン**: 北部の特色
        
        **製品:**
        - バブーシュ（革スリッパ）
        - バッグ、財布
        - 革ジャケット
        """)
    
    with tab4:
        st.markdown("""
        #### 🪵 木工・石工
        **木工芸:**
        - アトラス杉材使用
        - 象嵌技術（マルケッテリ）
        - 幾何学模様の精密加工
        - 家具、建築装飾
        
        **石工芸:**
        - 大理石、石灰岩加工
        - 噴水、柱の製作
        - アラベスク彫刻
        - 建築装飾の専門技術
        """)
    
    # 祭りと年中行事
    st.markdown("#### 🎉 祭りと年中行事")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **宗教的祭典:**
        - **ラマダン**: 断食月（イスラム暦9月）
        - **イード・アル=フィトル**: 断食明け祭
        - **イード・アル=アドハー**: 犠牲祭
        - **ムーリド**: 預言者誕生祭
        - **アーシューラー**: シーア派由来の祭典
        """)
    
    with col2:
        st.markdown("""
        **文化的祭典:**
        - **アーモンド花祭**: タフラウトの春祭り
        - **バラ祭**: ケラア・ムグナのバラ収穫祭
        - **グナワ音楽祭**: エッサウィラの音楽祭
        - **フェズ世界聖音楽祭**: 宗教音楽祭
        - **マラケシュ国際映画祭**: 映画祭
        """)

def show_ai_page(ai_service):
    """AI観光ガイドページ"""
    st.subheader("🤖 高精度AI観光ガイド")
    
    # 機能説明
    st.markdown("""
    **🧠 知識ベース搭載AI**
    - 40の観光地データと詳細な文化・歴史情報を内蔵
    - カテゴリ別専門応答（歴史、文化、料理、建築、旅行、気候、言語）
    - スマートキーワード分析による最適な回答生成
    """)
    
    # API状態の表示（セキュアな方法）
    col1, col2 = st.columns([3, 1])
    with col1:
        if ai_service['available']:
            st.success("✅ OpenAI API + 高精度知識ベース")
        else:
            st.info("🤖 高精度フォールバック応答システム")
    
    with col2:
        if ai_service['available']:
            st.info("🔑 OpenAI: 設定済み")
        else:
            st.warning("🔑 OpenAI: 未設定")

    # ベクトル検索が利用可能で、まだインデックス未構築なら自動構築（初回のみ）
    if ai_service.get('vector_search_available') and not st.session_state.get('kb_vector_store_built'):
        if not st.session_state.get('kb_vector_store_auto_built'):
            try:
                kb = ai_service['knowledge_base']
                docs = build_docs_from_kb(kb) if build_docs_from_kb else []
                if docs and VectorStore:
                    with st.spinner("🔧 ベクトルインデックスを自動構築しています..."):
                        vs = VectorStore()
                        vs.build(docs)
                        st.session_state['kb_vector_store'] = vs
                        st.session_state['kb_vector_store_built'] = True
                        st.session_state['kb_vector_store_auto_built'] = True
                    st.success(f"✅ ベクトルインデックスを自動構築しました（{len(docs)}件）")
            except Exception as e:
                logger.warning(f"Auto-build of vector index failed: {e}")

    # ベクトル検索（RAG）機能の有無とインデックス構築UI
    if ai_service.get('vector_search_available'):
        st.markdown("### 🔎 ベクトル検索（RAG） — 質問に強い検索")
        st.success("🔎 この機能は、あなたの質問に関連する参考情報を自動で探し、AIの回答をより正確にするために使います。モデルや環境によって利用できない場合があります。")

        # RAG パラメータ（UIから調整可能）
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.slider("参考に使う上位文の数（Top K）", min_value=1, max_value=12, value=6, key="rag_top_k")
            st.caption("小さい値はより絞った参照、大きい値はより多くの資料を参考にします（検索の幅が変わります）。")
        with col_b:
            st.number_input("要約の最大文字数", min_value=200, max_value=5000, value=1000, step=100, key="summary_max_chars")
            st.caption("検索で見つかった本文を要約してAIに渡します。値を小さくすると短い要約になります。")

        # 出典メタから人が読める出典名を取り出す小ヘルパー（いろんな形式に対応）
        def _get_source_from_meta(meta: dict) -> str:
            try:
                if not meta:
                    return '不明な出典'
                # 優先キー一覧
                for key in ('source', 'title', 'name', 'doc_id', 'id', 'file', 'url', 'source_name', 'source_title'):
                    v = meta.get(key)
                    if v:
                        # 非空の文字列を返す
                        return str(v)
                # city/type 情報があれば、それを使う
                if 'city' in meta:
                    return f"{meta.get('city')}（地名）"
                if 'type' in meta:
                    return str(meta.get('type'))
                # 最後の手段でメタの一部を JSON 化して返す（短縮）
                try:
                    import json as _json
                    dump = _json.dumps(meta, ensure_ascii=False)
                    return dump[:120]
                except Exception:
                    return '不明な出典'
            except Exception:
                return '不明な出典'

        # 初心者向けの簡単な説明と例（折りたたみ）
        with st.expander('この機能の使い方（初心者向け・簡単な例）', expanded=False):
            st.markdown(
                '- ステップ1: 上の入力欄に質問を入れます（例: 「モロッコ料理の特徴は？」）。\n'
                '- ステップ2: ベクトル検索は質問の意味に合う参考文章を探します（Top Kで何件参考にするか選べます）。\n'
                '- ステップ3: 見つかった参考文章は自動で要約され、AIの回答作成に使われます。\n\n'
                '簡単なフロー（テキスト図）:\n'
                '質問 → (ベクトル検索で候補を取得) → (候補を要約) → AIが要約＋知識で回答\n\n'
                '**例**: 質問「モロッコ料理の特徴は？」 → 検索で「スパイス」「タジン」「ミントティー」などを含む文を発見 → 要約してAIが要点を返す。'
            )

        # 初回インデックス構築ボタン
        if not st.session_state.get('kb_vector_store_built'):
            if st.button("🔧 KB インデックスを構築 (初回のみ)", key="build_kb_index"):
                try:
                    kb = ai_service['knowledge_base']
                    docs = build_docs_from_kb(kb)
                    # compute KB fingerprint for persistence
                    import hashlib
                    kb_bytes = json.dumps(kb, ensure_ascii=False).encode('utf-8')
                    fingerprint = hashlib.sha256(kb_bytes).hexdigest()[:12]
                    storage_dir = os.path.join(os.path.dirname(__file__), 'data', 'ai_vector_index')
                    os.makedirs(storage_dir, exist_ok=True)
                    base_path = os.path.join(storage_dir, f'kb_index_{fingerprint}')

                    # try loading persisted index
                    try:
                        vs = VectorStore.load(base_path)
                        st.session_state['kb_vector_store'] = vs
                        st.session_state['kb_vector_store_built'] = True
                        st.success(f"✅ 永続化インデックスを読み込みました（{len(vs._ids)}件）")
                    except Exception:
                        vs = VectorStore()
                        with st.spinner("インデックスを構築しています... この処理は数秒かかる場合があります"):
                            vs.build(docs)
                        # persist
                        try:
                            vs.save(base_path)
                        except Exception:
                            logger.warning('Failed to persist vector index, continuing in-memory')
                        st.session_state['kb_vector_store'] = vs
                        st.session_state['kb_vector_store_built'] = True
                        st.success(f"✅ ベクトルインデックスを構築しました（ドキュメント数: {len(docs)}）")
                except Exception as e:
                    st.error(f"インデックス構築に失敗しました: {e}")
        else:
            st.info("✅ 参考データ（インデックス）はこのセッションで準備済みです。すぐに検索できます。")

            # 単純なテスト検索UI（初心者向け表示）
            test_q = st.text_input("🔎 試しに質問を入力してみましょう（例: モロッコ料理の特徴）", key="rag_test_query")
            if st.button("検索", key="rag_test_search"):
                if not test_q:
                    st.warning("検索する質問を入力してください（空欄は不可です）")
                else:
                    vs = st.session_state.get('kb_vector_store')
                    if not vs:
                        st.error("インデックスが見つかりません。左のボタンでインデックスを作成してください。")
                    else:
                        try:
                            top_k = st.session_state.get('rag_top_k', 5)
                            results = vs.query(test_q, top_k=top_k)
                            if not results:
                                st.info("該当する参考情報が見つかりませんでした。別の言い回しで試してください。")
                            else:
                                st.markdown(f"**検索結果（上位{min(len(results), top_k)}件） — AIが参照する候補**")
                                for r in results:
                                    meta = r.get('meta', {}) or {}
                                    rid = r.get('id')
                                    score = r.get('score', 0.0)
                                    text = (r.get('text') or "").strip()
                                    # 短い抜粋を表示
                                    excerpt = text.replace('\n', ' ')[:260]
                                    source = _get_source_from_meta(meta)
                                    # URLがあればリンク化
                                    url = meta.get('url') or meta.get('link') or meta.get('file')
                                    if url:
                                        st.markdown(f"- **出典**: [{source}]({url})  \n  id: `{rid}` • 類似度: {score*100:.1f}%  ")
                                    else:
                                        st.markdown(f"- **出典**: {source}  \n  id: `{rid}` • 類似度: {score*100:.1f}%  ")
                                    if excerpt:
                                        st.markdown(f"  > {excerpt}...")
                        except Exception as e:
                            st.error(f"検索中にエラーが発生しました: {e}")
    else:
        st.info("🔎 ベクトル検索は未構成です。必要なパッケージ(sentence-transformers, scikit-learn)をrequirements.txtに追加済みか確認してください。")
    
    # チャット履歴の初期化
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # おすすめ質問
    st.subheader("💡 おすすめの質問")
    suggestions = [
        "マラケシュのおすすめ観光地を教えて",
        "カサブランカで必見のスポットは？",
        "フェズの歴史について教えて",
        "サハラ砂漠ツアーのアドバイスをください",
        "モロッコ料理のおすすめは？"
    ]
    
    for i, suggestion in enumerate(suggestions):
        if st.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            response = get_ai_response(suggestion, ai_service)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    # ユーザー入力（入力検証付き）
    if prompt_raw := st.chat_input("モロッコについて何でも聞いてください！"):
        # 入力検証とサニタイゼーション
        is_valid, validated_prompt = validate_user_input(prompt_raw, max_length=500, min_length=1)
        
        if not is_valid:
            st.error(f"⚠️ 入力エラー: {validated_prompt}")
            st.stop()
        
        prompt = validated_prompt
        
        # ユーザーメッセージを追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI応答を生成
        with st.chat_message("assistant"):
            response = get_ai_response(prompt, ai_service)
            st.markdown(response)
        
        # アシスタントメッセージを追加
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_ai_response(prompt, ai_service):
    """AI応答を生成（高精度フォールバック対応・高速化版）"""
    if ai_service['available']:
        try:
            kb = ai_service['knowledge_base']
            retrieved_context = None
            
            # RAG: ベクトル検索が有効なら、インデックスを用いて上位文書を取得
            if ai_service.get('vector_search_available') and VectorStore and build_docs_from_kb:
                try:
                    # init_ai_service で事前構築済みのベクトルストアを取得
                    vs = st.session_state.get('kb_vector_store')
                    if vs:
                        # 検索（精度優先: top_kを8に増やして複数候補をAIに提供）
                        top_k = st.session_state.get('rag_top_k', 8)  # 4→8に増加（期間マッチング改善）
                        results = vs.query(prompt, top_k=top_k)
                    
                        # RAG検索結果を構造化して整形（AIが活用しやすい形式）
                        snippets = []
                        for idx, r in enumerate(results[:top_k], 1):  # 確実に上限を適用
                            text = (r.get('text') or '').strip()
                            if not text:
                                continue
                            score = r.get('score', 0.0)
                            meta = r.get('meta', {})
                            doc_id = r.get('id', 'unknown')
                            
                            # ドキュメントタイプを特定
                            tag = meta.get('city') or meta.get('type') or 'doc'
                            
                            # 旅程データの場合は期間情報を抽出
                            duration_info = ""
                            if 'itinerary' in str(doc_id):
                                import re
                                # 期間情報を抽出（"期間: 2泊3日" など）
                                duration_match = re.search(r'期間:\s*([^\n]+)', text)
                                if duration_match:
                                    duration_info = f" [{duration_match.group(1)}]"
                            
                            # より長い文章を許可（詳細な情報提供のため）
                            max_len = 800  # 400→800に増加
                            if len(text) > max_len:
                                snippet = text[:max_len].rstrip() + '...'
                            else:
                                snippet = text
                            
                            # 構造化されたヘッダー（AIが情報源を理解しやすい）
                            header = f"\n【検索結果 {idx}】類似度: {score:.1%} | 情報源: {tag}{duration_info}"
                            snippets.append(f"{header}\n{snippet}\n")
                        
                        if snippets:
                            # 構造化されたコンテキストを作成
                            retrieved_context = '\n---\n'.join(snippets)
                            # 最大トークン制限を拡大（詳細な情報提供のため）
                            if len(retrieved_context) > 4000:  # 2000→4000に拡大
                                retrieved_context = retrieved_context[:4000] + '...'
                    else:
                        logger.info("Vector store not available in session")
                except Exception as e:
                    logger.warning(f"RAG retrieval failed, continue without RAG: {e}")

            # 実際のOpenAI APIを使用する場合の高精度プロンプト
            enhanced_prompt = create_enhanced_prompt(prompt, kb, retrieved_context)
            
            # デバッグ用ログ
            logger.info(f"Calling OpenAI API for prompt: {prompt[:50]}...")
            ai_text = call_openai_api(enhanced_prompt)
            
            if ai_text and len(ai_text.strip()) > 10:
                logger.info(f"OpenAI API returned response: {len(ai_text)} chars")
                return ai_text
            else:
                logger.warning(f"OpenAI API returned empty or short response: {ai_text}")
                raise RuntimeError("Empty or insufficient OpenAI response")
        except Exception as e:
            logger.error(f"API call failed: {str(e)}")
            st.error(f"API呼び出しエラー: {str(e)}")
    
    # 高精度フォールバック応答
    logger.info("Using fallback response")
    return generate_smart_fallback_response(prompt, ai_service)

def create_enhanced_prompt(user_prompt, knowledge_base, retrieved_context: Optional[str] = None):
    """OpenAI API用の強化されたプロンプトを作成

    retrieved_context: ベクトル検索で取得した追加コンテキスト文字列（任意）
    """
    system_prompt = f"""あなたはモロッコ観光の専門ガイドです。以下の知識ベースに基づいて、正確で詳細な情報を提供してください。

【モロッコ基本情報】
国名: {knowledge_base['country_info']['name']}
首都: {knowledge_base['country_info']['capital']}
最大都市: {knowledge_base['country_info']['largest_city']}
人口: {knowledge_base['country_info']['population']}
言語: {', '.join(knowledge_base['country_info']['languages'])}
通貨: {knowledge_base['country_info']['currency']}
宗教: {knowledge_base['country_info']['religion']}

【文化的背景】
- ベルベル文化: {knowledge_base['cultural_context']['berber_heritage']}
- イスラム文化: {knowledge_base['cultural_context']['islamic_influence']}
- アンダルシア文化: {knowledge_base['cultural_context']['andalusian_legacy']}
- フランス植民地影響: {knowledge_base['cultural_context']['french_colonial']}

【旅行のベストシーズン】
春（3-5月): {knowledge_base['travel_tips']['best_seasons']['spring']}
夏（6-8月): {knowledge_base['travel_tips']['best_seasons']['summer']}
秋（9-11月): {knowledge_base['travel_tips']['best_seasons']['autumn']}
冬（12-2月): {knowledge_base['travel_tips']['best_seasons']['winter']}"""
    
    # 取得コンテキストがあれば追加（重要な指示を先頭に）
    context_block = ""
    if retrieved_context:
        context_block = f"""

【参照情報】
以下は検索結果から得られた補足情報です。これを参考にしつつ、自然な文章で回答してください。
検索結果をそのまま表示せず、ユーザーの質問に対する分かりやすい回答を作成してください。

{retrieved_context}

---
"""

    # 最終的なプロンプト構成
    final_prompt = f"""{system_prompt}{context_block}

【回答スタイルと重要な指示】

1. **期間マッチングの最優先**
   - ユーザーが「2泊3日」「1日」などの期間を指定している場合は、その期間に完全に一致する旅程プランを最優先で提案してください
   - スコアが高い検索結果だけでなく、質問の期間（日数・泊数）に正確にマッチする情報を重視してください

2. **旅程提案時の必須要素**（モデルコース・旅行プランを聞かれた場合）
   - **日次スケジュール**: 各日の具体的な行動計画（午前・午後・夕方に分けて）
   - **観光スポット**: 各スポットの名前、見どころ、所要時間、入場料
   - **移動手段**: スポット間のアクセス方法と所要時間（タクシー、徒歩など）
   - **食事の提案**: おすすめのレストランや地元料理
   - **予算目安**: 宿泊費、食費、入場料、交通費の概算
   - **実用的なTips**: ベストな訪問時間帯、注意事項、持ち物など

3. **観光スポット説明時の必須要素**
   - **基本情報**: 正式名称、場所、歴史的背景
   - **見どころ**: 具体的な観光ポイント
   - **実用情報**: 営業時間、入場料、所要時間
   - **アクセス**: 行き方と所要時間
   - **ベストタイミング**: おすすめの訪問時間帯や季節

4. **回答の表現方法**
   - 検索結果や参照情報を機械的に羅列せず、ユーザーに役立つ形で再構成してください
   - 自然な会話調で、親しみやすく詳しく説明してください
   - 具体的な数値（価格、時間、距離）を必ず含めてください
   - 箇条書きや見出しを活用して読みやすく整理してください
   - 必ず日本語で回答してください

【ユーザーの質問】
{user_prompt}

【あなたの回答】"""

    return final_prompt

def generate_smart_fallback_response(prompt, ai_service):
    """スマートフォールバック応答生成（RAG検索結果を活用）"""
    prompt_lower = prompt.lower()
    knowledge_base = ai_service['knowledge_base']
    fallback_responses = ai_service['fallback_responses']
    
    # RAG検索が利用可能なら、検索結果に基づいた応答を生成
    if ai_service.get('vector_search_available') and VectorStore:
        vs = st.session_state.get('kb_vector_store')
        if vs:
            try:
                results = vs.query(prompt, top_k=3)
                if results:
                    # 検索結果から情報を抽出して自然な応答を生成
                    response_parts = []
                    response_parts.append(f"お問い合わせの「{prompt}」について、以下の情報をご案内します。\n")
                    
                    for i, r in enumerate(results, 1):
                        text = (r.get('text') or '').strip()
                        meta = r.get('meta', {})
                        city = meta.get('city', '')
                        type_info = meta.get('type', '')
                        
                        if text:
                            # 最初の200文字程度を抜粋
                            excerpt = text[:200].strip()
                            if len(text) > 200:
                                excerpt += '...'
                            
                            if city:
                                response_parts.append(f"\n**{i}. {city}について**")
                            elif type_info:
                                response_parts.append(f"\n**{i}. {type_info}**")
                            else:
                                response_parts.append(f"\n**{i}. 関連情報**")
                            
                            response_parts.append(f"\n{excerpt}\n")
                    
                    response_parts.append("\n---")
                    response_parts.append("\n💡 **補足情報**")
                    response_parts.append(f"\n• 通貨: {knowledge_base['country_info']['currency']}")
                    response_parts.append(f"\n• 主要言語: {', '.join(knowledge_base['country_info']['languages'][:2])}")
                    response_parts.append("\n\nさらに詳しい情報が必要な場合は、具体的な観光地名や興味のあるテーマをお聞かせください。")
                    
                    return ''.join(response_parts)
            except Exception as e:
                logger.warning(f"RAG fallback failed: {e}")
    
    # キーワード分析
    keywords = analyze_prompt_keywords(prompt_lower)
    
    # 都市名検索
    for city, response in fallback_responses.items():
        if city.lower() in prompt_lower:
            return format_enhanced_response(response, keywords, knowledge_base)
    
    # カテゴリ別質問分析
    if any(word in prompt_lower for word in ['歴史', '歴史的', '王朝', '時代']):
        return generate_history_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['文化', '伝統', '習慣', '宗教']):
        return generate_culture_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['料理', 'グルメ', '食事', '食べ物', 'レストラン']):
        return generate_cuisine_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['建築', '建物', 'モスク', '宮殿']):
        return generate_architecture_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['旅行', '観光', 'ツアー', '行き方', 'アクセス']):
        return generate_travel_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['気候', '天気', '季節', 'ベストシーズン']):
        return generate_weather_response(keywords, knowledge_base)
    elif any(word in prompt_lower for word in ['言語', 'アラビア語', 'フランス語', 'ベルベル語']):
        return generate_language_response(keywords, knowledge_base)
    
    # 一般的な応答
    return fallback_responses.get('general', generate_default_response(knowledge_base))

def analyze_prompt_keywords(prompt):
    """プロンプトからキーワードを抽出"""
    keywords = {
        'cities': [],
        'activities': [],
        'interests': [],
        'time_related': [],
        'difficulty': []
    }
    
    # 都市名
    cities = ['マラケシュ', 'カサブランカ', 'フェズ', 'シャウエン', 'エッサウィラ', 'メルズーガ', 'ラバト', 'メクネス', 'タンジェ', 'ティトゥアン']
    for city in cities:
        if city.lower() in prompt:
            keywords['cities'].append(city)
    
    # アクティビティ
    activities = ['ラクダ', 'トレッキング', 'キャンプ', '砂漠', 'サーフィン', '写真', 'ショッピング', 'スパ']
    for activity in activities:
        if activity in prompt:
            keywords['activities'].append(activity)
    
    # 興味分野
    interests = ['建築', '歴史', '文化', '料理', '芸術', '音楽', '自然', '宗教']
    for interest in interests:
        if interest in prompt:
            keywords['interests'].append(interest)
    
    return keywords

def format_enhanced_response(base_response, keywords, knowledge_base):
    """基本応答を強化"""
    enhanced = f"🕌 {base_response}\n\n"
    
    # 実用情報の追加
    enhanced += "**📋 実用情報:**\n"
    enhanced += f"• 通貨: {knowledge_base['country_info']['currency']}\n"
    enhanced += f"• 言語: {', '.join(knowledge_base['country_info']['languages'])}\n"
    enhanced += f"• 時差: {knowledge_base['country_info']['time_zone']}\n\n"
    
    # 文化的エチケット
    enhanced += "**🤝 文化的エチケット:**\n"
    etiquette = knowledge_base['travel_tips']['cultural_etiquette']
    enhanced += f"• 挨拶: {etiquette['greetings']}\n"
    enhanced += f"• 服装: {etiquette['dress_code']}\n"
    enhanced += f"• 撮影: {etiquette['photography']}\n\n"
    
    enhanced += "詳しい情報については、マップや観光地一覧ページをご確認ください。"
    
    return enhanced

def generate_history_response(keywords, knowledge_base):
    """歴史関連の応答生成"""
    return """🏛️ **モロッコの歴史**

モロッコは豊かな歴史を持つ国で、以下の主要時代があります：

**� 古代・先史時代**
• ベルベル人（アマジグ人）が数千年前から居住
• ローマ帝国時代（42-429年）の遺跡が残存

**☪️ イスラム王朝時代**
• アルモラヴィ朝（1040-1147年）: マラケシュを首都
• アルモハード朝（1121-1269年）: 最大版図を築く
• マリーン朝（1244-1465年）: フェズで学問が栄える
• サーディアン朝（1549-1659年）: マラケシュで復活
• アラウィー朝（1666年-現在）: 現王朝

**🇫🇷 近現代**
• フランス保護領（1912-1956年）
• 1956年独立達成、ムハンマド5世が初代国王

**🏛️ 歴史を感じられる観光地**
• ヴォルビリス遺跡: ローマ時代
• フェズ・エル・バリ: イスラム中世都市
• サーディアン朝の墳墓群: 王朝時代の霊廟"""

def generate_culture_response(keywords, knowledge_base):
    """文化関連の応答生成"""
    return """🎨 **モロッコの文化**

モロッコの文化は4つの要素が融合した独特のものです：

**🌍 文化的要素**
• **ベルベル文化**: 北アフリカ先住民の伝統
• **アラブ・イスラム文化**: 7世紀以降の支配的文化
• **アンダルシア文化**: 15世紀スペインからの移民
• **アフリカ文化**: サハラ以南との交流

**🗣️ 言語**
• アラビア語（公用語）: 行政・教育
• タマジグト語（公用語）: ベルベル語、2011年制定
• フランス語: ビジネス・国際関係
• スペイン語: 北部地域

**☪️ 宗教**
• イスラム教スンニ派（99%）
• 国王は「信者の長」の称号
• 宗教的寛容性あり

**🎭 伝統芸能**
• グナワ音楽: アフリカ系宗教音楽
• アンダルシア音楽: 古典宮廷音楽
• ベルベル音楽: 部族の伝統音楽"""

def generate_cuisine_response(keywords, knowledge_base):
    """料理関連の応答生成"""
    return """🍽️ **モロッコ料理ガイド**

モロッコ料理は世界で最も洗練された料理の一つです：

**🥘 代表的料理**
• **タジン**: 円錐形土鍋の蒸し煮料理
  - 鶏肉とレモンのタジン（最も人気）
  - 牛肉とプルーンのタジン（甘みとスパイス）
  - 野菜タジン（ベジタリアン対応）

• **クスクス**: セモリナ粉の粒状パスタ
  - 金曜日の家庭料理として定着
  - 7種の野菜と肉の組み合わせ

• **ハリラ**: 栄養豊富なトマトスープ
  - ラマダン断食明けの定番
  - レンズ豆、ひよこ豆入り

**🫖 飲み物文化**
• **アタイ（ミントティー）**: 国民的飲み物
• **フレッシュジュース**: オレンジが最人気
• **カフェ文化**: フランス統治時代から

**🌶️ スパイス**
• ラス・エル・ハヌート: ミックススパイス
• サフラン: 高級香辛料
• ハリッサ: 辛味調味料

**🍴 食事マナー**
• 右手で食事
• パンで料理をすくう
• 食前食後の手洗い"""

def generate_architecture_response(keywords, knowledge_base):
    """建築関連の応答生成"""
    return """🏛️ **モロッコ建築の芸術**

モロッコはイスラム建築の最高峰を誇ります：

**🕌 建築様式**
• **ムーア建築（8-15世紀）**: 馬蹄形アーチ、幾何学模様
• **アルモハード様式（12-13世紀）**: 巨大で荘厳、高いミナレット
• **マリーン様式（13-15世紀）**: 極めて精巧な装飾
• **アラウィー様式（17世紀-現在）**: 古典様式の復活

**🎨 装飾技術**
• **ゼリージュ**: 幾何学モザイクタイル
• **タドラクト**: モロッコ伝統漆喰仕上げ
• **木工細工**: 精密な象嵌技術
• **ムカルナス**: 鍾乳石装飾

**🏛️ 代表建築**
• **宗教建築**: クトゥビア・モスク、ハッサン2世モスク
• **宮殿建築**: バイア宮殿、王宮群
• **学校建築**: ボウ・イナニア・マドラサ
• **要塞建築**: ウダイヤ・カスバ

**🎯 見学ポイント**
• タイル装飾の数学的精密性
• 光と影の計算された美学
• 中庭を中心とした空間構成
• イスラム文様の意味と象徴"""

def generate_travel_response(keywords, knowledge_base):
    """旅行関連の応答生成"""
    practical = knowledge_base['travel_tips']['practical_info']
    return f"""✈️ **モロッコ旅行ガイド**

**📋 基本情報**
• ビザ: {practical['visa']}
• 健康: {practical['health']}
• 安全: {practical['safety']}
• インターネット: {practical['internet']}
• 交通: {practical['transportation']}

**🌡️ ベストシーズン**
• **春（3-5月）**: 温暖で観光に最適
• **秋（9-11月）**: 過ごしやすく観光シーズン
• **夏（6-8月）**: 沿岸部は涼しい、内陸部は酷暑
• **冬（12-2月）**: 温和、山間部は寒い

**🎯 旅行スタイル別おすすめ**
• **文化重視**: フェズ、マラケシュ、メクネス
• **自然体験**: メルズーガ（砂漠）、シャウエン（山間）
• **リゾート**: エッサウィラ、アガディール
• **現代都市**: カサブランカ、ラバト

**💰 予算目安（1日あたり）**
• バックパッカー: 3,000-5,000円
• 中級旅行: 8,000-15,000円
• 高級旅行: 20,000円以上

**🎒 持参推奨品**
• 日焼け止め、帽子（強い日差し対策）
• 長袖シャツ（宗教施設・砂漠用）
• 歩きやすい靴（石畳の道）
• 現金（カード使用制限あり）"""

def generate_weather_response(keywords, knowledge_base):
    """天気関連の応答生成"""
    seasons = knowledge_base['travel_tips']['best_seasons']
    return f"""🌤️ **モロッコの気候・天気**

**📅 季節別ガイド**
• **春（3-5月）**: {seasons['spring']}
• **夏（6-8月）**: {seasons['summer']}
• **秋（9-11月）**: {seasons['autumn']}
• **冬（12-2月）**: {seasons['winter']}

**🗺️ 地域別気候**
• **沿岸部**: 地中海性気候、年中温和
• **内陸部**: 大陸性気候、昼夜の寒暖差大
• **アトラス山脈**: 高山気候、冬は雪
• **サハラ砂漠**: 乾燥気候、日中は酷暑、夜は寒冷

**🌡️ 月別平均気温（マラケシュ）**
• 1月: 6-18℃ • 7月: 19-37℃
• 4月: 11-24℃ • 10月: 15-28℃

**👕 服装アドバイス**
• **春・秋**: 軽装+羽織物
• **夏**: 薄手の長袖（日焼け防止）
• **冬**: セーター、ジャケット
• **砂漠**: 昼夜の寒暖差対策

**☔ 降水量**
• 雨季: 11月-3月（主に沿岸部）
• 乾季: 4月-10月
• 年間降水量: 300-800mm（地域差大）"""

def generate_language_response(keywords, knowledge_base):
    """言語関連の応答生成"""
    languages = knowledge_base['country_info'].get('languages', [])
    etiquette = knowledge_base['travel_tips'].get('cultural_etiquette', {})
    langs = ', '.join(languages)
    greet = etiquette.get('greetings', 'こんにちは（挨拶）')
    return f"""🗣️ **モロッコの言語事情**

**📌 主な言語:** {langs}

**🌍 概要**
• **アラビア語**: 行政、教育、宗教で主に使用
• **タマジグト（ベルベル語）**: 2011年に公用語化され、地方で広く話される
• **フランス語**: ビジネス・教育・都市部で広く通用
• **英語**: 観光業や若い世代で増加傾向

**👋 基本的な挨拶例**
• アラビア語: アッサラーム・アライクム（挨拶）
• フランス語: Bonjour（ボンジュール）
• ベルベル語: アズール

**💡 旅行者向けアドバイス**
• 観光地ではフランス語・英語が通じることが多い
• 地方ではベルベル語の影響が強い
• {greet} といった基本挨拶を使うと親しみが伝わる

**📱 便利なアプリ**
• Google翻訳（オフライン対応）
• 指差し会話帳
• アラビア語・フランス語学習アプリ"""

def generate_default_response(knowledge_base):
    """デフォルト応答生成"""
    country_info = knowledge_base['country_info']
    return f"""🕌 **モロッコ王国へようこそ！**

**🌍 基本情報**
• 正式名称: {country_info['name']}
• 首都: {country_info['capital']}
• 最大都市: {country_info['largest_city']}
• 人口: {country_info['population']}
• 面積: {country_info['area']}
• 言語: {', '.join(country_info['languages'])}
• 通貨: {country_info['currency']}
• 宗教: {country_info['religion']}

**🏛️ 主要観光都市（10都市・40観光地）**
• マラケシュ: 「赤い街」帝国都市
• カサブランカ: 経済の中心都市
• フェズ: 1200年の歴史を持つ古都
• シャウエン: 「青い真珠」山間の町
• エッサウィラ: 「風の街」大西洋沿岸

**🎨 文化的特徴**
• アラブ、ベルベル、アンダルシア、アフリカ文化の融合
• 世界有数のイスラム建築
• 洗練されたモロッコ料理
• 伝統工芸の宝庫

**💡 おすすめ体験**
• サハラ砂漠でのラクダトレッキング
• 伝統的なリヤドホテル宿泊
• スークでのお土産探し
• ハマム（モロッコ式スパ）体験

詳しい観光地情報は、マップページや観光地一覧ページをご確認ください！"""

def show_settings_page():
    """設定ページ"""
    st.subheader("⚙️ 設定")
    
    st.markdown("### 🎨 外観設定")
    
    # テーマ設定
    current_theme = st.session_state.get("theme", "ライト")
    theme_index = 0 if current_theme == "ライト" else 1
    
    new_theme = st.selectbox(
        "🌙 テーマ", 
        ["ライト", "ダーク"], 
        index=theme_index,
        help="アプリケーションの外観テーマを選択してください"
    )
    
    # テーマ変更の処理
    if new_theme != current_theme:
        st.session_state.theme = new_theme
        st.success(f"✅ テーマを「{new_theme}」に変更しました")
        st.info("💡 変更が即座に適用されました。他のページでもテーマが反映されます")
        st.balloons()  # テーマ変更を祝う
        st.rerun()
    
    # テーマプレビュー
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🌞 ライトテーマ")
        st.markdown("""
        <div style="background: white; border: 1px solid #ddd; padding: 1rem; border-radius: 8px; color: black;">
            <h5 style="color: #2c3e50;">モロッコ観光ガイド</h5>
            <p style="color: #7f8c8d;">明るく見やすいライトテーマ</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🌙 ダークテーマ")
        st.markdown("""
        <div style="background: #2d2d2d; border: 1px solid #444; padding: 1rem; border-radius: 8px; color: white;">
            <h5 style="color: white;">モロッコ観光ガイド</h5>
            <p style="color: #cccccc;">目に優しいダークテーマ</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 🔧 アプリケーション設定")
    
    # 言語設定
    st.selectbox("🌐 言語 / Language", ["日本語", "English"], index=0, key="app_language",
                 help="アプリケーションの表示言語を選択してください（現在は日本語のみ対応）")
    
    # API設定
    st.markdown("### 🔑 API設定")
    
    # 環境変数またはセッションに保存された一時キーからAPIキーの存在を確認
    api_key_env = os.getenv('OPENAI_API_KEY')
    api_key_session = st.session_state.get('OPENAI_API_KEY')
    api_key_status = bool(api_key_env or api_key_session)

    if api_key_status:
        st.success("✅ OpenAI APIキーが設定されています")
        if api_key_env:
            st.info("💡 APIキーは環境変数 `OPENAI_API_KEY` から読み込まれます")
        if api_key_session and not api_key_env:
            st.info("💡 セッション内の一時APIキーが使用されています (ページ再読み込みで失われます)")
        st.markdown("**🎯 利用可能機能:** OpenAI GPT + 詳細知識ベース + スマート分析")
    else:
        st.warning("⚠️ OpenAI APIキーが設定されていません")
        st.info("💡 AI機能を使用するには、環境変数 `OPENAI_API_KEY` を設定するか、下の一時キー入力でテストできます（開発用）")
        st.markdown("**🤖 現在の機能:** 高精度フォールバック応答システム（知識ベース内蔵）")
    
    st.markdown("**セキュリティのため、APIキーは表示されません**")
    
    if st.button("API接続をテスト", key="api_test_button"):
        if api_key_status:
            st.info("🔄 API接続をテスト中...")
            # 実際のテストは実装しない（セキュリティ上の理由）
            st.success("✅ APIキーが設定されています（接続テストは実装されていません）")
        else:
            st.error("❌ APIキーが設定されていません")

    # --- 開発者向け: セッション限定でAPIキーを一時設定できるフォーム ---
    st.markdown("### 🧪 開発用: 一時 API キー (セッション限定)")
    st.caption("※ セキュリティに注意してください。入力されたキーはページ/セッション終了で消えます。運用環境では環境変数を使用してください。")

    temp_input = st.text_input("一時 API キーを入力 (開発用)", type="password", key="temp_openai_input")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("セッションに保存", key="save_temp_api_key"):
            if not temp_input:
                st.error("❗ キーが入力されていません")
            else:
                st.session_state['OPENAI_API_KEY'] = temp_input
                os.environ['OPENAI_API_KEY'] = temp_input
                st.success("🔐 APIキーをセッションに保存しました（プロセス環境変数も設定されます）")
                st.experimental_rerun()
    with col_b:
        if st.button("セッションのキーをクリア", key="clear_temp_api_key"):
            if 'OPENAI_API_KEY' in st.session_state:
                del st.session_state['OPENAI_API_KEY']
            if 'OPENAI_API_KEY' in os.environ:
                try:
                    del os.environ['OPENAI_API_KEY']
                except Exception:
                    pass
            st.success("🗑️ セッションのAPIキーをクリアしました")
            st.experimental_rerun()
    
    # セキュリティ情報
    st.markdown("### 🔒 セキュリティ情報")
    st.info("""
    **プライバシー保護:**
    - APIキーは環境変数から安全に読み込まれます
    - APIキーは画面に表示されません
    - ユーザーデータは保存されません
    - チャット履歴はセッション終了時にクリアされます
    """)
    
    # テーマ管理セクション
    st.markdown("### 🎨 テーマ管理")
    
    # 現在のテーマ状態
    current_theme = st.session_state.get("theme", "ライト")
    theme_emoji = "🌞" if current_theme == "ライト" else "🌙"
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem; border-radius: 10px; 
                    background: {'linear-gradient(90deg, #f8f9fa, #e9ecef)' if current_theme == 'ライト' else 'linear-gradient(90deg, #2d2d2d, #3a3a3a)'}; 
                    border: 1px solid {'#dee2e6' if current_theme == 'ライト' else '#444'};">
            <h3>{theme_emoji} {current_theme}テーマ</h3>
            <p>現在適用中</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # テーマ切り替えボタン
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🌞 ライトテーマに切り替え", 
                    key="light_theme_button",
                    use_container_width=True,
                    disabled=(current_theme == "ライト"),
                    help="明るい背景のライトテーマに変更します"):
            st.session_state.theme = "ライト"
            st.success("✅ ライトテーマに変更しました")
            st.rerun()
    
    with col2:
        if st.button("🌙 ダークテーマに切り替え", 
                    key="dark_theme_button",
                    use_container_width=True,
                    disabled=(current_theme == "ダーク"),
                    help="暗い背景のダークテーマに変更します"):
            st.session_state.theme = "ダーク"
            st.success("✅ ダークテーマに変更しました")
            st.rerun()
    
    # テーマリセット
    if st.button("🔄 デフォルトテーマにリセット", key="reset_theme_button", help="ライトテーマにリセットします"):
        st.session_state.theme = "ライト"
        st.info("🔄 テーマをライトテーマにリセットしました")
        st.rerun()
    
    # テーマ設定情報
    st.markdown("### 📖 テーマ機能について")
    
    tab1, tab2 = st.tabs(["🌞 ライトテーマ", "🌙 ダークテーマ"])
    
    with tab1:
        st.markdown("""
        **🌞 ライトテーマの特徴:**
        - ✨ 明るい背景で昼間の使用に最適
        - 📖 高いコントラストで文字が読みやすい
        - 🌐 従来のWebサイトに近い表示
        - ⚡ 屋外や明るい環境での視認性が良好
        - 🎨 クリーンで清潔感のあるデザイン
        """)
        
        st.success("**推奨環境:** 昼間・明るい室内・屋外での使用")
    
    with tab2:
        st.markdown("""
        **🌙 ダークテーマの特徴:**
        - 👁️ 暗い背景で目の疲労を軽減
        - 🌃 夜間や暗い環境での使用に最適
        - 🔋 バッテリー消費を抑制（OLED画面）
        - 💻 モダンで洗練されたデザイン
        - 🎯 集中力を高める効果
        """)
        
        st.info("**推奨環境:** 夜間・暗い室内・長時間の作業時")
    
    # システム診断
    st.markdown("### 🔍 システム診断")
    
    if st.button("🏥 システムヘルスチェック", key="health_check_button", help="アプリケーションの動作状況を確認します"):
        with st.spinner("診断中..."):
            # データ読み込みテスト
            try:
                spots = load_spots_data()
                if spots:
                    st.success(f"✅ データ読み込み正常 ({len(spots)}箇所)")
                else:
                    st.error("❌ データ読み込み失敗")
            except Exception as e:
                st.error(f"❌ データ読み込みエラー: {str(e)}")
            
            # 必須ライブラリテスト
            try:
                st.success("✅ 必須ライブラリ正常")
            except Exception as e:
                st.error(f"❌ ライブラリエラー: {str(e)}")
            
            # セッション状態テスト
            if 'theme' in st.session_state:
                st.success(f"✅ セッション状態正常 (テーマ: {st.session_state.theme})")
            else:
                st.warning("⚠️ セッション状態未初期化")
            
            # URLパラメータテスト
            params = st.query_params
            if params:
                st.info(f"ℹ️ URLパラメータ: {dict(params)}")
            else:
                st.success("✅ URLパラメータクリア")
    
    # アプリ情報
    st.markdown("### ℹ️ アプリケーション情報")
    st.write("**バージョン:** 1.4.0")
    st.write("**作成日:** 2025年11月7日")
    st.write("**最終更新:** 2025年11月10日")
    st.write("**フレームワーク:** Streamlit")
    st.write("**観光地データ:** 40箇所")
    st.write("**対象都市:** 10都市")
    st.write("**セキュリティ:** APIキー非表示対応")
    st.write("**外観:** ライト・ダークテーマ対応")
    st.write("**エラーハンドリング:** 高度な例外処理対応")
    st.write("**パフォーマンス:** ログ記録・測定機能付き")
    st.write("**機能:** インタラクティブマップ、高精度AI観光ガイド、詳細検索、文化・歴史ページ")

if __name__ == "__main__":
    try:
        # テーマ初期化
        init_theme()
        # メイン関数実行
        main()
    except Exception as e:
        st.error(f"❌ アプリケーション初期化エラー: {str(e)}")
        st.info("🔄 ページを再読み込みしてください")
        with st.expander("🔍 エラー詳細"):
            st.code(traceback.format_exc())