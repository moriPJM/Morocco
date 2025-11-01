/**
 * リアルタイム情報表示機能
 */

class RealtimeInfoWidget {
    constructor() {
        this.container = null;
        this.updateInterval = 300000; // 5分間隔で更新
        this.intervalId = null;
        this.init();
    }

    init() {
        this.createWidget();
        this.loadInitialData();
        this.startAutoUpdate();
    }

    createWidget() {
        // リアルタイム情報ウィジェットの作成
        const widget = document.createElement('div');
        widget.id = 'realtime-widget';
        widget.className = 'realtime-widget position-fixed';
        widget.style.cssText = `
            top: 20px;
            right: 20px;
            width: 320px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            z-index: 1000;
            font-size: 0.85rem;
            max-height: 500px;
            overflow-y: auto;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        widget.innerHTML = `
            <div class="p-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <h6 class="mb-0 fw-bold text-primary">
                        <i class="fas fa-globe-africa me-2"></i>リアルタイム情報
                    </h6>
                    <div>
                        <button class="btn btn-sm btn-outline-secondary me-1" onclick="realtimeWidget.refresh()" title="更新">
                            <i class="fas fa-sync-alt"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="realtimeWidget.toggle()" title="閉じる">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
                
                <div id="realtime-content">
                    <div class="text-center py-3">
                        <div class="spinner-border spinner-border-sm text-primary" role="status">
                            <span class="visually-hidden">読み込み中...</span>
                        </div>
                        <p class="small mt-2 mb-0">情報を取得中...</p>
                    </div>
                </div>
                
                <div class="text-center mt-2">
                    <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>
                        <span id="last-update">--</span>
                    </small>
                </div>
            </div>
        `;

        document.body.appendChild(widget);
        this.container = widget;

        // 表示トグルボタンの作成
        this.createToggleButton();
    }

    createToggleButton() {
        const toggleBtn = document.createElement('button');
        toggleBtn.id = 'realtime-toggle';
        toggleBtn.className = 'btn btn-primary btn-sm position-fixed';
        toggleBtn.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 999;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        `;
        toggleBtn.innerHTML = '<i class="fas fa-globe-africa"></i>';
        toggleBtn.title = 'リアルタイム情報を表示';
        toggleBtn.onclick = () => this.toggle();

        document.body.appendChild(toggleBtn);
    }

    async loadInitialData() {
        try {
            const response = await fetch('/api/chat/realtime-info');
            const data = await response.json();

            if (data.success) {
                this.displayData(data.data);
                this.updateTimestamp();
            } else {
                this.showError('情報の取得に失敗しました');
            }
        } catch (error) {
            console.error('Realtime data loading error:', error);
            this.showError('接続エラーが発生しました');
        }
    }

    displayData(data) {
        const content = document.getElementById('realtime-content');
        
        let html = '';

        // 天気情報
        if (data.weather) {
            const weather = data.weather;
            html += `
                <div class="mb-3">
                    <h6 class="fw-bold text-primary mb-2">
                        <i class="fas fa-cloud-sun me-2"></i>${weather.city} 天気
                    </h6>
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <span class="h5 mb-0">${weather.temperature}°C</span>
                            <small class="text-muted ms-1">(体感${weather.feels_like}°C)</small>
                        </div>
                        <div class="text-end">
                            <div class="small">${weather.description}</div>
                            <div class="small text-muted">湿度${weather.humidity}%</div>
                        </div>
                    </div>
                </div>
            `;
        }

        // 為替情報
        if (data.exchange_rates) {
            const rates = data.exchange_rates;
            html += `
                <div class="mb-3">
                    <h6 class="fw-bold text-success mb-2">
                        <i class="fas fa-exchange-alt me-2"></i>為替レート
                    </h6>
                    <div class="row g-2">
                        <div class="col-4">
                            <div class="text-center small">
                                <div class="fw-bold">1円</div>
                                <div class="text-primary">${rates.jpy_to_mad}MAD</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="text-center small">
                                <div class="fw-bold">1USD</div>
                                <div class="text-primary">${rates.usd_to_mad}MAD</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="text-center small">
                                <div class="fw-bold">1EUR</div>
                                <div class="text-primary">${rates.eur_to_mad}MAD</div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // 安全情報
        if (data.travel_advisories) {
            const safety = data.travel_advisories;
            html += `
                <div class="mb-3">
                    <h6 class="fw-bold text-warning mb-2">
                        <i class="fas fa-shield-alt me-2"></i>安全情報
                    </h6>
                    <div class="small">
                        <div class="mb-1"><strong>${safety.safety_level}</strong></div>
                        <div class="text-muted">${safety.general_advice[0]}</div>
                    </div>
                </div>
            `;
        }

        // イベント情報
        if (data.events && data.events.length > 0) {
            html += `
                <div class="mb-3">
                    <h6 class="fw-bold text-info mb-2">
                        <i class="fas fa-calendar-alt me-2"></i>イベント
                    </h6>
                    <div class="small">
            `;
            
            data.events.slice(0, 2).forEach(event => {
                html += `
                    <div class="mb-1">
                        <div class="fw-bold">${event.name}</div>
                        <div class="text-muted">${event.location} • ${event.period}</div>
                    </div>
                `;
            });
            
            html += '</div></div>';
        }

        content.innerHTML = html;
    }

    showError(message) {
        const content = document.getElementById('realtime-content');
        content.innerHTML = `
            <div class="text-center py-3 text-danger">
                <i class="fas fa-exclamation-triangle mb-2"></i>
                <p class="small mb-0">${message}</p>
            </div>
        `;
    }

    updateTimestamp() {
        const timestamp = document.getElementById('last-update');
        if (timestamp) {
            const now = new Date();
            timestamp.textContent = now.toLocaleTimeString('ja-JP', {
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    }

    toggle() {
        const widget = this.container;
        const toggleBtn = document.getElementById('realtime-toggle');
        
        if (widget.style.transform === 'translateX(0%)') {
            widget.style.transform = 'translateX(100%)';
            toggleBtn.style.display = 'block';
        } else {
            widget.style.transform = 'translateX(0%)';
            toggleBtn.style.display = 'none';
        }
    }

    async refresh() {
        const refreshBtn = document.querySelector('#realtime-widget .fa-sync-alt');
        if (refreshBtn) {
            refreshBtn.classList.add('fa-spin');
        }

        try {
            await this.loadInitialData();
        } finally {
            if (refreshBtn) {
                refreshBtn.classList.remove('fa-spin');
            }
        }
    }

    startAutoUpdate() {
        this.intervalId = setInterval(() => {
            this.loadInitialData();
        }, this.updateInterval);
    }

    stopAutoUpdate() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    destroy() {
        this.stopAutoUpdate();
        if (this.container) {
            this.container.remove();
        }
        const toggleBtn = document.getElementById('realtime-toggle');
        if (toggleBtn) {
            toggleBtn.remove();
        }
    }
}

// グローバル変数として初期化
let realtimeWidget = null;

// ページ読み込み完了後に初期化
document.addEventListener('DOMContentLoaded', function() {
    // 少し遅延させて他の初期化が完了してから実行
    setTimeout(() => {
        if (typeof RealtimeInfoWidget !== 'undefined') {
            realtimeWidget = new RealtimeInfoWidget();
        }
    }, 1000);
});

// ページ離脱時のクリーンアップ
window.addEventListener('beforeunload', function() {
    if (realtimeWidget) {
        realtimeWidget.destroy();
    }
});