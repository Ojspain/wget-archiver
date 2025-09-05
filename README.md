
# Web Archive Scraper

This Python script is a versatile tool designed to scrape URLs from a paginated website archive, such as a blog or news site. It's built to handle two common pagination styles and can optionally download the collected pages.

## Features

-   **Two Scraping Modes:**
    
    -   **Numbered Pages:** Scrape a range of pages using a URL format that contains a `'{page}'` placeholder (e.g., `"?page={page}"`).
        
    -   **"Next" Link:** Navigate through a website's archive by following a specific CSS selector for the "next page" link until no more are found.
        
    
-   **Rate Limiting:** A built-in delay between requests helps you avoid overwhelming the target server.
    
-   **Flexible Output:**
    
    -   Save all found URLs to a plain text file.
        
    -   Automatically download all collected article URLs using the command-line tool `wget`.
        

## Installation

You can install this script and its dependencies by cloning the repository and using pip.

    git clone https://github.com/Ojspain/wget-archiver
    cd wget-archiver
    python3 -m venv venv
    source venv/bin/activate
    pip install .
This will set up the script and make the command line tool usable in the directory it was installed in.
## Usage

The script is run from the command line with various arguments to control its behavior.

### General Syntax

```
wget-archiver <url> --target-selector "<css_selector>" [options]
```

### Basic Examples

**1. Scraping with a "Next Page" Link (Default Mode)**

The script will start at the provided URL and follow the link that matches the `--next-selector`.

```
wget-archiver "https://example.com/blog/" --target-selector "h2.entry-title a" --next-selector "a.next-page"

```

-   `"https://example.com/blog/"` is the starting URL.
    
-   `"h2.entry-title a"` is the CSS selector for the article links you want to collect.
    
-   `"a.next-page"` is the CSS selector for the link to the next page in the archive.
    

**2. Scraping Numbered Pages**
Use this when a site’s archive is split across numbered pages (e.g. `?page=1`, `?page=2`, …).  
If the first page doesn’t have a page number in its URL, provide it with `--first-page-url`.  
The script will fetch that first page, then continue automatically from page 2 onward.

```
wget-archiver "https://example.com/archive/page/{page}" --use numbers --start 1 --end 10 --target-selector "div.post-list h3 a" --output-txt articles.txt
```

-   `"https://example.com/archive/page/{page}"` is the URL pattern. The script will replace `{page}` with the page number.
    
-   `--use numbers` enables the numbered page mode.
    
-   `--start 1` and `--end 10` define the page range to scrape.
    
-   `"div.post-list h3 a"` is the CSS selector for the article links.
    
-   `--output-txt articles.txt` saves all found URLs to a file named `articles.txt`.
    

**3. Downloading Articles with `wget`**

You can use the `--wget` flag to automatically download the collected pages.

```
python scraper.py "[https://example.com/blog/](https://example.com/blog/)" --target-selector "h2 a" --wget --output-dir blog-archives

```

-   `--wget` enables the download feature.
    
-   `--output-dir blog-archives` specifies the local directory to save the files.
    

### All Arguments

-   **`url`** (required): The base URL for scraping. Use the `'{page}'` placeholder for numbered mode (e.g., `'?page={page}'`).
    
-   **`--use {numbers, next}`**: The scraping mode. Defaults to `next`.
    
-   **`--start <int>`**: The starting page number (only for `numbers` mode). Defaults to `1`.
    
-   **`--end <int>`**: The ending page number (only for `numbers` mode).
    
-   **`--rate-limit <float>`**: The number of seconds to wait between each HTTP request. Defaults to `1.0`.
    
-   **`--target-selector "<css_selector>"`** (required): The CSS selector for the target tags you want to scrape, such as the article links.
    
-   **`--next-selector "<css_selector>"`**: The CSS selector for the "next page" link (only for `next` mode). Defaults to `"a.next.page-numbers"`.
    
-   **`--output-txt <filename>`**: The name of a text file to save the collected URLs to.
    
-   **`--wget`**: A flag to download all found URLs using `wget`.
    
-   **`--output-dir <directory>`**: The output directory for downloaded files (only for `--wget` mode). Defaults to `output`.
    
-   **`--first-page-url <url>`**: An alternative URL for the first page (for `numbers` mode). Use this if page `1` has a different URL format than the subsequent pages
