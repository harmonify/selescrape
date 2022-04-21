# Selescrape

Selescrape is a [Python](https://www.python.org/) [web scraping](https://en.wikipedia.org/wiki/Web_scraping) project based on [Selenium](https://www.selenium.dev/) library.

## Disclaimer

This project is only for educational purposes. I do not encourage anyone to scrape websites, especially those websites that may have terms and conditions against such actions.

## Installation

1. Install [Firefox](https://www.mozilla.org/en-US/firefox/new/) browser.
2. Install [geckodriver](https://github.com/mozilla/geckodriver/releases) for Firefox.
3. Install [Python](https://www.python.org/) 3.7+.
4. Add Python to PATH.
5. Install required packages.

```bash
pip install -r requirements.txt
```

## Usage

### Setup

You can run any _scraper_ or `src/lib/utilities/config.py` directly to setup the configuration file for the first time.

### Running Scraper

You should run scrapers from `src/` directory.

```bash
# run scraper without any arguments
python <scraper-script>.py

# or
python <scraper-script>.py https://www.example.com
```

Refer to each scraper implementation for more details.
