"""
モロッコ観光ガイド - Streamlit版
Morocco Tourism Guide App powered by Streamlit
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# ページ設定
st.set_page_config(
    page_title="モロッコ観光ガイド",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# カスタムCSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #e74c3c, #c0392b);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .spot-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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
</style>
""", unsafe_allow_html=True)

# 観光地データ
@st.cache_data
def load_spots_data():
    """観光地データを読み込み"""
    spots = [
        # マラケシュの観光地（12箇所）
        {
            'id': 1,
            'name': 'ジャマ・エル・フナ広場',
            'city': 'マラケシュ',
            'category': '広場・市場',
            'description': 'マラケシュの心臓部に位置する世界遺産の広場。日中は屋台や土産物店が並び、夜になると大道芸人やミュージシャンが集まり賑やかな雰囲気を楽しめます。',
            'verified': True,
            'lat': 31.625964,
            'lng': -7.989250
        },
        {
            'id': 2,
            'name': 'クトゥビア・モスク',
            'city': 'マラケシュ',
            'category': '宗教建築',
            'description': 'マラケシュのシンボルとして親しまれる12世紀建造のモスク。高さ77メートルのミナレットは街のどこからでも見える。',
            'verified': True,
            'lat': 31.624307,
            'lng': -7.993252
        },
        {
            'id': 3,
            'name': 'バイア宮殿',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'description': '19世紀末に建てられた豪華な宮殿。美しいタイル装飾とアンダルシア様式の庭園が見どころ。',
            'verified': True,
            'lat': 31.620947,
            'lng': -7.982908
        },
        {
            'id': 4,
            'name': 'マジョレル庭園',
            'city': 'マラケシュ',
            'category': '庭園',
            'description': 'フランス人画家ジャック・マジョレルが造成した美しい植物園。後にイヴ・サンローランが所有し、現在は博物館も併設。',
            'verified': True,
            'lat': 31.641214,
            'lng': -8.003674
        },
        {
            'id': 5,
            'name': 'サーディアン朝の墳墓群',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'description': '16世紀のサーディアン朝の王族が眠る墳墓群。精巧なイスラム装飾が施された霊廟が見どころ。',
            'verified': True,
            'lat': 31.621439,
            'lng': -7.984467
        },
        # カサブランカの観光地（8箇所）
        {
            'id': 6,
            'name': 'ハッサン2世モスク',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'description': '世界で3番目に大きなモスク。高さ210メートルのミナレットを持ち、海に面した美しい立地が特徴的。',
            'verified': True,
            'lat': 33.608311,
            'lng': -7.632815
        },
        {
            'id': 7,
            'name': 'リック・カフェ',
            'city': 'カサブランカ',
            'category': '文化施設',
            'description': '映画「カサブランカ」をモチーフにしたレストラン・カフェ。1940年代の雰囲気を再現した内装が人気。',
            'verified': True,
            'lat': 33.594629,
            'lng': -7.619054
        },
        # フェズの観光地（5箇所）
        {
            'id': 8,
            'name': 'フェズ・エル・バリ',
            'city': 'フェズ',
            'category': '都市・建築',
            'description': '世界最大の歩行者専用都市として知られる旧市街。迷路のような路地に伝統的な建物や工房が密集。',
            'verified': True,
            'lat': 34.063611,
            'lng': -4.972222
        },
        {
            'id': 9,
            'name': 'カラウィーン大学',
            'city': 'フェズ',
            'category': '歴史建築',
            'description': '859年に創設された世界最古の大学の一つ。現在も宗教教育機関として機能している。',
            'verified': True,
            'lat': 34.064444,
            'lng': -4.974167
        },
        # メルズーガの観光地（3箇所）
        {
            'id': 10,
            'name': 'エルグ・シェビ砂丘',
            'city': 'メルズーガ',
            'category': '自然',
            'description': 'サハラ砂漠の美しい砂丘群。ラクダトレッキングや砂漠キャンプの拠点として人気。',
            'verified': True,
            'lat': 31.099167,
            'lng': -4.010556
        },
        # シャウエンの観光地（3箇所）
        {
            'id': 11,
            'name': 'シャウエン旧市街',
            'city': 'シャウエン',
            'category': '都市・建築',
            'description': '青い街として有名な山間の美しい町。建物の壁が青く塗られた独特の景観が魅力。',
            'verified': True,
            'lat': 35.168889,
            'lng': -5.268333
        },
        # エッサウィラの観光地（4箇所）
        {
            'id': 12,
            'name': 'エッサウィラ・メディナ',
            'city': 'エッサウィラ',
            'category': '都市・建築',
            'description': '大西洋に面した要塞都市の旧市街。ポルトガル植民地時代の建築が残る美しい港町。',
            'verified': True,
            'lat': 31.513056,
            'lng': -9.769444
        }
    ]
    
    return spots

def init_ai_service():
    """AI機能の初期化（簡易版）"""
    return {
        'available': bool(os.getenv('OPENAI_API_KEY')),
        'fallback_responses': {
            'マラケシュ': 'マラケシュは「赤い街」として知られ、ジャマ・エル・フナ広場やクトゥビア・モスクなどの見どころがあります。',
            'カサブランカ': 'カサブランカはモロッコ最大の都市で、ハッサン2世モスクが有名です。',
            'フェズ': 'フェズは古都として知られ、世界最大の歩行者専用都市フェズ・エル・バリがあります。',
            'メルズーガ': 'メルズーガはサハラ砂漠の玄関口で、エルグ・シェビ砂丘でのラクダトレッキングが人気です。',
            'シャウエン': 'シャウエンは「青い街」として有名で、美しい山間の町です。',
            'エッサウィラ': 'エッサウィラは大西洋に面した港町で、風光明媚な要塞都市です。'
        }
    }

def main():
    """メインアプリケーション"""
    
    # ヘッダー
    st.markdown("""
    <div class="main-header">
        <h1>🕌 モロッコ観光ガイド</h1>
        <p>Morocco Tourism Guide - あなたの完璧なモロッコ旅行をサポート</p>
    </div>
    """, unsafe_allow_html=True)
    
    # サイドバー
    st.sidebar.title("🧭 ナビゲーション")
    page = st.sidebar.selectbox(
        "ページを選択",
        ["🏠 ホーム", "🗺️ マップ", "📍 観光地一覧", "🤖 AI観光ガイド", "⚙️ 設定"]
    )
    
    # データ読み込み
    spots = load_spots_data()
    ai_service = init_ai_service()
    
    if page == "🏠 ホーム":
        show_home_page(spots)
    elif page == "🗺️ マップ":
        show_map_page(spots)
    elif page == "📍 観光地一覧":
        show_spots_page(spots)
    elif page == "🤖 AI観光ガイド":
        show_ai_page(ai_service)
    elif page == "⚙️ 設定":
        show_settings_page()

def show_home_page(spots):
    """ホームページ"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📍 観光地数", len(spots))
    
    with col2:
        cities = set(spot['city'] for spot in spots)
        st.metric("🏙️ 都市数", len(cities))
    
    with col3:
        verified_count = sum(1 for spot in spots if spot.get('verified', False))
        st.metric("✅ 認定スポット", verified_count)
    
    st.markdown("---")
    
    # おすすめ観光地
    st.subheader("🌟 おすすめ観光地")
    
    recommended_spots = [spot for spot in spots if spot.get('verified', False)][:6]
    
    cols = st.columns(2)
    for i, spot in enumerate(recommended_spots):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="spot-card">
                    <div class="spot-title">{spot['name']}</div>
                    <div class="spot-meta">
                        📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                        {' • <span class="verified-badge">認定済み</span>' if spot.get('verified') else ''}
                    </div>
                    <p>{spot['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)

def show_map_page(spots):
    """マップページ"""
    st.subheader("🗺️ モロッコ観光地マップ")
    
    # フィルター
    col1, col2 = st.columns(2)
    
    with col1:
        cities = ["すべて"] + sorted(set(spot['city'] for spot in spots))
        selected_city = st.selectbox("都市で絞り込み", cities)
    
    with col2:
        categories = ["すべて"] + sorted(set(spot['category'] for spot in spots))
        selected_category = st.selectbox("カテゴリで絞り込み", categories)
    
    # フィルタリング
    filtered_spots = spots
    if selected_city != "すべて":
        filtered_spots = [spot for spot in filtered_spots if spot['city'] == selected_city]
    if selected_category != "すべて":
        filtered_spots = [spot for spot in filtered_spots if spot['category'] == selected_category]
    
    # マップ作成
    if filtered_spots:
        # マップの中心を計算
        center_lat = sum(spot['lat'] for spot in filtered_spots) / len(filtered_spots)
        center_lng = sum(spot['lng'] for spot in filtered_spots) / len(filtered_spots)
        
        m = folium.Map(
            location=[center_lat, center_lng], 
            zoom_start=6,
            tiles="OpenStreetMap"
        )
        
        # マーカーを追加
        for spot in filtered_spots:
            popup_html = f"""
            <div style="width: 250px;">
                <h4>{spot['name']}</h4>
                <p><b>📍 {spot['city']}</b></p>
                <p><b>🏷️ {spot['category']}</b></p>
                {'<p><span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">✅ 認定済み</span></p>' if spot.get('verified') else ''}
                <p>{spot['description'][:100]}...</p>
            </div>
            """
            
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
        map_data = st_folium(m, width=700, height=500)
        
        # 観光地リスト
        st.subheader(f"📍 観光地一覧 ({len(filtered_spots)}件)")
        
        for spot in filtered_spots:
            with st.expander(f"{spot['name']} - {spot['city']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(spot['description'])
                with col2:
                    st.write(f"**カテゴリ:** {spot['category']}")
                    if spot.get('verified'):
                        st.success("✅ 認定済み")
    else:
        st.warning("選択した条件に一致する観光地がありません。")

def show_spots_page(spots):
    """観光地一覧ページ"""
    st.subheader("📍 観光地一覧")
    
    # 検索機能
    search_term = st.text_input("🔍 観光地を検索", placeholder="名前や都市名で検索...")
    
    # フィルター
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cities = ["すべて"] + sorted(set(spot['city'] for spot in spots))
        selected_city = st.selectbox("都市", cities)
    
    with col2:
        categories = ["すべて"] + sorted(set(spot['category'] for spot in spots))
        selected_category = st.selectbox("カテゴリ", categories)
    
    with col3:
        show_verified_only = st.checkbox("認定済みのみ表示")
    
    # フィルタリング
    filtered_spots = spots
    
    if search_term:
        filtered_spots = [
            spot for spot in filtered_spots 
            if search_term.lower() in spot['name'].lower() or 
               search_term.lower() in spot['city'].lower()
        ]
    
    if selected_city != "すべて":
        filtered_spots = [spot for spot in filtered_spots if spot['city'] == selected_city]
    
    if selected_category != "すべて":
        filtered_spots = [spot for spot in filtered_spots if spot['category'] == selected_category]
    
    if show_verified_only:
        filtered_spots = [spot for spot in filtered_spots if spot.get('verified', False)]
    
    # 結果表示
    st.write(f"**{len(filtered_spots)}件** の観光地が見つかりました")
    
    # 観光地カード表示
    cols = st.columns(2)
    for i, spot in enumerate(filtered_spots):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="spot-card">
                    <div class="spot-title">{spot['name']}</div>
                    <div class="spot-meta">
                        📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                        {' • <span class="verified-badge">認定済み</span>' if spot.get('verified') else ''}
                    </div>
                    <p>{spot['description']}</p>
                    <p><small>座標: {spot['lat']:.4f}, {spot['lng']:.4f}</small></p>
                </div>
                """, unsafe_allow_html=True)

def show_ai_page(ai_service):
    """AI観光ガイドページ"""
    st.subheader("🤖 AI観光ガイド")
    
    if not ai_service['available']:
        st.warning("⚠️ OpenAI APIキーが設定されていません。フォールバック応答を使用します。")
    
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
    
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                response = get_ai_response(suggestion, ai_service)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()
    
    # ユーザー入力
    if prompt := st.chat_input("モロッコについて何でも聞いてください！"):
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
    """AI応答を生成（フォールバック対応）"""
    if ai_service['available']:
        try:
            # 実際のOpenAI APIを使用する場合はここに実装
            # 現在はフォールバック応答を使用
            pass
        except:
            pass
    
    # フォールバック応答
    prompt_lower = prompt.lower()
    for city, response in ai_service['fallback_responses'].items():
        if city.lower() in prompt_lower:
            return f"🕌 {response}\n\n詳しい情報については、マップや観光地一覧ページをご確認ください。"
    
    return """🕌 モロッコについてのご質問ありがとうございます！

モロッコは北アフリカに位置する魅力的な国で、以下のような特徴があります：

🏛️ **主要都市**
- マラケシュ：「赤い街」として知られる歴史都市
- カサブランカ：モロッコ最大の経済都市
- フェズ：古都として知られる文化都市
- シャウエン：「青い街」で有名な山間の町

🍽️ **グルメ**
- タジン料理：蓋付き土鍋で作る伝統料理
- クスクス：金曜日の家庭料理
- ミントティー：モロッコの国民的飲み物

🎨 **文化**
- ベルベル文化とアラブ文化の融合
- 美しいイスラム建築
- 伝統的な手工芸品

具体的な観光地については、マップページや観光地一覧ページで詳しい情報をご覧いただけます！"""

def show_settings_page():
    """設定ページ"""
    st.subheader("⚙️ 設定")
    
    st.markdown("### 🔧 アプリケーション設定")
    
    # 言語設定
    language = st.selectbox("言語 / Language", ["日本語", "English"], index=0)
    
    # テーマ設定
    theme = st.selectbox("テーマ", ["ライト", "ダーク"], index=0)
    
    # API設定
    st.markdown("### 🔑 API設定")
    api_key = st.text_input("OpenAI APIキー", type="password", help="AI機能を使用するにはAPIキーが必要です")
    
    if st.button("設定を保存"):
        st.success("設定が保存されました！")
    
    # アプリ情報
    st.markdown("### ℹ️ アプリケーション情報")
    st.write("**バージョン:** 1.0.0")
    st.write("**作成日:** 2025年11月7日")
    st.write("**フレームワーク:** Streamlit")
    st.write("**観光地データ:** 12箇所")

if __name__ == "__main__":
    main()