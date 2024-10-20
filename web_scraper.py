import os
import hashlib
import json
import logging
from typing import List, Tuple
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import urllib.parse
import re

def scrape_google_and_links(query: str, max_links: int = 5) -> List[str]:
    """
    Scrapes Google search results and linked pages for a given query. Saves image URLs.

    Args:
        query (str): The search query to use.
        max_links (int): Maximum number of links to scrape. Defaults to 5.

    Returns:
        list: A list of scraped content from the links.
    """
    image_urls = []
    scraped_contents = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Perform Google search
            encoded_query = urllib.parse.quote(query)
            google_url = f"https://www.google.com/search?q={encoded_query}"
            page.goto(google_url)
            logging.info(f"Searching Google for: {query}")

            # Scrape search results
            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            search_results = soup.find_all('div', class_='yuRUbf')
            
            links = [result.find('a')['href'] for result in search_results]

            # Create a directory to store HTML files
            storage_dir = "scraped_html"
            os.makedirs(storage_dir, exist_ok=True)

            # Scrape content from each link
            for link in links[:max_links]:
                scraped_content, link_image_urls = scrape_single_link(page, link, storage_dir)
                if scraped_content:
                    scraped_contents.append(scraped_content)
                    image_urls.extend(link_image_urls)

        finally:
            browser.close()

    # Save image URLs to a file
    with open('image_urls.json', 'w') as f:
        json.dump(image_urls, f)

    return scraped_contents

def scrape_single_link(page, link: str, storage_dir: str) -> Tuple[str, List[str]]:
    """Scrapes content and image URLs from a single link."""
    try:
        page.goto(link, timeout=10000)  # 10 seconds timeout
        content = page.content()
        
        # Generate a unique filename based on the link
        filename = hashlib.md5(link.encode()).hexdigest() + ".html"
        filepath = os.path.join(storage_dir, filename)
        
        # Save the HTML content
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Extract image URLs
        image_urls = extract_image_urls(page, link)
        
        return text_content, image_urls
    except Exception as e:
        logging.error(f"Error scraping {link}: {str(e)}")
        return None, []

def extract_image_urls(page, base_url: str) -> List[str]:
    """Extracts image URLs from the current page."""
    image_urls = []
    for img in page.query_selector_all('img'):
        src = img.get_attribute('src')
        if src:
            # Handle relative URLs
            if not src.startswith(('http://', 'https://')):
                src = urllib.parse.urljoin(base_url, src)
            
            # Include more image formats and don't filter by extension
            image_urls.append(src)
    
    # Extract background images from inline styles
    elements_with_bg = page.query_selector_all('[style*="background-image"]')
    for element in elements_with_bg:
        style = element.get_attribute('style')
        url_match = re.search(r'url\(["\']?(.*?)["\']?\)', style)
        if url_match:
            bg_url = url_match.group(1)
            if not bg_url.startswith(('http://', 'https://')):
                bg_url = urllib.parse.urljoin(base_url, bg_url)
            image_urls.append(bg_url)
    
    return list(set(image_urls))  # Remove duplicates

def get_image_urls() -> List[str]:
    """
    Retrieves image URLs from a JSON file.

    Returns:
        list: A list of image URLs.
    """
    logging.info("Getting image URLs")
    
    with open('image_urls.json', 'r') as f:
        return json.load(f)
