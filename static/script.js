const chatContainer = document.getElementById('messages-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Auto-resize textarea
userInput.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    if (this.value === '') {
        this.style.height = 'auto';
    }
});

// Handle Enter key
userInput.addEventListener('keydown', function (e) {
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

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function removeMessage(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}


// --- Agent Management Logic ---

const modal = document.getElementById('agent-modal');
const manageAgentsBtn = document.getElementById('manage-agents-btn');
const closeModalSpan = document.getElementsByClassName('close-modal')[0];
const agentsList = document.getElementById('agents-list');
const addAgentBtn = document.getElementById('add-agent-btn');
const agentFormContainer = document.getElementById('agent-form-container');
const agentForm = document.getElementById('agent-form');
const cancelFormBtn = document.getElementById('cancel-form-btn');
const formTitle = document.getElementById('form-title');

// Open Modal
manageAgentsBtn.onclick = function () {
    modal.style.display = "block";
    fetchAgents();
}

// Close Modal
closeModalSpan.onclick = function () {
    modal.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Fetch Agents
async function fetchAgents() {
    try {
        const response = await fetch('/api/agents');
        const agents = await response.json();
        renderAgents(agents);
    } catch (error) {
        console.error('Error fetching agents:', error);
    }
}

// Render Agents
function renderAgents(agents) {
    agentsList.innerHTML = '';
    agents.forEach(agent => {
        const card = document.createElement('div');
        card.className = 'agent-card';
        card.innerHTML = `
            <div class="agent-card-header">
                <span class="agent-name">${agent.name}</span>
                <label class="switch">
                    <input type="checkbox" ${agent.is_active ? 'checked' : ''} onchange="toggleAgent('${agent.id}', this.checked)">
                    <span class="slider"></span>
                </label>
            </div>
            <div class="agent-desc" title="${agent.description}">${agent.description}</div>
            <div class="agent-actions">
                <button class="edit-btn" onclick="editAgent('${agent.id}')">✏️ Editar</button>
                <button class="delete-btn" onclick="deleteAgent('${agent.id}')">🗑️ Excluir</button>
            </div>
        `;
        agentsList.appendChild(card);
    });
}

// Toggle Agent Status
async function toggleAgent(id, isActive) {
    try {
        // First get the current agent data to preserve other fields
        const agents = await (await fetch('/api/agents')).json();
        const agent = agents.find(a => a.id === id);
        if (!agent) return;

        agent.is_active = isActive;

        await fetch(`/api/agents/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(agent)
        });

        // Refresh team in backend
        await fetch('/api/team/refresh', { method: 'POST' });

    } catch (error) {
        console.error('Error toggling agent:', error);
        fetchAgents(); // Revert UI on error
    }
}

// Add Agent Button
addAgentBtn.onclick = function () {
    showForm();
}

// Cancel Form
cancelFormBtn.onclick = function () {
    hideForm();
}

// Show/Hide Form
function showForm(agent = null) {
    agentFormContainer.style.display = 'block';
    if (agent) {
        formTitle.textContent = 'Editar Agente';
        document.getElementById('agent-id').value = agent.id;
        document.getElementById('agent-name').value = agent.name;
        document.getElementById('agent-desc').value = agent.description;
        document.getElementById('agent-prompt').value = agent.prompt;
    } else {
        formTitle.textContent = 'Novo Agente';
        agentForm.reset();
        document.getElementById('agent-id').value = '';
    }
}

function hideForm() {
    agentFormContainer.style.display = 'none';
    agentForm.reset();
}

// Edit Agent
window.editAgent = async function (id) {
    const agents = await (await fetch('/api/agents')).json();
    const agent = agents.find(a => a.id === id);
    if (agent) {
        showForm(agent);
    }
}

// Delete Agent
window.deleteAgent = async function (id) {
    if (!confirm('Tem certeza que deseja excluir este agente?')) return;

    try {
        await fetch(`/api/agents/${id}`, { method: 'DELETE' });
        await fetch('/api/team/refresh', { method: 'POST' });
        fetchAgents();
    } catch (error) {
        console.error('Error deleting agent:', error);
    }
}

// Handle Form Submit
agentForm.onsubmit = async function (e) {
    e.preventDefault();

    const id = document.getElementById('agent-id').value;
    const name = document.getElementById('agent-name').value;
    const desc = document.getElementById('agent-desc').value;
    const prompt = document.getElementById('agent-prompt').value;

    // Generate ID from name if new
    const agentId = id || name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');

    const agentData = {
        id: agentId,
        name: name,
        description: desc,
        prompt: prompt,
        is_active: true // Default to active on create/update (or preserve if we fetched it, but for simplicity here true)
    };

    // If updating, we should preserve is_active status. 
    // But since we didn't store it in the form, let's fetch it first if it's an update.
    if (id) {
        const agents = await (await fetch('/api/agents')).json();
        const existing = agents.find(a => a.id === id);
        if (existing) agentData.is_active = existing.is_active;
    }

    try {
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/agents/${id}` : '/api/agents';

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(agentData)
        });

        if (!response.ok) throw new Error('Failed to save agent');

        await fetch('/api/team/refresh', { method: 'POST' });

        hideForm();
        fetchAgents();

    } catch (error) {
        console.error('Error saving agent:', error);
        alert('Erro ao salvar agente: ' + error.message);
    }
}
