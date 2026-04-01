import requests
from bs4 import BeautifulSoup
import random
import re
import os
import json
from typing import List, Dict, Optional
from models import ScrapedResult
from services.scoring import calculate_relevance_score

# Mock User-Agents (In a real app, I'd import from headers.agents like darkdump.py did)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
]

class DarkDumpScraper:
    def __init__(self, use_tor=False):
        self.use_tor = use_tor
        self.proxy_config = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        } if use_tor else {}
        self.ahmia_base = "https://ahmia.fi"
        self.ahmia_search = f"{self.ahmia_base}/search/?q="

    def _get_headers(self):
        return {'User-Agent': random.choice(USER_AGENTS)}

    def search_ahmia(self, query: str, amount: int = 20) -> List[Dict]:
        """Fetch search results from Ahmia.fi"""
        headers = self._get_headers()
        try:
            # First, hit home to get nonce/form tokens if needed (ahmia sometimes requires it)
            homepage = requests.get(self.ahmia_base, headers=headers, timeout=10)
            soup = BeautifulSoup(homepage.content, 'html.parser')
            nonce_el = soup.select_one('#searchForm input[type="hidden"]')
            
            url = self.ahmia_search + query
            if nonce_el:
                url += f"&{nonce_el.get('name')}={nonce_el.get('value')}"
            
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code != 200:
                return []
                
            soup = BeautifulSoup(response.content, 'html.parser')
            results_container = soup.find(id='ahmiaResultsPage')
            if not results_container:
                return []
                
            results = []
            for item in results_container.find_all('li', class_='result')[:amount]:
                link_el = item.find('a')
                cite_el = item.find('cite')
                desc_el = item.find('p')
                
                if not link_el or not cite_el:
                    continue
                    
                site_url = cite_el.text.strip()
                if not site_url.startswith('http'):
                    site_url = "http://" + site_url
                    
                results.append({
                    'title': link_el.text.strip(),
                    'url': site_url,
                    'description': desc_el.text.strip() if desc_el else "No description available"
                })
            return results
        except Exception as e:
            print(f"Error searching Ahmia: {e}")
            return []

    def scrape_onion(self, url: str, primary_keyword: str, secondary_keywords: List[str], include_images: bool = False) -> Optional[ScrapedResult]:
        """Scrape an individual onion site and calculate relevance score."""
        headers = self._get_headers()
        try:
            # Scraping onion requires Tor proxy
            response = requests.get(url, headers=headers, proxies=self.proxy_config, timeout=30)
            if response.status_code != 200:
                return None
                
            soup = BeautifulSoup(response.content, 'html.parser')
            text_content = soup.get_text(separator=' ', strip=True)
            title = soup.title.string if soup.title else "Untitled"
            
            # Extract metadata
            metadata = {}
            for meta in soup.find_all('meta'):
                name = meta.get('name') or meta.get('property')
                if name:
                    metadata[name] = meta.get('content')
            
            # Extract images
            images = []
            if include_images:
                img_tags = soup.find_all('img')
                for img in img_tags:
                    src = img.get('src')
                    if src:
                        if not src.startswith('http'):
                            src = url.rstrip('/') + '/' + src.lstrip('/')
                        images.append(src)
                        
            # Scoring
            score, matched_kws = calculate_relevance_score(text_content, title, primary_keyword, secondary_keywords)
            
            # Snippet generation (around one of the keywords)
            snippet = ""
            if matched_kws:
                match = re.search(f".{{0,100}}{re.escape(matched_kws[0])}.{{0,100}}", text_content, re.IGNORECASE)
                if match:
                    snippet = "..." + match.group(0) + "..."
            
            # Additional extraction logic
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text_content)
            
            return ScrapedResult(
                title=title,
                url=url,
                description=metadata.get('description', "No meta description"),
                snippet=snippet or text_content[:200] + "...",
                score=score,
                matched_keywords=matched_kws,
                metadata=metadata,
                emails=list(set(emails))[:5],
                images=images[:10]
            )
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return None
