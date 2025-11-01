#!/usr/bin/env python3
"""
Morocco Travel App - Streamlit版
Streamlit Cloud用メインファイル
"""

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# ページ設定
st.set_page_config(
    page_title="🇲🇦 Morocco Travel Guide",
    page_icon="🇲🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# OpenAI設定
api_key = os.getenv('VITE_OPENAI_API_KEY') or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

def main():
    """メインアプリケーション"""
    
    # ヘッダー
    st.title("🇲🇦 Morocco Travel Guide")
    st.markdown("**AI-powered travel assistant for Morocco**")
    
    # サイドバー
    with st.sidebar:
        st.header("🗺️ Navigation")
        page = st.selectbox(
            "Choose a section:",
            ["🏠 Home", "🤖 AI Guide", "🔤 Translator", "📖 Travel Guides", "🗺️ Map Info"]
        )
    
    # メインコンテンツ
    if page == "🏠 Home":
        show_home()
    elif page == "🤖 AI Guide":
        show_ai_guide()
    elif page == "🔤 Translator":
        show_translator()
    elif page == "📖 Travel Guides":
        show_guides()
    elif page == "🗺️ Map Info":
        show_map_info()

def show_home():
    """ホームページ"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Welcome to Morocco! 🇲🇦")
        st.write("""
        Discover the beauty and culture of Morocco with our AI-powered travel guide.
        
        **Features:**
        - 🤖 AI Travel Assistant
        - 🔤 Multi-language Translator  
        - 📖 Comprehensive Travel Guides
        - 🗺️ Interactive Maps
        - 🎵 Speech Synthesis
        """)
    
    with col2:
        st.image("https://images.unsplash.com/photo-1539650116574-75c0c6d73d0e?w=500", 
                 caption="Beautiful Morocco")

def show_ai_guide():
    """AIガイド"""
    st.header("🤖 AI Travel Assistant")
    
    if not client:
        st.error("❌ OpenAI API key not found. Please set OPENAI_API_KEY in secrets.")
        return
    
    # チャット履歴
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "こんにちは！モロッコ旅行についてお手伝いします。何をお聞きになりたいですか？ 🇲🇦"}
        ]
    
    # チャット表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # ユーザー入力
    if prompt := st.chat_input("モロッコについて質問してください..."):
        # ユーザーメッセージを追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # AI応答を生成
        with st.chat_message("assistant"):
            with st.spinner("回答を生成中..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": """あなたはモロッコ旅行の専門ガイドです。
                            モロッコの観光地、文化、歴史、料理、言語、習慣について詳しく日本語で回答してください。
                            親しみやすく実用的な情報を提供し、安全な旅行のためのアドバイスも含めてください。"""},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500,
                        temperature=0.7
                    )
                    
                    ai_response = response.choices[0].message.content
                    st.write(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    st.error(f"エラーが発生しました: {str(e)}")

def show_translator():
    """翻訳機能"""
    st.header("🔤 Multi-language Translator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("From")
        source_lang = st.selectbox("Source Language", 
                                  ["Japanese", "English", "French", "Arabic"], key="source")
        source_text = st.text_area("Enter text to translate:", height=150)
    
    with col2:
        st.subheader("To")
        target_lang = st.selectbox("Target Language", 
                                  ["Arabic", "French", "English", "Japanese"], key="target")
        
        if st.button("🔄 Translate"):
            if source_text:
                # 簡単な翻訳辞書（実際にはGoogle Translate APIなどを使用）
                translations = {
                    "hello": {"Arabic": "مرحبا", "French": "bonjour", "Japanese": "こんにちは"},
                    "thank you": {"Arabic": "شكراً لك", "French": "merci", "Japanese": "ありがとう"},
                    "welcome to morocco": {"Arabic": "مرحباً بكم في المغرب", "French": "bienvenue au maroc", "Japanese": "モロッコへようこそ"}
                }
                
                translated = translations.get(source_text.lower(), {}).get(target_lang, f"[Translation: {source_text}]")
                st.text_area("Translation:", value=translated, height=150)
            else:
                st.warning("Please enter text to translate.")
    
    # よく使うフレーズ
    st.subheader("📝 Common Phrases")
    phrases = [
        {"en": "Hello", "ar": "مرحبا", "fr": "Bonjour", "ja": "こんにちは"},
        {"en": "Thank you", "ar": "شكراً لك", "fr": "Merci", "ja": "ありがとう"},
        {"en": "Welcome to Morocco", "ar": "مرحباً بكم في المغرب", "fr": "Bienvenue au Maroc", "ja": "モロッコへようこそ"},
        {"en": "How much?", "ar": "كم الثمن؟", "fr": "Combien ça coûte?", "ja": "いくらですか？"},
        {"en": "Where is...?", "ar": "أين...؟", "fr": "Où est...?", "ja": "...はどこですか？"},
    ]
    
    for phrase in phrases:
        col1, col2, col3, col4 = st.columns(4)
        col1.write(f"🇺🇸 {phrase['en']}")
        col2.write(f"🇲🇦 {phrase['ar']}")
        col3.write(f"🇫🇷 {phrase['fr']}")
        col4.write(f"🇯🇵 {phrase['ja']}")

def show_guides():
    """旅行ガイド"""
    st.header("📖 Morocco Travel Guides")
    
    # タブで分類
    tab1, tab2, tab3, tab4 = st.tabs(["🏛️ Cities", "🍽️ Cuisine", "🎭 Culture", "🏔️ Nature"])
    
    with tab1:
        st.subheader("Major Cities")
        
        cities = [
            {
                "name": "Marrakech",
                "description": "The Red City - Famous for its bustling souks and historic medina",
                "highlights": ["Jemaa el-Fnaa Square", "Koutoubia Mosque", "Majorelle Garden"]
            },
            {
                "name": "Casablanca", 
                "description": "Economic capital with modern architecture and Atlantic coastline",
                "highlights": ["Hassan II Mosque", "Corniche", "Art Deco Architecture"]
            },
            {
                "name": "Fez",
                "description": "Cultural capital known for its medieval medina and traditional crafts",
                "highlights": ["Fez el-Bali", "Al Quaraouiyine University", "Tanneries"]
            }
        ]
        
        for city in cities:
            with st.expander(f"🏛️ {city['name']}"):
                st.write(city['description'])
                st.write("**Must-see attractions:**")
                for highlight in city['highlights']:
                    st.write(f"• {highlight}")
    
    with tab2:
        st.subheader("Moroccan Cuisine")
        st.write("Discover the rich flavors of Moroccan cooking...")
        
        dishes = ["Tagine", "Couscous", "Pastilla", "Harira", "Mint Tea"]
        for dish in dishes:
            st.write(f"🍽️ **{dish}**")
    
    with tab3:
        st.subheader("Culture & Traditions")
        st.write("Learn about Moroccan customs and traditions...")
    
    with tab4:
        st.subheader("Natural Wonders")
        st.write("Explore Morocco's diverse landscapes...")

def show_map_info():
    """地図情報"""
    st.header("🗺️ Interactive Map Information")
    st.write("Map integration would go here...")
    
    # 簡単な地域情報
    regions = {
        "Marrakech-Safi": "Home to the imperial city of Marrakech",
        "Casablanca-Settat": "Economic hub of Morocco", 
        "Fez-Meknes": "Cultural and historical center",
        "Rabat-Sale-Kenitra": "Capital region"
    }
    
    selected_region = st.selectbox("Select a region:", list(regions.keys()))
    st.info(regions[selected_region])

if __name__ == "__main__":
    main()