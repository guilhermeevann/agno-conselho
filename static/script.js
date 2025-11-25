const chatContainer = document.getElementById('messages-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') {
        this.style.height = 'auto';
    }
});

// Handle Enter key
userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

sendBtn.addEventListener('click', sendMessage);

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    // Add user message
    addMessage(text, 'user');
    userInput.value = '';
    userInput.style.height = 'auto';

    // Disable input while loading
    userInput.disabled = true;
    sendBtn.disabled = true;

    // Add loading indicator
    const loadingId = addLoadingMessage();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: text })
        });

        if (!response.ok) {
            throw new Error('Erro na comunicação com o servidor');
        }

        const data = await response.json();
        
        // Remove loading and add response
        removeMessage(loadingId);
        addMessage(data.response, 'ai');

    } catch (error) {
        console.error('Error:', error);
        removeMessage(loadingId);
        addMessage('Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente.', 'ai');
    } finally {
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    if (sender === 'ai') {
        // Parse Markdown for AI messages
        contentDiv.innerHTML = marked.parse(text);
    } else {
        contentDiv.textContent = text;
    }
    
    div.appendChild(contentDiv);
    chatContainer.appendChild(div);
    scrollToBottom();
    return div.id = 'msg-' + Date.now();
}

function addLoadingMessage() {
    const div = document.createElement('div');
    div.className = 'message ai-message';
    div.id = 'loading-' + Date.now();
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<em>Pensando...</em>';
    
    div.appendChild(contentDiv);
    chatContainer.appendChild(div);
    scrollToBottom();
    return div.id;
}

function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}
