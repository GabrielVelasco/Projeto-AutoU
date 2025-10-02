// Estado da aplicação
const appState = {
    emails: [],
    currentTab: 'text',
    selectedFile: null
};

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    initializeTabs();
    initializeFileUpload();
    initializeClassifyButton();
    initializeClearButton();
    loadEmailsFromStorage();
});

// ========== TAB MANAGEMENT ==========
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabName = button.dataset.tab;
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Atualiza botões
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabName);
    });
    
    // Atualiza conteúdo
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.toggle('active', content.id === `${tabName}-tab`);
    });
    
    appState.currentTab = tabName;
}

// ========== FILE UPLOAD ==========
function initializeFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('fileUploadArea');
    
    // Click to upload
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // File selected
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            handleFileSelect(file);
        }
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) {
            handleFileSelect(file);
        }
    });
}

function handleFileSelect(file) {
    const allowedTypes = ['text/plain', 'application/pdf'];
    
    if (!allowedTypes.includes(file.type)) {
        showNotification('Apenas arquivos PDF ou TXT são permitidos', 'error');
        return;
    }
    
    if (file.size > 16 * 1024 * 1024) {
        showNotification('Arquivo muito grande. Máximo: 16MB', 'error');
        return;
    }
    
    appState.selectedFile = file;
    displaySelectedFile(file);
}

function displaySelectedFile(file) {
    const selectedFileDiv = document.getElementById('selectedFile');
    selectedFileDiv.style.display = 'flex';
    selectedFileDiv.innerHTML = `
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
            </svg>
            <span><strong>${file.name}</strong> (${formatFileSize(file.size)})</span>
        </div>
        <button onclick="clearFileSelection()" style="background: none; border: none; cursor: pointer; color: var(--gray-500);">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    `;
}

function clearFileSelection() {
    appState.selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('selectedFile').style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// ========== CLASSIFICATION ==========
function initializeClassifyButton() {
    const classifyBtn = document.getElementById('classifyBtn');
    classifyBtn.addEventListener('click', handleClassify);
}

async function handleClassify() {
    let requestBody;
    let requestHeaders = {};
    
    if (appState.currentTab === 'text') {
        const text = document.getElementById('emailText').value.trim();
        
        if (!text) {
            showNotification('Por favor, insira o texto do e-mail', 'error');
            return;
        }
        
        // Envia JSON para texto
        requestBody = JSON.stringify({ text: text });
        requestHeaders['Content-Type'] = 'application/json';
    } else if (appState.currentTab === 'file') {
        if (!appState.selectedFile) {
            showNotification('Por favor, selecione um arquivo', 'error');
            return;
        }
        
        // Envia FormData para arquivo
        const formData = new FormData();
        formData.append('file', appState.selectedFile);
        requestBody = formData;
        // Não define Content-Type para FormData (browser define automaticamente)
    }
    
    // Show loading
    showLoading(true);
    
    try {
        const response = await fetch('/api/classify', {
            method: 'POST',
            headers: requestHeaders,
            body: requestBody
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Adiciona novos e-mails ao estado
            appState.emails = [...data.emails, ...appState.emails];
            
            // Salva no localStorage
            saveEmailsToStorage();
            
            // Renderiza resultados
            renderResults();
            
            // Limpa inputs
            document.getElementById('emailText').value = '';
            clearFileSelection();
            
            showNotification(`${data.total} e-mail(s) classificado(s) com sucesso!`, 'success');
        } else {
            showNotification(data.error || 'Erro ao classificar e-mails', 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showNotification('Erro ao conectar com o servidor', 'error');
    } finally {
        showLoading(false);
    }
}

// ========== RESULTS RENDERING ==========
function renderResults() {
    const resultsSection = document.getElementById('resultsSection');
    const emailsList = document.getElementById('emailsList');
    
    if (appState.emails.length === 0) {
        resultsSection.style.display = 'none';
        return;
    }
    
    resultsSection.style.display = 'block';
    
    // Atualiza estatísticas
    updateStats();
    
    // Renderiza lista de e-mails
    emailsList.innerHTML = appState.emails.map((email, index) => createEmailCard(email, index)).join('');
    
    // Adiciona event listeners
    document.querySelectorAll('.email-header').forEach(header => {
        header.addEventListener('click', () => {
            const card = header.closest('.email-card');
            card.classList.toggle('expanded');
        });
    });
}

function createEmailCard(email, index) {
    const isImportant = email.classificacao === 'Importante';
    const preview = email.email_limpo.substring(0, 150) + (email.email_limpo.length > 150 ? '...' : '');
    
    return `
        <div class="email-card" data-index="${index}">
            <div class="email-header">
                <div class="email-header-left">
                    <span class="email-classification classification-${isImportant ? 'importante' : 'despresivel'}">
                        ${isImportant ? '⚠️ Importante' : '✓ Despresível'}
                    </span>
                    <div class="email-preview">${preview}</div>
                </div>
                <svg class="email-expand-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
            </div>
            <div class="email-body">
                <div class="email-content">${email.email_limpo}</div>
                
                ${email.resposta_sugerida ? `
                    <div class="email-response">
                        <div class="response-label">💡 Resposta Sugerida:</div>
                        <div class="response-text">${email.resposta_sugerida}</div>
                    </div>
                ` : ''}
                
                ${email.palavras_chave && email.palavras_chave.length > 0 ? `
                    <div class="keywords">
                        ${email.palavras_chave.map(kw => `<span class="keyword-tag">${kw}</span>`).join('')}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

function updateStats() {
    const total = appState.emails.length;
    const important = appState.emails.filter(e => e.classificacao === 'Importante').length;
    const dismissible = total - important;
    
    document.getElementById('totalEmails').textContent = total;
    document.getElementById('importantEmails').textContent = important;
    document.getElementById('dismissibleEmails').textContent = dismissible;
}

// ========== CLEAR FUNCTIONALITY ==========
function initializeClearButton() {
    const clearBtn = document.getElementById('clearAllBtn');
    clearBtn.addEventListener('click', () => {
        if (confirm('Tem certeza que deseja limpar todos os e-mails analisados?')) {
            appState.emails = [];
            saveEmailsToStorage();
            renderResults();
            showNotification('Todos os e-mails foram removidos', 'success');
        }
    });
}

// ========== LOCAL STORAGE ==========
function saveEmailsToStorage() {
    try {
        localStorage.setItem('classifiedEmails', JSON.stringify(appState.emails));
    } catch (error) {
        console.error('Erro ao salvar no localStorage:', error);
    }
}

function loadEmailsFromStorage() {
    try {
        const stored = localStorage.getItem('classifiedEmails');
        if (stored) {
            appState.emails = JSON.parse(stored);
            renderResults();
        }
    } catch (error) {
        console.error('Erro ao carregar do localStorage:', error);
    }
}

// ========== UI HELPERS ==========
function showLoading(show) {
    const loadingState = document.getElementById('loadingState');
    const classifyBtn = document.getElementById('classifyBtn');
    
    if (show) {
        loadingState.style.display = 'block';
        classifyBtn.disabled = true;
        classifyBtn.style.opacity = '0.6';
    } else {
        loadingState.style.display = 'none';
        classifyBtn.disabled = false;
        classifyBtn.style.opacity = '1';
    }
}

function showNotification(message, type = 'info') {
    // Cria elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? 'var(--success-color)' : type === 'error' ? 'var(--danger-color)' : 'var(--primary-color)'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: var(--shadow-lg);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        max-width: 400px;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove após 4 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Adiciona animações de notificação ao CSS dinâmicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
