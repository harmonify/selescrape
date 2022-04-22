from lib import BaseScraper


def main(args=None):
    """
    Main function.

    Command line syntax:

    `python fetch_html.py <url> [file_name] [config] [wait_for_selector]
    [wait_for_selector_timeout]`

    - `<>` are required arguments
    - `[]` are optional arguments
    """
    try:
        # initialize scraper
        url = ""
        while url == "":
            url = args[0] if len(args) >= 1 else input("Enter URL: ")
        file_name = args[1] if len(args) >= 2 else input(
            "Enter file name (default is auto-generated): ")
        config = args[2] if len(args) >= 3 else input(
            "Enter config name (default: selescrape.json): ")
        wait_for_selector = args[3] if len(args) >= 4 else input(
            "Enter css selector to wait for when fetching html (default: None): ")
        wait_for_selector_timeout = 0
        if wait_for_selector != "":
            wait_for_selector_timeout = args[4] if len(args) >= 5 else input(
                "Enter wait timeout when fetching html (default: 0): ")
        scraper = BaseScraper(url, file_name, config,
                              wait_for_selector, wait_for_selector_timeout)

        # run scraper
        scraper.fetch_html()
        scraper.save_html()
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
