/* 
   JAVASCRIPT PRINCIPAL - app.js
   =============================
   
   Arquivo JavaScript principal da Adega Rádio Tatuapé FM
   
   Conceitos abordados:
   - JavaScript ES6+
   - DOM manipulation
   - Event handling
   - AJAX/Fetch API
   - Local Storage
   - Error handling
   - Utility functions
*/

// CONFIGURAÇÕES GLOBAIS
// =====================
const ADEGA_CONFIG = {
    // URLs da API
    API_BASE: window.location.origin,
    WHATSAPP_NUMBER: '5511970603441',
    PIX_EMAIL: 'radiotatuapefm@gmail.com',
    
    // Configurações de UI
    TOAST_DURATION: 3000,
    LOADING_MIN_TIME: 500,
    
    // Debugging
    DEBUG: true,
    
    // Mensagens
    MESSAGES: {
        CARRINHO_VAZIO: 'Carrinho vazio',
        PRODUTO_ADICIONADO: 'Produto adicionado ao carrinho!',
        PRODUTO_REMOVIDO: 'Produto removido do carrinho',
        ERRO_CONEXAO: 'Erro de conexão. Tente novamente.',
        ERRO_GENERICO: 'Algo deu errado. Tente novamente.',
        CONFIRMACAO_REMOCAO: 'Tem certeza que deseja remover este item?',
        PIX_COPIADO: 'Chave PIX copiada!'
    }
};

// UTILITÁRIOS GLOBAIS
// ===================

/**
 * Utilitário para logging com controle de debug
 */
const Logger = {
    log: (message, data = null) => {
        if (ADEGA_CONFIG.DEBUG) {
            console.log(`[ADEGA] ${message}`, data || '');
        }
    },
    
    error: (message, error = null) => {
        if (ADEGA_CONFIG.DEBUG) {
            console.error(`[ADEGA ERROR] ${message}`, error || '');
        }
    },
    
    warn: (message, data = null) => {
        if (ADEGA_CONFIG.DEBUG) {
            console.warn(`[ADEGA WARN] ${message}`, data || '');
        }
    }
};

/**
 * Utilitários para formatação
 */
const Formatter = {
    /**
     * Formata valor como moeda brasileira
     * @param {number} value - Valor a ser formatado
     * @returns {string} Valor formatado
     */
    currency: (value) => {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },
    
    /**
     * Formata telefone brasileiro
     * @param {string} phone - Telefone a ser formatado
     * @returns {string} Telefone formatado
     */
    phone: (phone) => {
        const cleaned = phone.replace(/\D/g, '');
        
        if (cleaned.length === 11) {
            return cleaned.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
        } else if (cleaned.length === 10) {
            return cleaned.replace(/^(\d{2})(\d{4})(\d{4}).*/, '($1) $2-$3');
        }
        
        return phone;
    },
    
    /**
     * Formata data brasileira
     * @param {Date|string} date - Data a ser formatada
     * @returns {string} Data formatada
     */
    date: (date) => {
        const d = new Date(date);
        return d.toLocaleDateString('pt-BR');
    },
    
    /**
     * Formata data e hora brasileira
     * @param {Date|string} datetime - Data/hora a ser formatada
     * @returns {string} Data/hora formatada
     */
    datetime: (datetime) => {
        const d = new Date(datetime);
        return d.toLocaleString('pt-BR');
    }
};

/**
 * Utilitários para validação
 */
const Validator = {
    /**
     * Valida email
     */
    email: (email) => {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },
    
    /**
     * Valida telefone brasileiro
     */
    phone: (phone) => {
        const cleaned = phone.replace(/\D/g, '');
        return cleaned.length >= 10 && cleaned.length <= 11;
    },
    
    /**
     * Valida se string não está vazia
     */
    required: (value) => {
        return value && value.trim().length > 0;
    },
    
    /**
     * Valida comprimento mínimo
     */
    minLength: (value, min) => {
        return value && value.trim().length >= min;
    }
};

/**
 * Utilitários para Local Storage
 */
const Storage = {
    /**
     * Salva item no localStorage
     */
    set: (key, value) => {
        try {
            localStorage.setItem(`adega_${key}`, JSON.stringify(value));
            return true;
        } catch (error) {
            Logger.error('Erro ao salvar no localStorage', error);
            return false;
        }
    },
    
    /**
     * Recupera item do localStorage
     */
    get: (key, defaultValue = null) => {
        try {
            const item = localStorage.getItem(`adega_${key}`);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            Logger.error('Erro ao ler do localStorage', error);
            return defaultValue;
        }
    },
    
    /**
     * Remove item do localStorage
     */
    remove: (key) => {
        try {
            localStorage.removeItem(`adega_${key}`);
            return true;
        } catch (error) {
            Logger.error('Erro ao remover do localStorage', error);
            return false;
        }
    },
    
    /**
     * Limpa todos os dados da adega do localStorage
     */
    clear: () => {
        try {
            const keys = Object.keys(localStorage).filter(key => key.startsWith('adega_'));
            keys.forEach(key => localStorage.removeItem(key));
            return true;
        } catch (error) {
            Logger.error('Erro ao limpar localStorage', error);
            return false;
        }
    }
};

// SISTEMA DE NOTIFICAÇÕES
// =======================

/**
 * Sistema de notificações toast
 */
class NotificationSystem {
    constructor() {
        this.container = null;
        this.init();
    }
    
    /**
     * Inicializa o sistema
     */
    init() {
        this.createContainer();
    }
    
    /**
     * Cria container para as notificações
     */
    createContainer() {
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.className = 'position-fixed';
            this.container.style.cssText = `
                top: 20px;
                right: 20px;
                z-index: 1050;
                max-width: 350px;
            `;
            document.body.appendChild(this.container);
        }
    }
    
    /**
     * Exibe notificação
     * @param {string} message - Mensagem
     * @param {string} type - Tipo (success, error, warning, info)
     * @param {number} duration - Duração em ms
     */
    show(message, type = 'info', duration = ADEGA_CONFIG.TOAST_DURATION) {
        const toast = this.createToast(message, type);
        this.container.appendChild(toast);
        
        // Anima entrada
        requestAnimationFrame(() => {
            toast.classList.add('show');
        });
        
        // Remove automaticamente
        if (duration > 0) {
            setTimeout(() => {
                this.remove(toast);
            }, duration);
        }
        
        return toast;
    }
    
    /**
     * Cria elemento toast
     */
    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `alert alert-${this.getAlertClass(type)} alert-dismissible fade mb-2`;
        toast.style.cssText = 'margin-bottom: 10px;';
        
        toast.innerHTML = `
            <i class="fas fa-${this.getIcon(type)} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-dismiss="toast"></button>
        `;
        
        // Event listener para fechar
        const closeBtn = toast.querySelector('.btn-close');
        closeBtn.addEventListener('click', () => {
            this.remove(toast);
        });
        
        return toast;
    }
    
    /**
     * Remove toast
     */
    remove(toast) {
        if (toast && toast.parentNode) {
            toast.classList.remove('show');
            toast.classList.add('fade');
            
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 150);
        }
    }
    
    /**
     * Obtém classe do Bootstrap para o tipo
     */
    getAlertClass(type) {
        const classes = {
            success: 'success',
            error: 'danger',
            warning: 'warning',
            info: 'info'
        };
        return classes[type] || 'info';
    }
    
    /**
     * Obtém ícone para o tipo
     */
    getIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    // Métodos de conveniência
    success(message, duration) { return this.show(message, 'success', duration); }
    error(message, duration) { return this.show(message, 'error', duration); }
    warning(message, duration) { return this.show(message, 'warning', duration); }
    info(message, duration) { return this.show(message, 'info', duration); }
}

// SISTEMA DE LOADING
// ==================

/**
 * Sistema de loading global
 */
class LoadingSystem {
    constructor() {
        this.overlay = null;
        this.activeRequests = 0;
    }
    
    /**
     * Mostra loading
     */
    show(message = 'Carregando...') {
        this.activeRequests++;
        
        if (!this.overlay) {
            this.createOverlay(message);
        } else {
            this.updateMessage(message);
        }
        
        this.overlay.style.display = 'flex';
    }
    
    /**
     * Esconde loading
     */
    hide() {
        this.activeRequests = Math.max(0, this.activeRequests - 1);
        
        if (this.activeRequests === 0 && this.overlay) {
            this.overlay.style.display = 'none';
        }
    }
    
    /**
     * Força esconder (para casos de erro)
     */
    forceHide() {
        this.activeRequests = 0;
        if (this.overlay) {
            this.overlay.style.display = 'none';
        }
    }
    
    /**
     * Cria overlay de loading
     */
    createOverlay(message) {
        this.overlay = document.createElement('div');
        this.overlay.id = 'loading-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            flex-direction: column;
        `;
        
        this.overlay.innerHTML = `
            <div class="loading-spinner mb-3"></div>
            <div class="text-white" id="loading-message">${message}</div>
        `;
        
        document.body.appendChild(this.overlay);
    }
    
    /**
     * Atualiza mensagem do loading
     */
    updateMessage(message) {
        const messageEl = this.overlay?.querySelector('#loading-message');
        if (messageEl) {
            messageEl.textContent = message;
        }
    }
}

// SISTEMA HTTP
// ============

/**
 * Sistema HTTP para requisições AJAX
 */
class HttpClient {
    constructor() {
        this.baseURL = ADEGA_CONFIG.API_BASE;
        this.loading = new LoadingSystem();
    }
    
    /**
     * Requisição GET
     */
    async get(url, options = {}) {
        return this.request(url, { ...options, method: 'GET' });
    }
    
    /**
     * Requisição POST
     */
    async post(url, data = null, options = {}) {
        return this.request(url, {
            ...options,
            method: 'POST',
            body: data ? JSON.stringify(data) : null,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
    }
    
    /**
     * Requisição PUT
     */
    async put(url, data = null, options = {}) {
        return this.request(url, {
            ...options,
            method: 'PUT',
            body: data ? JSON.stringify(data) : null,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
    }
    
    /**
     * Requisição DELETE
     */
    async delete(url, options = {}) {
        return this.request(url, { ...options, method: 'DELETE' });
    }
    
    /**
     * Requisição genérica
     */
    async request(url, options = {}) {
        const fullURL = url.startsWith('http') ? url : `${this.baseURL}${url}`;
        
        // Mostra loading se não especificado o contrário
        if (options.showLoading !== false) {
            this.loading.show();
        }
        
        try {
            Logger.log(`HTTP ${options.method || 'GET'}`, fullURL);
            
            const response = await fetch(fullURL, {
                ...options,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    ...options.headers
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
            }
            
            const contentType = response.headers.get('Content-Type');
            let data;
            
            if (contentType && contentType.includes('application/json')) {
                data = await response.json();
            } else {
                data = await response.text();
            }
            
            Logger.log('HTTP Response', data);
            return data;
            
        } catch (error) {
            Logger.error('HTTP Error', error);
            throw error;
        } finally {
            if (options.showLoading !== false) {
                this.loading.hide();
            }
        }
    }
}

// INSTÂNCIAS GLOBAIS
// ==================
const notifications = new NotificationSystem();
const loading = new LoadingSystem();
const http = new HttpClient();

// FUNÇÕES GLOBAIS DE CONVENIÊNCIA
// ===============================

/**
 * Mostra notificação de sucesso
 */
function showSuccess(message, duration) {
    return notifications.success(message, duration);
}

/**
 * Mostra notificação de erro
 */
function showError(message, duration) {
    return notifications.error(message, duration);
}

/**
 * Mostra notificação de aviso
 */
function showWarning(message, duration) {
    return notifications.warning(message, duration);
}

/**
 * Mostra notificação informativa
 */
function showInfo(message, duration) {
    return notifications.info(message, duration);
}

/**
 * Copia texto para clipboard
 */
async function copyToClipboard(text, successMessage = 'Copiado!') {
    try {
        if (navigator.clipboard) {
            await navigator.clipboard.writeText(text);
        } else {
            // Fallback para navegadores antigos
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            document.execCommand('copy');
            textArea.remove();
        }
        
        showSuccess(successMessage);
        return true;
        
    } catch (error) {
        Logger.error('Erro ao copiar para clipboard', error);
        showError('Erro ao copiar. Tente copiar manualmente.');
        return false;
    }
}

/**
 * Formata moeda brasileira
 */
function formatCurrency(value) {
    return Formatter.currency(value);
}

/**
 * Debounce para otimizar eventos
 */
function debounce(func, wait, immediate = false) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func.apply(this, args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func.apply(this, args);
    };
}

/**
 * Throttle para otimizar eventos
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// INICIALIZAÇÃO
// =============

/**
 * Inicializa aplicação quando DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    Logger.log('Aplicação inicializada');
    
    // Inicializa funcionalidades globais
    initGlobalFeatures();
    
    // Event listeners globais
    setupGlobalEventListeners();
    
    // Detecta páginas específicas e inicializa funcionalidades
    initPageSpecificFeatures();
});

/**
 * Inicializa funcionalidades globais
 */
function initGlobalFeatures() {
    // Smooth scroll para links internos
    setupSmoothScroll();
    
    // Tooltips do Bootstrap
    setupTooltips();
    
    // Auto-hide alerts após um tempo
    setupAutoHideAlerts();
}

/**
 * Configura scroll suave
 */
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Inicializa tooltips do Bootstrap
 */
function setupTooltips() {
    // Verifica se Bootstrap está disponível
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Configura auto-hide para alerts
 */
function setupAutoHideAlerts() {
    document.querySelectorAll('.alert:not(.alert-permanent)').forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.classList.remove('show');
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 150);
            }
        }, 5000);
    });
}

/**
 * Event listeners globais
 */
function setupGlobalEventListeners() {
    // Tratamento de erros JavaScript
    window.addEventListener('error', function(e) {
        Logger.error('JavaScript Error', {
            message: e.message,
            filename: e.filename,
            lineno: e.lineno,
            colno: e.colno,
            error: e.error
        });
    });
    
    // Tratamento de promessas rejeitadas
    window.addEventListener('unhandledrejection', function(e) {
        Logger.error('Unhandled Promise Rejection', e.reason);
    });
}

/**
 * Inicializa funcionalidades específicas de cada página
 */
function initPageSpecificFeatures() {
    const currentPage = getCurrentPageName();
    Logger.log('Página atual detectada', currentPage);
    
    switch (currentPage) {
        case 'index':
            Logger.log('Inicializando funcionalidades da página inicial');
            break;
        case 'carrinho':
            Logger.log('Inicializando funcionalidades do carrinho');
            break;
        case 'checkout':
            Logger.log('Inicializando funcionalidades do checkout');
            break;
        case 'pedido_confirmado':
            Logger.log('Inicializando funcionalidades da confirmação');
            break;
    }
}

/**
 * Obtém nome da página atual
 */
function getCurrentPageName() {
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index' || path.includes('index')) {
        return 'index';
    } else if (path.includes('carrinho')) {
        return 'carrinho';
    } else if (path.includes('checkout')) {
        return 'checkout';
    } else if (path.includes('pedido_confirmado')) {
        return 'pedido_confirmado';
    }
    
    return 'unknown';
}

// EXPORTA PARA ESCOPO GLOBAL
// ==========================
window.ADEGA = {
    config: ADEGA_CONFIG,
    Logger,
    Formatter,
    Validator,
    Storage,
    notifications,
    loading,
    http,
    showSuccess,
    showError,
    showWarning,
    showInfo,
    copyToClipboard,
    formatCurrency,
    debounce,
    throttle
};

Logger.log('Sistema JavaScript da Adega carregado com sucesso!');
