// モロッコ観光ガイドアプリ - メインJavaScript

class MoroccoGuideApp {
    constructor() {
        this.apiBase = '/api';
        this.currentLanguage = 'ja';
        this.favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
        this.init();
    }

    init() {
        // 共通初期化処理
        this.setupEventListeners();
        this.loadUserPreferences();
    }

    setupEventListeners() {
        // 検索フォーム
        const searchForm = document.getElementById('searchForm');
        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.performSearch();
            });
        }

        // お気に入りボタン
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('favorite-btn')) {
                this.toggleFavorite(e.target);
            }
        });
    }

    loadUserPreferences() {
        // ローカルストレージから設定を読み込み
        const savedLanguage = localStorage.getItem('language');
        if (savedLanguage) {
            this.currentLanguage = savedLanguage;
        }
    }

    // API呼び出し
    async apiCall(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.apiBase}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API call failed:', error);
            this.showError('データの取得に失敗しました');
            throw error;
        }
    }

    // 観光スポット関連
    async loadSpots(category = null, search = null) {
        let endpoint = '/spots/';
        const params = new URLSearchParams();
        
        if (category) params.append('category', category);
        if (search) params.append('q', search);
        
        if (params.toString()) {
            endpoint += `search?${params}`;
        }

        try {
            const data = await this.apiCall(endpoint);
            return data.data || [];
        } catch (error) {
            return [];
        }
    }

    async getSpotDetail(spotId) {
        try {
            const data = await this.apiCall(`/spots/${spotId}`);
            return data.data;
        } catch (error) {
            return null;
        }
    }

    // チャット機能
    async sendChatMessage(message) {
        try {
            const data = await this.apiCall('/chat/message', {
                method: 'POST',
                body: JSON.stringify({ message })
            });
            return data.response;
        } catch (error) {
            return 'エラーが発生しました。もう一度お試しください。';
        }
    }

    // お気に入り機能
    toggleFavorite(button) {
        const spotId = button.dataset.spotId;
        const isActive = button.classList.contains('active');
        
        if (isActive) {
            this.removeFavorite(spotId);
            button.classList.remove('active');
            button.innerHTML = '<i class="far fa-heart"></i>';
        } else {
            this.addFavorite(spotId);
            button.classList.add('active');
            button.innerHTML = '<i class="fas fa-heart"></i>';
        }
    }

    addFavorite(spotId) {
        if (!this.favorites.includes(spotId)) {
            this.favorites.push(spotId);
            this.saveFavorites();
        }
    }

    removeFavorite(spotId) {
        this.favorites = this.favorites.filter(id => id !== spotId);
        this.saveFavorites();
    }

    saveFavorites() {
        localStorage.setItem('favorites', JSON.stringify(this.favorites));
    }

    isFavorite(spotId) {
        return this.favorites.includes(spotId);
    }

    // UI ヘルパー
    showLoading(element) {
        element.innerHTML = '<div class="loading"></div>';
    }

    showError(message) {
        // Bootstrap Toast またはアラートを表示
        console.error(message);
        alert(message); // 簡易実装
    }

    showSuccess(message) {
        console.log(message);
        // 成功メッセージの表示
    }

    // 検索機能
    performSearch() {
        const searchInput = document.getElementById('searchInput');
        const query = searchInput?.value?.trim();
        
        if (query) {
            this.loadSpots(null, query).then(spots => {
                this.displaySearchResults(spots);
            });
        }
    }

    displaySearchResults(spots) {
        // 検索結果を表示する実装
        console.log('Search results:', spots);
    }

    // 地図関連
    async loadMapMarkers() {
        try {
            const data = await this.apiCall('/maps/markers');
            return data.markers || [];
        } catch (error) {
            return [];
        }
    }

    // 言語切り替え
    setLanguage(lang) {
        this.currentLanguage = lang;
        localStorage.setItem('language', lang);
        // ページリロードまたは動的言語切り替え
        location.reload();
    }

    // ユーティリティ
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ja-JP');
    }

    formatCurrency(amount, currency = 'MAD') {
        return new Intl.NumberFormat('ja-JP', {
            style: 'currency',
            currency: currency === 'MAD' ? 'USD' : currency // MADが対応していない場合USDで表示
        }).format(amount);
    }

    // 星評価表示
    renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        
        let stars = '';
        stars += '<i class="fas fa-star text-warning"></i>'.repeat(fullStars);
        if (hasHalfStar) stars += '<i class="fas fa-star-half-alt text-warning"></i>';
        stars += '<i class="far fa-star text-warning"></i>'.repeat(emptyStars);
        
        return stars;
    }
}

// アプリケーション初期化
const app = new MoroccoGuideApp();

// グローバル関数（テンプレートから呼び出し用）
function searchSpots() {
    app.performSearch();
}

function filterByCategory(category) {
    app.loadSpots(category).then(spots => {
        app.displaySearchResults(spots);
    });
}

function viewSpotDetail(spotId) {
    window.location.href = `/spots#${spotId}`;
}

function showMap() {
    const mapModal = new bootstrap.Modal(document.getElementById('mapModal'));
    mapModal.show();
    
    // 地図の初期化処理をここに追加
    if (typeof initMap === 'function') {
        initMap();
    }
}

// ページ読み込み完了時の処理
document.addEventListener('DOMContentLoaded', function() {
    console.log('🇲🇦 モロッコ観光ガイドアプリが初期化されました');
});