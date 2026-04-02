# Darkdump Optimized - AI-Powered Intelligence

## 🚀 About 
**Darkdump Optimized** is a high-performance OSINT interface designed for deep web investigations. It transforms raw natural language queries into structured intelligence using **Groq AI** and performs deep, JavaScript-rendered scans of `.onion` sites using **Playwright**.

### Key Enhancements:
- **Smart Search**: Enter natural language (e.g., *"Find leaks for YouTube"*) and get AI-expanded queries.
- **Deep Intel Sniper**: Automatically detects **Bitcoin/Ethereum addresses**, **API Keys**, and **Private Keys**.
- **JS-Rendering**: Full support for JavaScript-heavy onion sites via **Playwright**.
- **Unified Engine**: Streamlined codebase with zero legacy dependencies (NLTK/TextBlob).

## 🛠 Installation
1) ``git clone https://github.com/josh0xA/darkdump``<br/>
2) ``cd darkdump``<br/>
3) ``python -m pip install -r requirements.txt``<br/>
4) ``playwright install chromium``<br/>
5) ``python darkdump.py --help``<br/>

## 🔍 Intelligence Modes: 

### 1. Smart Intelligence Search
`python darkdump.py -q "corporate data leaks" -a 5 --scrape --js`
*   **-q**: Query string (Natural language supported via Groq)
*   **-a**: Number of results
*   **--scrape**: Perform deep intelligence extraction
*   **--js**: Force Playwright rendering (Default for .onion)

### 2. Direct Vector Investigation (New)
`python darkdump.py -u "http://[target].onion" --scrape`
*   **-u**: Directly target a specific link for immediate deep-scrape intelligence.

## ⚙️ Tor Configuration 
Ensure your Tor service is running on **port 9150** (Tor Browser) or **9050** (Tor Service). Darkdump handles the proxy routing automatically.

## 🧠 AI Integration
Darkdump now requires a `GROQ_API_KEY` in a `backend/.env` file for Smart Search and Topic Sentiment capabilities.

## ⚖️ Ethical Notice
This tool is for educational and authorized intelligence gathering only. The developers are not responsible for any misuse.

## 🤝 License 
MIT License
Copyright (c) Josh Schiavone / Optimized by Antigravity AI
