# OLX Car Cover Scraper

A Python web scraper that extracts car cover listings from OLX India and saves results to CSV and JSON formats. Built for data engineering and analysis purposes.

## Features

- **Robust Scraping**: Multiple fallback selectors handle OLX's dynamic HTML structure
- **Respectful Crawling**: Built-in delays and proper headers to avoid overwhelming servers
- **Dual Export**: Saves data in both CSV and JSON formats for maximum compatibility
- **Error Handling**: Comprehensive exception handling and data validation
- **Configurable**: Command-line arguments for customization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Cyril-36/olx-scraper.git
cd olx-scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python olx_scraper.py
```

### Advanced Usage
```bash
# Scrape 5 pages with 2-second delay
python olx_scraper.py --pages 5 --delay 2.0

# Custom output filenames
python olx_scraper.py --output-csv my_results.csv --output-json my_results.json

# Quick test (1 page only)
python olx_scraper.py --pages 1
```

### Command Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--pages` | 3 | Number of pages to scrape |
| `--delay` | 1.5 | Delay between requests (seconds) |
| `--output-csv` | `olx_car_covers.csv` | CSV output filename |
| `--output-json` | `olx_car_covers.json` | JSON output filename |

## Output Format

### CSV Structure
```csv
title,price,location,url,image_url
Car Cover for Sedan Cars,₹ 899,Mumbai,https://www.olx.in/item/...,https://...
Waterproof Car Cover,₹ 1200,Delhi,https://www.olx.in/item/...,https://...
```

### JSON Structure
```json
[
  {
    "title": "Car Cover for Sedan Cars",
    "price": "₹ 899",
    "location": "Mumbai",
    "url": "https://www.olx.in/item/...",
    "image_url": "https://..."
  }
]
```

## Sample Output

```
Starting scrape for 3 pages...
Scraping page 1: https://www.olx.in/items/q-car-cover
Found 20 items using selector: [data-aut-id="itemBox"]
Extracted 18 valid items from page 1
Scraping page 2: https://www.olx.in/items/q-car-cover?page=2
Found 20 items using selector: [data-aut-id="itemBox"]
Extracted 19 valid items from page 2
Total items scraped: 45

Data saved to CSV: output/olx_car_covers.csv
Data saved to JSON: output/olx_car_covers.json
```

## Technical Details

- **Language**: Python 3.7+
- **Libraries**: requests, BeautifulSoup4, lxml
- **Approach**: Object-oriented design with comprehensive error handling
- **Data Extraction**: Multiple fallback selectors for robust parsing
- **Rate Limiting**: Configurable delays between requests

## File Structure

```
olx-scraper/
├── olx_scraper.py       # Main scraper script
├── requirements.txt     # Python dependencies
├── README.md           # Documentation
└── output/             # Generated output files (created automatically)
    ├── olx_car_covers.csv
    └── olx_car_covers.json
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Chaitanya Pudota**
- GitHub: [@Cyril-36](https://github.com/Cyril-36)
- LinkedIn: [chaitanya-pudota](https://linkedin.com/in/chaitanya-pudota)

---

*Built as part of data engineering portfolio demonstrating web scraping, data processing, and automation skills.*
