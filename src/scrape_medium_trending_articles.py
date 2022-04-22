import sys
import threading
from lib import MediumTrendingLinksScraper, MediumArticleScraper


def main(args=None):
    """
    Main function.

    Command line syntax:
    `python scrape_medium_trending_articles.py [file_name] [config]`

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
        print("Trending article links:\n")
        for i, link in enumerate(scraper.trending_links):
            print(f"{i+1}). {link}\n")
        print("==============================\n")

        # ask user to choose to fetch the articles or not
        while True:
            answer = input("\nDo you want to fetch the articles? (y/n): ")
            if answer == "n":
                sys.exit(0)
            if answer != "y":
                print("Please enter 'y' or 'n'.")
                continue
            threads = []
            for link in scraper.trending_links:
                t = threading.Thread(
                    target=fetch_trending_article, args=(link, scraper.config))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            break
    except KeyboardInterrupt:
        print("\nExiting...")


def fetch_trending_article(url, config):
    article = MediumArticleScraper(url, config=config) # omit file_name
    article.fetch_html()
    article.scrape_article_content()
    article.save_html()


if __name__ == '__main__':
    main(sys.argv[1:])
