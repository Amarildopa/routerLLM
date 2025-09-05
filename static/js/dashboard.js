// 🚀 RouterLLM Dashboard - JavaScript para funcionalidades em tempo real

class RouterDashboard {
    constructor() {
        this.charts = {};
        this.updateInterval = null;
        this.init();
    }

    init() {
        this.setupCharts();
        this.startRealTimeUpdates();
        this.setupEventListeners();
        this.loadInitialData();
    }

    setupCharts() {
        // Gráfico de uso por modelo
        const modelUsageCtx = document.getElementById('modelUsageChart').getContext('2d');
        this.charts.modelUsage = new Chart(modelUsageCtx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#667eea',
                        '#764ba2',
                        '#f093fb',
                        '#f5576c',
                        '#4facfe'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 20,
                            usePointStyle: true
                        }
                    }
                }
            }
        });

        // Gráfico de custo por hora
        const costCtx = document.getElementById('costChart').getContext('2d');
        this.charts.cost = new Chart(costCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Custo (USD)',
                    data: [],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '$' + value.toFixed(4);
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Teste da API
        document.getElementById('testButton').addEventListener('click', () => {
            this.testAPI();
        });

        // Enter no textarea
        document.getElementById('testMessage').addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                this.testAPI();
            }
        });
    }

    async loadInitialData() {
        try {
            await this.updateStats();
            await this.updateModels();
            await this.updateActivity();
            this.setStatus('online');
        } catch (error) {
            console.error('Erro ao carregar dados iniciais:', error);
            this.setStatus('offline');
        }
    }

    startRealTimeUpdates() {
        // Atualizar a cada 5 segundos
        this.updateInterval = setInterval(() => {
            this.updateStats();
            this.updateModels();
            this.updateActivity();
        }, 5000);
    }

    async updateStats() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            
            document.getElementById('totalRequests').textContent = data.total_requests || 0;
            document.getElementById('totalCost').textContent = `$${(data.total_cost || 0).toFixed(4)}`;
            document.getElementById('avgResponseTime').textContent = `${Math.round((data.avg_response_time || 0) * 1000)}ms`;
            
            // Atualizar gráfico de uso por modelo
            this.updateModelUsageChart(data.model_usage || {});
            
        } catch (error) {
            console.error('Erro ao atualizar estatísticas:', error);
        }
    }

    async updateModels() {
        try {
            const response = await fetch('/models');
            const data = await response.json();
            
            const modelsGrid = document.getElementById('modelsGrid');
            modelsGrid.innerHTML = '';
            
            let activeCount = 0;
            
            for (const [modelName, modelData] of Object.entries(data.models)) {
                const isAvailable = modelData.available;
                if (isAvailable) activeCount++;
                
                const modelCard = document.createElement('div');
                modelCard.className = `model-card ${isAvailable ? 'available' : 'unavailable'}`;
                
                modelCard.innerHTML = `
                    <h4>${modelName}</h4>
                    <div class="model-status">
                        <i class="fas fa-${isAvailable ? 'check-circle' : 'times-circle'}"></i>
                        <span>${isAvailable ? 'Disponível' : 'Indisponível'}</span>
                    </div>
                    <p>Custo: $${modelData.cost_per_1k_tokens}/1k tokens</p>
                    <p>Velocidade: ${modelData.speed}</p>
                `;
                
                modelsGrid.appendChild(modelCard);
            }
            
            document.getElementById('activeModels').textContent = activeCount;
            
        } catch (error) {
            console.error('Erro ao atualizar modelos:', error);
        }
    }

    async updateActivity() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            
            // Simular atividade recente (em produção, isso viria de um endpoint específico)
            const activities = this.generateMockActivity(data);
            this.displayActivity(activities);
            
        } catch (error) {
            console.error('Erro ao atualizar atividade:', error);
        }
    }

    generateMockActivity(stats) {
        const activities = [];
        const now = new Date();
        
        // Adicionar algumas atividades baseadas nas estatísticas
        if (stats.total_requests > 0) {
            activities.push({
                type: 'success',
                title: 'Request processado',
                description: `Modelo: ${stats.most_used_model || 'N/A'}`,
                time: new Date(now.getTime() - Math.random() * 300000) // Últimos 5 min
            });
        }
        
        if (stats.total_cost > 0) {
            activities.push({
                type: 'info',
                title: 'Custo atualizado',
                description: `Total: $${stats.total_cost.toFixed(4)}`,
                time: new Date(now.getTime() - Math.random() * 600000) // Últimos 10 min
            });
        }
        
        return activities.slice(0, 5); // Máximo 5 atividades
    }

    displayActivity(activities) {
        const activityList = document.getElementById('activityList');
        activityList.innerHTML = '';
        
        if (activities.length === 0) {
            activityList.innerHTML = '<p style="text-align: center; color: #718096; padding: 2rem;">Nenhuma atividade recente</p>';
            return;
        }
        
        activities.forEach(activity => {
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            
            const timeAgo = this.getTimeAgo(activity.time);
            
            activityItem.innerHTML = `
                <div class="activity-icon ${activity.type}">
                    <i class="fas fa-${this.getActivityIcon(activity.type)}"></i>
                </div>
                <div class="activity-content">
                    <h4>${activity.title}</h4>
                    <p>${activity.description} • ${timeAgo}</p>
                </div>
            `;
            
            activityList.appendChild(activityItem);
        });
    }

    getActivityIcon(type) {
        const icons = {
            success: 'check',
            error: 'times',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    getTimeAgo(date) {
        const now = new Date();
        const diff = now - date;
        const minutes = Math.floor(diff / 60000);
        
        if (minutes < 1) return 'Agora mesmo';
        if (minutes < 60) return `${minutes}min atrás`;
        
        const hours = Math.floor(minutes / 60);
        if (hours < 24) return `${hours}h atrás`;
        
        const days = Math.floor(hours / 24);
        return `${days}d atrás`;
    }

    updateModelUsageChart(modelUsage) {
        const labels = Object.keys(modelUsage);
        const data = Object.values(modelUsage);
        
        this.charts.modelUsage.data.labels = labels;
        this.charts.modelUsage.data.datasets[0].data = data;
        this.charts.modelUsage.update();
    }

    async testAPI() {
        const message = document.getElementById('testMessage').value.trim();
        const forceModel = document.getElementById('forceModel').value;
        const testResult = document.getElementById('testResult');
        
        if (!message) {
            alert('Digite uma mensagem para testar!');
            return;
        }
        
        const testButton = document.getElementById('testButton');
        testButton.disabled = true;
        testButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testando...';
        
        try {
            const payload = { message };
            if (forceModel) payload.force_model = forceModel;
            
            const startTime = Date.now();
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });
            
            const endTime = Date.now();
            const data = await response.json();
            
            if (response.ok) {
                testResult.innerHTML = `
                    <h4><i class="fas fa-check-circle" style="color: #38a169;"></i> Teste bem-sucedido!</h4>
                    <p><strong>Modelo usado:</strong> ${data.model_used}</p>
                    <p><strong>Raciocínio:</strong> ${data.reasoning}</p>
                    <p><strong>Custo:</strong> $${data.cost_estimate.toFixed(4)}</p>
                    <p><strong>Tempo:</strong> ${data.response_time.toFixed(2)}s</p>
                    <p><strong>Tokens:</strong> ${data.tokens_used}</p>
                    <p><strong>Resposta:</strong> ${data.response.substring(0, 200)}${data.response.length > 200 ? '...' : ''}</p>
                `;
            } else {
                testResult.innerHTML = `
                    <h4><i class="fas fa-times-circle" style="color: #e53e3e;"></i> Erro no teste</h4>
                    <p>${data.detail || 'Erro desconhecido'}</p>
                `;
            }
            
        } catch (error) {
            testResult.innerHTML = `
                <h4><i class="fas fa-times-circle" style="color: #e53e3e;"></i> Erro de conexão</h4>
                <p>${error.message}</p>
            `;
        } finally {
            testButton.disabled = false;
            testButton.innerHTML = '<i class="fas fa-paper-plane"></i> Testar';
            testResult.classList.add('show');
            
            // Atualizar estatísticas após o teste
            this.updateStats();
        }
    }

    setStatus(status) {
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        if (status === 'online') {
            statusDot.classList.add('online');
            statusText.textContent = 'Online';
        } else {
            statusDot.classList.remove('online');
            statusText.textContent = 'Offline';
        }
    }

    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Inicializar dashboard quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new RouterDashboard();
});

// Função global para teste da API (compatibilidade)
function testAPI() {
    if (window.dashboard) {
        window.dashboard.testAPI();
    }
}
