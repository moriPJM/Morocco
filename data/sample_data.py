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
                description="マラケシュの心臓部に位置する世界遺産の広場。「死者の集会」を意味するこの広場は、1000年以上の歴史を持つモロッコ文化の縮図です。日中は蛇使い、猿回し、ヘナタトゥー師、オレンジジュース売りで賑わい、夕方からは100以上の屋台が現れ、タジン、クスクス、ハリラスープなど本格的なモロッコ料理を味わえます。夜にはベルベル音楽やアラブ古典音楽の演奏者が集まり、まさに「生きた博物館」として機能しています。周囲にはスーク（市場）が広がり、バザール文化の入り口でもあります。",
                description_en="UNESCO World Heritage square at the heart of Marrakech, meaning 'Assembly of the Dead'. This 1000-year-old square is a microcosm of Moroccan culture with snake charmers, monkey handlers, henna artists and orange juice vendors by day, transforming into a massive food court with over 100 stalls by evening.",
                category="広場・市場",
                city="マラケシュ",
                latitude=31.625901,
                longitude=-7.989161,
                image_url="https://example.com/jemaa.jpg",
                best_time_to_visit="夕方〜夜",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="サハラ砂漠",
                name_en="Sahara Desert",
                name_ar="الصحراء الكبرى",
                description="アフリカ大陸北部に広がる世界最大の熱帯砂漠で、面積は約900万平方キロメートル（アメリカ合衆国とほぼ同じ大きさ）。モロッコ側では特にメルズーガ周辺のエルグ・シェビ砂丘が有名で、高さ150メートルを超える美しい砂山が連なります。ラクダキャラバンでの砂漠トレッキング、ベルベルテントでのキャンプ体験、満天の星空観察が主な楽しみ方。砂漠の民ベルベル人のガイドによる伝統的なライフスタイルの紹介、砂丘サーフィン、四輪駆動車での砂漠ドライブなど多彩なアクティビティがあります。日中は40度を超える暑さですが、夜は氷点下近くまで下がる寒暖差も体験の一部です。",
                description_en="The world's largest hot desert covering 9 million square kilometers across North Africa. Morocco's section features the famous Erg Chebbi dunes near Merzouga, with sand mountains reaching over 150 meters. Experience camel trekking, Berber tent camping, stargazing, sandboarding, and 4WD desert drives with traditional Berber guides.",
                category="自然",
                city="メルズーガ",
                latitude=31.0801,
                longitude=-4.0133,
                image_url="https://example.com/sahara.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="ツアー料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="シャウエン",
                name_en="Chefchaouen",
                name_ar="شفشاون",
                description="リフ山脈の斜面に築かれた「青い真珠」と呼ばれる美しい山間都市。15世紀にアンダルシアから逃れてきたムスリムとユダヤ人によって建設され、建物の壁が鮮やかな青色に塗られているのが特徴です。この青色は虫除け効果、暑さ対策、そして神聖さを表すという説があります。旧市街（メディナ）は迷路のように入り組んだ石畳の路地で構成され、手織りのウールブランケット、陶器、銀細工などの伝統工芸品店が軒を連ねます。カスバ（要塞）からは街全体を見渡せ、周囲の山々の景色も楽しめます。ハシシ（大麻）の産地としても知られ、リラックスした雰囲気が漂う町です。",
                description_en="The 'Blue Pearl' built on Rif Mountain slopes by Andalusian Muslims and Jews in the 15th century. Buildings painted in distinctive blue shades for insect repellent, cooling effects, and spiritual significance. The medina features maze-like cobblestone alleys filled with traditional handicraft shops selling woolen blankets, pottery, and silverware.",
                category="都市・建築",
                city="シャウエン",
                latitude=35.1711,
                longitude=-5.2636,
                image_url="https://example.com/chefchaouen.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ハッサン2世モスク",
                name_en="Hassan II Mosque",
                name_ar="مسجد الحسن الثاني",
                description="カサブランカの海岸に聳え立つ現代モロッコ建築の傑作。1993年に完成したこのモスクは、高さ210メートルのミナレット（世界最高）を持ち、25,000人を収容できる巨大な礼拝堂があります。フランス人建築家ミシェル・ピンソーの設計で、モロッコの伝統的なイスラム建築と現代技術が見事に融合。内部には手彫りの木材、精密なモザイクタイル（ゼリージュ）、イタリア産大理石、ベネチアンガラスのシャンデリアが使われています。床の一部はガラス張りで、下に流れる大西洋を見ることができる珍しい構造。非ムスリムも見学可能で、英語・フランス語・アラビア語のガイドツアーが利用できます。",
                description_en="Masterpiece of modern Moroccan architecture completed in 1993, featuring the world's tallest minaret at 210 meters. Designed by French architect Michel Pinseau, it accommodates 25,000 worshippers and showcases traditional Islamic architecture merged with modern technology, including hand-carved wood, intricate zellige mosaics, Italian marble, and glass floors overlooking the Atlantic.",
                category="宗教建築",
                city="カサブランカ",
                latitude=33.6083,
                longitude=-7.6319,
                image_url="https://example.com/hassan2.jpg",
                best_time_to_visit="通年",
                entry_fee="120ディルハム",
                opening_hours="9:00-18:00"
            ),
            TourismSpot(
                name="フェズ旧市街",
                name_en="Fez Medina",
                name_ar="فاس البالي",
                description="9世紀に建設された世界最古の大学都市で、ユネスコ世界遺産に登録されています。「フェズ・エル・バリ」と呼ばれる旧市街は、世界最大の歩行者専用都市として約9,400の路地と約30万人の住民を擁します。1200年の歴史を持つこの迷宮都市には、古代から続く皮なめし工場、手織り絨毯工房、真鍮細工店、陶器工房など約9,000の店舗があり、中世の職人文化が今も息づいています。アル・カラウィーン大学（859年創立）は世界最古の大学として知られ、数多くのマドラサ（神学校）では精巧なイスラム装飾芸術を見ることができます。迷路のような構造は防御目的で設計され、現在でも地元ガイドなしでは迷子になる可能性が高い複雑な街です。",
                description_en="Founded in the 9th century, this UNESCO World Heritage site is the world's oldest university city and largest car-free urban area. Fez el-Bali contains 9,400 narrow alleys, 300,000 residents, and about 9,000 shops including ancient tanneries, carpet workshops, brass smithies, and pottery studios. Home to Al-Karaouine University (founded 859 AD), the world's oldest continuously operating university.",
                category="歴史地区",
                city="フェズ",
                latitude=34.0631,
                longitude=-4.9998,
                image_url="https://example.com/fez.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アイト・ベン・ハドゥ",
                name_en="Ait Ben Haddou",
                name_ar="آيت بن حدو",
                description="11世紀に建設されたベルベル人の要塞村（クサル）で、ユネスコ世界遺産に登録されています。ワルザザードから約30km、アトラス山脈南麓に位置するこの要塞都市は、サハラ砂漠と北部を結ぶキャラバンルートの重要な中継地として栄えました。日干し煉瓦（アドベ）と石、木材で建設された建築物群は、砂漠の厳しい環境に適応した伝統的なベルベル建築の傑作。映画「アラビアのロレンス」「グラディエーター」「ゲーム・オブ・スローンズ」など数多くのハリウッド作品のロケ地として使用され、「モロッコのハリウッド」とも呼ばれます。現在も数家族が住み続けており、伝統的な生活様式を垣間見ることができます。頂上の要塞からはアトラス山脈と砂漠の境界線を一望できる絶景スポットです。",
                description_en="11th-century fortified Berber village (ksar) and UNESCO World Heritage site, serving as a crucial caravan route stop between the Sahara and northern regions. Built with adobe, stone, and wood in traditional Berber architecture, it's famous as a filming location for 'Lawrence of Arabia,' 'Gladiator,' and 'Game of Thrones,' earning the nickname 'Morocco's Hollywood.' Several families still inhabit this living heritage site.",
                category="歴史建築",
                city="ワルザザード",
                latitude=31.0473,
                longitude=-7.1316,
                image_url="https://example.com/aitbenhaddou.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="10ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="マジョレル庭園",
                name_en="Majorelle Garden",
                name_ar="حدائق ماجوريل",
                description="1923年にフランス人画家ジャック・マジョレルが造園した12ヘクタールの植物園で、現在はイヴ・サンローラン財団が管理しています。「マジョレル・ブルー」と呼ばれる鮮やかなコバルトブルーで塗られた建物とエキゾチックな植物が調和した美しい庭園。300種以上の植物が世界各地から集められ、特にサボテンコレクション、バンブー、ヤシの木、ブーゲンビリアが見事です。園内にはベルベル博物館があり、北アフリカの先住民ベルベル人の文化、工芸品、ジュエリー、テキスタイルが展示されています。ファッションデザイナーのイヴ・サンローランが愛した場所で、彼の遺灰の一部もここに散骨されました。庭園の随所に配置されたアートオブジェクトや噴水、鳥のさえずりが都市の喧騒を忘れさせる癒しの空間を作り出しています。",
                description_en="12-hectare botanical garden created in 1923 by French painter Jacques Majorelle, now managed by the Yves Saint Laurent Foundation. Famous for 'Majorelle Blue' cobalt buildings harmonizing with over 300 exotic plant species from worldwide. Features the Berber Museum showcasing North African indigenous culture, crafts, jewelry, and textiles. Beloved by fashion designer Yves Saint Laurent, whose ashes are partially scattered here.",
                category="庭園・公園",
                city="マラケシュ",
                latitude=31.6416,
                longitude=-8.0033,
                image_url="https://example.com/majorelle.jpg",
                best_time_to_visit="朝・夕方",
                entry_fee="70ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="バイア宮殿",
                name_en="Bahia Palace",
                name_ar="قصر الباهية",
                description="19世紀後期に宰相バ・アフメッドによって建設された8ヘクタールの壮大な宮殿。「美しさ」を意味する「バイア」の名の通り、モロッコ・アンダルシア建築の粋を集めた傑作です。宮殿は150の部屋、中庭、リヤド（内庭）、庭園で構成され、精巧なゼリージュ（モザイクタイル）、手彫りの杉材、色鮮やかなステンドグラス、アラベスク模様の漆喰装飾が見事に調和しています。特に「大中庭」は1,500平方メートルの広さを持つ圧巻の空間。各部屋の天井はそれぞれ異なるデザインで装飾され、イスラム幾何学文様の美しさを堪能できます。フランス保護領時代にはフランス駐留軍の司令部として使用され、現在は迎賓館として国賓を迎える重要な建物でもあります。",
                description_en="Magnificent 8-hectare palace built in the late 19th century by Grand Vizier Ba Ahmed, showcasing the finest Moroccan-Andalusian architecture. Named 'Bahia' meaning 'beauty,' it features 150 rooms, courtyards, riads, and gardens with exquisite zellige mosaics, hand-carved cedar wood, colorful stained glass, and intricate arabesque plasterwork. The Grand Courtyard spans 1,500 square meters.",
                category="宮殿・建築",
                city="マラケシュ",
                latitude=31.6165,
                longitude=-7.9813,
                image_url="https://example.com/bahia.jpg",
                best_time_to_visit="午前中",
                entry_fee="20ディルハム",
                opening_hours="9:00-17:00"
            ),
            TourismSpot(
                name="ベン・ユーセフ・マドラサ",
                name_en="Ben Youssef Madrasa",
                name_ar="مدرسة ابن يوسف",
                description="14世紀に建設され、16世紀にサアド朝によって再建されたアフリカ最大のイスラム神学校。最盛期には900人以上の学生が学んでいました。132の学生房を持つこの建築群は、イスラム装飾芸術の教科書とも言える精巧な美しさを誇ります。中央の大理石の中庭を囲むように配置された祈祷室では、コーランの朗誦が響き渡っていました。壁面を覆う手彫りの漆喰装飾、幾何学模様のゼリージュ、アラビア書道、杉材の精密な木工細工が見事に調和し、「イスラム芸術の宝石」と称されています。各部屋は狭いながらも機能的に設計され、学生たちの質素な修行生活を物語っています。現在は博物館として一般公開され、モロッコの教育史と宗教建築の粋を体験できます。",
                description_en="Africa's largest Islamic college built in the 14th century and rebuilt by the Saadian dynasty in the 16th century. At its peak, over 900 students studied here in 132 student cells. Known as the 'Jewel of Islamic Art,' it features exquisite hand-carved stucco, geometric zellige patterns, Arabic calligraphy, and precise cedar woodwork surrounding a central marble courtyard where Quranic recitations once echoed.",
                category="歴史建築",
                city="マラケシュ",
                latitude=31.6315,
                longitude=-7.9898,
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
                description="18世紀にフランス人建築家によって設計された大西洋岸の港町で、ユネスコ世界遺産に登録されています。「風の街」とも呼ばれ、年中強い貿易風が吹くため、サーフィンやウィンドサーフィン、カイトサーフィンのメッカとして知られています。ポルトガル風の城壁に囲まれた旧市街（メディナ）は、白と青を基調とした美しい街並みで、アーティストや音楽家が多く住む芸術の街でもあります。毎年6月に開催される「グナワ音楽祭」は世界最大規模のアフリカ音楽フェスティバル。新鮮な魚介類が豊富で、特にイワシ、タコ、ウニが名物。トゥヤ（テトラクリニス）の木工細工は伝統工芸として有名で、精巧な象嵌細工を見学・購入できます。旧市街の城壁からは大西洋の絶景を眺められ、映画「オセロ」や「ゲーム・オブ・スローンズ」のロケ地としても使用されました。",
                description_en="18th-century Atlantic port city designed by French architect, UNESCO World Heritage site known as 'Wind City.' Famous for year-round trade winds making it a surfing, windsurfing, and kitesurfing mecca. The Portuguese-style walled medina features white and blue architecture, home to many artists and musicians. Hosts the world's largest African music festival, Gnawa Music Festival in June, and famous for fresh seafood and traditional thuya woodworking.",
                category="都市・海岸",
                city="エッサウィラ",
                latitude=31.5125,
                longitude=-9.7737,
                image_url="https://example.com/essaouira.jpg",
                best_time_to_visit="春〜秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="トドラ渓谷",
                name_en="Todra Gorge",
                name_ar="مضايق تودرا",
                description="アトラス山脈東部に位置する壮大な峡谷で、最狭部の幅はわずか10メートル、高さ300メートルの石灰岩の崖が聳え立ちます。数百万年をかけてトドラ川が刻んだこの自然の造形美は、「モロッコのグランドキャニオン」と称されます。垂直に切り立った岩壁は世界屈指のロッククライミングスポットとして知られ、初心者から上級者まで楽しめる多様なルートが設定されています。峡谷の入り口には緑豊かなオアシスが広がり、ナツメヤシ、アーモンド、イチジクの木々が砂漠とのコントラストを生み出しています。ベルベル人の村々が点在し、伝統的な日干し煉瓦の家屋と現代的なホテルが共存。早朝と夕方には岩肌が黄金色に輝き、写真撮影に最適な時間帯です。徒歩でのハイキング、四輪駆動車でのオフロード、ロバでのトレッキングなど様々な楽しみ方があります。",
                description_en="Spectacular limestone gorge in the eastern Atlas Mountains with walls reaching 300 meters high and narrowing to just 10 meters wide. Carved over millions of years by the Todra River, this 'Moroccan Grand Canyon' is a world-class rock climbing destination with routes for all skill levels. The entrance features lush palm oases with date palms, almonds, and fig trees, while traditional Berber villages dot the landscape with adobe houses.",
                category="自然・渓谷",
                city="ティネリール",
                latitude=31.5872,
                longitude=-5.5975,
                image_url="https://example.com/todra.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アトラス山脈",
                name_en="Atlas Mountains",
                name_ar="جبال الأطلس",
                description="モロッコを南西から北東に2,500kmにわたって横断する山脈群で、北アフリカの背骨とも呼ばれます。高アトラス、中アトラス、アンチアトラスの3つの山系からなり、最高峰はトゥブカル山（4,167m）。ベルベル人（アマジグ人）が古来より住み続けており、標高に応じて異なる文化と生活様式を体験できます。春には野生のバラやアーモンドの花が咲き乱れ、夏には緑豊かな谷間でハイキングが楽しめます。伝統的なベルベル村では日干し煉瓦の家屋、段々畑、古来からの農業技術を見学でき、ホームステイも可能。山岳ガイドと共に行うトレッキングでは、雪を頂いた山々、深い渓谷、滝、高山植物など変化に富んだ自然を満喫できます。イムリルは高アトラス山脈の玄関口として知られ、トゥブカル山登山のベースキャンプとして機能しています。",
                description_en="Mountain range stretching 2,500km across Morocco from southwest to northeast, known as the 'backbone of North Africa.' Composed of High Atlas, Middle Atlas, and Anti-Atlas ranges with Toubkal peak (4,167m) as the highest point. Home to indigenous Berber (Amazigh) people maintaining traditional lifestyles across different altitudes, offering homestays, trekking, and cultural immersion experiences with terraced fields and ancient agricultural techniques.",
                category="自然・山脈",
                city="イムリル",
                latitude=31.1364,
                longitude=-7.9203,
                image_url="https://example.com/atlas.jpg",
                best_time_to_visit="4月〜10月",
                entry_fee="ガイド料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="マラケシュ・スーク",
                name_en="Marrakech Souks",
                name_ar="أسواق مراكش",
                description="ジャマ・エル・フナ広場から放射状に広がる中東最大級の迷宮市場で、約2,600の店舗が軒を連ねる商業の聖地。1000年以上の歴史を持つこの市場群は、専門分野ごとに区域が分かれており、絨毯スーク、革製品スーク、金属工芸スーク、香辛料スーク、織物スークなどがあります。サハラ砂漠の塩、アルガンオイル、サフラン、クミン、シナモンなどの香辛料が色とりどりに積まれ、手織りのベルベル絨毯、真鍮製のランプ、革のバブーシュ（スリッパ）、陶器、銀細工など伝統工芸品の宝庫。職人たちが実際に作業する様子を見学でき、価格交渉（バルガニング）はモロッコ文化の重要な体験の一つ。狭い路地は日陰を作り出し、昼間の暑さを和らげる伝統的な都市設計の知恵が生きています。迷子になることも楽しみの一つで、地元ガイドのサポートを受けながら探索するのがおすすめです。",
                description_en="Labyrinthine marketplace radiating from Jemaa el-Fnaa square with about 2,600 shops, one of the Middle East's largest markets with over 1000 years of history. Organized by specialty into carpet souks, leather goods, metalwork, spices, and textiles. Features Sahara salt, argan oil, saffron, and traditional crafts like Berber carpets, brass lamps, leather babouches, pottery, and silverware. Artisans work on-site, and bargaining (bargaining) is an essential cultural experience.",
                category="市場・ショッピング",
                city="マラケシュ",
                latitude=31.6295,
                longitude=-7.9881,
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
                description="西サハラ地域の大西洋岸に位置する幅40km、長さ100kmの巨大なラグーンで、サハラ砂漠が直接大西洋と出会う地球上でも稀有な場所。年間300日以上風が吹く「風の楽園」として、カイトサーフィンとウィンドサーフィンの世界的メッカとなっています。水深が浅く（平均1-2m）、水温も年中温暖なため初心者から上級者まで楽しめる理想的な環境。ピンクフラミンゴ、ペリカン、サギなど200種以上の渡り鳥が生息する重要な生態系でもあり、バードウォッチングの聖地でもあります。ラグーン内にはドラゴン島という小島があり、キャンプやピクニックが可能。砂漠と海の境界線、塩田、遊牧民の集落など、地球の原始的な美しさを体験できる最後の秘境の一つです。近年はエコツーリズムの拠点として注目されています。",
                description_en="Massive lagoon (40km wide, 100km long) on the Atlantic coast of Western Sahara where the desert directly meets the ocean. Known as 'Wind Paradise' with over 300 windy days annually, making it a world-class kitesurfing and windsurfing destination. Shallow waters (1-2m average depth) and warm temperatures year-round create ideal conditions for all skill levels. Home to over 200 migratory bird species including pink flamingos, pelicans, and herons.",
                category="自然・ラグーン",
                city="ダクラ",
                latitude=23.7148,
                longitude=-15.9574,
                image_url="https://example.com/dakhla.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ヴォルビリス遺跡",
                name_en="Volubilis",
                name_ar="وليلي",
                description="紀元前3世紀から3世紀まで栄えた古代ローマ都市の遺跡で、ユネスコ世界遺産に登録されています。ベルベル語で「夾竹桃の花」を意味するウリリから名前が付けられたこの都市は、ローマ帝国の最西端の重要都市として機能していました。40ヘクタールの広大な敷地には、保存状態の良いモザイク床、住宅跡、商店街、公衆浴場、凱旋門、バジリカなどが残り、当時の繁栄ぶりを物語っています。特に「バッカス神の家」「オルフェウスの家」「騎士の家」のモザイクは色彩豊かで芸術的価値が高く、ローマ神話や日常生活の場面が精巧に描かれています。オリーブオイル生産の中心地でもあり、当時の搾油所跡も見学できます。隣接するムーレイ・イドリス聖地と合わせて訪れることで、古代ローマ文化とイスラム文化の対比を感じることができる貴重なスポットです。",
                description_en="Ancient Roman city ruins flourishing from 3rd century BC to 3rd century AD, UNESCO World Heritage site. Named after the Berber word for 'oleander flowers,' it served as the westernmost important city of the Roman Empire. The 40-hectare site features well-preserved mosaics, residential areas, shops, public baths, triumphal arch, and basilica, with particularly stunning mosaics in the 'House of Bacchus,' 'House of Orpheus,' and 'House of the Knight' depicting mythology and daily life.",
                category="遺跡・考古学",
                city="ムーレイ・イドリス",
                latitude=34.0742,
                longitude=-5.5531,
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
                image_url="https://example.com/ifrane.jpg",
                best_time_to_visit="夏・冬",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ティエット・ミラル滝",
                name_en="Cascade d'Ouzoud",
                name_ar="شلالات أوزود",
                description="アトラス山脈にある壮大な滝。高さ110mから流れ落ちる美しい景観が楽しめる。",
                description_en="Spectacular waterfalls in the Atlas Mountains, cascading 110 meters down rocky cliffs.",
                category="自然・滝",
                city="アズィラル",
                latitude=32.0167,
                longitude=-6.7167,
                image_url="https://example.com/ouzoud.jpg",
                best_time_to_visit="春・夏",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ラス・エル・マー岬",
                name_en="Cap Spartel",
                name_ar="رأس سبارطيل",
                description="アフリカ大陸北西端の岬。大西洋と地中海が出会う地点で灯台からの眺めが絶景。",
                description_en="The northwestern tip of Africa where the Atlantic and Mediterranean meet.",
                category="自然・岬",
                city="タンジェ",
                latitude=35.7931,
                longitude=-5.9244,
                image_url="https://example.com/cap_spartel.jpg",
                best_time_to_visit="夕方",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アル・アクサー・モスク",
                name_en="Kutubiyya Mosque",
                name_ar="جامع الكتبية",
                description="マラケシュのシンボル的存在の大モスク。77mの美しいミナレットが特徴的。",
                description_en="Marrakech's iconic mosque with a beautiful 77-meter minaret.",
                category="宗教建築",
                city="マラケシュ",
                latitude=31.6225,
                longitude=-7.9929,
                image_url="https://example.com/koutoubia.jpg",
                best_time_to_visit="夕方",
                entry_fee="無料（外観のみ）",
                opening_hours="外観は24時間"
            ),
            TourismSpot(
                name="ルグズのカスバ",
                name_en="Kasbah Taourirt",
                name_ar="قصبة تاوريرت",
                description="ワルザザードにある19世紀の要塞宮殿。映画のロケ地としても有名。",
                description_en="A 19th-century fortress palace in Ouarzazate, famous as a filming location.",
                category="歴史建築",
                city="ワルザザード",
                latitude=30.9189,
                longitude=-6.8936,
                image_url="https://example.com/taourirt.jpg",
                best_time_to_visit="午前中",
                entry_fee="20ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="アルガンの森",
                name_en="Argan Forest",
                name_ar="غابة الأركان",
                description="世界で唯一のアルガンオイルの産地。山羊が木に登る珍しい光景が見られる。",
                description_en="The world's only source of argan oil, famous for goats climbing trees.",
                category="自然・森林",
                city="エッサウィラ",
                latitude=31.1728,
                longitude=-9.4611,
                image_url="https://example.com/argan.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="サコマ庭園",
                name_en="Menara Gardens",
                name_ar="حدائق المنارة",
                description="マラケシュにある12世紀の庭園。オリーブ畑と池、アトラス山脈の眺めが美しい。",
                description_en="12th-century gardens in Marrakech with olive groves and Atlas Mountain views.",
                category="庭園・公園",
                city="マラケシュ",
                latitude=31.6014,
                longitude=-8.0367,
                image_url="https://example.com/menara.jpg",
                best_time_to_visit="夕方",
                entry_fee="無料",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="テトゥアン",
                name_en="Tetouan",
                name_ar="تطوان",
                description="「白い鳩」と呼ばれる美しい都市。アンダルシア建築の影響を受けた旧市街は世界遺産。",
                description_en="Known as 'White Dove', this city features Andalusian architecture and a UNESCO medina.",
                category="歴史都市",
                city="テトゥアン",
                latitude=35.5889,
                longitude=-5.3626,
                image_url="https://example.com/tetouan.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="アシラ",
                name_en="Asilah",
                name_ar="أصيلة",
                description="大西洋沿いの美しい港町。白壁にカラフルな壁画が描かれたアートの街。",
                description_en="A beautiful Atlantic port town known for colorful murals on white walls.",
                category="都市・アート",
                city="アシラ",
                latitude=35.4659,
                longitude=-6.0345,
                image_url="https://example.com/asilah.jpg",
                best_time_to_visit="春・夏",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ジベル・サグロ",
                name_en="Jebel Saghro",
                name_ar="جبل صاغرو",
                description="火山岩でできた独特な山域。トレッキングやベルベル文化体験ができる。",
                description_en="Unique volcanic mountain range offering trekking and Berber cultural experiences.",
                category="自然・山岳",
                city="ケルア・ムグーナ",
                latitude=31.1500,
                longitude=-6.0000,
                image_url="https://example.com/saghro.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="ガイド料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="フェズの皮なめし工場",
                name_en="Chouara Tannery",
                name_ar="دباغة شوارة",
                description="フェズ旧市街にある1000年以上の歴史を持つ世界最古の皮なめし工場。「シュアラ」と呼ばれるこの工場では、中世から変わらない伝統的な手法で羊、山羊、牛、ラクダの皮を加工しています。石灰、鳩の糞、塩、水を使った天然の薬剤で皮をなめし、ハンナ（ヘナ）、サフラン、ミント、インディゴなどの植物染料で美しい色に染め上げます。上から見下ろすと、直径数メートルの石造りの染色桶がハニカム状に並び、赤、黄、青、緑、茶色の鮮やかな色彩が印象的な光景を作り出しています。作業員が腰まで桶に浸かって皮を踏んで加工する光景は、まさに生きた中世の職人技。周囲の建物の屋上テラスから見学が可能で、工房では完成した革製品の購入もできます。強烈な匂いがするため、ミントの葉を鼻に当てるのが見学の際のコツです。",
                description_en="World's oldest tannery in Fez medina, operating for over 1000 years using unchanged medieval methods. The Chouara tannery processes sheep, goat, cow, and camel hides using natural agents like lime, pigeon droppings, salt, and water, then dyes them with plant-based colors including henna, saffron, mint, and indigo. Stone vats arranged in honeycomb patterns create a spectacular view from rooftop terraces, with workers waist-deep processing leather by foot.",
                category="工芸・産業",
                city="フェズ",
                latitude=34.0647,
                longitude=-4.9736,
                image_url="https://example.com/tannery.jpg",
                best_time_to_visit="午前中",
                entry_fee="チップ制",
                opening_hours="8:00-17:00"
            ),
            TourismSpot(
                name="アルーダ砂丘",
                name_en="Erg Chebbi",
                name_ar="عرق الشبي",
                description="メルズーガ近郊の美しい砂丘群。サハラ砂漠体験の拠点として人気。",
                description_en="Beautiful sand dunes near Merzouga, the gateway to Sahara Desert experiences.",
                category="自然・砂丘",
                city="メルズーガ",
                latitude=31.0969,
                longitude=-4.0133,
                image_url="https://example.com/erg_chebbi.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="ツアー料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="タンジェの旧市街",
                name_en="Tangier Medina",
                name_ar="المدينة القديمة طنجة",
                description="アフリカとヨーロッパの文化が交差する国際都市の歴史地区。",
                description_en="Historic quarter of the international city where African and European cultures meet.",
                category="歴史地区",
                city="タンジェ",
                latitude=35.7595,
                longitude=-5.8340,
                image_url="https://example.com/tangier_medina.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="M'ハミド砂漠",
                name_en="M'hamid Desert",
                name_ar="صحراء مهاميد",
                description="サハラ砂漠の入り口となる小さなオアシス村。静寂な砂漠体験ができる。",
                description_en="A small oasis village serving as gateway to the Sahara, offering peaceful desert experiences.",
                category="自然・オアシス",
                city="ムハミド",
                latitude=29.8167,
                longitude=-5.7167,
                image_url="https://example.com/mhamid.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="スコウラのカスバ",
                name_en="Kasbah Amridil",
                name_ar="قصبة أمريديل",
                description="ダデス川沿いにある保存状態の良いカスバ。ベルベル建築の傑作。",
                description_en="Well-preserved kasbah along the Dades River, a masterpiece of Berber architecture.",
                category="歴史建築",
                city="スコウラ",
                latitude=31.0500,
                longitude=-6.5667,
                image_url="https://example.com/amridil.jpg",
                best_time_to_visit="午前中",
                entry_fee="10ディルハム",
                opening_hours="8:00-18:00"
            ),
            TourismSpot(
                name="イミルシル湖",
                name_en="Lake Isli",
                name_ar="بحيرة إيسلي",
                description="アトラス山脈の高地にある美しい湖。ベルベルの結婚祭りで有名。",
                description_en="Beautiful high-altitude lake in the Atlas Mountains, famous for Berber marriage festival.",
                category="自然・湖",
                city="イミルシル",
                latitude=32.1500,
                longitude=-5.6167,
                image_url="https://example.com/isli.jpg",
                best_time_to_visit="夏・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ワリディア",
                name_en="Oualidia",
                name_ar="الوليدية",
                description="大西洋岸の美しいラグーン。牡蠣の養殖地として有名で、新鮮なシーフードが楽しめる。",
                description_en="Beautiful Atlantic lagoon famous for oyster farming and fresh seafood.",
                category="海岸・ラグーン",
                city="ワリディア",
                latitude=32.7333,
                longitude=-9.0333,
                image_url="https://example.com/oualidia.jpg",
                best_time_to_visit="春〜秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="トゥブカル山",
                name_en="Mount Toubkal",
                name_ar="جبل توبقال",
                description="北アフリカ最高峰（4,167m）。登山愛好家に人気のトレッキングスポット。",
                description_en="North Africa's highest peak at 4,167m, popular among trekking enthusiasts.",
                category="自然・山岳",
                city="イムリル",
                latitude=31.0592,
                longitude=-7.9167,
                image_url="https://example.com/toubkal.jpg",
                best_time_to_visit="5月〜9月",
                entry_fee="ガイド・許可証必要",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ナドール・ラグーン",
                name_en="Nador Lagoon",
                name_ar="بحيرة الناظور",
                description="地中海沿岸の大きなラグーン。バードウォッチングと自然観察の楽園。",
                description_en="Large Mediterranean lagoon, a paradise for birdwatching and nature observation.",
                category="自然・ラグーン",
                city="ナドール",
                latitude=35.1744,
                longitude=-2.9244,
                image_url="https://example.com/nador.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="リッシニの洞窟",
                name_en="Caves of Hercules",
                name_ar="مغارة هرقل",
                description="タンジェ近郊の神話に登場する洞窟。大西洋に開いた美しい洞窟口が有名。",
                description_en="Mythical caves near Tangier with a beautiful opening facing the Atlantic Ocean.",
                category="自然・洞窟",
                city="タンジェ",
                latitude=35.7867,
                longitude=-5.9289,
                image_url="https://example.com/hercules.jpg",
                best_time_to_visit="午前中",
                entry_fee="5ディルハム",
                opening_hours="9:00-19:00"
            ),
            TourismSpot(
                name="ベニ・メラル",
                name_en="Beni Mellal",
                name_ar="بني ملال",
                description="アトラス山脈の麓にある農業都市。美しいオリーブ畑とオレンジ畑が広がる。",
                description_en="Agricultural city at the foot of Atlas Mountains with beautiful olive and orange groves.",
                category="都市・農業",
                city="ベニ・メラル",
                latitude=32.3372,
                longitude=-6.3498,
                image_url="https://example.com/benimellal.jpg",
                best_time_to_visit="春・夏",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="クッキング・スクール・マラケシュ",
                name_en="Traditional Cooking School",
                name_ar="مدرسة الطبخ التقليدي",
                description="本格的なモロッコ料理を学べる料理教室。タジンやクスクスの作り方を体験。",
                description_en="Traditional cooking school where you can learn authentic Moroccan cuisine including tajine and couscous.",
                category="文化体験・料理",
                city="マラケシュ",
                latitude=31.6295,
                longitude=-7.9881,
                image_url="https://example.com/cooking.jpg",
                best_time_to_visit="通年",
                entry_fee="300-500ディルハム",
                opening_hours="予約制"
            ),
            TourismSpot(
                name="カサブランカ中央市場",
                name_en="Casablanca Central Market",
                name_ar="السوق المركزي الدار البيضاء",
                description="モロッコ最大の都市の活気ある市場。新鮮な食材から工芸品まで何でも揃う。",
                description_en="Vibrant market in Morocco's largest city with fresh produce and handicrafts.",
                category="市場・ショッピング",
                city="カサブランカ",
                latitude=33.5889,
                longitude=-7.6114,
                image_url="https://example.com/casa_market.jpg",
                best_time_to_visit="午前中",
                entry_fee="無料",
                opening_hours="8:00-20:00"
            ),
            TourismSpot(
                name="ベルベル村ホームステイ",
                name_en="Berber Village Homestay",
                name_ar="الإقامة في القرية الأمازيغية",
                description="アトラス山脈のベルベル村での宿泊体験。伝統的な生活様式を肌で感じられる。",
                description_en="Authentic homestay experience in Atlas Mountain Berber villages.",
                category="文化体験・宿泊",
                city="イムリル",
                latitude=31.1364,
                longitude=-7.9203,
                image_url="https://example.com/berber_village.jpg",
                best_time_to_visit="春〜秋",
                entry_fee="宿泊料金による",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ハマム（伝統浴場）",
                name_en="Traditional Hammam",
                name_ar="الحمام التقليدي",
                description="モロッコ伝統の公衆浴場。アルガンオイルを使った美容とリラクゼーション体験。",
                description_en="Traditional Moroccan bathhouse experience with argan oil treatments and relaxation.",
                category="文化体験・リラクゼーション",
                city="マラケシュ",
                latitude=31.6295,
                longitude=-7.9881,
                image_url="https://example.com/hammam.jpg",
                best_time_to_visit="通年",
                entry_fee="50-200ディルハム",
                opening_hours="8:00-22:00"
            ),
            TourismSpot(
                name="フェズ陶器工房",
                name_en="Fez Pottery Workshop",
                name_ar="ورشة الفخار فاس",
                description="フェズブルーで有名な陶器作りの工房見学。職人技を間近で見学できる。",
                description_en="Famous pottery workshop in Fez, known for Fez Blue ceramics and traditional craftsmanship.",
                category="工芸・文化体験",
                city="フェズ",
                latitude=34.0631,
                longitude=-4.9998,
                image_url="https://example.com/pottery.jpg",
                best_time_to_visit="午前中",
                entry_fee="無料（購入推奨）",
                opening_hours="9:00-18:00"
            ),
            TourismSpot(
                name="ローズバレー",
                name_en="Valley of Roses",
                name_ar="وادي الورود",
                description="アトラス山脈南麓の「薔薇の谷」として知られる美しい渓谷で、世界最高品質のダマスクローズ（ロサ・ダマスセナ）の産地。毎年5月中旬から6月上旬にかけて、谷全体がピンク色の花で染まり、濃厚で甘い香りに包まれます。この時期に開催される「バラ祭り（フェスティバル・ドゥ・ローズ）」では、バラの女王選出、伝統音楽の演奏、ローズウォーターやローズオイルの蒸留見学、地元特産品の販売が行われます。ベルベル人の農家では手摘みされたバラの花びらから、世界で最も価値の高いエッセンシャルオイルを伝統的な蒸留法で抽出。1キログラムのローズオイルを作るには約4トンの花びらが必要という貴重な製品です。谷間にはバラ畑、アーモンド畑、オリーブ畑が段々状に広がり、雪を頂いたアトラス山脈を背景とした絶景を楽しめます。バラ以外の時期でも、ベルベル村の伝統的な生活様式や手工芸品作りを見学できます。",
                description_en="Beautiful valley known as 'Valley of Roses' in the Atlas Mountains foothills, producing the world's finest Damascus roses (Rosa damascena). Every mid-May to early June, the entire valley turns pink with blooming roses and fills with intense, sweet fragrance. The annual 'Rose Festival' features rose queen selection, traditional music, rose water and oil distillation demonstrations, and local product sales. Berber farmers hand-pick petals to create precious essential oil using traditional distillation methods - requiring 4 tons of petals for 1kg of oil.",
                category="自然・農業",
                city="ケルア・ムグーナ",
                latitude=31.4167,
                longitude=-6.1833,
                image_url="https://example.com/roses.jpg",
                best_time_to_visit="5月（バラ祭り）",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ジャマ・エル・フナ広場の屋台街",
                name_en="Jemaa el-Fnaa Food Stalls",
                name_ar="أكشاك الطعام ساحة جامع الفنا",
                description="夜になると現れる屋台街。エスカルゴ、羊の脳みそなど珍しい料理も味わえる。",
                description_en="Evening food stalls offering exotic local dishes including snails and traditional delicacies.",
                category="グルメ・ストリートフード",
                city="マラケシュ",
                latitude=31.625901,
                longitude=-7.989161,
                image_url="https://example.com/food_stalls.jpg",
                best_time_to_visit="夜",
                entry_fee="料理代のみ",
                opening_hours="19:00-深夜"
            ),
            TourismSpot(
                name="カスバ・ウダイヤ博物館",
                name_en="Museum of Oudaias Kasbah",
                name_ar="متحف قصبة الأوداية",
                description="ラバトの要塞内にある博物館。モロッコの伝統工芸品や歴史的遺物を展示。",
                description_en="Museum inside Rabat's fortress showcasing Moroccan traditional crafts and historical artifacts.",
                category="博物館・歴史",
                city="ラバト",
                latitude=34.0242,
                longitude=-6.8417,
                image_url="https://example.com/oudaias_museum.jpg",
                best_time_to_visit="午前中",
                entry_fee="10ディルハム",
                opening_hours="9:00-17:00"
            ),
            TourismSpot(
                name="タフィラルト・オアシス",
                name_en="Tafilalet Oasis",
                name_ar="واحة تافيلالت",
                description="モロッコ最大のオアシス。ナツメヤシの森と伝統的な灌漑システムが見どころ。",
                description_en="Morocco's largest oasis featuring date palm forests and traditional irrigation systems.",
                category="自然・オアシス",
                city="エルラシディア",
                latitude=31.9314,
                longitude=-4.4267,
                image_url="https://example.com/tafilalet.jpg",
                best_time_to_visit="10月〜4月",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="ムーレイ・イドリス",
                name_en="Moulay Idriss",
                name_ar="مولاي إدريس",
                description="モロッコ建国の父とされる聖者の聖地。美しい白い街並みと聖廟が見どころ。",
                description_en="Holy city dedicated to the founder of Morocco, featuring beautiful white architecture and shrine.",
                category="宗教・聖地",
                city="ムーレイ・イドリス",
                latitude=34.0542,
                longitude=-5.5178,
                image_url="https://example.com/moulay_idriss.jpg",
                best_time_to_visit="春・秋",
                entry_fee="無料",
                opening_hours="24時間"
            ),
            TourismSpot(
                name="スキ・リゾート・ウカイメデン",
                name_en="Oukaimeden Ski Resort",
                name_ar="منتجع أوكايمدن للتزلج",
                description="アフリカで数少ないスキーリゾート。アトラス山脈の雪景色とスキーが楽しめる。",
                description_en="One of Africa's few ski resorts, offering skiing and snow activities in the Atlas Mountains.",
                category="スポーツ・レジャー",
                city="ウカイメデン",
                latitude=31.2056,
                longitude=-7.8589,
                image_url="https://example.com/ski.jpg",
                best_time_to_visit="12月〜3月",
                entry_fee="リフト料金による",
                opening_hours="8:00-17:00"
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
            ),
            TravelRoute(
                name="グルメ＆文化体験ツアー5日間",
                description="モロッコの食文化と伝統工芸を深く体験する美食の旅",
                duration_days=5,
                difficulty="Easy",
                route_data={
                    "cities": ["マラケシュ", "フェズ", "カサブランカ"],
                    "spots": [1, 33, 37, 5, 35, 34],
                    "daily_plan": {
                        "day1": "マラケシュ到着、ジャマ・エル・フナ広場屋台街体験",
                        "day2": "料理教室とハマム体験",
                        "day3": "フェズへ移動、陶器工房見学",
                        "day4": "カサブランカ、中央市場散策",
                        "day5": "帰国"
                    }
                }
            ),
            TravelRoute(
                name="ナチュラル・モロッコ8日間",
                description="自然と絶景を楽しむアウトドア重視の旅",
                duration_days=8,
                difficulty="Medium",
                route_data={
                    "cities": ["マラケシュ", "アズィラル", "イムリル", "エッサウィラ"],
                    "spots": [1, 21, 39, 14, 25, 26, 12],
                    "daily_plan": {
                        "day1": "マラケシュ到着",
                        "day2": "ウズドの滝トレッキング",
                        "day3-4": "アトラス山脈、トゥブカル山ベースキャンプ",
                        "day5": "ベルベル村ホームステイ体験",
                        "day6": "アルガンの森見学",
                        "day7": "エッサウィラでビーチリラックス",
                        "day8": "帰国"
                    }
                }
            ),
            TravelRoute(
                name="聖地巡礼とスピリチュアル体験6日間",
                description="モロッコの宗教的・スピリチュアルな側面を体験する心の旅",
                duration_days=6,
                difficulty="Easy",
                route_data={
                    "cities": ["カサブランカ", "ラバト", "ムーレイ・イドリス", "フェズ", "マラケシュ"],
                    "spots": [4, 10, 41, 19, 5, 23, 1],
                    "daily_plan": {
                        "day1": "カサブランカ、ハッサン2世モスク",
                        "day2": "ラバト観光、ウダイヤのカスバ",
                        "day3": "ムーレイ・イドリス聖地訪問、ヴォルビリス遺跡",
                        "day4": "フェズ、古い神学校見学",
                        "day5": "マラケシュ、クトゥビアモスク",
                        "day6": "ジャマ・エル・フナ広場で瞑想体験、帰国"
                    }
                }
            ),
            TravelRoute(
                name="アドベンチャー・エクストリーム12日間",
                description="サハラ砂漠からアトラス山脈まで、モロッコの大自然を制覇する冒険の旅",
                duration_days=12,
                difficulty="Hard",
                route_data={
                    "cities": ["マラケシュ", "ムハミド", "メルズーガ", "ティネリール", "イムリル"],
                    "spots": [1, 30, 31, 2, 13, 39, 14, 42],
                    "daily_plan": {
                        "day1": "マラケシュ到着",
                        "day2-3": "ムハミド砂漠キャンプ",
                        "day4-5": "アルーダ砂丘、サハラ砂漠縦断",
                        "day6": "トドラ渓谷ロッククライミング",
                        "day7-9": "トゥブカル山登頂チャレンジ",
                        "day10": "ウカイメデンでスキー体験",
                        "day11": "ベルベル村宿泊",
                        "day12": "マラケシュ経由帰国"
                    }
                }
            ),
            TravelRoute(
                name="アートとクリエイティブツアー4日間",
                description="モロッコの芸術と創造性を体験する文化的な旅",
                duration_days=4,
                difficulty="Easy",
                route_data={
                    "cities": ["アシラ", "テトゥアン", "タンジェ"],
                    "spots": [28, 27, 32, 29],
                    "daily_plan": {
                        "day1": "アシラ到着、壁画アート鑑賞",
                        "day2": "テトゥアン、アンダルシア建築見学",
                        "day3": "タンジェ旧市街散策、ヘラクレスの洞窟",
                        "day4": "ラス・エル・マー岬で夕日鑑賞、帰国"
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