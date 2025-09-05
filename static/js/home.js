// 🏠 Home Chat - JavaScript para interface de chat

class HomeChat {
    constructor() {
        this.messageCount = 0;
        this.totalCost = 0;
        this.totalTime = 0;
        this.totalTokens = 0;
        this.currentModel = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadCurrentModel();
        this.autoResizeTextarea();
        this.initTheme();
    }

    setupEventListeners() {
        const chatInput = document.getElementById('chatInput');
        const sendBtn = document.getElementById('sendBtn');

        // Enter para enviar (Ctrl+Enter)
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Enter para nova linha (sem Ctrl)
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.ctrlKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            this.autoResizeTextarea();
        });

        // Botão de enviar
        sendBtn.addEventListener('click', () => {
            this.sendMessage();
        });
    }

    autoResizeTextarea() {
        const textarea = document.getElementById('chatInput');
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
    }

    async loadCurrentModel() {
        try {
            const response = await fetch('/models');
            const data = await response.json();
            
            // Encontrar o modelo padrão disponível
            const availableModels = Object.entries(data.models)
                .filter(([name, info]) => info.available)
                .map(([name, info]) => ({ name, ...info }));

            if (availableModels.length > 0) {
                this.currentModel = availableModels[0];
                this.updateModelIndicator(this.currentModel);
            } else {
                this.updateModelIndicator({ name: 'Nenhum modelo disponível', provider: 'none' });
            }
        } catch (error) {
            console.error('Erro ao carregar modelos:', error);
            this.updateModelIndicator({ name: 'Erro ao carregar', provider: 'error' });
        }
    }

    updateModelIndicator(model) {
        const modelName = document.getElementById('modelName');
        const modelIcon = document.getElementById('modelIcon');
        
        modelName.textContent = model.name;
        
        // Atualizar ícone baseado no provider
        const iconMap = {
            'openai': 'fab fa-openai',
            'anthropic': 'fas fa-robot',
            'google': 'fab fa-google',
            'none': 'fas fa-exclamation-triangle',
            'error': 'fas fa-times-circle'
        };
        
        const iconClass = iconMap[model.provider] || 'fas fa-brain';
        modelIcon.className = `model-icon ${model.provider}`;
        modelIcon.innerHTML = `<i class="${iconClass}"></i>`;
    }

    async sendMessage() {
        const chatInput = document.getElementById('chatInput');
        const message = chatInput.value.trim();
        
        if (!message) return;

        // Limpar input
        chatInput.value = '';
        this.autoResizeTextarea();

        // Adicionar mensagem do usuário
        this.addMessage('user', message);

        // Mostrar indicador de digitação
        this.showTypingIndicator();

        // Desabilitar botão
        const sendBtn = document.getElementById('sendBtn');
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    user_id: 'home_user'
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Adicionar resposta do assistente
                this.addMessage('assistant', data.response, {
                    model: data.model_used,
                    reasoning: data.reasoning,
                    cost: data.cost_estimate,
                    time: data.response_time,
                    tokens: data.tokens_used
                });

                // Atualizar estatísticas
                this.updateStats(data.cost_estimate, data.response_time, data.tokens_used);

                // Atualizar modelo atual se mudou
                if (data.model_used !== this.currentModel?.name) {
                    this.currentModel = { name: data.model_used, provider: this.getProviderFromModel(data.model_used) };
                    this.updateModelIndicator(this.currentModel);
                }
            } else {
                this.addMessage('assistant', `❌ Erro: ${data.detail || 'Erro desconhecido'}`, { isError: true });
            }

        } catch (error) {
            this.addMessage('assistant', `❌ Erro de conexão: ${error.message}`, { isError: true });
        } finally {
            // Ocultar indicador de digitação
            this.hideTypingIndicator();
            
            // Reabilitar botão
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
        }
    }

    addMessage(type, content, metadata = {}) {
        const chatMessages = document.getElementById('chatMessages');
        
        // Remover mensagem de boas-vindas se existir
        const welcomeMessage = chatMessages.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'message-bubble';
        bubbleDiv.textContent = content;

        const metaDiv = document.createElement('div');
        metaDiv.className = 'message-meta';

        if (type === 'assistant' && metadata.model) {
            const modelBadge = document.createElement('span');
            modelBadge.className = 'model-badge';
            modelBadge.innerHTML = `<i class="fas fa-brain"></i> ${metadata.model}`;
            metaDiv.appendChild(modelBadge);
        }

        if (metadata.cost) {
            const costSpan = document.createElement('span');
            costSpan.innerHTML = `💰 $${metadata.cost.toFixed(6)}`;
            metaDiv.appendChild(costSpan);
        }

        if (metadata.time) {
            const timeSpan = document.createElement('span');
            timeSpan.innerHTML = `⏱️ ${metadata.time.toFixed(2)}s`;
            metaDiv.appendChild(timeSpan);
        }

        if (metadata.tokens) {
            const tokensSpan = document.createElement('span');
            tokensSpan.innerHTML = `🔢 ${metadata.tokens} tokens`;
            metaDiv.appendChild(tokensSpan);
        }

        contentDiv.appendChild(bubbleDiv);
        contentDiv.appendChild(metaDiv);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Atualizar contador de mensagens
        if (type === 'user') {
            this.messageCount++;
            this.updateMessageCount();
        }
    }

    updateStats(cost, time, tokens) {
        this.totalCost += cost;
        this.totalTime += time;
        this.totalTokens += tokens;

        document.getElementById('totalCost').textContent = `$${this.totalCost.toFixed(6)}`;
        document.getElementById('tokensUsed').textContent = `${this.totalTokens} tokens`;
        
        if (this.messageCount > 0) {
            const avgTime = this.totalTime / this.messageCount;
            document.getElementById('avgTime').textContent = `${avgTime.toFixed(1)}s`;
        }
    }

    updateMessageCount() {
        document.getElementById('messageCount').textContent = `${this.messageCount} mensagens`;
    }

    showTypingIndicator() {
        document.getElementById('typingIndicator').style.display = 'flex';
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    hideTypingIndicator() {
        document.getElementById('typingIndicator').style.display = 'none';
    }

    getProviderFromModel(modelName) {
        if (modelName.includes('gpt')) return 'openai';
        if (modelName.includes('claude')) return 'anthropic';
        if (modelName.includes('gemini')) return 'google';
        return 'unknown';
    }

    initTheme() {
        // Carregar tema salvo ou usar preferência do sistema
        const savedTheme = localStorage.getItem('routerllm-theme');
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        const theme = savedTheme || systemTheme;
        
        this.setTheme(theme);
        
        // Configurar toggle
        const themeToggle = document.getElementById('themeToggle');
        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('routerllm-theme', theme);
        
        // Atualizar ícone do toggle
        const themeIcon = document.getElementById('themeIcon');
        if (theme === 'dark') {
            themeIcon.className = 'fas fa-moon';
            themeIcon.style.color = '#fbbf24';
        } else {
            themeIcon.className = 'fas fa-sun';
            themeIcon.style.color = '#f59e0b';
        }
    }
}

// Função global para ações rápidas
function sendQuickMessage(message) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = message;
    if (window.homeChat) {
        window.homeChat.sendMessage();
    }
}

// Função global para enviar mensagem
function sendMessage() {
    if (window.homeChat) {
        window.homeChat.sendMessage();
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.homeChat = new HomeChat();
});
