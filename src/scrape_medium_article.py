import sys
from lib import MediumArticleScraper


def main(args=None):
    """
    Main function.

    Command line syntax:
    python scrape_medium_article.py <url> [file_name] [config_name] [wait_for] [wait_timeout]

    <> are required arguments
    [] are optional arguments
    """
    try:
        # initialize scraper
        url = ""
        while url == "":
            url = args[0] if len(args) >= 1 else input("Enter URL: ")
        file_name = args[1] if len(args) >= 2 else input(
            "Enter file name (default is auto-generated): ")
        config_name = args[2] if len(args) >= 3 else input(
            "Enter config name (default: selescrape.json): ")
        wait_for = args[3] if len(args) >= 4 else input(
            "Enter wait for selector when fetching html (default: None): ")
        wait_timeout = args[4] if len(args) >= 5 else input(
            "Enter wait timeout when fetching html (default: 0): ")
        scraper = MediumArticleScraper(url, file_name, config_name,
                                       wait_for, wait_timeout)
        # run scraper
        scraper.fetch_html()
        scraper.scrape_article_content()
        scraper.save_html()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    main(sys.argv[1:])
