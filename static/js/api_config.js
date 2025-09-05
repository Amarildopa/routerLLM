// 🔧 API Configuration - JavaScript para tela de configuração

class ApiConfigManager {
    constructor() {
        this.init();
    }

    init() {
        this.loadCurrentKeys();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Enter para salvar
        document.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.target.classList.contains('form-input')) {
                const provider = e.target.id.replace('Key', '');
                this.saveApiKey(provider);
            }
        });
    }

    async loadCurrentKeys() {
        console.log('🔍 Carregando chaves atuais...');
        
        try {
            const response = await fetch('/api-config/status');
            const data = await response.json();
            
            // Atualizar status de cada API
            this.updateApiStatus('openai', data.openai);
            this.updateApiStatus('anthropic', data.anthropic);
            this.updateApiStatus('google', data.google);
            
            // Atualizar status geral
            this.updateOverallStatus(data);
            
        } catch (error) {
            console.error('Erro ao carregar status:', error);
            this.showAlert('Erro ao carregar status das APIs', 'error');
        }
    }

    updateApiStatus(provider, status) {
        const statusElement = document.getElementById(`${provider}Status`);
        const keyInput = document.getElementById(`${provider}Key`);
        
        if (status.available) {
            statusElement.className = 'status-indicator connected';
            statusElement.innerHTML = '<i class="fas fa-check-circle"></i><span>Conectado</span>';
            keyInput.value = status.key ? this.maskKey(status.key) : '';
            keyInput.disabled = false;
        } else {
            statusElement.className = 'status-indicator disconnected';
            statusElement.innerHTML = '<i class="fas fa-times-circle"></i><span>Desconectado</span>';
            keyInput.value = '';
            keyInput.disabled = false;
        }
    }

    updateOverallStatus(data) {
        const connectedCount = Object.values(data).filter(api => api.available).length;
        const totalCount = Object.keys(data).length;
        
        const statusDot = document.getElementById('statusDot');
        const statusText = document.getElementById('statusText');
        
        if (connectedCount === totalCount) {
            statusDot.className = 'status-dot online';
            statusText.textContent = `Todas as APIs conectadas (${connectedCount}/${totalCount})`;
        } else if (connectedCount > 0) {
            statusDot.className = 'status-dot';
            statusText.textContent = `Parcialmente conectado (${connectedCount}/${totalCount})`;
        } else {
            statusDot.className = 'status-dot';
            statusText.textContent = 'Nenhuma API conectada';
        }
    }

    maskKey(key) {
        if (!key || key.length < 10) return key;
        return key.substring(0, 8) + '...' + key.substring(key.length - 4);
    }

    toggleVisibility(inputId) {
        const input = document.getElementById(inputId);
        const button = event.target;
        
        if (input.type === 'password') {
            input.type = 'text';
            button.innerHTML = '<i class="fas fa-eye-slash"></i> Ocultar';
        } else {
            input.type = 'password';
            button.innerHTML = '<i class="fas fa-eye"></i> Mostrar';
        }
    }

    async testApiKey(provider) {
        const keyInput = document.getElementById(`${provider}Key`);
        const key = keyInput.value.trim();
        
        if (!key) {
            this.showAlert('Digite uma chave de API para testar', 'warning');
            return;
        }

        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Testando...';
        button.disabled = true;

        try {
            const response = await fetch('/api-config/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider: provider,
                    api_key: key
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showAlert(`✅ ${provider.toUpperCase()} conectado com sucesso!`, 'success');
                this.updateApiStatus(provider, { available: true, key: key });
            } else {
                this.showAlert(`❌ Erro na conexão ${provider.toUpperCase()}: ${result.error}`, 'error');
            }

        } catch (error) {
            this.showAlert(`❌ Erro ao testar ${provider.toUpperCase()}: ${error.message}`, 'error');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async saveApiKey(provider) {
        const keyInput = document.getElementById(`${provider}Key`);
        const key = keyInput.value.trim();
        
        if (!key) {
            this.showAlert('Digite uma chave de API para salvar', 'warning');
            return;
        }

        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando...';
        button.disabled = true;

        try {
            const response = await fetch('/api-config/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    provider: provider,
                    api_key: key
                })
            });

            const result = await response.json();

            if (result.success) {
                this.showAlert(`✅ Chave ${provider.toUpperCase()} salva com sucesso!`, 'success');
                // Recarregar status após salvar
                setTimeout(() => this.loadCurrentKeys(), 1000);
            } else {
                this.showAlert(`❌ Erro ao salvar ${provider.toUpperCase()}: ${result.error}`, 'error');
            }

        } catch (error) {
            this.showAlert(`❌ Erro ao salvar ${provider.toUpperCase()}: ${error.message}`, 'error');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    async saveAllKeys() {
        const providers = ['openai', 'anthropic', 'google'];
        const keys = {};
        
        for (const provider of providers) {
            const key = document.getElementById(`${provider}Key`).value.trim();
            if (key) {
                keys[provider] = key;
            }
        }

        if (Object.keys(keys).length === 0) {
            this.showAlert('Nenhuma chave para salvar', 'warning');
            return;
        }

        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Salvando todas...';
        button.disabled = true;

        try {
            const response = await fetch('/api-config/save-all', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(keys)
            });

            const result = await response.json();

            if (result.success) {
                this.showAlert(`✅ ${result.saved_count} chaves salvas com sucesso!`, 'success');
                setTimeout(() => this.loadCurrentKeys(), 1000);
            } else {
                this.showAlert(`❌ Erro ao salvar chaves: ${result.error}`, 'error');
            }

        } catch (error) {
            this.showAlert(`❌ Erro ao salvar chaves: ${error.message}`, 'error');
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    showAlert(message, type = 'info') {
        // Remover alertas anteriores
        const existingAlerts = document.querySelectorAll('.alert-temp');
        existingAlerts.forEach(alert => alert.remove());

        // Criar novo alerta
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-temp`;
        alert.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : 'info-circle'}"></i>
            ${message}
        `;

        // Inserir no topo da página
        const container = document.querySelector('.config-container');
        container.insertBefore(alert, container.firstChild);

        // Remover após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
}

// Funções globais para compatibilidade com onclick
function toggleVisibility(inputId) {
    if (window.apiConfig) {
        window.apiConfig.toggleVisibility(inputId);
    }
}

function testApiKey(provider) {
    if (window.apiConfig) {
        window.apiConfig.testApiKey(provider);
    }
}

function saveApiKey(provider) {
    if (window.apiConfig) {
        window.apiConfig.saveApiKey(provider);
    }
}

function loadCurrentKeys() {
    if (window.apiConfig) {
        window.apiConfig.loadCurrentKeys();
    }
}

function saveAllKeys() {
    if (window.apiConfig) {
        window.apiConfig.saveAllKeys();
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.apiConfig = new ApiConfigManager();
});
