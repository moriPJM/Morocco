import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

const resources = {
  ja: {
    translation: {
      navigation: {
        home: 'ホーム',
        translator: '翻訳',
        guides: 'ガイド',
        map: 'マップ',
        favorites: 'お気に入り'
      },
      home: {
        welcome: 'モロッコへようこそ',
        subtitle: '究極の旅行コンパニオン',
        description: 'リアルタイム翻訳と現地の情報を特徴とする包括的な旅行ガイドで、モロッコの魔法を発見してください。',
        featuresTitle: '機能',
        featuresSubtitle: 'モロッコ旅行に必要なすべて',
        ctaTitle: 'モロッコを探索する準備はできましたか？',
        ctaSubtitle: '今すぐ旅を始めましょう。',
        ctaDescription: '包括的な旅行コンパニオンでモロッコの美しさと文化を発見してください。'
      },
      translator: {
        title: '言語翻訳',
        selectSource: '翻訳元言語を選択',
        selectTarget: '翻訳先言語を選択',
        enterText: '翻訳するテキストを入力...',
        translate: '翻訳する',
        swap: '言語を入れ替え',
        commonPhrases: 'よく使うフレーズ',
        clickToInsert: 'クリックして入力欄に挿入',
        translating: '翻訳中...',
        resultPlaceholder: '翻訳結果がここに表示されます...'
      },
      guides: {
        title: '旅行ガイド',
        cities: '都市',
        culture: '文化',
        cuisine: '料理',
        attractions: '観光地',
        subtitle: 'モロッコを探索するための包括的なガイド',
        travelTips: '旅行のコツ',
        bestTimeTitle: '訪問のベストタイム',
        bestTimeDesc: '春（3-5月）と秋（9-11月）が過ごしやすい気候です',
        cultureTitle: '文化的エチケット',
        cultureDesc: '特に宗教的な場所を訪れる際は控えめな服装を心がけましょう',
        citiesTitle: '都市ガイド',
        cuisineTitle: '料理ガイド',
        infoTitle: '基本情報',
        currencyTitle: '通貨',
        currencyDesc: 'モロッコディルハム（MAD）- 都市部ではATMが広く利用できます',
        languageTitle: '言語',
        languageDesc: 'アラビア語とベルベル語が公用語、フランス語も広く話されています'
      },
      languages: {
        english: '英語',
        arabic: 'アラビア語',
        french: 'フランス語',
        berber: 'ベルベル語（タマジグト語）',
        japanese: '日本語'
      },
      features: {
        translator: {
          title: '言語翻訳',
          description: 'アラビア語、フランス語、ベルベル語、英語、日本語間でテキストを翻訳'
        },
        guides: {
          title: '旅行ガイド',
          description: 'モロッコの都市、文化、料理に関する包括的なガイド'
        },
        maps: {
          title: 'インタラクティブマップ',
          description: '詳細なマップと観光地でモロッコをナビゲート'
        },
        favorites: {
          title: 'お気に入り',
          description: 'お気に入りの場所や情報を保存してクイックアクセス'
        }
      },
      map: {
        title: 'モロッコのインタラクティブマップ',
        subtitle: '主要都市と観光地を探索',
        legend: '凡例',
        majorCities: '主要都市',
        coastalCities: '沿岸都市',
        featuredDestinations: '注目の目的地',
        cities: {
          marrakech: 'マラケシュ',
          marrakechDesc: '赤い街 - 歴史的なメディナと活気あるスーク',
          casablanca: 'カサブランカ',
          casablancaDesc: '経済の中心地とハッサン2世モスク',
          fez: 'フェズ',
          fezDesc: '古代メディナのある帝都',
          rabat: 'ラバト',
          rabatDesc: '王宮のある首都',
          chefchaouen: 'シャウエン',
          chefchaouenDesc: 'リフ山脈の青い真珠',
          essaouira: 'エッサウィラ',
          essaouiraDesc: 'ポルトガル建築の沿岸都市'
        }
      },
      favorites: {
        title: 'お気に入り',
        subtitle: '保存した場所、フレーズ、ガイド',
        noFavoritesTitle: 'お気に入りがありません',
        noFavoritesDesc: 'モロッコを探索して、お気に入りの場所、フレーズ、ガイドをここに保存しましょう！',
        quickActions: 'クイックアクション',
        explorePlaces: '場所を探索',
        explorePlacesDesc: '新しい目的地を発見',
        learnPhrases: 'フレーズを学習',
        learnPhrasesDesc: '便利な翻訳を追加',
        browseGuides: 'ガイドを閲覧',
        browseGuidesDesc: '旅行のコツを保存',
        removeFromFavorites: 'お気に入りから削除',
        sampleItems: {
          place: 'ジャマ・エル・フナ広場',
          placeDesc: 'マラケシュ メディナの中央広場',
          phrase: 'مرحباً بكم في المغرب',
          phraseDesc: 'モロッコへようこそ',
          guide: 'ミントティーの儀式',
          guideDesc: '伝統的なお茶の準備ガイド',
          guideContent: '本格的なモロッコのミントティーの準備手順'
        }
      }
    }
  },
  en: {
    translation: {
      navigation: {
        home: 'Home',
        translator: 'Translator',
        guides: 'Guides',
        map: 'Map',
        favorites: 'Favorites'
      },
      home: {
        welcome: 'Welcome to Morocco',
        subtitle: 'Your Ultimate Travel Companion',
        description: 'Discover the magic of Morocco with our comprehensive travel guide, featuring real-time translation and local insights.'
      },
      translator: {
        title: 'Language Translator',
        selectSource: 'Select source language',
        selectTarget: 'Select target language',
        enterText: 'Enter text to translate...',
        translate: 'Translate',
        swap: 'Swap languages'
      },
      guides: {
        title: 'Travel Guides',
        cities: 'Cities',
        culture: 'Culture',
        cuisine: 'Cuisine',
        attractions: 'Attractions'
      },
      languages: {
        english: 'English',
        arabic: 'Arabic',
        french: 'French',
        berber: 'Berber (Tamazight)',
        japanese: 'Japanese'
      },
      features: {
        translator: {
          title: 'Language Translator',
          description: 'Translate text between Arabic, French, Berber, English, and Japanese'
        },
        guides: {
          title: 'Travel Guides',
          description: 'Comprehensive guides about Moroccan cities, culture, and cuisine'
        },
        maps: {
          title: 'Interactive Maps',
          description: 'Navigate Morocco with detailed maps and points of interest'
        },
        favorites: {
          title: 'Favorites',
          description: 'Save your favorite places and information for quick access'
        }
      }
    }
  },
  fr: {
    translation: {
      navigation: {
        home: 'Accueil',
        translator: 'Traducteur',
        guides: 'Guides',
        map: 'Carte',
        favorites: 'Favoris'
      },
      home: {
        welcome: 'Bienvenue au Maroc',
        subtitle: 'Votre Compagnon de Voyage Ultime',
        description: 'Découvrez la magie du Maroc avec notre guide de voyage complet, avec traduction en temps réel et conseils locaux.'
      },
      translator: {
        title: 'Traducteur de Langue',
        selectSource: 'Sélectionnez la langue source',
        selectTarget: 'Sélectionnez la langue cible',
        enterText: 'Entrez le texte à traduire...',
        translate: 'Traduire',
        swap: 'Échanger les langues'
      },
      guides: {
        title: 'Guides de Voyage',
        cities: 'Villes',
        culture: 'Culture',
        cuisine: 'Cuisine',
        attractions: 'Attractions'
      },
      languages: {
        english: 'Anglais',
        arabic: 'Arabe',
        french: 'Français',
        berber: 'Berbère (Tamazight)'
      }
    }
  },
  ar: {
    translation: {
      navigation: {
        home: 'الرئيسية',
        translator: 'المترجم',
        guides: 'الأدلة',
        map: 'الخريطة',
        favorites: 'المفضلة'
      },
      home: {
        welcome: 'مرحباً بكم في المغرب',
        subtitle: 'رفيقكم المثالي في السفر',
        description: 'اكتشفوا سحر المغرب مع دليل السفر الشامل، مع ترجمة فورية ونصائح محلية.'
      },
      translator: {
        title: 'مترجم اللغة',
        selectSource: 'اختر اللغة المصدر',
        selectTarget: 'اختر اللغة الهدف',
        enterText: 'أدخل النص للترجمة...',
        translate: 'ترجم',
        swap: 'تبديل اللغات'
      },
      guides: {
        title: 'أدلة السفر',
        cities: 'المدن',
        culture: 'الثقافة',
        cuisine: 'المأكولات',
        attractions: 'المعالم السياحية'
      },
      languages: {
        english: 'الإنجليزية',
        arabic: 'العربية',
        french: 'الفرنسية',
        berber: 'الأمازيغية'
      }
    }
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'ja',
    lng: 'ja',
    debug: true,
    interpolation: {
      escapeValue: false,
    },
  })

export default i18n