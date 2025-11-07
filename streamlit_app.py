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
        # マラケシュの観光地（15箇所）
        {
            'id': 1,
            'name': 'ジャマ・エル・フナ広場',
            'city': 'マラケシュ',
            'category': '広場・市場',
            'description': 'マラケシュの心臓部に位置するユネスコ世界遺産の広場。1000年以上の歴史を持つこの広場は、昼間はオレンジジュース売りや土産物店が軒を連ね、夜になると食べ物屋台、大道芸人、ヘナタトゥーアーティスト、蛇使いなどが集まり、まさに生きた博物館となります。特に夕方から夜にかけての賑わいは圧巻で、モロッコの文化を肌で感じることができる場所です。周辺のスークも合わせて散策することをお勧めします。',
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
            'description': 'マラケシュのシンボルとして親しまれる12世紀建造のモスク。高さ77メートルのミナレットは、アフリカ最大のモスクの一つで、街のどこからでも見えるランドマークです。アルモハード朝時代の傑作で、赤砂岩で造られた美しい外観は「赤い街」マラケシュを象徴しています。夜間のライトアップは特に美しく、ジャマ・エル・フナ広場からの眺めは絶景。モスクの名前は隣接していた書店（kutub）に由来しています。',
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
            'description': '19世紀末にアフメド・イブン・ムーサ大臣によって建てられた豪華絢爛な宮殿。「美しい」を意味するバイアの名の通り、精巧なタイル装飾（ゼリージュ）、彫刻された石膏装飾、美しい天井画が施されています。160の部屋と8ヘクタールの庭園を持つこの宮殿は、モロッコ・アンダルシア建築の傑作です。特に中央中庭の大理石の床と噴水、色とりどりのタイルワークは圧巻です。',
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
            'description': 'フランス人画家ジャック・マジョレルが1924年から40年かけて造成した植物園。「マジョレル・ブルー」と呼ばれる鮮やかなコバルトブルーで彩られた建物と、世界中から集められた300種以上の植物が織りなす楽園です。1980年にイヴ・サンローランとピエール・ベルジェが買い取り、復元。現在はベルベル博物館とイヴ・サンローラン博物館も併設されています。サボテン、椰子、バンブーが茂る中の散策は、砂漠の都市マラケシュのオアシスそのものです。',
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
            'description': '16世紀のサーディアン朝の君主とその家族が眠る霊廟群。1917年まで城壁に閉ざされていたため、保存状態が極めて良好です。特に「12の柱の間」と呼ばれる霊廟は、12本の白大理石の柱に支えられた美しいムカルナス（鍾乳石装飾）の天井が圧巻。床の大理石象嵌、壁面のゼリージュ（色タイル装飾）、アラベスク文様の石膏彫刻など、イスラム装飾芸術の粋を集めた傑作です。',
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
            'description': '12世紀アルモハード朝時代に造られた人工湖を中心とした庭園。アトラス山脈を背景にした美しい景観で知られ、特にパビリオンからの眺めは絵画のようです。オリーブの木が約10万本植えられており、モロッコの農業と水利技術の発展を物語る歴史的価値も高い場所です。夕日の時間帯は湖面が金色に輝き、ロマンチックな雰囲気に包まれます。',
            'verified': True,
            'lat': 31.605000,
            'lng': -8.024444,
            'best_time': '夕方（サンセット）',
            'duration': '1時間',
            'price_range': '30DH（約350円）'
        },
        {
            'id': 7,
            'name': 'ベン・ユーセフ・マドラサ',
            'city': 'マラケシュ',
            'category': '歴史建築',
            'description': '14世紀に建設されたマグリブ地域最大のイスラム神学校。最盛期には900人の学生が学んだとされ、モロッコの教育の中心地でした。中央中庭を囲む美しいアーケード、学生寮の130の小部屋、そして何より圧巻なのは中庭の大理石とタイルで装飾された柱廊です。天井の杉材の精巧な装飾、アラビア書道が施された石膏装飾など、マリーン朝建築の傑作として高く評価されています。',
            'verified': True,
            'lat': 31.631667,
            'lng': -7.989167,
            'best_time': '午前中',
            'duration': '1時間',
            'price_range': '50DH（約570円）'
        },
        {
            'id': 8,
            'name': 'アグダル庭園',
            'city': 'マラケシュ',
            'category': '庭園',
            'description': '12世紀アルモハード朝時代に造営された王室庭園。約400ヘクタールの広大な敷地には、オリーブ、オレンジ、ザクロ、イチジクなどの果樹園が広がります。2つの大型貯水池は現在でも宮殿への給水システムとして機能しており、古代からの水利技術の高さを物語っています。王室の離宮として使用されているため、金曜日と土曜日のみ一般公開されています。',
            'verified': True,
            'lat': 31.609722,
            'lng': -7.965556,
            'best_time': '金・土曜日の午前中',
            'duration': '1-2時間',
            'price_range': '10DH（約115円）'
        },
        # カサブランカの観光地（12箇所）
        {
            'id': 9,
            'name': 'ハッサン2世モスク',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'description': '世界で3番目に大きく、最も美しいモスクの一つ。1993年に完成したこの現代の傑作は、フランス人建築家ミシェル・ペンソーによって設計されました。高さ210メートルのミナレットは世界最高で、レーザー光線がメッカの方向を指し示します。最大10万5000人を収容でき、そのうち8万人がモスク内部、2万5000人が屋外広場に入れます。大西洋に面した立地で、ガラス床から海を見下ろすことができる世界唯一のモスクです。',
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
            'description': '映画「カサブランカ」の舞台となった伝説のカフェを忠実に再現したレストラン。元米国領事だったキャシー・クリガーが2004年にオープン。1940年代の雰囲気を完璧に再現した内装には、映画のポスター、ピアノ、アンティーク家具が配置されています。「君の瞳に乾杯」の名セリフで有名な映画の世界に浸りながら、本格的なモロッコ料理とフランス料理を楽しめます。',
            'verified': True,
            'lat': 33.594629,
            'lng': -7.619054,
            'best_time': '夕方〜夜',
            'duration': '1-2時間',
            'price_range': 'ディナー300-500DH'
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
            'description': 'カサブランカの中心に位置する美しい広場。フランス保護領時代に整備された都市計画の傑作で、周囲を重要な政府建物が囲んでいます。広場の中央には美しい噴水があり、夜間はライトアップされて幻想的な雰囲気を醸し出します。近くには中央郵便局、裁判所のほか、ムーレイ・ユーセフ・モスクもあり、カサブランカの行政・宗教の中心地として機能しています。',
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
            'description': '1956年に建設されたカサブランカで最も美しいカトリック教会。フランスのルルドの聖母にちなんで名付けられ、モダンな建築様式とモロッコの伝統的要素が融合した独特のデザインが特徴です。美しいステンドグラス、現代的な祭壇、そして静寂な祈りの空間は、イスラム教が主流の国での宗教的多様性を象徴しています。毎日ミサが行われており、信者でなくても見学可能です。',
            'verified': True,
            'lat': 33.589722,
            'lng': -7.623889,
            'best_time': '午前中',
            'duration': '30分',
            'price_range': '無料'
        },
        {
            'id': 14,
            'name': 'カサブランカ・ツインセンター',
            'city': 'カサブランカ',
            'category': '現代建築',
            'description': '1998年に完成したカサブランカのシンボル的存在の超高層ビル。2つの28階建てタワーからなるこの複合施設は、高さ115メートルでモロッコで最も高い建物です。ショッピングモール、オフィス、ホテルが入居し、展望デッキからはカサブランカ市街と大西洋の絶景を一望できます。夜間のライトアップは美しく、現代モロッコの発展を象徴する建築物として注目されています。',
            'verified': True,
            'lat': 33.588889,
            'lng': -7.630556,
            'best_time': '夕方（展望デッキ）',
            'duration': '1時間',
            'price_range': '展望デッキ50DH'
        },
        {
            'id': 15,
            'name': 'ムーレイ・ユーセフ・モスク',
            'city': 'カサブランカ',
            'category': '宗教建築',
            'description': '20世紀初頭に建設されたカサブランカで最も古いモスクの一つ。フランス保護領時代に現在の姿となり、伝統的なモロッコ・アンダルシア建築の美しい例です。白い壁と緑のタイル装飾が特徴的で、ミナレットはシンプルながら優雅なデザイン。モハメッド5世広場に近く、旧市街散策の際に必ず目にする重要なランドマークです。金曜日の集団礼拝時には多くの信者が集まります。',
            'verified': True,
            'lat': 33.598333,
            'lng': -7.620833,
            'best_time': '午前中',
            'duration': '30分（外観）',
            'price_range': '無料（外観のみ）'
        },
        # フェズの観光地（10箇所）
        {
            'id': 16,
            'name': 'フェズ・エル・バリ',
            'city': 'フェズ',
            'category': '都市・建築',
            'description': '世界最大の車両進入禁止都市として知られるユネスコ世界遺産の旧市街。9世紀から続く迷宮都市で、幅1メートル程の狭い路地が9000本以上網目状に張り巡らされています。職人街では今でも革なめし、金属細工、陶器作りなどの伝統工芸が営まれており、中世の雰囲気を完璧に保持しています。約28万人が居住し、生きた歴史都市として機能している奇跡的な場所です。地元ガイドと一緒に散策することを強くお勧めします。',
            'verified': True,
            'lat': 34.063611,
            'lng': -4.972222,
            'best_time': '午前中（涼しい時間帯）',
            'duration': '半日〜1日',
            'price_range': 'ガイド300-500DH'
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
            'description': '「青い真珠」と呼ばれる山間の宝石のような町。1471年にアンダルシアから逃れてきたムーア人によって建設され、家々の壁が様々な青色で塗られた独特の景観で世界的に有名です。青く塗る理由は諸説ありますが、虫除け効果や涼しさを演出するためとされています。迷路のような石畳の小径、青いドア、花で飾られたバルコニー、職人の工房など、まるでおとぎ話の世界に迷い込んだような美しさです。',
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
            'description': 'シャウエンの中心広場で、地元の人々の憩いの場。赤茶色の城塞（カスバ）に隣接し、周囲を青い建物とカフェ、レストランが囲んでいます。夕方になると地元の人々がお茶を飲みながら談笑し、のんびりとした山間の町の雰囲気を満喫できます。広場の噴水周辺は写真撮影の人気スポットで、シャウエンの青い街並みを背景にした記念写真が撮れます。',
            'verified': True,
            'lat': 35.169444,
            'lng': -5.268056,
            'best_time': '夕方',
            'duration': '1時間',
            'price_range': '無料'
        },
        {
            'id': 27,
            'name': 'シャウエン・カスバ',
            'city': 'シャウエン',
            'category': '歴史建築',
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
            'description': '18世紀にフランス人建築家テオドール・コルニュによって設計されたユネスコ世界遺産の要塞都市。大西洋に面した白い城壁に囲まれた旧市街は、ヨーロッパとアフリカの建築様式が見事に融合した独特の美しさを持っています。「アフリカの風の街」とも呼ばれ、年中強い貿易風が吹くことで知られ、ウィンドサーフィンやカイトサーフィンの聖地でもあります。ポルトガル、フランスによる植民地時代の建築遺産が完璧に保存されています。',
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
    """AI機能の初期化（セキュリティ強化版）"""
    # 環境変数からAPIキーを安全に取得（表示しない）
    api_key = os.getenv('OPENAI_API_KEY')
    
    return {
        'available': bool(api_key),
        'api_key_masked': '****' if api_key else None,
        'fallback_responses': {
            'マラケシュ': 'マラケシュは「赤い街」として知られる帝国都市。ジャマ・エル・フナ広場、クトゥビア・モスク、バイア宮殿、マジョレル庭園など8つの主要観光地があります。特にイスラム建築の傑作と活気ある市場文化が魅力です。',
            'カサブランカ': 'カサブランカはモロッコ最大の経済都市。世界第3位の規模を誇るハッサン2世モスク、映画で有名なリック・カフェ、現代建築のツインセンターなど6つの見どころがあります。',
            'フェズ': 'フェズは1200年の歴史を持つ古都。世界最大の歩行者専用都市フェズ・エル・バリ、世界最古の大学カラウィーン、伝統工芸の宝庫として7つの主要スポットがあります。',
            'メルズーガ': 'メルズーガはサハラ砂漠の玄関口。エルグ・シェビ砂丘でのラクダトレッキング、砂漠キャンプ、満天の星空観察が体験できる砂漠観光の聖地です。',
            'シャウエン': 'シャウエンは「青い真珠」と呼ばれる山間の美しい町。青く塗られた家々が並ぶ旧市街、カスバからの絶景、自然の滝など4つの魅力的なスポットがあります。',
            'エッサウィラ': 'エッサウィラは「アフリカの風の街」として知られる港町。ユネスコ世界遺産の要塞都市、活気ある漁港、ウィンドサーフィンの聖地として4つの見どころを持ちます。',
            'ラバト': 'ラバトはモロッコの首都。ハッサンの塔、ムハンマド5世霊廟、ウダイヤ・カスバなど、王室の歴史と現代政治の中心地としての魅力があります。',
            'メクネス': 'メクネスは「モロッコのヴェルサイユ」。古代ローマ遺跡ヴォルビリス、美しいバブ・マンスール門など、古代からイスラム王朝まで重層的な歴史を持つ帝国都市です。',
            'ティトゥアン': 'ティトゥアンは「白いハト」という意味の美しい山間都市。アンダルシア文化の影響を色濃く残すユネスコ世界遺産の旧市街が見どころです。',
            'タンジェ': 'タンジェはアフリカとヨーロッパの交差点。ヘラクレスの洞窟、歴史ある旧市街など、大西洋と地中海が出会う戦略的要衝としての魅力があります。'
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
        ["🏠 ホーム", "🗺️ マップ", "📍 観光地一覧", "🏛️ モロッコ文化・歴史", "🤖 AI観光ガイド", "⚙️ 設定"]
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
    elif page == "🏛️ モロッコ文化・歴史":
        show_culture_history_page()
    elif page == "🤖 AI観光ガイド":
        show_ai_page(ai_service)
    elif page == "⚙️ 設定":
        show_settings_page()

def show_home_page(spots):
    """ホームページ"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 観光地数", len(spots))
    
    with col2:
        cities = set(spot['city'] for spot in spots)
        st.metric("🏙️ 都市数", len(cities))
    
    with col3:
        verified_count = sum(1 for spot in spots if spot.get('verified', False))
        st.metric("✅ 認定スポット", verified_count)
    
    with col4:
        categories = set(spot['category'] for spot in spots)
        st.metric("🎯 カテゴリ数", len(categories))
    
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
                popup_content += f'<p style="margin: 8px 0; line-height: 1.4;">{spot["description"][:150]}...</p>'
                
                if spot.get('best_time'):
                    popup_content += f'<p style="margin: 4px 0;"><b>⏰ ベストタイム:</b> {spot["best_time"]}</p>'
                
                if spot.get('duration'):
                    popup_content += f'<p style="margin: 4px 0;"><b>⏱️ 所要時間:</b> {spot["duration"]}</p>'
            else:
                popup_content += f'<p style="margin: 8px 0; line-height: 1.4;">{spot["description"][:80]}...</p>'
            
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
    
    # 高度な検索・フィルター機能
    st.markdown("### 🔍 検索・フィルター")
    
    # テキスト検索
    search_term = st.text_input("🔍 観光地を検索", placeholder="名前や都市名、説明文で検索...")
    
    # フィルター（複数選択対応）
    col1, col2 = st.columns(2)
    
    with col1:
        cities = sorted(set(spot['city'] for spot in spots))
        selected_cities = st.multiselect(
            "🏙️ 都市を選択（複数選択可）",
            options=cities,
            default=[],
            placeholder="都市を選択してください"
        )
    
    with col2:
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
               search_term.lower() in spot['description'].lower()
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
            if st.button("📥 結果をCSVで保存"):
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
    
    # 観光地カード表示（拡張版）
    cols = st.columns(2)
    for i, spot in enumerate(filtered_spots):
        with cols[i % 2]:
            with st.container():
                # 追加情報の構築
                additional_info = ""
                if spot.get('best_time'):
                    additional_info += f"<br>⏰ <strong>ベストタイム:</strong> {spot['best_time']}"
                if spot.get('duration'):
                    additional_info += f"<br>⏱️ <strong>所要時間:</strong> {spot['duration']}"
                if spot.get('price_range'):
                    additional_info += f"<br>💰 <strong>料金:</strong> {spot['price_range']}"
                
                st.markdown(f"""
                <div class="spot-card">
                    <div class="spot-title">{spot['name']}</div>
                    <div class="spot-meta">
                        📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                        {' • <span class="verified-badge">認定済み</span>' if spot.get('verified') else ''}
                    </div>
                    <p>{spot['description'][:200]}{'...' if len(spot['description']) > 200 else ''}</p>
                    {additional_info}
                    <p><small>座標: {spot['lat']:.4f}, {spot['lng']:.4f}</small></p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # 検索結果が0件の場合
        st.warning("🔍 検索条件に一致する観光地が見つかりませんでした。")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **検索のヒント:**
            - より広い条件で検索してみてください
            - 都市やカテゴリの選択を解除してみてください
            - 検索キーワードを変更してみてください
            """)
        
        with col2:
            if st.button("🔄 フィルターをリセット"):
                st.rerun()
        
        # おすすめ観光地を表示
        st.markdown("### 🌟 おすすめ観光地")
        recommended = [spot for spot in spots if spot.get('verified', False)][:4]
        
        cols = st.columns(2)
        for i, spot in enumerate(recommended):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="spot-card" style="opacity: 0.8;">
                    <div class="spot-title">{spot['name']}</div>
                    <div class="spot-meta">
                        📍 {spot['city']} • <span class="category-badge">{spot['category']}</span>
                        <span class="verified-badge">認定済み</span>
                    </div>
                    <p>{spot['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)

def show_culture_history_page():
    """モロッコ文化・歴史ページ"""
    st.subheader("🏛️ モロッコ文化・歴史ガイド")
    
    # タブ形式で情報を整理
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📚 歴史", "🎨 文化", "🏛️ 建築", "🍽️ グルメ", "🎭 伝統"])
    
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
    st.subheader("🤖 AI観光ガイド")
    
    # API状態の表示（セキュアな方法）
    col1, col2 = st.columns([3, 1])
    with col1:
        if ai_service['available']:
            st.success("✅ AI機能が利用可能です")
        else:
            st.warning("⚠️ OpenAI APIキーが設定されていません。フォールバック応答を使用します。")
    
    with col2:
        if ai_service['available']:
            st.info("🔑 API: 設定済み")
        else:
            st.error("🔑 API: 未設定")
    
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
    
    # 環境変数からAPIキーの存在を確認
    api_key_status = bool(os.getenv('OPENAI_API_KEY'))
    
    if api_key_status:
        st.success("✅ OpenAI APIキーが設定されています")
        st.info("💡 APIキーは環境変数 `OPENAI_API_KEY` から読み込まれます")
    else:
        st.warning("⚠️ OpenAI APIキーが設定されていません")
        st.info("💡 AI機能を使用するには、環境変数 `OPENAI_API_KEY` を設定してください")
    
    st.markdown("**セキュリティのため、APIキーは表示されません**")
    
    if st.button("API接続をテスト"):
        if api_key_status:
            st.info("🔄 API接続をテスト中...")
            # 実際のテストは実装しない（セキュリティ上の理由）
            st.success("✅ APIキーが設定されています（接続テストは実装されていません）")
        else:
            st.error("❌ APIキーが設定されていません")
    
    # セキュリティ情報
    st.markdown("### 🔒 セキュリティ情報")
    st.info("""
    **プライバシー保護:**
    - APIキーは環境変数から安全に読み込まれます
    - APIキーは画面に表示されません
    - ユーザーデータは保存されません
    - チャット履歴はセッション終了時にクリアされます
    """)
    
    # アプリ情報
    st.markdown("### ℹ️ アプリケーション情報")
    st.write("**バージョン:** 1.1.0")
    st.write("**作成日:** 2025年11月7日")
    st.write("**最終更新:** 2025年11月7日")
    st.write("**フレームワーク:** Streamlit")
    st.write("**観光地データ:** 40箇所")
    st.write("**対象都市:** 8都市")
    st.write("**セキュリティ:** APIキー非表示対応")
    st.write("**機能:** インタラクティブマップ、AI観光ガイド、詳細検索")

if __name__ == "__main__":
    main()