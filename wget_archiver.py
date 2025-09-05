import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse, urljoin
import argparse
import logging
import time
import os
import subprocess

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_args():
    parser = argparse.ArgumentParser(description="General archive scraper")
    parser.add_argument("url", help="Base URL. Use '{page}' for numbered mode (e.g. '?page={page}' or '/page/{page}/')")
    parser.add_argument("--use", choices=["numbers", "next"], default="next",
                        help="Scraping mode: 'numbers' or 'next'")
    parser.add_argument("--start", type=int, default=1, help="Start page number (for 'numbers')")
    parser.add_argument("--end", type=int, default=None, help="End page number (for 'numbers')")
    parser.add_argument("--rate-limit", type=float, default=1.0, help="Seconds to wait between requests")
    parser.add_argument("--target-selector", required=True,
                        help="CSS selector for the target tags you want to scrape (e.g. 'h2.entry-title a')")
    parser.add_argument("--next-selector", default="a.next.page-numbers",
                        help="CSS selector for next page link (only used in 'next' mode')")
    parser.add_argument("--output-txt", help="Output all article URLs to a text file")
    parser.add_argument("--wget", action="store_true", help="Download all found article URLs using wget")
    parser.add_argument("--output-dir", default="output", help="Output directory for downloaded files")
    parser.add_argument("--alt-url", help="Alternative URL for the start page (for 'numbers' mode, e.g., if page 1 has no number)")
    return parser.parse_args()

def fetch_and_parse(url, rate_limit_sleep):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error accessing {url}: {e}")
        return None
    finally:
        time.sleep(rate_limit_sleep)

def extract_articles(soup, selector, base_url):
    found = set()
    for a in soup.select(selector):
        href = a.get("href")
        if href:
            full_url = urljoin(base_url, href)
            found.add(full_url)
    return found


def scrape_by_number(base_url, start, end, rate_limit, target_selector, alt_url):
    if "{page}" not in base_url and not (start == 1 and alt_url):
        logging.error("In 'numbers' mode, URL must contain '{page}' placeholder, or '--alt-url' must be provided when starting at page 1.")
        sys.exit(1)

    page = start
    all_articles = set()

    while True:
        if end and page > end:
            break

        if page == 1 and alt_url:
            url = alt_url
        else:
            url = base_url.format(page=page)

        logging.info(f"Scraping page {page}: {url}")
        soup = fetch_and_parse(url, rate_limit)
        if not soup:
            break

        articles = extract_articles(soup, target_selector, url)
        if not articles:
            logging.info("No articles found. Stopping.")
            break

        for a in articles:
            logging.info(f"Found: {a}")
        all_articles.update(articles)
        page += 1

    return all_articles

def scrape_by_next(start_url, rate_limit, target_selector, next_selector):
    visited = set()
    all_articles = set()
    url = start_url

    while url and url not in visited:
        visited.add(url)
        logging.info(f"Scraping: {url}")
        soup = fetch_and_parse(url, rate_limit)
        if not soup:
            break

        articles = extract_articles(soup, target_selector, url)
        if not articles:
            logging.info("No articles found. Stopping.")
            break

        for a in articles:
            logging.info(f"Found: {a}")
        all_articles.update(articles)

        next_tag = soup.select_one(next_selector)
        url = urljoin(url, next_tag['href']) if next_tag and next_tag.has_attr('href') else None

    return all_articles

def main():
    args = get_args()
    if args.use == "numbers":
        articles = scrape_by_number(args.url, args.start, args.end, args.rate_limit, args.target_selector, args.alt_url)
    else:
        articles = scrape_by_next(args.url, args.rate_limit, args.target_selector, args.next_selector)

    logging.info(f"\nTotal unique articles collected: {len(articles)}")

    if args.output_txt:
        with open(args.output_txt, "w") as f:
            for article in sorted(articles):
                f.write(article + "\n")
        logging.info(f"Wrote output to {args.output_txt}")

    if args.wget:
        logging.info("Starting wget download of all URLs...")
        os.makedirs(args.output_dir, exist_ok=True)
        try:
            with open("wget_commands.sh", "w") as f:
                for url in articles:
                    clean_url = url.rstrip('/')
                    parsed = urlparse(clean_url)
                    filename = parsed.path.split('/')[-1]
                    if not filename.endswith('.html'):
                        filename += '.html'
                    f.write(f"wget -nc -O '{args.output_dir}/{filename}' '{url}'\n")
            subprocess.run(["bash", "wget_commands.sh"], check=True)
            os.remove("wget_commands.sh")
        except subprocess.CalledProcessError as e:
            logging.error(f"wget failed: {e}")

if __name__ == "__main__":
    main()
