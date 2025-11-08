import requests
from bs4 import BeautifulSoup
from typing import Tuple, Optional
import re


def scrape_wikipedia_article(url: str) -> Tuple[str, str]:
    """
    Scrape Wikipedia article and extract title and content.
    
    Args:
        url: Wikipedia article URL
        
    Returns:
        Tuple of (title, cleaned_content)
    """
    try:
        # Make request to Wikipedia
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1', {'id': 'firstHeading'}) or soup.find('h1')
        title = title_elem.get_text().strip() if title_elem else "Unknown Title"
        
        # Extract main content
        content_div = soup.find('div', {'id': 'mw-content-text'}) or soup.find('div', {'class': 'mw-parser-output'})
        
        if not content_div:
            raise ValueError("Could not find content div")
        
        # Remove unwanted elements
        for element in content_div.find_all(['div', 'span', 'table', 'ul', 'ol'], class_=re.compile(r'reference|cite|navbox|infobox|thumb|metadata|mw-editsection')):
            element.decompose()
        
        # Extract text from paragraphs
        paragraphs = content_div.find_all('p')
        text_content = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            # Remove citation references like [1], [2], etc.
            text = re.sub(r'\[\d+\]', '', text)
            text = re.sub(r'\[citation needed\]', '', text, flags=re.IGNORECASE)
            if text and len(text) > 50:  # Only include substantial paragraphs
                text_content.append(text)
        
        # Join paragraphs and clean up
        full_content = '\n\n'.join(text_content)
        
        # Further cleanup
        full_content = re.sub(r'\s+', ' ', full_content)  # Multiple spaces to single
        full_content = re.sub(r'\n\s*\n', '\n\n', full_content)  # Multiple newlines to double
        
        if len(full_content) < 100:
            raise ValueError("Insufficient content extracted from article")
        
        return title, full_content
        
    except requests.RequestException as e:
        raise ValueError(f"Error fetching Wikipedia article: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing Wikipedia article: {str(e)}")

