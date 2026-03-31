const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;
const ONIONSEARCH_PATH = 'C:\\Users\\Rudraksh\\AppData\\Roaming\\Python\\Python313\\Scripts\\onionsearch.exe';

app.use(cors());
app.use(bodyParser.json());
app.use(express.static('public'));

let currentSearch = {
    status: 'idle',
    results: [],
    logs: [],
    startTime: null
};

app.post('/api/search', (req, res) => {
    const { query, limit = 1, proxy = '127.0.0.1:9150' } = req.body;

    if (!query) {
        return res.status(400).json({ error: 'Search query is required' });
    }

    if (currentSearch.status === 'running') {
        return res.status(400).json({ error: 'A search is already in progress' });
    }

    const timestamp = new Date().getTime();
    const outputFilename = `web_output_${timestamp}.txt`;
    const outputPath = path.join(__dirname, outputFilename);

    currentSearch = {
        status: 'running',
        results: [],
        logs: [`Starting search for: "${query}"...`],
        startTime: new Date()
    };

    const args = [
        query,
        '--proxy', proxy,
        '--limit', limit.toString(),
        '--output', outputFilename
    ];

    const child = spawn(ONIONSEARCH_PATH, args, { cwd: __dirname });

    child.stdout.on('data', (data) => {
        const line = data.toString();
        currentSearch.logs.push(line);
        console.log(`STDOUT: ${line}`);
    });

    child.stderr.on('data', (data) => {
        const line = data.toString();
        currentSearch.logs.push(line);
        console.error(`STDERR: ${line}`);
    });

    child.on('close', (code) => {
        currentSearch.status = 'finished';
        currentSearch.logs.push(`Process exited with code ${code}`);
        
        // Parse results if file exists
        if (fs.existsSync(outputPath)) {
            const content = fs.readFileSync(outputPath, 'utf-8');
            const lines = content.split('\n');
            currentSearch.results = lines
                .filter(line => line.trim())
                .map(line => {
                    const match = line.match(/"([^"]*)","([^"]*)","([^"]*)"/);
                    if (match) {
                        return { engine: match[1], title: match[2], url: match[3] };
                    }
                    return null;
                })
                .filter(Boolean);
        }
    });

    res.json({ message: 'Search started', id: timestamp });
});

app.get('/api/status', (req, res) => {
    res.json(currentSearch);
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
