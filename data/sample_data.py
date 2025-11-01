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
            )
        ]
        
        # データベースに追加
        for spot in spots:
            db.session.add(spot)
        
        for route in routes:
            db.session.add(route)
        
        db.session.commit()
        print("✅ サンプルデータが正常に投入されました")

if __name__ == "__main__":
    from app import create_app
    
    app = create_app()
    load_sample_data(app)