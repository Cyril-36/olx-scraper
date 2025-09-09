#!/usr/bin/env python3
"""
OLX Car Cover Search Scraper
Description: Scrapes OLX India search results for car covers and exports to CSV/JSON
"""

import requests
from bs4 import BeautifulSoup
import csv
import json
import time
import os
from urllib.parse import urljoin
import argparse

class OLXScraper:
    def __init__(self, base_url="https://www.olx.in/items/q-car-cover", delay=1.5):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        
        # Set headers to mimic real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        
        self.results = []
    
    def get_page_url(self, page_num):
        """Generate URL for specific page number"""
        if page_num == 1:
            return self.base_url
        return f"{self.base_url}?page={page_num}"
    
    def extract_item_data(self, item_card):
        """Extract data from individual listing card"""
        try:
            # Title extraction with multiple fallback selectors
            title = None
            title_selectors = ['h6', '[data-aut-id="itemTitle"]', '.title', 'h6._2caa7']
            for selector in title_selectors:
                title_elem = item_card.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    break
            
            # Price extraction
            price = None
            price_selectors = ['span._2b6f3', '[data-aut-id="itemPrice"]', '.price', 'span[class*="price"]']
            for selector in price_selectors:
                price_elem = item_card.select_one(selector)
                if price_elem:
                    price_text = price_elem.get_text(strip=True)
                    if '₹' in price_text or any(char.isdigit() for char in price_text):
                        price = price_text
                        break
            
            # Location extraction
            location = None
            location_selectors = ['span._2e28f', '[data-aut-id="item-location"]', '.location']
            for selector in location_selectors:
                loc_elem = item_card.select_one(selector)
                if loc_elem:
                    location = loc_elem.get_text(strip=True)
                    break
            
            # URL extraction
            url = None
            link_elem = item_card.find('a', href=True)
            if link_elem:
                href = link_elem['href']
                url = urljoin('https://www.olx.in', href) if not href.startswith('http') else href
            
            # Image URL extraction
            image_url = None
            img_elem = item_card.find('img')
            if img_elem and img_elem.get('src'):
                image_url = img_elem['src']
            
            # Return structured data
            return {
                'title': title or 'N/A',
                'price': price or 'N/A',
                'location': location or 'N/A',
                'url': url or 'N/A',
                'image_url': image_url or 'N/A'
            }
            
        except Exception as e:
            print(f"Error extracting item data: {str(e)}")
            return None
    
    def scrape_page(self, page_num):
        """Scrape single page and extract all listings"""
        try:
            url = self.get_page_url(page_num)
            print(f"Scraping page {page_num}: {url}")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Multiple selectors to find item cards (OLX structure changes)
            card_selectors = [
                '[data-aut-id="itemBox"]',
                'li.EIR5N',
                'div._2fp1f',
                '.item-card',
                '[class*="item"]'
            ]
            
            items_found = []
            for selector in card_selectors:
                items = soup.select(selector)
                if items:
                    items_found = items
                    print(f"Found {len(items)} items using selector: {selector}")
                    break
            
            if not items_found:
                print(f"No items found on page {page_num} - trying alternative extraction")
                # Fallback: look for any div/li with links to /item/
                items_found = soup.find_all(['div', 'li'], string=lambda text: text and 'car' in text.lower() if text else False)
            
            page_results = []
            for item_card in items_found:
                item_data = self.extract_item_data(item_card)
                if item_data and item_data['title'] != 'N/A':
                    page_results.append(item_data)
            
            print(f"Extracted {len(page_results)} valid items from page {page_num}")
            return page_results
            
        except requests.RequestException as e:
            print(f"Network error on page {page_num}: {str(e)}")
            return []
        except Exception as e:
            print(f"Error scraping page {page_num}: {str(e)}")
            return []
    
    def scrape_multiple_pages(self, max_pages=3):
        """Scrape multiple pages with delay between requests"""
        print(f"Starting scrape for {max_pages} pages...")
        all_results = []
        
        for page in range(1, max_pages + 1):
            page_results = self.scrape_page(page)
            all_results.extend(page_results)
            
            # Add delay between pages to be respectful
            if page < max_pages:
                time.sleep(self.delay)
        
        self.results = all_results
        print(f"Total items scraped: {len(all_results)}")
        return all_results
    
    def save_to_csv(self, filename='olx_car_covers.csv'):
        """Save results to CSV file"""
        if not self.results:
            print("No data to save!")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'price', 'location', 'url', 'image_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in self.results:
                writer.writerow(item)
        
        print(f"Data saved to CSV: {filepath}")
        return filepath
    
    def save_to_json(self, filename='olx_car_covers.json'):
        """Save results to JSON file"""
        if not self.results:
            print("No data to save!")
            return
        
        # Create output directory if it doesn't exist
        os.makedirs('output', exist_ok=True)
        filepath = os.path.join('output', filename)
        
        with open(filepath, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.results, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Data saved to JSON: {filepath}")
        return filepath
    
    def print_summary(self):
        """Print summary of scraped data"""
        if not self.results:
            print("No data found!")
            return
        
        print(f"\n--- SCRAPING SUMMARY ---")
        print(f"Total items found: {len(self.results)}")
        print(f"Sample items:")
        
        for i, item in enumerate(self.results[:3]):  # Show first 3 items
            print(f"\n{i+1}. {item['title']}")
            print(f"   Price: {item['price']}")
            print(f"   Location: {item['location']}")
            print(f"   URL: {item['url'][:50]}..." if len(item['url']) > 50 else f"   URL: {item['url']}")

def main():
    parser = argparse.ArgumentParser(description='Scrape OLX car cover listings')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages to scrape (default: 3)')
    parser.add_argument('--delay', type=float, default=1.5, help='Delay between requests in seconds (default: 1.5)')
    parser.add_argument('--output-csv', default='olx_car_covers.csv', help='CSV output filename')
    parser.add_argument('--output-json', default='olx_car_covers.json', help='JSON output filename')
    
    args = parser.parse_args()
    
    # Create scraper instance
    scraper = OLXScraper(delay=args.delay)
    
    # Scrape data
    results = scraper.scrape_multiple_pages(args.pages)
    
    if results:
        # Save to both formats
        csv_path = scraper.save_to_csv(args.output_csv)
        json_path = scraper.save_to_json(args.output_json)
        
        # Print summary
        scraper.print_summary()
        
        print(f"\n--- FILES CREATED ---")
        print(f"CSV: {csv_path}")
        print(f"JSON: {json_path}")
    else:
        print("No data was scraped. Please check the OLX website structure or network connection.")

if __name__ == "__main__":
    main()
