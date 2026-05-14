const API_BASE_URL = "/api";

let selectedDocId = null;

// Helper: Fetch with JSON response
async function fetchJson(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: { 'Content-Type': 'application/json' },
            ...options
        });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.error("Fetch error:", error);
        alert(`Error: ${error.message}`);
        throw error;
    }
}

// 1. Health Check
async function checkHealth() {
    const el = document.getElementById('api-status');
    try {
        const data = await fetchJson('/health');
        if (data.status === 'ok') {
            el.className = 'status-badge ok';
            el.textContent = 'API: Online';
        }
    } catch (e) {
        el.className = 'status-badge error';
        el.textContent = 'API: Offline';
    }
}

// 2. Ingest Document
document.getElementById('ingest-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        title: document.getElementById('doc-title').value,
        content: document.getElementById('doc-content').value,
        source: document.getElementById('doc-source').value,
        license: document.getElementById('doc-license').value
    };
    
    await fetchJson('/documents', {
        method: 'POST',
        body: JSON.stringify(payload)
    });
    
    alert('Document registered successfully!');
    e.target.reset();
    loadDocuments();
});

// 3. Load Documents
async function loadDocuments() {
    const listEl = document.getElementById('doc-list');
    listEl.innerHTML = '<li>Loading...</li>';
    
    try {
        const docs = await fetchJson('/documents');
        listEl.innerHTML = '';
        
        if (docs.length === 0) {
            listEl.innerHTML = '<li>No documents found.</li>';
            return;
        }
        
        docs.forEach(doc => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <strong>[${doc.id}] ${doc.title}</strong>
                    <div style="font-size:0.8em; color:var(--text-muted)">Source: ${doc.source}</div>
                </div>
                <button class="btn small outline" onclick="selectDocument(${doc.id}, '${doc.title.replace(/'/g, "\\'")}')">Select</button>
            `;
            listEl.appendChild(li);
        });
    } catch (e) {
        listEl.innerHTML = '<li>Failed to load documents.</li>';
    }
}

document.getElementById('refresh-docs').addEventListener('click', loadDocuments);

// 4. Document Actions
window.selectDocument = function(id, title) {
    selectedDocId = id;
    document.getElementById('selected-doc-title').textContent = `Selected: [${id}] ${title}`;
    document.getElementById('doc-actions').classList.remove('hidden');
    document.getElementById('chunks-display').classList.add('hidden');
};

document.getElementById('btn-create-chunks').addEventListener('click', async () => {
    if (!selectedDocId) return;
    const res = await fetchJson(`/documents/${selectedDocId}/chunks`, { method: 'POST' });
    const display = document.getElementById('chunks-display');
    display.classList.remove('hidden');
    display.textContent = `Created ${res.length} chunks.\n\n` + JSON.stringify(res, null, 2);
});

document.getElementById('btn-get-chunks').addEventListener('click', async () => {
    if (!selectedDocId) return;
    const res = await fetchJson(`/documents/${selectedDocId}/chunks`);
    const display = document.getElementById('chunks-display');
    display.classList.remove('hidden');
    display.textContent = `Found ${res.length} chunks.\n\n` + JSON.stringify(res, null, 2);
});

document.getElementById('btn-index').addEventListener('click', async () => {
    if (!selectedDocId) return;
    const res = await fetchJson(`/documents/${selectedDocId}/index`, { method: 'POST' });
    const display = document.getElementById('chunks-display');
    display.classList.remove('hidden');
    display.textContent = `Indexed Successfully!\n\n` + JSON.stringify(res, null, 2);
});

// 5. Search
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        query: document.getElementById('search-query').value,
        limit: parseInt(document.getElementById('search-limit').value)
    };
    
    const display = document.getElementById('search-results');
    display.classList.remove('hidden');
    display.textContent = 'Searching...';
    
    const res = await fetchJson('/search', {
        method: 'POST',
        body: JSON.stringify(payload)
    });
    
    display.textContent = JSON.stringify(res, null, 2);
});

// 6. Ask
document.getElementById('ask-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        question: document.getElementById('ask-question').value,
        limit: parseInt(document.getElementById('ask-limit').value)
    };
    
    const display = document.getElementById('ask-results');
    display.classList.remove('hidden');
    document.getElementById('ask-answer-text').textContent = 'Generating answer...';
    document.getElementById('ask-sources-list').innerHTML = '';
    
    const res = await fetchJson('/ask', {
        method: 'POST',
        body: JSON.stringify(payload)
    });
    
    document.getElementById('ask-answer-text').textContent = res.answer;
    document.getElementById('ask-provider').textContent = `Provider: ${res.provider}`;
    document.getElementById('ask-model').textContent = `Model: ${res.model}`;
    document.getElementById('ask-latency').textContent = `${res.latency_ms}ms`;
    
    const sourcesList = document.getElementById('ask-sources-list');
    sourcesList.innerHTML = '';
    res.sources.forEach(src => {
        const li = document.createElement('li');
        li.innerHTML = `
            <strong>[Score: ${src.score.toFixed(3)}] ${src.title}</strong>
            <p style="font-size:0.85em; margin-top:0.25rem;">${src.content.substring(0, 150)}...</p>
        `;
        sourcesList.appendChild(li);
    });
});

// 7. Agent Ask
document.getElementById('agent-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        question: document.getElementById('agent-question').value,
        limit: parseInt(document.getElementById('agent-limit').value)
    };
    
    const display = document.getElementById('agent-results');
    display.classList.remove('hidden');
    document.getElementById('agent-answer-text').textContent = 'Agent is thinking...';
    document.getElementById('agent-workflow-list').innerHTML = '';
    document.getElementById('agent-sources-list').innerHTML = '';
    document.getElementById('agent-sources-box').classList.add('hidden');
    
    const res = await fetchJson('/agent/ask', {
        method: 'POST',
        body: JSON.stringify(payload)
    });
    
    document.getElementById('agent-intent').textContent = res.intent;
    document.getElementById('agent-answer-text').textContent = res.answer;
    document.getElementById('agent-provider').textContent = `Provider: ${res.provider}`;
    document.getElementById('agent-model').textContent = `Model: ${res.model}`;
    document.getElementById('agent-latency').textContent = `${res.latency_ms}ms`;
    
    const workflowList = document.getElementById('agent-workflow-list');
    res.workflow.forEach(w => {
        const li = document.createElement('li');
        li.textContent = `[${w.step}] -> ${w.result}`;
        workflowList.appendChild(li);
    });

    if (res.sources && res.sources.length > 0) {
        document.getElementById('agent-sources-box').classList.remove('hidden');
        const sourcesList = document.getElementById('agent-sources-list');
        res.sources.forEach(src => {
            const li = document.createElement('li');
            li.innerHTML = `
                <strong>[Score: ${src.score.toFixed(3)}] ${src.title}</strong>
                <p style="font-size:0.85em; margin-top:0.25rem;">${src.content.substring(0, 150)}...</p>
            `;
            sourcesList.appendChild(li);
        });
    }
});

// 8. Logs & Feedback
let currentLogId = null;

async function loadLogs() {
    const listEl = document.getElementById('log-list');
    listEl.innerHTML = '<li>Loading logs...</li>';
    try {
        const logs = await fetchJson('/logs/asks');
        listEl.innerHTML = '';
        if (logs.length === 0) {
            listEl.innerHTML = '<li>No logs found.</li>';
            return;
        }
        logs.forEach(log => {
            const li = document.createElement('li');
            li.innerHTML = `
                <div>
                    <strong>[${log.id}] ${log.endpoint_type}</strong> - ${log.question}
                    <div style="font-size:0.8em; color:var(--text-muted)">
                        Intent: ${log.intent || 'N/A'} | Latency: ${log.latency_ms}ms
                    </div>
                </div>
                <button class="btn small outline" onclick="viewLogDetail(${log.id})">View</button>
            `;
            listEl.appendChild(li);
        });
    } catch (e) {
        listEl.innerHTML = '<li>Failed to load logs.</li>';
    }
}

document.getElementById('refresh-logs').addEventListener('click', loadLogs);

window.viewLogDetail = async function(id) {
    currentLogId = id;
    const box = document.getElementById('log-detail-box');
    box.classList.remove('hidden');
    
    document.getElementById('detail-question').textContent = 'Loading...';
    
    try {
        const log = await fetchJson(`/logs/asks/${id}`);
        
        document.getElementById('detail-endpoint').textContent = log.endpoint_type;
        document.getElementById('detail-intent').textContent = log.intent || 'N/A';
        document.getElementById('detail-provider').textContent = `${log.provider} (${log.model})`;
        document.getElementById('detail-latency').textContent = `${log.latency_ms}ms`;
        
        document.getElementById('detail-question').textContent = log.question;
        document.getElementById('detail-answer').textContent = log.answer;
        
        const sourcesList = document.getElementById('detail-sources-list');
        sourcesList.innerHTML = '';
        if (log.sources && log.sources.length > 0) {
            log.sources.forEach(src => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>[Score: ${src.score.toFixed(3)}] ${src.title}</strong><br>${src.content.substring(0, 100)}...`;
                sourcesList.appendChild(li);
            });
        } else {
            sourcesList.innerHTML = '<li>No sources used.</li>';
        }
        
        const feedbackList = document.getElementById('detail-feedback-list');
        feedbackList.innerHTML = '';
        if (log.feedback && log.feedback.length > 0) {
            log.feedback.forEach(fb => {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${fb.rating}</strong>: ${fb.comment || ''}`;
                feedbackList.appendChild(li);
            });
        } else {
            feedbackList.innerHTML = '<li>No feedback yet.</li>';
        }
    } catch (e) {
        console.error(e);
    }
};

document.getElementById('feedback-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    if (!currentLogId) return;
    
    const payload = {
        rating: document.getElementById('feedback-rating').value,
        comment: document.getElementById('feedback-comment').value
    };
    
    await fetchJson(`/logs/asks/${currentLogId}/feedback`, {
        method: 'POST',
        body: JSON.stringify(payload)
    });
    
    alert('Feedback submitted!');
    e.target.reset();
    viewLogDetail(currentLogId);
});

// Initialize
checkHealth();
loadDocuments();
loadLogs();
