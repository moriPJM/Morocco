"""
サンプルデータ投入スクリプト
"""

from backend.models.tourism import TourismSpot, TravelRoute, db
from backend.services.database import db as database

def load_sample_data(app):
    """サンプルのモロッコ観光データを投入"""
    
    with app.app_context():
        # 既存データをクリア
        TourismSpot.query.delete()
        TravelRoute.query.delete()
        
        # 観光スポットサンプルデータ
        spots = [
            TourismSpot(
                name="ジャマ・エル・フナ広場",
                name_en="Jemaa el-Fnaa",
                name_ar="ساحة جامع الفنا",
                description="マラケシュの中心部にある賑やかな広場。昼は屋台や物売り、夜には大道芸人や音楽家で溢れる。",
                description_en="The bustling central square of Marrakech, filled with food stalls and street performers.",
                category="広場・市場",
                city="マラケシュ",
                latitude=31.625901,
                longitude=-7.989161,
                rating=4.5,
                image_url="https://example.com/jemaa.jpg",
                best_time_to_visit="夕方〜夜",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="サハラ砂漠",
                name_en="Sahara Desert",
                name_ar="الصحراء الكبرى",
                description="世界最大の砂漠。メルズーガからのラクダツアーや砂丘での星空観察が人気。",
                description_en="The world's largest hot desert. Camel tours and stargazing are popular activities.",
                category="自然",
                city="メルズーガ",
                latitude=31.0801,
                longitude=-4.0133,
                rating=4.8,
                image_url="https://example.com/sahara.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="ツアー料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="シャウエン",
                name_en="Chefchaouen",
                name_ar="شفشاون",
                description="青い街として有名な美しい山間の町。フォトジェニックな街並みが魅力。",
                description_en="A beautiful mountain town famous for its blue-painted buildings.",
                category="都市・建築",
                city="シャウエン",
                latitude=35.1711,
                longitude=-5.2636,
                rating=4.7,
                image_url="https://example.com/chefchaouen.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ハッサン2世モスク",
                name_en="Hassan II Mosque",
                name_ar="مسجد الحسن الثاني",
                description="カサブランカにある巨大なモスク。美しい建築と海沿いの立地が特徴。",
                description_en="A magnificent mosque in Casablanca, known for its stunning architecture.",
                category="宗教建築",
                city="カサブランカ",
                latitude=33.6083,
                longitude=-7.6319,
                rating=4.6,
                image_url="https://example.com/hassan2.jpg",
                best_time_to_visit="通年",
                entry_fee="120ディルハム",
                opening_hours="9:00-18:00"
            ),
            TourismSpot(
                name="フェズ旧市街",
                name_en="Fez Medina",
                name_ar="فاس البالي",
                description="世界最大の自動車通行禁止区域。迷路のような旧市街は世界遺産。",
                description_en="The world's largest car-free urban area and a UNESCO World Heritage site.",
                category="歴史地区",
                city="フェズ",
                latitude=34.0631,
                longitude=-4.9998,
                rating=4.4,
                image_url="https://example.com/fez.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アイト・ベン・ハドゥ",
                name_en="Ait Ben Haddou",
                name_ar="آيت بن حدو",
                description="映画のロケ地として有名な要塞都市。世界遺産に登録されている。",
                description_en="A fortified city famous as a filming location for many movies.",
                category="歴史建築",
                city="ワルザザード",
                latitude=31.0473,
                longitude=-7.1316,
                rating=4.5,
                image_url="https://example.com/aitbenhaddou.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="10ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="マジョレル庭園",
                name_en="Majorelle Garden",
                name_ar="حدائق ماجوريل",
                description="イヴ・サンローランが愛した美しい庭園。鮮やかな青色の建物が印象的。",
                description_en="A beautiful garden loved by Yves Saint Laurent, famous for its vibrant blue buildings.",
                category="庭園・公園",
                city="マラケシュ",
                latitude=31.6416,
                longitude=-8.0033,
                rating=4.3,
                image_url="https://example.com/majorelle.jpg",
                best_time_to_visit="朝・夕方",
                entry_fee="70ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="バイア宮殿",
                name_en="Bahia Palace",
                name_ar="قصر الباهية",
                description="19世紀に建てられた豪華な宮殿。美しいタイルワークと庭園が見どころ。",
                description_en="A lavish 19th-century palace known for its beautiful tilework and gardens.",
                category="宮殿・建築",
                city="マラケシュ",
                latitude=31.6165,
                longitude=-7.9813,
                rating=4.2,
                image_url="https://example.com/bahia.jpg",
                best_time_to_visit="午前中",
                entry_fee="20ディルハム",
                opening_hours="9:00-17:00"
            ),
            TourismSpot(
                name="ベン・ユーセフ・マドラサ",
                name_en="Ben Youssef Madrasa",
                name_ar="مدرسة ابن يوسف",
                description="アフリカ最大のイスラム神学校。精巧な装飾が施された美しい建築。",
                description_en="Africa's largest Islamic college, featuring intricate decorative architecture.",
                category="歴史建築",
                city="マラケシュ",
                latitude=31.6315,
                longitude=-7.9898,
                rating=4.4,
                image_url="https://example.com/benyoussef.jpg",
                best_time_to_visit="午前中",
                entry_fee="50ディルハム",
                opening_hours="9:00-18:00"
            ),
            TourismSpot(
                name="ウダイヤのカスバ",
                name_en="Kasbah of the Udayas",
                name_ar="قصبة الأوداية",
                description="ラバトにある要塞都市。白と青の美しい街並みと大西洋の絶景。",
                description_en="A fortified city in Rabat with beautiful white and blue buildings overlooking the Atlantic.",
                category="歴史地区",
                city="ラバト",
                latitude=34.0242,
                longitude=-6.8417,
                rating=4.3,
                image_url="https://example.com/udayas.jpg",
                best_time_to_visit="夕方",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ハッサンの塔",
                name_en="Hassan Tower",
                name_ar="صومعة حسان",
                description="ラバトにある12世紀の未完成のミナレット。モロッコの象徴的建造物。",
                description_en="An incomplete 12th-century minaret in Rabat, an iconic symbol of Morocco.",
                category="歴史建築",
                city="ラバト",
                latitude=34.0242,
                longitude=-6.8239,
                rating=4.1,
                image_url="https://example.com/hassan_tower.jpg",
                best_time_to_visit="午前中",
                entry_fee="無料",
                opening_hours="8:30-18:00"
            ),
            TourismSpot(
                name="エッサウィラ",
                name_en="Essaouira",
                name_ar="الصويرة",
                description="大西洋に面した港町。城壁に囲まれた旧市街と美しいビーチが魅力。",
                description_en="A coastal port city with a walled medina and beautiful beaches on the Atlantic.",
                category="都市・海岸",
                city="エッサウィラ",
                latitude=31.5125,
                longitude=-9.7737,
                rating=4.5,
                image_url="https://example.com/essaouira.jpg",
                best_time_to_visit="春〜秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="トドラ渓谷",
                name_en="Todra Gorge",
                name_ar="مضايق تودرا",
                description="壮大な岩壁に囲まれた美しい渓谷。ロッククライミングの聖地。",
                description_en="A spectacular gorge with towering rock walls, popular for rock climbing.",
                category="自然・渓谷",
                city="ティネリール",
                latitude=31.5872,
                longitude=-5.5975,
                rating=4.6,
                image_url="https://example.com/todra.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アトラス山脈",
                name_en="Atlas Mountains",
                name_ar="جبال الأطلس",
                description="モロッコを横断する山脈。ハイキングやベルベル村訪問が人気。",
                description_en="Mountain range crossing Morocco, popular for hiking and visiting Berber villages.",
                category="自然・山脈",
                city="イムリル",
                latitude=31.1364,
                longitude=-7.9203,
                rating=4.7,
                image_url="https://example.com/atlas.jpg",
                best_time_to_visit="4月〜10月",
                entry_fee="ガイド料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="マラケシュ・スーク",
                name_en="Marrakech Souks",
                name_ar="أسواق مراكش",
                description="迷路のような市場街。香辛料、絨毯、工芸品などが所狭しと並ぶ。",
                description_en="Labyrinthine markets filled with spices, carpets, and handicrafts.",
                category="市場・ショッピング",
                city="マラケシュ",
                latitude=31.6295,
                longitude=-7.9881,
                rating=4.3,
                image_url="https://example.com/souks.jpg",
                best_time_to_visit="午前中",
                entry_fee="無料",
                opening_hours="9:00-19:00"
            ),
            TourismSpot(
                name="アガディール・ビーチ",
                name_en="Agadir Beach",
                name_ar="شاطئ أكادير",
                description="モロッコ最大のビーチリゾート。美しい砂浜とマリンスポーツが楽しめる。",
                description_en="Morocco's largest beach resort with beautiful sandy beaches and water sports.",
                category="ビーチ・リゾート",
                city="アガディール",
                latitude=30.4278,
                longitude=-9.5981,
                rating=4.2,
                image_url="https://example.com/agadir.jpg",
                best_time_to_visit="通年",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="メクネス",
                name_en="Meknes",
                name_ar="مكناس",
                description="王朝の古都。バブ・マンスール門や王室厩舎跡が見どころ。",
                description_en="An imperial city known for Bab Mansour gate and royal stables ruins.",
                category="歴史都市",
                city="メクネス",
                latitude=33.8935,
                longitude=-5.5473,
                rating=4.1,
                image_url="https://example.com/meknes.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料（一部有料）",
                opening_hours="9:00-17:00"
            ),
            TourismSpot(
                name="カッタラ・ダクラ",
                name_en="Dakhla Lagoon",
                name_ar="الداخلة",
                description="サハラ砂漠と大西洋が出会う秘境。カイトサーフィンの世界的スポット。",
                description_en="A remote destination where the Sahara meets the Atlantic, famous for kitesurfing.",
                category="自然・ラグーン",
                city="ダクラ",
                latitude=23.7148,
                longitude=-15.9574,
                rating=4.8,
                image_url="https://example.com/dakhla.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ヴォルビリス遺跡",
                name_en="Volubilis",
                name_ar="وليلي",
                description="古代ローマの遺跡群。保存状態の良いモザイクが見どころ。世界遺産。",
                description_en="Ancient Roman ruins with well-preserved mosaics. UNESCO World Heritage site.",
                category="遺跡・考古学",
                city="ムーレイ・イドリス",
                latitude=34.0742,
                longitude=-5.5531,
                rating=4.0,
                image_url="https://example.com/volubilis.jpg",
                best_time_to_visit="午前中",
                entry_fee="20ディルハム",
                opening_hours="8:30-18:30"
            ),
            TourismSpot(
                name="イフラン",
                name_en="Ifrane",
                name_ar="إفران",
                description="「モロッコのスイス」と呼ばれる高原都市。ヨーロッパ風の街並みが特徴。",
                description_en="A highland city called 'Switzerland of Morocco' with European-style architecture.",
                category="都市・高原",
                city="イフラン",
                latitude=33.5228,
                longitude=-5.1106,
                rating=4.2,
                image_url="https://example.com/ifrane.jpg",
                best_time_to_visit="夏・冬",
                entry_fee="無料",
                opening_hours="24時間"
            )
        ]
        
        # 旅行ルートサンプルデータ
        routes = [
            TravelRoute(
                name="王道モロッコ周遊7日間",
                description="カサブランカ→ラバト→フェズ→シャウエン→マラケシュを巡る定番ルート",
                duration_days=7,
                difficulty="Easy",
                route_data={
                    "cities": ["カサブランカ", "ラバト", "フェズ", "シャウエン", "マラケシュ"],
                    "spots": [4, 5, 3, 1],
                    "daily_plan": {
                        "day1": "カサブランカ到着、ハッサン2世モスク見学",
                        "day2": "ラバト観光、フェズへ移動",
                        "day3": "フェズ旧市街散策",
                        "day4": "シャウエン観光",
                        "day5": "マラケシュへ移動",
                        "day6": "マラケシュ観光",
                        "day7": "帰国"
                    }
                }
            ),
            TravelRoute(
                name="サハラ砂漠アドベンチャー4日間",
                description="マラケシュからサハラ砂漠への冒険ツアー",
                duration_days=4,
                difficulty="Medium",
                route_data={
                    "cities": ["マラケシュ", "アイト・ベン・ハドゥ", "メルズーガ"],
                    "spots": [1, 6, 2],
                    "daily_plan": {
                        "day1": "マラケシュ出発、アイト・ベン・ハドゥ見学",
                        "day2": "サハラ砂漠到着、ラクダツアー",
                        "day3": "砂漠キャンプ、星空観察",
                        "day4": "マラケシュ帰着"
                    }
                }
            ),
            TravelRoute(
                name="青い街シャウエンとフェズ歴史探訪3日間",
                description="モロッコ北部の美しい街を巡る文化的な旅",
                duration_days=3,
                difficulty="Easy",
                route_data={
                    "cities": ["フェズ", "シャウエン"],
                    "spots": [5, 3],
                    "daily_plan": {
                        "day1": "フェズ到着、旧市街散策",
                        "day2": "シャウエンへ移動、青い街観光",
                        "day3": "シャウエン散策、帰路"
                    }
                }
            ),
            TravelRoute(
                name="マラケシュ完全攻略2日間",
                description="マラケシュの主要観光スポットを効率よく巡る",
                duration_days=2,
                difficulty="Easy",
                route_data={
                    "cities": ["マラケシュ"],
                    "spots": [1, 7, 8, 9, 15],
                    "daily_plan": {
                        "day1": "ジャマ・エル・フナ広場、マジョレル庭園、スーク散策",
                        "day2": "バイア宮殿、ベン・ユーセフ・マドラサ見学"
                    }
                }
            ),
            TravelRoute(
                name="大西洋岸リゾート満喫5日間",
                description="カサブランカ、ラバト、エッサウィラの海岸都市を巡る",
                duration_days=5,
                difficulty="Easy",
                route_data={
                    "cities": ["カサブランカ", "ラバト", "エッサウィラ"],
                    "spots": [4, 10, 11, 12],
                    "daily_plan": {
                        "day1": "カサブランカ到着、ハッサン2世モスク",
                        "day2": "ラバト観光、ウダイヤのカスバ",
                        "day3": "エッサウィラへ移動",
                        "day4": "エッサウィラ観光、ビーチでリラックス",
                        "day5": "カサブランカ経由で帰国"
                    }
                }
            ),
            TravelRoute(
                name="アトラス山脈トレッキング6日間",
                description="ベルベル村を訪れながらアトラス山脈をハイキング",
                duration_days=6,
                difficulty="Hard",
                route_data={
                    "cities": ["マラケシュ", "イムリル", "トドラ渓谷"],
                    "spots": [1, 13, 14],
                    "daily_plan": {
                        "day1": "マラケシュからイムリルへ",
                        "day2-4": "アトラス山脈トレッキング",
                        "day5": "トドラ渓谷観光",
                        "day6": "マラケシュ帰着"
                    }
                }
            ),
            TravelRoute(
                name="古代遺跡と王朝都市10日間",
                description="モロッコの歴史を深く学ぶ充実の文化ツアー",
                duration_days=10,
                difficulty="Medium",
                route_data={
                    "cities": ["カサブランカ", "ラバト", "メクネス", "フェズ", "マラケシュ", "ワルザザード"],
                    "spots": [4, 10, 11, 17, 19, 5, 1, 6],
                    "daily_plan": {
                        "day1": "カサブランカ到着",
                        "day2": "ラバト観光",
                        "day3": "メクネス、ヴォルビリス遺跡",
                        "day4-5": "フェズ滞在",
                        "day6-7": "マラケシュ観光",
                        "day8-9": "アイト・ベン・ハドゥ、ワルザザード",
                        "day10": "帰国"
                    }
                }
            )
        ]
        
        # データベースに追加
        for spot in spots:
            db.session.add(spot)
        
        for route in routes:
            db.session.add(route)
        
        db.session.commit()
        print("[OK] Sample tourism data loaded successfully")

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    load_sample_data(app)