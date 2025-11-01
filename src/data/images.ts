// モロッコ旅行アプリの画像データベース

export interface ImageData {
  id: string
  url: string
  alt: string
  category: 'city' | 'culture' | 'cuisine' | 'landscape' | 'architecture'
  location?: string
  tags: string[]
  description?: string
}

export const moroccoImages: ImageData[] = [
  // マラケシュの画像
  {
    id: 'marrakech-panorama-user',
    url: '/images/marrakech-panorama.jpg',
    alt: 'マラケシュの赤い街並みとアトラス山脈の絶景パノラマ',
    category: 'city',
    location: 'マラケシュ',
    tags: ['パノラマ', '屋上', 'アトラス山脈', '赤い街', '絶景'],
    description: 'マラケシュの屋上から見た息を呑む美しい景色。赤い建物群の向こうに雪を被ったアトラス山脈が連なる、モロッコを代表する絶景です。'
  },
  {
    id: 'marrakech-jemaa-el-fnaa',
    url: 'https://res.cloudinary.com/dk0ndttcl/image/upload/t_main_visual.q_eco/v1/stw/grjebasj2c5fmtqrxoh1',
    alt: 'ジャマ・エル・フナ広場の夜景 - 赤いテントが並ぶ夜市',
    category: 'city',
    location: 'マラケシュ',
    tags: ['夜市', '広場', '伝統', '賑やか'],
    description: 'マラケシュの中心部にある世界的に有名な広場。夜になると食べ物の屋台や芸人が集まり、活気に満ちた雰囲気を楽しめます。'
  },
  {
    id: 'marrakech-medina',
    url: 'https://res.cloudinary.com/dk0ndttcl/image/upload/t_main_visual.q_eco/v1/stw/grjebasj2c5fmtqrxoh1',
    alt: 'マラケシュのメディナの路地',
    category: 'city',
    location: 'マラケシュ',
    tags: ['メディナ', '路地', '伝統建築', '迷路'],
    description: '赤い街マラケシュの旧市街。迷路のような路地には伝統的な店舗が軒を連ね、モロッコの歴史を感じることができます。'
  },
  {
    id: 'marrakech-majorelle',
    url: 'https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=400&h=250&fit=crop',
    alt: 'マジョレル庭園の美しい青い建物',
    category: 'city',
    location: 'マラケシュ',
    tags: ['庭園', '青', 'アート', 'イヴ・サンローラン'],
    description: 'フランス人画家ジャック・マジョレルが作った庭園。後にイヴ・サンローランが愛した美しい青色の建物と植物が印象的です。'
  },

  // カサブランカの画像
  {
    id: 'casablanca-hassan-ii-user',
    url: '/images/casablanca-hassan-ii.jpg',
    alt: 'カサブランカのハッサン2世モスクと海岸都市の風景',
    category: 'city',
    location: 'カサブランカ',
    tags: ['ハッサン2世モスク', '海岸', '現代都市', 'パノラマ', '大西洋'],
    description: '大西洋に面したカサブランカの壮大な景色。世界で3番目に大きなハッサン2世モスクと現代的な都市が美しく調和した風景です。'
  },
  {
    id: 'casablanca-hassan-ii',
    url: 'https://images.unsplash.com/photo-1555993539-1732b0258235?w=400&h=250&fit=crop',
    alt: 'ハッサン2世モスクの壮大な建築',
    category: 'architecture',
    location: 'カサブランカ',
    tags: ['モスク', '建築', '宗教', '現代'],
    description: '世界で3番目に大きなモスク。大西洋に面した壮大な建築で、現代モロッコの象徴的な建物です。'
  },
  {
    id: 'casablanca-corniche',
    url: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=250&fit=crop',
    alt: 'カサブランカの海岸線コルニッシュ',
    category: 'landscape',
    location: 'カサブランカ',
    tags: ['海岸', 'コルニッシュ', '散歩', '夕日'],
    description: '大西洋に面した美しい海岸線。夕日の時間帯には多くの人が散歩を楽しみ、ロマンチックな雰囲気が漂います。'
  },
  {
    id: 'casablanca-art-deco',
    url: 'https://images.unsplash.com/photo-1580662018303-2e0b5a9c9d36?w=400&h=250&fit=crop',
    alt: 'カサブランカのアールデコ建築',
    category: 'architecture',
    location: 'カサブランカ',
    tags: ['アールデコ', '建築', '歴史', 'フランス植民地時代'],
    description: 'フランス植民地時代に建てられたアールデコ様式の建物群。現代的な都市の中に歴史的な美しさが残されています。'
  },

  // フェズの画像
  {
    id: 'fez-tannery-user',
    url: '/images/fez-tannery.jpg',
    alt: 'フェズの伝統的な革なめし工場 - 色とりどりの染料桶',
    category: 'culture',
    location: 'フェズ',
    tags: ['革なめし', '染料', '伝統工芸', '職人', '古典技法'],
    description: '何世紀も変わらない伝統的な革なめしの技法。色とりどりの染料が並ぶ光景は、フェズの最も象徴的で印象的な風景の一つです。'
  },
  {
    id: 'fez-tannery',
    url: 'https://images.unsplash.com/photo-1561129568-ed5bb6acea97?w=400&h=250&fit=crop',
    alt: 'フェズの革なめし工場',
    category: 'culture',
    location: 'フェズ',
    tags: ['革', '伝統工芸', '職人', '古典'],
    description: '何世紀も変わらない伝統的な革なめしの技法。色とりどりの染料が並ぶ光景は、フェズの象徴的な風景です。'
  },
  {
    id: 'fez-medina',
    url: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=400&h=250&fit=crop&crop=bottom',
    alt: 'フェズ・エル・バリの迷路のような路地',
    category: 'city',
    location: 'フェズ',
    tags: ['メディナ', '迷路', '世界遺産', '中世'],
    description: '世界最大の自動車の入れない都市として知られるフェズ・エル・バリ。中世の雰囲気がそのまま残る迷路のような旧市街です。'
  },
  {
    id: 'fez-madrasa',
    url: 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400&h=250&fit=crop',
    alt: 'ブー・イナニア・マドラサの美しいタイル装飾',
    category: 'architecture',
    location: 'フェズ',
    tags: ['マドラサ', 'タイル', '装飾', 'イスラム建築'],
    description: '14世紀に建てられたイスラム神学校。精巧なタイル装飾と木彫りは、モロッコ建築の最高傑作の一つです。'
  },

  // シャウエンの画像
  {
    id: 'chefchaouen-blue-steps',
    url: 'https://images.unsplash.com/photo-1577717903315-1691ae25ab3f?w=400&h=250&fit=crop',
    alt: 'シャウエンの青い階段と美しい装飾',
    category: 'city',
    location: 'シャウエン',
    tags: ['青い街', '階段', 'インスタ映え', '山間部'],
    description: '「青い真珠」と呼ばれるシャウエンの象徴的な階段。青と白のコントラストが美しく、世界中の観光客を魅了します。'
  },
  {
    id: 'chefchaouen-streets',
    url: 'https://images.unsplash.com/photo-1518509562904-e7ef99cdcc86?w=400&h=250&fit=crop',
    alt: 'シャウエンの青い街並み',
    category: 'city',
    location: 'シャウエン',
    tags: ['青い街', '街並み', 'リフ山脈', '平和'],
    description: 'リフ山脈の麓にある美しい青い街。穏やかで平和な雰囲気は、多くの旅行者に癒しを提供します。'
  },

  // 料理の画像
  {
    id: 'tagine-dish-user',
    url: '/images/tagine-dish.jpg',
    alt: 'モロッコの伝統的なタジン料理 - 円錐形の蓋と色とりどりの小皿',
    category: 'cuisine',
    tags: ['タジン', '伝統料理', '土鍋', 'モロッコ料理', '家庭料理'],
    description: '伝統的なタジン鍋で作られた本格的なモロッコ料理。円錐形の蓋により水分が循環し、素材の旨味が凝縮された絶品料理です。'
  },
  {
    id: 'tagine-dish',
    url: 'https://images.unsplash.com/photo-1544736150-6f4a0b10d4e4?w=400&h=250&fit=crop',
    alt: 'モロッコの伝統料理タジン',
    category: 'cuisine',
    tags: ['タジン', '料理', '伝統', '土鍋'],
    description: '円錐形の蓋が特徴的なモロッコの代表料理。蒸し焼き効果で素材の旨味を最大限に引き出します。'
  },
  {
    id: 'couscous-user',
    url: '/images/couscous-dish.jpg',
    alt: 'モロッコの伝統的なクスクス - 牛肉と野菜の美しい盛り付け',
    category: 'cuisine',
    tags: ['クスクス', '牛肉', '野菜', '金曜日', '家族料理', '伝統陶器'],
    description: '美しいモロッコの青い陶器に盛られた本格的なクスクス。牛肉と色とりどりの野菜が見事に調和した、金曜日の家族団らんの象徴的な料理です。'
  },
  {
    id: 'couscous',
    url: 'https://images.unsplash.com/photo-1573160103600-9663fbf3e55b?w=400&h=250&fit=crop',
    alt: '金曜日の伝統料理クスクス',
    category: 'cuisine',
    tags: ['クスクス', '金曜日', '家族', '伝統'],
    description: 'セモリナ粉から作られる粒状のパスタ。金曜日に家族が集まって食べる大切な伝統料理です。'
  },
  {
    id: 'mint-tea-user',
    url: '/images/mint-tea.jpg',
    alt: 'モロッコの伝統的なミントティー - 透明なガラスのティーポットとカップ',
    category: 'cuisine',
    tags: ['ミントティー', '緑茶', 'ガラス', 'おもてなし', '伝統飲料'],
    description: '透明なガラスのティーポットで淹れられた美しい緑色のミントティー。モロッコのおもてなしの象徴として、ゲストを迎える際に必ず振る舞われる特別な飲み物です。'
  },
  {
    id: 'mint-tea',
    url: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=250&fit=crop',
    alt: 'モロッコの国民的飲み物ミントティー',
    category: 'cuisine',
    tags: ['ミントティー', '緑茶', 'おもてなし', '文化'],
    description: '緑茶にミントと砂糖を加えたモロッコの国民的飲み物。おもてなしの心を表す特別な飲み物です。'
  },

  // 文化・伝統工芸
  {
    id: 'traditional-crafts',
    url: 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=250&fit=crop',
    alt: 'モロッコの伝統工芸品',
    category: 'culture',
    tags: ['工芸品', '陶器', '手作り', '職人'],
    description: '熟練した職人によって作られるモロッコの美しい伝統工芸品。各地域で独特の技法と文様があります。'
  },

  // 風景
  {
    id: 'sahara-desert',
    url: 'https://images.unsplash.com/photo-1573160103600-9663fbf3e55b?w=400&h=250&fit=crop',
    alt: 'サハラ砂漠の砂丘',
    category: 'landscape',
    tags: ['砂漠', 'サハラ', '砂丘', '冒険'],
    description: '世界最大の砂漠サハラ。果てしなく続く砂丘は、人生で一度は見たい絶景です。'
  },
  {
    id: 'atlas-mountains',
    url: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=250&fit=crop',
    alt: 'アトラス山脈の雪景色',
    category: 'landscape',
    tags: ['山脈', 'アトラス', '雪', 'ハイキング'],
    description: 'モロッコを南北に走るアトラス山脈。冬には雪に覆われ、美しい景観を楽しめます。'
  },
  {
    id: 'essaouira-port',
    url: 'https://images.unsplash.com/photo-1591348669106-17979d7cb887?w=400&h=250&fit=crop',
    alt: 'エッサウィラの港町',
    category: 'city',
    location: 'エッサウィラ',
    tags: ['港町', '海', '城壁', 'シーフード'],
    description: '大西洋に面した美しい港町。中世の城壁に囲まれた旧市街と新鮮なシーフードが魅力です。'
  }
]

// カテゴリ別画像取得関数
export const getImagesByCategory = (category: ImageData['category']): ImageData[] => {
  return moroccoImages.filter(image => image.category === category)
}

// ロケーション別画像取得関数
export const getImagesByLocation = (location: string): ImageData[] => {
  return moroccoImages.filter(image => image.location === location)
}

// タグで画像検索関数
export const getImagesByTag = (tag: string): ImageData[] => {
  return moroccoImages.filter(image => image.tags.includes(tag))
}

// IDで特定の画像取得関数
export const getImageById = (id: string): ImageData | undefined => {
  return moroccoImages.find(image => image.id === id)
}

// ランダムに画像を取得する関数
export const getRandomImages = (count: number, category?: ImageData['category']): ImageData[] => {
  const sourceImages = category ? getImagesByCategory(category) : moroccoImages
  const shuffled = [...sourceImages].sort(() => 0.5 - Math.random())
  return shuffled.slice(0, count)
}