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

    // 検索機能とカテゴリーフィルター
    async performSearch() {
        const searchInput = document.getElementById('searchInput');
        const query = searchInput?.value?.trim();
        
        if (!query) {
            this.showError('検索キーワードを入力してください');
            return;
        }
        
        // ローディング表示
        this.showSearchLoading();
        
        try {
            const spots = await this.loadSpots(null, query);
            this.displaySearchResults(spots, query);
            
            // 検索履歴を保存（ローカルストレージ）
            this.saveSearchHistory(query);
        } catch (error) {
            this.showError('検索中にエラーが発生しました');
        }
    }

    async filterByCategory(category) {
        console.log('Filtering by category:', category);
        this.showSearchLoading();
        try {
            // カテゴリーでの検索はcategoryパラメータを使用
            const endpoint = `/spots/search?category=${encodeURIComponent(category)}`;
            console.log('API endpoint:', endpoint);
            const data = await this.apiCall(endpoint);
            console.log('API response:', data);
            const spots = data.data || [];
            console.log('Filtered spots count:', spots.length);
            this.displaySearchResults(spots, null, category);
        } catch (error) {
            console.error('Category filter error:', error);
            this.showError('カテゴリーフィルター中にエラーが発生しました');
        }
    }

    async filterByCity(city) {
        console.log('Filtering by city:', city);
        this.showSearchLoading();
        try {
            // 都市での検索はcityパラメータを使用
            const endpoint = `/spots/search?city=${encodeURIComponent(city)}`;
            console.log('API endpoint:', endpoint);
            const data = await this.apiCall(endpoint);
            console.log('API response:', data);
            const spots = data.data || [];
            console.log('Filtered spots count:', spots.length);
            this.displaySearchResults(spots, null, null, city);
        } catch (error) {
            console.error('City filter error:', error);
            this.showError('都市フィルター中にエラーが発生しました');
        }
    }

    saveSearchHistory(query) {
        let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
        history = history.filter(h => h !== query); // 重複削除
        history.unshift(query); // 先頭に追加
        history = history.slice(0, 10); // 最新10件まで
        localStorage.setItem('searchHistory', JSON.stringify(history));
    }

    getSearchHistory() {
        return JSON.parse(localStorage.getItem('searchHistory') || '[]');
    }

    showSearchLoading() {
        const container = document.getElementById('recommendedSpots') || document.getElementById('searchResults');
        if (container) {
            container.innerHTML = `
                <div class="col-12 text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">検索中...</span>
                    </div>
                    <p class="mt-2 text-muted">検索中...</p>
                </div>
            `;
        }
    }

    displaySearchResults(spots, query, category, city) {
        // 検索結果表示用のコンテナを準備
        let container = document.getElementById('searchResults');
        if (!container) {
            // 検索結果コンテナが存在しない場合は作成
            const mainContainer = document.getElementById('recommendedSpots')?.parentElement;
            if (mainContainer) {
                container = document.createElement('div');
                container.id = 'searchResults';
                container.className = 'row';
                mainContainer.appendChild(container);
                
                // おすすめスポットを隠す
                const recommendedContainer = document.getElementById('recommendedSpots')?.parentElement;
                if (recommendedContainer) {
                    recommendedContainer.style.display = 'none';
                }
            }
        }
        
        if (!container) return;
        
        // 検索結果なしの場合
        if (spots.length === 0) {
            const searchTerm = query || category || city;
            let searchType = '検索';
            if (category) searchType = 'カテゴリー';
            if (city) searchType = '都市';
            
            container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h4 class="text-muted">${searchType}結果が見つかりませんでした</h4>
                    <p class="text-muted">「${searchTerm}」に関する観光スポットが見つかりませんでした。<br>
                    別のキーワードで検索してみてください。</p>
                    
                    <div class="mt-4">
                        <h6 class="text-muted mb-3">おすすめキーワード:</h6>
                        <div class="d-flex flex-wrap justify-content-center gap-2">
                            <button class="btn btn-outline-primary btn-sm" onclick="app.searchSuggestion('マラケシュ')">マラケシュ</button>
                            <button class="btn btn-outline-primary btn-sm" onclick="app.searchSuggestion('フェズ')">フェズ</button>
                            <button class="btn btn-outline-primary btn-sm" onclick="app.searchSuggestion('サハラ砂漠')">サハラ砂漠</button>
                            <button class="btn btn-outline-primary btn-sm" onclick="app.searchSuggestion('タジン')">タジン料理</button>
                        </div>
                    </div>
                    
                    <button class="btn btn-primary mt-3" onclick="clearSearch()">
                        <i class="fas fa-arrow-left me-2"></i>おすすめスポットに戻る
                    </button>
                </div>
            `;
            return;
        }
        
        // 検索結果ヘッダー
        const searchTerm = query || category || city;
        let resultType = '検索結果';
        let icon = 'search';
        
        if (category) {
            resultType = 'カテゴリー検索';
            icon = 'filter';
        } else if (city) {
            resultType = '都市検索';
            icon = 'map-marker-alt';
        }
        
        let html = `
            <div class="col-12 mb-3">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <h4 class="mb-1">
                            <i class="fas fa-${icon} text-primary me-2"></i>
                            ${resultType}: "${searchTerm}"
                        </h4>
                        <p class="text-muted small mb-0">${spots.length}件の観光スポットが見つかりました</p>
                    </div>
                    <div>
                        <button class="btn btn-outline-secondary btn-sm me-2" onclick="clearSearch()">
                            <i class="fas fa-times me-1"></i>クリア
                        </button>
                        <div class="dropdown d-inline">
                            <button class="btn btn-outline-primary btn-sm dropdown-toggle" type="button" data-bs-toggle="dropdown">
                                <i class="fas fa-sort me-1"></i>並び替え
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="#" onclick="app.sortResults('relevance')">関連度順</a></li>
                                <li><a class="dropdown-item" href="#" onclick="app.sortResults('name')">名前順</a></li>
                                <li><a class="dropdown-item" href="#" onclick="app.sortResults('city')">都市順</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
                <hr class="my-3">
            </div>
        `;
        
        // 検索結果を表示
        spots.forEach(spot => {
            const isFav = this.isFavorite(spot.id.toString());
            const relevanceScore = spot.relevance_score || 0;
            
            html += `
                <div class="col-lg-4 col-md-6 mb-3">
                    <div class="card h-100 border-0 shadow-sm search-result-card position-relative">
                        ${relevanceScore > 80 ? '<div class="badge bg-success position-absolute top-0 end-0 m-2 z-index-1">高関連度</div>' : ''}
                        ${spot.image_url ? `
                            <img src="${spot.image_url}" class="card-img-top" alt="${spot.name}" style="height: 200px; object-fit: cover;">
                        ` : `
                            <div class="card-img-top bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                                <i class="fas fa-image fa-2x text-muted"></i>
                            </div>
                        `}
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h6 class="card-title fw-bold text-primary mb-0">${spot.name}</h6>
                                <button class="btn btn-sm favorite-btn ${isFav ? 'active' : ''}" 
                                        data-spot-id="${spot.id}" onclick="app.toggleFavorite(${spot.id})">
                                    <i class="fas fa-heart"></i>
                                </button>
                            </div>
                            <div class="mb-2">
                                <span class="badge bg-secondary me-1">${spot.category}</span>
                                <span class="badge bg-info">${spot.city}</span>
                                ${relevanceScore > 0 ? `<span class="badge bg-success ms-1">${relevanceScore}%</span>` : ''}
                            </div>
                            <p class="card-text text-muted small">${this.truncateText(spot.description, 100)}</p>
                            ${spot.entry_fee ? `<p class="small text-success mb-1"><i class="fas fa-ticket-alt me-1"></i>${spot.entry_fee}</p>` : ''}
                            ${spot.opening_hours ? `<p class="small text-warning mb-1"><i class="fas fa-clock me-1"></i>${spot.opening_hours}</p>` : ''}
                        </div>
                        <div class="card-footer bg-transparent border-0 pt-0">
                            <button class="btn btn-primary btn-sm w-100" onclick="viewSpotDetail(${spot.id})">
                                <i class="fas fa-info-circle me-1"></i>詳細を見る
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });
        
        container.innerHTML = html;
        
        // 検索結果にスクロール
        container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    searchSuggestion(keyword) {
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.value = keyword;
            this.performSearch();
        }
    }

    sortResults(sortBy) {
        // 現在の検索結果を取得して再ソート
        const container = document.getElementById('searchResults');
        if (!container) return;
        
        // 実装は簡略化 - 実際には検索APIに再度リクエストする
        console.log('Sorting by:', sortBy);
    }

    truncateText(text, maxLength) {
        if (!text) return '';
        return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
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


}

// アプリケーション初期化
const app = new MoroccoGuideApp();

// グローバル関数（テンプレートから呼び出し用）
function searchSpots() {
    app.performSearch();
}

function filterByCategory(category) {
    app.filterByCategory(category);
}

function filterByCity(city) {
    app.filterByCity(city);
}

function viewSpotDetail(spotId) {
    window.location.href = `/spots#${spotId}`;
}

function toggleFavorite(spotId) {
    app.toggleFavorite({ dataset: { spotId: spotId.toString() } });
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