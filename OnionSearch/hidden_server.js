const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 4000;
const SITE_DIR = path.join(__dirname, 'hidden_site');

const server = http.createServer((req, res) => {
  let filePath = path.join(SITE_DIR, req.url === '/' ? 'index.html' : req.url);
  const ext = path.extname(filePath);
  const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
  };
  const contentType = mimeTypes[ext] || 'text/plain';

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not Found');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(data);
  });
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`Hidden site running at http://127.0.0.1:${PORT}`);
});
