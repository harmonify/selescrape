import sys
from lib import MediumTrendingLinksScraper


def main(args=None):
    """
    Main function.

    Command line syntax:
    `python scrape_medium_trending_links.py [file_name] [config]`

    - `<>` are required arguments
    - `[]` are optional arguments
    """
    try:
        # initialize scraper
        url = "https://www.medium.com"
        file_name = args[1] if len(args) >= 2 else input(
            "Enter file name (default is auto-generated): ")
        config = args[2] if len(args) >= 3 else input(
            "Enter config name (default: selescrape.json): ")
        scraper = MediumTrendingLinksScraper(url, file_name, config)
        # run scraper
        scraper.fetch_html()
        scraper.scrape_trending_links()
        scraper.save_trending_links()

        # print out trending links
        print("\n==============================")
        print("Trending article links:")
        for link in scraper.trending_links:
            print(link)
        print("==============================\n")
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    main(sys.argv[1:])
