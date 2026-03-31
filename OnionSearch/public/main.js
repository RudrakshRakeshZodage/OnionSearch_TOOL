const searchForm = document.getElementById('search-form');
const queryInput = document.getElementById('query');
const limitInput = document.getElementById('limit');
const proxyInput = document.getElementById('proxy');
const searchBtn = document.getElementById('search-btn');
const terminalLogs = document.getElementById('terminal-logs');
const resultsContainer = document.getElementById('results-container');
const resultsBody = document.getElementById('results-body');
const systemStatus = document.getElementById('system-status');
const statusText = document.getElementById('status-text');

let pollInterval = null;

function addLog(message, type = 'system') {
    const logLine = document.createElement('div');
    logLine.className = `log-line ${type}`;
    logLine.textContent = `[${new Date().toLocaleTimeString()}] > ${message}`;
    terminalLogs.appendChild(logLine);
    terminalLogs.scrollTop = terminalLogs.scrollHeight;
}

function updateStatus(status) {
    if (status === 'running') {
        systemStatus.style.backgroundColor = '#bc13fe';
        systemStatus.style.boxShadow = '0 0 10px #bc13fe';
        statusText.textContent = 'SCANNING DEEP WEB...';
        searchBtn.disabled = true;
        searchBtn.classList.add('loading');
    } else if (status === 'finished') {
        systemStatus.style.backgroundColor = '#00ff9d';
        systemStatus.style.boxShadow = '0 0 10px #00ff9d';
        statusText.textContent = 'SCRAPE COMPLETE';
        searchBtn.disabled = false;
        searchBtn.classList.remove('loading');
        clearInterval(pollInterval);
    } else {
        systemStatus.style.backgroundColor = '#475569';
        systemStatus.style.boxShadow = 'none';
        statusText.textContent = 'SYSTEM IDLE';
    }
}

function renderResults(results) {
    if (results.length > 0) {
        resultsContainer.style.display = 'block';
        resultsBody.innerHTML = '';
        results.forEach(res => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td><span class="engine-badge">${res.engine}</span></td>
                <td>${res.title}</td>
                <td><a href="${res.url}" target="_blank" class="onion-link">${res.url}</a></td>
            `;
            resultsBody.appendChild(row);
        });
    }
}

async function checkStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        updateStatus(data.status);
        
        // Update logs
        if (data.logs.length > terminalLogs.children.length - 1) {
            const newLogs = data.logs.slice(terminalLogs.children.length - 1);
            newLogs.forEach(log => addLog(log));
        }

        if (data.status === 'finished') {
            renderResults(data.results);
            addLog(`Scraping finished. Found ${data.results.length} results.`, 'system');
        }
    } catch (error) {
        console.error('Status check failed:', error);
    }
}

searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = queryInput.value.trim();
    const limit = parseInt(limitInput.value);
    const proxy = proxyInput.value.trim();

    if (!query) return;

    // Reset UI
    resultsContainer.style.display = 'none';
    terminalLogs.innerHTML = '';
    addLog(`Initializing scan for: ${query}`, 'system');
    
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, limit, proxy })
        });

        const data = await response.json();
        
        if (response.ok) {
            updateStatus('running');
            pollInterval = setInterval(checkStatus, 1000);
        } else {
            addLog(data.error || 'Failed to start search', 'error');
        }
    } catch (error) {
        addLog('Connection error: Could not reach backend.', 'error');
    }
});

// Initial Status Check
checkStatus();
