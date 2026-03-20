# Ingestion module
import requests
from bs4 import BeautifulSoup
import os
from typing import List, Dict, Optional
import re

class Ingestion:
    @staticmethod
    def fetch_url(url: str) -> Optional[Dict[str, str]]:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Basic cleanup
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            
            title = soup.title.string if soup.title else url
            text = soup.get_text(separator=' ', strip=True)
            
            return {
                "source": url,
                "title": title,
                "content": text,
                "length": len(text)
            }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    @staticmethod
    def read_file(file_path: str) -> Optional[Dict[str, str]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If HTML, clean it
            if file_path.endswith('.html'):
                soup = BeautifulSoup(content, 'html.parser')
                for script_or_style in soup(["script", "style"]):
                    script_or_style.decompose()
                title = soup.title.string if soup.title else os.path.basename(file_path)
                text = soup.get_text(separator=' ', strip=True)
            else:
                title = os.path.basename(file_path)
                text = content.strip()
            
            return {
                "source": file_path,
                "title": title,
                "content": text,
                "length": len(text)
            }
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return None

    @staticmethod
    def ingest_sources(urls: List[str] = None, folder_path: str = None) -> List[Dict[str, str]]:
        sources = []
        
        if urls:
            for url in urls:
                res = Ingestion.fetch_url(url)
                if res and res["content"]:
                    sources.append(res)
        
        if folder_path and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    res = Ingestion.read_file(file_path)
                    if res and res["content"]:
                        sources.append(res)
        
        return sources
